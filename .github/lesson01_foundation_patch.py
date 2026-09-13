from pathlib import Path
import re

lesson_path = Path('assets/lesson-01.js')
text = lesson_path.read_text(encoding='utf-8')

foundation_topics = r'''    {
      id: 'what', title: 'Что такое Revit и зачем он нужен', hint: 'Собираем модель здания из стен, дверей, окон и других объектов', tags: 'revit что это зачем bim бим модель здание объект стена дверь окно autocad cad чертежи',
      body: `<p><b>Revit — программа, в которой собирают информационную модель здания.</b> Не просто рисуют линии, похожие на стену, а ставят сам объект <b>«Стена»</b>. У него есть высота, толщина, материал, уровень и другие параметры.</p>
      <div class="r1-two"><div><h4>Когда чертишь линиями</h4><p>Линия сама не знает, что она стена. План, фасад и разрез легко начать править отдельно, а потом они расходятся.</p></div><div><h4>Когда работаешь в Revit</h4><p>Стена, дверь и окно — объекты одной модели. Планы, фасады, разрезы и 3D показывают эту же модель с разных сторон.</p></div></div>
      <div class="r1-example"><span class="r1-kicker">Простой пример</span><h4>Передвинул дверь один раз</h4><p>Она меняет положение на плане, в 3D и на тех фасадах и разрезах, где видна. Не потому что Revit угадывает, а потому что это один объект, а не несколько несвязанных рисунков.</p></div>
      <h4>Зачем это нужно</h4>${steps([
        '<b>Меньше ручного дублирования.</b> Не надо отдельно перерисовывать одно и то же изменение на каждом виде.',
        '<b>У объектов есть данные.</b> Размеры, материалы, уровни и марки можно использовать в видах и таблицах.',
        '<b>Проект проще проверять.</b> Можно открыть план, разрез или 3D и увидеть одну и ту же модель с нужной стороны.',
        '<b>Из модели получают документацию.</b> Планы, фасады, разрезы, листы и спецификации связаны с моделью.'
      ])}
      ${note('Revit и BIM — не одно и то же', 'Revit — один из инструментов. BIM шире: это процессы, правила, данные, люди и работа с информационной моделью на протяжении проекта.')}
      ${note('Revit не проектирует за тебя', 'Можно собрать красивую, но неправильную модель. Программа не заменяет понимание архитектуры, конструкций и норм.', 'r1-caution')}
      ${answer('Revit — это программа только для 3D?', '<p>Нет. 3D — лишь один из видов. Основная ценность в связанной модели, из которой получают планы, разрезы, фасады, таблицы и листы.</p>')}
      ${refs([['tour','обзор модели и связанных видов']])}`
    },
    {
      id: 'model', title: 'Как устроена модель: объект, параметр и вид', hint: 'Сначала пойми логику, потом кнопки перестанут выглядеть случайным набором', tags: 'модель объект элемент параметр свойства вид план разрез фасад 3d лист sheet view property',
      body: `<p>В Revit полезно сразу разделить пять вещей. Без этого интерфейс выглядит как кабина самолёта, которую зачем-то выдали первокурснику.</p>
      ${terms([
        ['Модель / Model','Само здание и все его элементы.'],
        ['Объект / Element','Конкретная стена, дверь, окно, уровень, перекрытие и т.д.'],
        ['Параметр / Parameter','Свойство объекта: высота, ширина, материал, уровень, комментарий.'],
        ['Вид / View','Способ посмотреть на модель: план, фасад, разрез, 3D, таблица.'],
        ['Лист / Sheet','Оформленная страница, на которую размещают виды перед печатью или PDF.']
      ])}
      <div class="r1-flow" aria-label="Логика модели Revit"><div><b>Объект модели</b><span>Например, дверь</span></div><span class="r1-flow-arrow" aria-hidden="true">→</span><div><b>Параметры</b><span>Размер, тип, уровень, комментарий</span></div><span class="r1-flow-arrow" aria-hidden="true">→</span><div><b>Виды и таблицы</b><span>Показывают и используют данные объекта</span></div></div>
      <h4>Попробуй на готовой модели</h4>${steps([
        'Открой учебную копию проекта. В Диспетчере проекта дважды открой план этажа.',
        'Выбери одну стену. В Свойствах найди её тип, нижнюю привязку и верхнюю привязку.',
        'Открой 3D-вид. Найди ту же стену. Это не копия стены, а тот же объект на другом виде.',
        'Сними выделение. В Свойствах теперь появятся параметры текущего вида, а не стены.'
      ])}
      ${note('Вид не хранит отдельное здание', 'План и 3D — разные окна в одну модель. Но у каждого вида есть собственные настройки масштаба, видимости и графики.')}
      ${answer('Если скрыть стену на одном виде, она удалится из модели?', '<p>Нет, если ты использовал скрытие на виде. Удаление элемента и управление его видимостью — разные действия.</p>')}
      ${refs([['properties','палитра свойств'],['browser','Диспетчер проекта'],['tour','работа с видами']])}`
    },
    {
      id: 'course', title: 'Что мы будем делать на курсе', hint: 'Один дом на весь семестр, а не новый файл ради каждой кнопки', tags: 'курс семестр дом результат rvt pdf участок dxf оси уровни стены перекрытия окна двери кровля лестница листы',
      body: `<p>На курсе не будем неделю изучать кнопку, а потом забывать, зачем она нужна. Берём <b>один дом</b> и постепенно доводим его от пустого проекта до понятной модели и двух листов PDF.</p>
      <div class="r1-file-grid"><div><b>1. Основа</b><p>Создаём проект, подключаем участок, ставим оси и уровни.</p></div><div><b>2. Дом</b><p>Стены, перекрытия, окна, двери, помещения, кровля и лестница.</p></div><div><b>3. Результат</b><p>Проверяем модель, приводим виды в порядок и собираем два листа.</p></div></div>
      <h4>Что должно остаться к концу семестра</h4>${steps([
        '<b>Один рабочий файл .RVT.</b> В нём находится модель твоего дома.',
        '<b>Два понятных листа PDF.</b> По ним можно понять проект без открытия Revit.',
        '<b>Умение самому найти и изменить элемент.</b> На финале нужно показать модель, а не только принести файл.',
        '<b>Понимание связей.</b> Что такое уровень, тип, экземпляр, вид и почему модель не должна разваливаться после небольшого изменения.'
      ])}
      ${note('Чего сейчас не требуется', 'Это учебная архитектурная модель, а не полный рабочий проект для стройки. Конструктивные расчёты, инженерные системы и полный комплект документации в первую пару не пытаемся запихнуть. Люди уже пробовали учить всё сразу, ничего хорошего из этого ритуала не вышло.')}
      <h4>Что сделать после этого пункта</h4>${steps([
        'Открой вкладку «Этапы работы» и быстро просмотри маршрут семестра.',
        'Вернись в первую пару. Дальше разберём, какой файл открывать, как его сохранить и где находятся основные окна.'
      ])}
      ${answer('Нужно ли на каждой паре начинать новый проект?', '<p>Нет. Почти весь семестр работаешь с тем же домом и постепенно его дополняешь.</p>')}
      ${refs([['create','создание проекта'],['tour','обзор проекта и видов']])}`
    },
    {
      id: 'home' '''
