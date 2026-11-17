"""Exercise progressive enhancement and deck interactions in Chromium.

Optional tooling: pip install playwright==1.65.2
Then: python -m playwright install chromium
Run: python scripts/check_browser.py [--screenshots EXISTING_DIRECTORY]
"""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def no_overflow(page):
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Horizontal overflow"


def check_fallback(browser, url, *, javascript=True, blocked=None):
    context = browser.new_context(
        java_script_enabled=javascript, viewport={"width": 375, "height": 812}, reduced_motion="reduce",
    )
    context.route("https://fonts.**/*", lambda route: route.abort())
    if blocked:
        context.route(f"**/{blocked}", lambda route: route.abort())
    page = context.new_page()
    page.goto(url)
    expect(page.locator("h1")).to_be_visible()
    assert page.locator("[data-reveal]").evaluate_all(
        "elements => elements.every(el => getComputedStyle(el).opacity === '1')"
    )
    if not javascript or blocked == "presentation.js":
        assert page.locator("[data-present]:visible").count() == 0
    if not javascript or blocked == "site.js":
        expect(page.locator("#navlinks")).to_be_visible()
        expect(page.locator("#menu")).to_be_hidden()
        for link in page.locator("#navlinks a").all():
            expect(link).to_be_visible()
    no_overflow(page)
    context.close()
    print(f"PASS: fallback (JavaScript={javascript}, blocked={blocked})")


