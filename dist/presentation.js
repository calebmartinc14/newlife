(() => {
  'use strict';
  const assets = { hand: 'assets/prosthesis.png', workshop: 'assets/workshop.png' };
  const slides = [
    { section:'inicio', label:'Portada', kicker:'NewLife 3D · Proyecto de clase', title:'Diseñar <em>nuevas posibilidades.</em>', lead:'Una propuesta de prótesis de mano personalizadas, desde el diseño digital hasta el prototipo.', image:assets.hand, alt:'Concepto generado con IA de una mano protésica en tonos grafito y cian', points:['Personalización','Fabricación bajo demanda','Diseño con una mirada circular'], note:'Proyecto conceptual. Las imágenes ilustran una idea, no un dispositivo existente.' },
    { section:'idea', label:'La empresa y la necesidad', kicker:'01 · La empresa', title:'Cada persona, <em>un punto de partida.</em>', lead:'NewLife diseñaría y prototiparía piezas de prótesis de mano adaptadas a cada caso.', points:['Necesidad: geometrías y ajustes que puedan revisarse para una persona concreta.','Clientes posibles: ortopedias, centros especializados y equipos de investigación.','Destinatarios: personas que necesiten una solución protésica, mediante profesionales cualificados.'], callout:'La propuesta nace en Granada: colaboración cercana y diseño documentado.', note:'Cualquier aplicación clínica exigiría evaluación y las autorizaciones correspondientes.' },
    { section:'producto', label:'El producto', kicker:'02 · Producto propuesto', title:'Una mano pensada <em>desde el ajuste.</em>', lead:'Un concepto de prótesis de mano con carcasas personalizadas y componentes sustituibles.', image:assets.hand, alt:'Visualización conceptual de una mano protésica generada con IA', points:['Adaptar medidas y geometría.','Revisar el modelo antes de volver a imprimir.','Estudiar el recambio de una pieza sin sustituir todo el conjunto.'], note:'Ventajas buscadas; el ajuste, la resistencia y la seguridad tendrían que comprobarse.' },
    { section:'producto', label:'Cómo funcionaría', kicker:'02 · Del diseño al prototipo', title:'Un proceso en <em>cuatro pasos.</em>', lead:'Un recorrido de fabricación propuesto, con revisión humana en cada etapa.', steps:[['01','Escuchar y medir','Definir necesidades con un profesional.'],['02','Diseñar en 3D','Crear el modelo CAD y revisar variantes.'],['03','Imprimir','Preparar las capas y fabricar una pieza de prueba.'],['04','Ensayar y ajustar','Analizar las pruebas y documentar una nueva versión.']], callout:'Medidas → modelo digital → pieza física → revisión', note:'Los ensayos conectados mediante IoT apoyarían la revisión del prototipo.' },
    { section:'tecnologia', label:'Tecnologías: impresión 3D e IA', kicker:'03 · Tecnologías habilitadoras · 1/2', title:'Del modelo a <em>la pieza.</em>', cards:[['3D','Impresión 3D','Fabricación de objetos capa a capa a partir de un modelo digital.','Imprimir una carcasa de prueba y fabricar solo esa pieza al cambiar sus medidas.'],['IA','Inteligencia artificial','Apoyo para comparar variantes de diseño con restricciones técnicas.','Proponer geometrías internas más ligeras; el equipo revisaría las opciones con simulaciones y ensayos.']], note:'Tecnologías del apartado 1 de los apuntes. La IA no certificaría la seguridad del diseño.' },
    { section:'tecnologia', label:'Tecnologías: IoT y nube', kicker:'03 · Tecnologías habilitadoras · 2/2', title:'Medir, compartir <em>y mejorar.</em>', cards:[['IoT','Internet de las cosas','Sensores conectados a una aplicación para consultar mediciones.','Enviar datos de fuerza y ciclos de apertura del banco de pruebas a un panel.'],['CL','Computación en la nube','Almacenamiento y colaboración sobre versiones de los modelos.','Compartir la versión 02 con el centro colaborador y recoger observaciones antes de imprimir.']], note:'Acceso autorizado y protección de datos como medidas transversales.' },
    { section:'sostenibilidad', label:'Sostenibilidad', kicker:'04 · Economía circular', title:'Fabricar lo necesario. <em>Reparar lo posible.</em>', lead:'Modelo elegido: producción JIT, bajo demanda. Se produciría tras definir el encargo, para limitar stock sin uso.', cards:[['01','Ecodiseño','Revisar el modelo digital y limitar soportes de impresión.','Comparar residuos y consumo por pieza para elegir mejoras.'],['02','Extensión de vida','Estudiar módulos sustituibles y recambios impresos.','Separar restos limpios por material y estudiar su recuperación en maquetas sin uso clínico.']], note:'La energía se mediría con IoT y registros en la nube. El beneficio ambiental tendría que comprobarse.' },
    { section:'mercado', label:'Mercado y diferenciación', kicker:'05 · Nuevos mercados', title:'Un servicio que continúa <em>después del diseño.</em>', image:assets.workshop, alt:'Taller de prototipado imaginario con impresora 3D, generado con IA', points:['Nueva necesidad: gestionar versiones y cambios del modelo en el tiempo.','Servicio propuesto: archivo digital y preparación de recambios bajo demanda.','Clientes: ortopedias, centros especializados, formación e investigación.','Diferenciación buscada: colaboración cercana, diseño modular y trazabilidad.'], note:'Referencias de competencia: Open Bionics y Ottobock. La comparación completa está en la web; no son colaboradores de NewLife.' },
    { section:'futuro', label:'Futuro: materiales avanzados', kicker:'06 · Tecnología emergente · 1/2', title:'Materiales con <em>nuevas posibilidades.</em>', lead:'Los materiales avanzados ofrecen propiedades específicas de resistencia, ligereza o respuesta al entorno.', points:['Propuesta: investigar un módulo de prueba con rigidez variable en zonas concretas.','Aplicación: comparar comportamientos sin fabricar una pieza completa para cada variante.','Ventaja buscada: explorar el equilibrio entre flexibilidad y soporte.'], callout:'Una línea de investigación, sujeta a ensayos de viabilidad y durabilidad.', note:'Apartado 5 de los apuntes. No se presenta como una solución desarrollada ni como una invención inédita.' },
    { section:'futuro', label:'Futuro: micro y nanoelectrónica', kicker:'06 · Tecnología emergente · 2/2', title:'Componentes pequeños. <em>Más puntos de medida.</em>', lead:'La micro y nanoelectrónica permite miniaturizar sensores y componentes de procesamiento.', points:['Propuesta: integrar una matriz de microsensores en una carcasa de prueba.','Aplicación: registrar el reparto de cargas durante ensayos controlados.','Ventaja buscada: obtener mediciones en más puntos con menos volumen añadido.'], callout:'Los datos orientarían ajustes del prototipo, con supervisión del equipo.', note:'Hipótesis de investigación. Afirmar que su uso no es habitual requeriría un estudio específico del sector.' },
    { section:'cierre', label:'Conclusión', kicker:'NewLife 3D · La idea en una frase', title:'Una prótesis empieza <em>con una persona.</em>', lead:'Diseño personalizado, fabricación digital y una mirada sostenible.', image:assets.workshop, alt:'Escena conceptual generada con IA de un taller de impresión 3D', points:['Escuchar antes de diseñar.','Probar antes de aplicar.','Medir antes de afirmar mejoras.'], note:'Gracias por escuchar. NewLife 3D es una propuesta académica de empresa del futuro.' }
  ];
  const deck = document.getElementById('presentation');
  const stage = document.getElementById('deck-stage');
  const picker = document.getElementById('deck-select');
  const prev = document.getElementById('deck-prev');
  const next = document.getElementById('deck-next');
  const count = document.getElementById('deck-count');
  const bar = document.getElementById('deck-bar');
  const live = document.getElementById('deck-live');
  const fullscreen = document.getElementById('deck-fullscreen');
  const exit = document.getElementById('deck-exit');
  let index = 0, opened = false, returnFocus = null, returnScroll = 0, touchStart = null;
  const background = [...document.querySelectorAll('body > header, body > main, body > footer')];
  const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const renderPoints = list => '<ul class="slide-points">'+list.map(text => '<li>'+escape(text)+'</li>').join('')+'</ul>';
  slides.forEach((slide, i) => {
    const el = document.createElement('article');
    el.className = 'deck-slide'; el.hidden = true; el.id = 'slide-'+(i+1);
    el.setAttribute('role','group'); el.setAttribute('aria-roledescription','diapositiva');
    el.setAttribute('aria-label',`${i+1} de ${slides.length}: ${slide.label}`);
    const heading = `<p class="slide-kicker">${escape(slide.kicker)}</p><h2 class="slide-title" id="slide-title-${i}">${slide.title}</h2>`;
    const intro = (slide.lead ? `<p class="slide-lead">${escape(slide.lead)}</p>` : '')+(slide.points ? renderPoints(slide.points) : '');
    if(slide.image){
      el.innerHTML = `<div class="slide-split"><div>${heading}${intro}</div><figure class="slide-figure"><img class="slide-image" src="${slide.image}" alt="${escape(slide.alt)}" decoding="async"><figcaption>Imagen conceptual generada con IA · No es un producto o taller real</figcaption></figure></div>`;
    }else{
      el.innerHTML = heading+intro;
      if(slide.cards) el.innerHTML += '<div class="slide-grid">'+slide.cards.map(([code,title,definition,example])=>`<div class="slide-block"><span class="slide-code">${escape(code)}</span><h3>${escape(title)}</h3><p>${escape(definition)}</p><p><strong>Ejemplo NewLife.</strong> ${escape(example)}</p></div>`).join('')+'</div>';
      if(slide.steps) el.innerHTML += '<div class="slide-steps">'+slide.steps.map(([code,title,text])=>`<div class="slide-block"><span class="slide-code">${code}</span><h3>${escape(title)}</h3><p>${escape(text)}</p></div>`).join('')+'</div>';
    }
    if(slide.callout) el.innerHTML += `<div class="slide-callout">${escape(slide.callout)}</div>`;
    if(slide.note) el.innerHTML += `<p class="slide-note">${escape(slide.note)}</p>`;
    stage.append(el);
    picker.add(new Option(`${String(i+1).padStart(2,'0')} · ${slide.label}`,String(i)));
  });
  const pages = [...stage.children];
  function show(value){
    index = Math.max(0,Math.min(slides.length-1,value));
    pages.forEach((page,i)=>{page.hidden=i!==index; if(i===index) page.scrollTop=0;});
    picker.value=String(index); prev.disabled=index===0; next.disabled=index===slides.length-1;
    count.textContent=`${String(index+1).padStart(2,'0')} / ${slides.length}`;
    bar.style.width=((index+1)/slides.length*100)+'%';
    live.textContent=`Diapositiva ${index+1} de ${slides.length}. ${slides[index].label}`;
  }
  function open(event){
    if(opened)return;
    returnFocus=event?.currentTarget || document.activeElement; returnScroll=window.scrollY;
    opened=true; deck.hidden=false; document.body.classList.add('presenting');
    background.forEach(el=>{el.inert=true;});
    show(index); exit.focus({preventScroll:true});
  }
  function close(section){
    if(!opened)return;
    opened=false;
    if(document.fullscreenElement===deck) document.exitFullscreen().catch(()=>{});
    deck.hidden=true;document.body.classList.remove('presenting'); background.forEach(el=>{el.inert=false;});
    if(section){document.getElementById(section)?.scrollIntoView({behavior:'instant'});const target=document.getElementById(section);if(target){target.setAttribute('tabindex','-1');target.focus({preventScroll:true});}}
    else {window.scrollTo({top:returnScroll,behavior:'instant'});returnFocus?.focus({preventScroll:true});}
  }
  document.querySelectorAll('[data-present]').forEach(button=>button.addEventListener('click',open));
  exit.addEventListener('click',()=>close());
  prev.addEventListener('click',()=>show(index-1));next.addEventListener('click',()=>show(index+1));
  picker.addEventListener('change',()=>show(Number(picker.value)));
  document.getElementById('deck-source').addEventListener('click',()=>close(slides[index].section));
  if(!deck.requestFullscreen)fullscreen.hidden=true;
  fullscreen.addEventListener('click',async()=>{
    try {if(document.fullscreenElement===deck)await document.exitFullscreen();else await deck.requestFullscreen();}
    catch{live.textContent='Pantalla completa no disponible. Puedes seguir presentando en esta ventana.';}
  });
  document.addEventListener('fullscreenchange',()=>{fullscreen.textContent=document.fullscreenElement===deck?'Reducir pantalla':'Pantalla completa';});
  document.addEventListener('keydown',event=>{
    if(!opened)return;
    if(event.key==='Escape'){event.preventDefault();close();return;}
    if(event.key==='Tab'){
      const focusables=[...deck.querySelectorAll('button:not(:disabled),select')].filter(el=>el.getClientRects().length);
      const first=focusables[0],last=focusables[focusables.length-1];
      if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
      else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}return;
    }
    if(event.altKey||event.ctrlKey||event.metaKey||event.target.matches('select,input,textarea,[contenteditable="true"]'))return;
    const key=event.key;
    if(['ArrowRight','ArrowDown','PageDown','ArrowLeft','ArrowUp','PageUp','Home','End'].includes(key)||(key===' '&&!event.target.matches('button'))){
      event.preventDefault();
      if(key==='Home')show(0);else if(key==='End')show(slides.length-1);
      else if(['ArrowLeft','ArrowUp','PageUp'].includes(key))show(index-1);else show(index+1);
    }
  });
  stage.addEventListener('touchstart',event=>{const t=event.changedTouches[0];touchStart={x:t.clientX,y:t.clientY};},{passive:true});
  stage.addEventListener('touchend',event=>{
    if(!touchStart)return;const t=event.changedTouches[0],dx=t.clientX-touchStart.x,dy=t.clientY-touchStart.y;
    if(Math.abs(dx)>70&&Math.abs(dx)>Math.abs(dy)*1.5)show(index+(dx<0?1:-1));touchStart=null;
  },{passive:true});
  stage.addEventListener('touchcancel',()=>{touchStart=null;},{passive:true});
  show(0);
})();