pattern = re.compile(r"    \{\n      id: 'why'.*?\n    \},\n    \{\n      id: 'home'", re.S)
text, count = pattern.subn(foundation_topics, text, count=1)
if count != 1:
    raise SystemExit(f'Expected one old foundation topic block, got {count}')
text = text.replace('data-r1-version="1.0.0"', 'data-r1-version="2.0.0"', 1)
old_header = '<h2 id="guide-title" tabindex="-1">Начало работы и интерфейс</h2><p>Создаём проект, разбираемся с окнами и сохраняем первую учебную копию. Забыл, где какая кнопка? Открой нужный пункт ниже.</p><div class="r1-header-notes"><span>8 раскрывающихся тем</span><span>Команды на русском и английском</span></div>'
new_header = '<h2 id="guide-title" tabindex="-1">Revit с нуля: модель, виды и интерфейс</h2><p>Сначала разберёмся, что вообще делает Revit и как устроена одна модель. Файлы, кнопки и окна идут уже после этого.</p><div class="r1-header-notes"><span>${topics.length} тем по порядку</span><span>Команды на русском и английском</span></div>'
if old_header not in text: raise SystemExit('Lesson header marker not found')
text = text.replace(old_header, new_header, 1)
text = text.replace('placeholder="Например: шаблон, сохранить, свойства"', 'placeholder="Например: модель, вид, шаблон"', 1)
old_practice = "${steps(['Создай проект из выбранного шаблона. Сохрани под своим именем как .RVT.','Открой план и 3D, расположи их рядом.','Найди Свойства, закрой их и верни через меню «Вид».','Выбери элемент и покажи его тип. Сними выделение и объясни, чьи параметры теперь в Свойствах.','Сохрани и снова открой файл. Назови, чем .RVT отличается от .RTE и .RFA.'])}<p><b>Если получилось:</b> ты можешь сам открыть проект, найти нужный вид и вернуться к работе. Если застрял, вернись к соответствующему пункту, а не начинай всё заново.</p>"
new_practice = "${steps(['Объясни своими словами: Revit хранит одну модель или набор несвязанных чертежей?','Покажи в готовом проекте объект, его параметры и два разных вида той же модели.','Создай проект из выбранного шаблона и сохрани под своим именем как .RVT.','Открой план и 3D, затем найди Диспетчер проекта и Свойства.','Назови, что делать с .RVT, .RTE и .RFA.'])}<p><b>Если получилось:</b> ты понимаешь базовую логику Revit и можешь сам открыть проект, найти нужный вид и продолжить работу. Кнопки потом меняются местами, эта логика остаётся.</p>"
if old_practice not in text: raise SystemExit('Final practice marker not found')
text = text.replace(old_practice, new_practice, 1)
text = text.replace("version:'1.0.0'", "version:'2.0.0'", 1)
lesson_path.write_text(text, encoding='utf-8')