def check_interactions(browser, url, screenshots):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    context.route("https://fonts.**/*", lambda route: route.abort())
    page = context.new_page()
    errors = []
    requests = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("response", lambda response: errors.append(f"HTTP {response.status}: {response.url}")
            if response.url.startswith(url) and response.status >= 400 else None)
    page.on("request", lambda request: requests.append(request.url))
    page.goto(url)
    expect(page.locator("[data-present]").first).to_be_visible()
    assert page.locator("#deck-stage img").count() == 0, "Deck images loaded before opening"
    page.keyboard.press("Tab")
    expect(page.locator(".skip-link")).to_be_focused()
    page.keyboard.press("Enter")
    expect(page.locator("main")).to_be_focused()

    for image in page.locator("main img").all():
        image.scroll_into_view_if_needed()
        expect(image).to_have_js_property("complete", True)
        assert image.evaluate("image => image.naturalWidth > 0 && image.currentSrc.endsWith('.webp')")
    assert not any(request.endswith(".png") for request in requests), "Unexpected PNG transfer"

    for width, height in ((1440, 900), (1280, 720), (1024, 768), (768, 1024), (375, 812), (320, 640)):
        page.set_viewport_size({"width": width, "height": height})
        page.evaluate("scrollTo(0, 0)")
        no_overflow(page)
        assert page.locator("header").bounding_box()["height"] <= 80, "Header controls wrapped"
        if width <= 1100:
            page.locator("#menu").click()
            for link in page.locator("#navlinks a").all():
                expect(link).to_be_visible()
            page.keyboard.press("Escape")
            expect(page.locator("#menu")).to_be_focused()
            expect(page.locator("#navlinks")).to_be_hidden()
            page.locator("#menu").click()
            page.locator('#navlinks a[href="#proceso"]').click()
            expect(page.locator('#navlinks a[href="#proceso"]')).to_have_attribute("aria-current", "location")
            expect(page.locator("#navlinks")).to_be_hidden()
        if screenshots and width in (1440, 375):
            page.evaluate("scrollTo(0, 0)")
            page.screenshot(path=str(screenshots / f"newlife-{width}.png"))
        print(f"PASS: page layout and navigation at {width}x{height}")

    page.set_viewport_size({"width": 1440, "height": 900})
    for launcher in page.locator("[data-present]").all():
        launcher.click()
        expect(page.locator("#presentation")).to_be_visible()
        expect(page.locator("#deck-exit")).to_be_focused()
        assert page.locator("main").evaluate("element => element.inert")
        page.keyboard.press("Escape")
        expect(page.locator("#presentation")).to_be_hidden()
        expect(launcher).to_be_focused()

    page.locator("[data-present]").first.click()
    page.locator("#deck-next").click()
    expect(page.locator("#deck-select")).to_have_value("1")
    page.keyboard.press("ArrowRight")
    expect(page.locator("#deck-select")).to_have_value("2")
    page.keyboard.press("End")
    expect(page.locator("#deck-select")).to_have_value("10")
    expect(page.locator("#deck-next")).to_be_disabled()
    page.locator("#deck-exit").focus()
    page.keyboard.press("Home")
    expect(page.locator("#deck-select")).to_have_value("0")
    expect(page.locator("#deck-prev")).to_be_disabled()
    page.locator("#deck-fullscreen").focus()
    page.keyboard.press("Shift+Tab")
    expect(page.locator("#deck-next")).to_be_focused()
    page.keyboard.press("Tab")
    expect(page.locator("#deck-fullscreen")).to_be_focused()

    page.locator("#deck-fullscreen").click()
    page.wait_for_function("document.fullscreenElement?.id === 'presentation'")
    page.locator("#deck-fullscreen").click()
    page.wait_for_function("document.fullscreenElement === null")

    for width, height in ((1440, 900), (844, 390), (375, 812), (320, 640)):
        page.set_viewport_size({"width": width, "height": height})
        for i in range(11):
            page.locator("#deck-select").select_option(str(i))
            slide = page.locator(f"#slide-{i + 1}")
            expect(slide).to_be_visible()
            assert slide.evaluate("element => element.scrollWidth <= element.clientWidth"), f"Slide {i + 1} overflows"
            assert slide.locator(".slide-kicker").evaluate(
                "element => element.getBoundingClientRect().top >= element.closest('.deck-slide').getBoundingClientRect().top"
            ), f"Slide {i + 1} starts above its scroll area"
            expect(page.locator("#deck-source")).to_be_visible()
            if slide.locator("img").count():
                image = slide.locator("img")
                image.scroll_into_view_if_needed()
                expect(image).to_have_js_property("complete", True)
                assert image.evaluate("element => element.naturalWidth > 0 && element.currentSrc.endsWith('.webp')")
        no_overflow(page)
        print(f"PASS: all 11 slides at {width}x{height}")

    if screenshots:
        page.locator("#deck-select").select_option("0")
        page.screenshot(path=str(screenshots / "newlife-slide-mobile.png"))
    page.locator("#deck-select").select_option("3")
    page.locator("#deck-source").click()
    expect(page.locator("#presentation")).to_be_hidden()
    expect(page.locator("#proceso")).to_be_focused()
    assert not page.locator("main").evaluate("element => element.inert")

    # Touch-style gestures exercise the same handler as a horizontal swipe.
    page.locator("[data-present]").first.click()
    page.locator("#deck-select").select_option("0")
    page.locator("#deck-stage").evaluate("""element => {
        const touch = (x, y) => new Touch({ identifier: 1, target: element, clientX: x, clientY: y });
        element.dispatchEvent(new TouchEvent('touchstart', { changedTouches: [touch(250, 150)] }));
        element.dispatchEvent(new TouchEvent('touchend', { changedTouches: [touch(100, 155)] }));
    }""")
    expect(page.locator("#deck-select")).to_have_value("1")
    page.keyboard.press("Escape")
    assert not errors, errors
    context.close()
    print("PASS: launchers, keyboard, focus trap/restoration, fullscreen, section return, and swipe handler")

    # With animations enabled, the page still reveals normally.
    context = browser.new_context(reduced_motion="no-preference")
    context.route("https://fonts.**/*", lambda route: route.abort())
    page = context.new_page()
    page.goto(url)
    page.wait_for_function("getComputedStyle(document.querySelector('[data-reveal]')).opacity === '1'")
    expect(page.locator("h1")).to_be_visible()
    context.close()
    print("PASS: normal-motion reveal")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshots", type=Path)
    args = parser.parse_args()
    if args.screenshots and not args.screenshots.is_dir():
        parser.error("--screenshots must be an existing directory")
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            url = f"http://127.0.0.1:{server.server_port}/dist/"
            check_fallback(browser, url, javascript=False)
            check_fallback(browser, url, blocked="presentation.js")
            check_fallback(browser, url, blocked="site.js")
            check_interactions(browser, url, args.screenshots)
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == "__main__":
    main()
