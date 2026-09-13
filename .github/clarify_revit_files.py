from pathlib import Path
import re

path = Path('assets/lesson-01.js')
text = path.read_text(encoding='utf-8')
pattern = re.compile(r"    \{\n      id: 'home'.*?\n    \},\n    \{\n      id: 'save'", re.S)
replacement = r'''    {
      id: 'home', title: 'RVT, RTE и RFA: что с ними делать', hint: 'RVT открываем, из RTE создаём проект, RFA загружаем внутрь RVT', tags: 'главная recent home новый открыть rvt rte rfa models projects families проект шаблон семейство',
      body: `<p><b>Главное правило:</b> рабочий файл с домом — <code>.RVT</code>. <code>.RTE</code> нужен только в момент создания нового проекта. <code>.RFA</code> — отдельный объект, который обычно загружают в уже открытый <code>.RVT</code>.</p>
      <div class="r1-file-grid"><div><code>.RVT</code><b>Продолжить работу с домом</b><p><b>Файл → Открыть.</b> Это основной файл курса: модель, виды, листы и таблицы.</p></div><div><code>.RTE</code><b>Начать новый проект</b><p><b>Файл → Создать → Проект.</b> Выбираешь шаблон .RTE и получаешь новый .RVT.</p></div><div><code>.RFA</code><b>Добавить дверь, окно или мебель</b><p>Сначала открываешь .RVT, затем <b>Вставить → Загрузить семейство.</b></p></div></div>
      <h4>Выбери свою ситуацию</h4>${steps([
        '<b>Тебе прислали готовый файл дома <code>house.rvt</code>.</b> Открой его через <b>Файл → Открыть → Проект</b> (<span lang="en">File → Open → Project</span>) или <kbd>Ctrl</kbd> + <kbd>O</kbd>. Работаешь и сохраняешь изменения в этом файле.',
        '<b>Нужно начать новый дом, а у тебя есть <code>course.rte</code>.</b> Нажми <b>Файл → Создать → Проект</b> (<span lang="en">File → New → Project</span>), выбери .RTE и затем сохрани созданный проект как .RVT.',
        '<b>Тебе дали <code>window.rfa</code>.</b> Сначала открой свой .RVT. Потом нажми <b>Вставить → Загрузить семейство</b> (<span lang="en">Insert → Load Family</span>) и выбери .RFA. После загрузки окно можно поставить в модель.'
      ])}
      ${note('Что сдаём на курсе', 'Почти всегда итоговый рабочий файл — .RVT. .RTE и .RFA помогают начать проект или добавить объект, но не заменяют файл дома.')}
      ${note('Не делай так', 'Не моделируй весь дом внутри .RFA. Не сохраняй обычный рабочий проект как .RTE. Не открывай .RFA двойным щелчком, если твоя задача — просто поставить объект в дом.', 'r1-caution')}
      ${terms([['.RVT · Project','Открыть и продолжить работу с домом'],['.RTE · Project Template','Создать из шаблона новый проект .RVT'],['.RFA · Family','Загрузить объект в открытый проект .RVT']])}
      <p>Стартовый экран может немного отличаться после обновлений Revit 2024. Ориентируйся на действие и расширение файла, а не на точное место кнопки.</p>
      ${answer('Мне прислали три файла: house.rvt, course.rte и window.rfa. С чего начать?', '<p>Для продолжения работы открой <code>house.rvt</code>. <code>course.rte</code> нужен, только если надо создать новый проект. <code>window.rfa</code> загрузи внутрь открытого .RVT через «Вставить → Загрузить семейство».</p>')}
      ${refs([['open','открытие проектов и совместимость версий'],['create','создание проекта из шаблона'],['load','загрузка семейства в проект']])}`
    },
    {
      id: 'save' '''
text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f'Expected one home topic, replaced {count}')
path.write_text(text, encoding='utf-8')

path = Path('assets/lesson-01-visuals.js')
text = path.read_text(encoding='utf-8')
old = "file: 'file-types.svg',\n      alt: 'Учебная схема файлов Revit: RVT, RTE и RFA',\n      caption: 'Три файла, которые надо различать с первой пары: проект, шаблон и семейство.'"
new = "file: 'file-types.svg?v=4',\n      alt: 'Схема: RVT открывают и редактируют; из RTE создают новый проект RVT; RFA загружают в открытый RVT',\n      caption: 'Коротко: .RVT открываем и редактируем; из .RTE создаём новый .RVT; .RFA загружаем в открытый .RVT.'"
if old not in text:
    raise SystemExit('Visual description marker not found')