visual_path = Path('assets/lesson-01-visuals.js')
visual = visual_path.read_text(encoding='utf-8')
visual_replacement = r'''    what: {
      file: 'what-is-revit.svg',
      alt: 'Учебная схема: Revit собирает модель здания из строительных объектов',
      caption: 'Revit хранит не просто линии, а объекты здания и их данные. Это учебная схема курса.'
    },
    model: {
      file: 'model-logic.svg',
      alt: 'Учебная схема логики Revit: объект, параметры, виды и листы',
      caption: 'Один объект модели имеет параметры и показывается на разных видах. Это учебная схема курса.'
    },
    course: {
      file: 'course-roadmap.svg',
      alt: 'Учебная схема курса Revit: основа проекта, модель дома и итоговые листы',
      caption: 'Весь семестр постепенно доводим один дом до рабочего RVT и двух листов PDF.'
    },
    home: {'''
visual_pattern = re.compile(r"    why: \{.*?\n    home: \{", re.S)
visual, count = visual_pattern.subn(visual_replacement, visual, count=1)
if count != 1: raise SystemExit(f'Expected one visuals foundation block, got {count}')
visual = visual.replace("version: '2.0.0'", "version: '3.0.0'", 1)
visual_path.write_text(visual, encoding='utf-8')

live_path = Path('lessons-live.js')
live = live_path.read_text(encoding='utf-8')
old = """      title: 'Начало работы и интерфейс',
      practice: 'Настройте рабочее место и создайте учебный проект из нужного шаблона.',
      points: [
        'Вступление: назначение Revit, применение и задачи.',"""
new = """      title: 'Revit с нуля: модель, виды и интерфейс',
      practice: 'Сначала разберитесь, что делает Revit и как устроена одна модель, затем создайте и сохраните учебный проект.',
      points: [
        'Что такое Revit и зачем он нужен.',
        'Модель, объекты, параметры, виды и листы.',
        'Что делаем на курсе и какой результат нужен.',"""
if old not in live: raise SystemExit('Live lesson marker not found')
live_path.write_text(live.replace(old,new,1),encoding='utf-8')

for file in ['.github/lesson-01/check.py','.github/workflows/lesson-01-live-check.yml']:
    path=Path(file)
    value=path.read_text(encoding='utf-8')
    value=value.replace('to_have_count(8)','to_have_count(10)')
    value=value.replace("#r1-why","#r1-what")
    value=value.replace("'Eight topics; later lessons remain hidden'","'Ten foundation-first topics; later lessons remain hidden'")
    value=value.replace("'All eight disclosures, steps, source links and self-check answers work'","'All ten disclosures, steps, source links and self-check answers work'")
    value=value.replace("assert len(result['images']) == 5","assert len(result['images']) >= 10")
    value=value.replace("All five local screenshots load; accessible image zoom closes with Escape","Lesson diagrams and interface screenshots load; accessible image zoom closes with Escape")
    path.write_text(value,encoding='utf-8')

svg_dir=Path('assets/lesson-01');svg_dir.mkdir(parents=True,exist_ok=True)
svg_dir.joinpath('what-is-revit.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" role="img" aria-labelledby="title desc"><title id="title">Что такое Revit</title><desc id="desc">Revit собирает модель здания из объектов, а затем показывает её на планах, фасадах, разрезах и в 3D.</desc><defs><style>.bg{fill:#f4f6ee}.card{fill:#fffefa;stroke:#cbd9ca;stroke-width:3}.ink{fill:#193e34}.muted{fill:#61796d}.accent{fill:#bd5938}.soft{fill:#e7efe2}.blue{fill:#e4eef3}.line{stroke:#193e34;stroke-width:5;fill:none;stroke-linecap:round;stroke-linejoin:round}.h{font:700 40px system-ui,sans-serif}.s{font:700 25px system-ui,sans-serif}.t{font:500 22px system-ui,sans-serif}.small{font:600 19px system-ui,sans-serif}</style></defs><rect class="bg" width="1200" height="675" rx="28"/><text class="ink h" x="60" y="72">Revit — модель здания, а не набор линий</text><text class="muted t" x="60" y="112">Ставим стены, двери и окна как объекты. Виды показывают одну и ту же модель.</text><g transform="translate(60 170)"><rect class="card" width="430" height="420" rx="24"/><text class="ink s" x="30" y="52">Объекты модели</text><rect class="soft" x="30" y="82" width="370" height="205" rx="18"/><path class="line" d="M85 238V125h225v113M85 238h270M150 238v-70h62v70M260 165h55v48h-55z"/><text class="accent small" x="30" y="330">Стена · дверь · окно · уровень</text><text class="muted t" x="30" y="370">У каждого объекта есть тип,</text><text class="muted t" x="30" y="402">размеры, материал и привязки.</text></g><path class="line" d="M525 380h105"/><path class="line" d="M610 360l20 20-20 20"/><g transform="translate(670 170)"><rect class="card" width="470" height="420" rx="24"/><text class="ink s" x="30" y="52">Виды этой же модели</text><g transform="translate(30 85)"><rect class="blue" width="190" height="120" rx="16"/><path class="line" d="M25 93h140V27H25zM70 27v66M116 27v66"/><text class="ink small" x="95" y="150" text-anchor="middle">План</text></g><g transform="translate(250 85)"><rect class="soft" width="190" height="120" rx="16"/><path class="line" d="M28 96h134V56l-67-35-67 35zM78 96V61h34v35"/><text class="ink small" x="95" y="150" text-anchor="middle">Фасад</text></g><text class="muted t" x="30" y="285">Разрез, 3D, таблица и лист тоже</text><text class="muted t" x="30" y="317">работают с этой же моделью.</text><rect class="soft" x="30" y="345" width="410" height="48" rx="14"/><text class="ink small" x="235" y="376" text-anchor="middle">Изменил объект → виды обновились</text></g></svg>''',encoding='utf-8')
svg_dir.joinpath('model-logic.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" role="img" aria-labelledby="title desc"><title id="title">Логика модели Revit</title><desc id="desc">Объект модели имеет параметры и отображается на видах, которые размещают на листах.</desc><defs><style>.bg{fill:#f4f6ee}.card{fill:#fffefa;stroke:#cbd9ca;stroke-width:3}.ink{fill:#193e34}.muted{fill:#61796d}.accent{fill:#bd5938}.green{fill:#e7efe2}.blue{fill:#e4eef3}.sand{fill:#f5eadf}.line{stroke:#193e34;stroke-width:5;fill:none;stroke-linecap:round;stroke-linejoin:round}.h{font:700 40px system-ui,sans-serif}.s{font:700 26px system-ui,sans-serif}.t{font:500 21px system-ui,sans-serif}.tag{font:700 18px system-ui,sans-serif}</style></defs><rect class="bg" width="1200" height="675" rx="28"/><text class="ink h" x="60" y="72">Как устроена одна модель Revit</text><text class="muted t" x="60" y="112">Объект хранится один раз. Параметры описывают его. Виды показывают его с нужной стороны.</text><g transform="translate(55 180)"><rect class="card" width="250" height="350" rx="24"/><rect class="green" x="24" y="24" width="202" height="128" rx="18"/><path class="line" d="M70 130V64h110v66M105 130V91h38v39"/><text class="accent tag" x="125" y="188" text-anchor="middle">ОБЪЕКТ</text><text class="ink s" x="125" y="224" text-anchor="middle">Дверь</text><text class="muted t" x="30" y="274">Один элемент</text><text class="muted t" x="30" y="307">в модели здания</text></g><path class="line" d="M325 355h75"/><path class="line" d="M380 335l20 20-20 20"/><g transform="translate(420 180)"><rect class="card" width="300" height="350" rx="24"/><text class="accent tag" x="150" y="55" text-anchor="middle">ПАРАМЕТРЫ</text><g transform="translate(28 85)"><rect class="sand" width="244" height="204" rx="18"/><text class="ink t" x="22" y="42">Тип: 900 × 2100</text><text class="ink t" x="22" y="82">Уровень: 1 этаж</text><text class="ink t" x="22" y="122">Материал: дерево</text><text class="ink t" x="22" y="162">Комментарий: спальня</text></g><text class="muted t" x="150" y="326" text-anchor="middle">Данные объекта</text></g><path class="line" d="M740 355h75"/><path class="line" d="M795 335l20 20-20 20"/><g transform="translate(835 180)"><rect class="card" width="310" height="350" rx="24"/><text class="accent tag" x="155" y="55" text-anchor="middle">ВИДЫ И ЛИСТЫ</text><g transform="translate(28 85)"><rect class="blue" width="115" height="90" rx="14"/><path class="line" d="M20 67h75V24H20zM53 24v43"/><text class="ink tag" x="57" y="118" text-anchor="middle">План</text></g><g transform="translate(167 85)"><rect class="green" width="115" height="90" rx="14"/><path class="line" d="M20 67h75V39L58 19 20 39z"/><text class="ink tag" x="57" y="118" text-anchor="middle">Фасад</text></g><text class="muted t" x="28" y="245">План, разрез, 3D,</text><text class="muted t" x="28" y="278">таблица и лист используют</text><text class="muted t" x="28" y="311">тот же объект и его данные.</text></g><rect class="green" x="225" y="570" width="750" height="55" rx="18"/><text class="ink s" x="600" y="606" text-anchor="middle">Это одна модель, а не несколько отдельных чертежей</text></svg>''',encoding='utf-8')
svg_dir.joinpath('course-roadmap.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" role="img" aria-labelledby="title desc"><title id="title">Маршрут курса Revit</title><desc id="desc">Один проект проходит путь от основы и модели дома к проверенным видам и двум листам PDF.</desc><defs><style>.bg{fill:#f4f6ee}.card{fill:#fffefa;stroke:#cbd9ca;stroke-width:3}.ink{fill:#193e34}.muted{fill:#61796d}.accent{fill:#bd5938}.green{fill:#e7efe2}.blue{fill:#e4eef3}.sand{fill:#f5eadf}.line{stroke:#193e34;stroke-width:5;fill:none;stroke-linecap:round;stroke-linejoin:round}.dash{stroke:#91a98f;stroke-width:6;fill:none;stroke-linecap:round;stroke-dasharray:12 15}.h{font:700 40px system-ui,sans-serif}.s{font:700 26px system-ui,sans-serif}.t{font:500 21px system-ui,sans-serif}.n{font:800 30px system-ui,sans-serif}</style></defs><rect class="bg" width="1200" height="675" rx="28"/><text class="ink h" x="60" y="72">Один дом на весь семестр</text><text class="muted t" x="60" y="112">Не заводим новый файл ради каждой темы. Постепенно доводим один RVT до нормального результата.</text><path class="dash" d="M175 340h850"/><g transform="translate(50 170)"><rect class="card" width="300" height="350" rx="24"/><circle class="blue" cx="55" cy="55" r="30"/><text class="accent n" x="55" y="66" text-anchor="middle">1</text><text class="ink s" x="30" y="120">Основа проекта</text><text class="muted t" x="30" y="165">Шаблон и сохранение</text><text class="muted t" x="30" y="200">Участок и DXF</text><text class="muted t" x="30" y="235">Оси и уровни</text><path class="line" d="M55 305h190M75 280v50M135 280v50M195 280v50"/></g><g transform="translate(450 170)"><rect class="card" width="300" height="350" rx="24"/><circle class="green" cx="55" cy="55" r="30"/><text class="accent n" x="55" y="66" text-anchor="middle">2</text><text class="ink s" x="30" y="120">Модель дома</text><text class="muted t" x="30" y="165">Стены и перекрытия</text><text class="muted t" x="30" y="200">Окна, двери, помещения</text><text class="muted t" x="30" y="235">Кровля и лестница</text><path class="line" d="M55 315V265h190v50M105 315v-80h90v80M130 315v-38h40v38"/></g><g transform="translate(850 170)"><rect class="card" width="300" height="350" rx="24"/><circle class="sand" cx="55" cy="55" r="30"/><text class="accent n" x="55" y="66" text-anchor="middle">3</text><text class="ink s" x="30" y="120">Понятный результат</text><text class="muted t" x="30" y="165">Проверенная модель</text><text class="muted t" x="30" y="200">Планы, разрез и фасады</text><text class="muted t" x="30" y="235">Два листа PDF</text><path class="line" d="M65 265h170v70H65zM85 285h70M85 305h120M85 325h95"/></g><rect class="green" x="260" y="570" width="680" height="55" rx="18"/><text class="ink s" x="600" y="606" text-anchor="middle">Финал: рабочий RVT + два понятных листа PDF</text></svg>''',encoding='utf-8')