path.write_text(text.replace(old, new, 1), encoding='utf-8')

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 735" role="img" aria-labelledby="title desc">
<title id="title">Что делать с файлами Revit RVT, RTE и RFA</title><desc id="desc">RVT открывают и редактируют. Из RTE создают новый проект RVT. RFA загружают в открытый проект RVT.</desc>
<defs><style>.bg{fill:#f4f6ee}.card{fill:#fffefa;stroke:#cbd9ca;stroke-width:3}.ink{fill:#193e34}.muted{fill:#61796d}.accent{fill:#bd5938}.blue{fill:#e4eef3}.green{fill:#e8efe2}.sand{fill:#f5eadf}.result{fill:#dfeadc}.line{stroke:#193e34;stroke-width:5;fill:none;stroke-linecap:round;stroke-linejoin:round}.h{font:700 38px system-ui,sans-serif}.sub{font:550 23px system-ui,sans-serif}.ext{font:800 52px system-ui,sans-serif}.t{font:500 21px system-ui,sans-serif}.s{font:700 24px system-ui,sans-serif}.action{font:750 22px system-ui,sans-serif}.bottom{font:700 23px system-ui,sans-serif}</style></defs>
<rect class="bg" width="1200" height="735" rx="28"/>
<text class="ink h" x="60" y="67">Что делать с .RVT, .RTE и .RFA</text>
<text class="muted sub" x="60" y="108">.RVT открываем и редактируем. Из .RTE создаём новый .RVT.</text>
<text class="muted sub" x="60" y="140">.RFA загружаем в уже открытый .RVT.</text>
<g transform="translate(60 180)"><rect class="card" width="330" height="430" rx="24"/><rect class="blue" x="24" y="24" width="282" height="108" rx="18"/><text class="accent ext" x="52" y="96">.RVT</text><path class="line" d="M225 46h44v62h-44zM235 59h24M235 74h24M235 89h17"/><text class="ink s" x="32" y="177">Уже есть дом</text><text class="muted t" x="32" y="216">Это модель, виды,</text><text class="muted t" x="32" y="247">листы и таблицы.</text><text class="ink action" x="32" y="306">Файл → Открыть</text><text class="muted t" x="32" y="343">Работаешь и сохраняешь</text><text class="muted t" x="32" y="374">изменения в этом файле.</text></g>
<g transform="translate(435 180)"><rect class="card" width="330" height="430" rx="24"/><rect class="green" x="24" y="24" width="282" height="108" rx="18"/><text class="accent ext" x="52" y="96">.RTE</text><path class="line" d="M220 98V51h54v57M231 51V37h32v14M234 75h26"/><text class="ink s" x="32" y="177">Нужен новый проект</text><text class="muted t" x="32" y="216">Это стартовые настройки,</text><text class="muted t" x="32" y="247">а не рабочий файл дома.</text><text class="ink action" x="32" y="298">Файл → Создать</text><text class="ink action" x="32" y="329">→ Проект</text><text class="muted t" x="32" y="368">Выбираешь .RTE</text><text class="muted t" x="32" y="399">и получаешь новый .RVT.</text></g>
<g transform="translate(810 180)"><rect class="card" width="330" height="430" rx="24"/><rect class="sand" x="24" y="24" width="282" height="108" rx="18"/><text class="accent ext" x="52" y="96">.RFA</text><path class="line" d="M220 106V46h58v60M230 106V64h38v42M244 106V81h12v25"/><text class="ink s" x="32" y="177">Нужен отдельный объект</text><text class="muted t" x="32" y="216">Дверь, окно, мебель</text><text class="muted t" x="32" y="247">или оборудование.</text><text class="ink action" x="32" y="296">Открой .RVT</text><text class="ink action" x="32" y="327">→ Вставить</text><text class="ink action" x="32" y="358">→ Загрузить семейство</text><text class="muted t" x="32" y="399">Выбираешь файл .RFA.</text></g>
<rect class="result" x="60" y="640" width="1080" height="58" rx="18"/><text class="ink bottom" x="600" y="677" text-anchor="middle">Итоговый рабочий файл на курсе — .RVT</text>
</svg>'''
Path('assets/lesson-01/file-types.svg').write_text(svg, encoding='utf-8')

path = Path('index.html')
text = path.read_text(encoding='utf-8')
text = text.replace('assets/lesson-01.js?v=1', 'assets/lesson-01.js?v=2')
text = text.replace('assets/lesson-01-visuals.js?v=2', 'assets/lesson-01-visuals.js?v=4')
path.write_text(text, encoding='utf-8')
