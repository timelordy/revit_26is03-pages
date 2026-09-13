from pathlib import Path
from urllib.request import Request, urlopen
import json
import re

assets = Path('assets/lesson-01')
assets.mkdir(parents=True, exist_ok=True)
shots = {
    'revit-home-2024.png': 'https://help.autodesk.com/cloudhelp/2024/ENU/RevitLT-GetStarted/images/GUID-BE73BD2D-2596-43C0-BFD8-FAFFD87253B2.png',
    'revit-3d-example.png': 'https://help.autodesk.com/cloudhelp/2024/ENU/RevitLT-DocumentPresent/images/GUID-DDD36267-D138-44D3-A4E5-E684F433A543.png',
}
for name, url in shots.items():
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 Revit-course-official-screenshot'})
    with urlopen(req, timeout=40) as response:
        body = response.read(8_000_001)
    if len(body) > 8_000_000 or not body.startswith(b'\x89PNG'):
        raise SystemExit('Invalid Autodesk screenshot: ' + name)
    (assets / name).write_bytes(body)

path = Path('assets/lesson-01-walkthrough.js')
text = path.read_text(encoding='utf-8')

old = '<div class="r1w-home-mock" aria-label="Упрощённая схема стартового экрана Revit"><div class="r1w-home-side"><b>Revit</b><span>Последние файлы</span><span>Autodesk Docs</span><span>Обучение</span></div><div class="r1w-home-main"><div><small>МОДЕЛИ / PROJECTS</small><b>Создать</b><b>Открыть</b><p>Здесь начинаем или открываем проект дома.</p></div><div><small>СЕМЕЙСТВА / FAMILIES</small><b>Создать</b><b>Открыть</b><p>Отдельные объекты: двери, окна, мебель. Пока сюда не лезем.</p></div><div class="r1w-home-recent"><small>ПОСЛЕДНИЕ ФАЙЛЫ</small><p>Недавно открытые проекты и семейства.</p></div></div></div>'
new = '${image(\'revit-home-2024.png\',\'Реальный стартовый экран Autodesk Revit 2024\',\'Реальный экран из справки Autodesk. Слева видны Models / Модели и кнопки Open / New. Нам сейчас нужна именно New.\')}<div class="r1w-four"><div><span>1</span><b>Models / Модели</b><p>Здесь создаём или открываем проект здания.</p></div><div><span>2</span><b>New / Создать</b><p>Эту кнопку нажимаем сейчас.</p></div><div><span>3</span><b>Open / Открыть</b><p>Она нужна, когда у тебя уже есть готовый .RVT.</p></div><div><span>4</span><b>Families / Семейства</b><p>Двери, окна и другие отдельные объекты. Пока не трогаем.</p></div></div>'
if old not in text:
    raise SystemExit('Public home mock block not found')
text = text.replace(old, new, 1)

replacements = {
    "${image('template-flow.svg','Схема: из шаблона RTE создаётся рабочий проект RVT','Шаблон нужен только как старт. Работать дальше будем уже в отдельном проекте.')}": '<p class="r1w-plain-note"><b>На этом шаге без картинки.</b> Смотри на реальное окно Revit перед собой: выбери Template file, ниже Project и нажми OK. Здесь важнее повторить три клика, чем смотреть на нарисованную копию окна.</p>',
    "${image('model-views.svg','Схема: одна модель Revit и несколько связанных видов','План, разрез, фасад и 3D — не отдельные здания. Это разные виды одной модели.')}": "${image('revit-3d-example.png','Реальный 3D-вид модели Autodesk Revit','Пример настоящего 3D-вида из справки Autodesk. У тебя модель будет проще — сейчас ищем только свою стену.')}",
    "${image('save-flow.svg','Схема сохранения рабочего проекта Revit и резервной копии','Основной файл курса — твой .RVT. После пары не оставляй единственную копию на компьютере аудитории.')}": '<p class="r1w-plain-note">Здесь без декоративной схемы: нажми путь выше в самом Revit, сохрани файл и сразу проверь его повторным открытием.</p>',
    "${image('file-types.svg','Что делать с файлами Revit RVT, RTE и RFA','Не зубри буквы. Смотри на действие, которое нужно сделать.')}": '<p class="r1w-plain-note">Тут картинка не нужна. Это не интерфейс Revit, а три типа файлов. Смотри на действие под каждым расширением.</p>',
}
for old, new in replacements.items():
    if old not in text:
        raise SystemExit('Expected fake walkthrough image not found: ' + old[:60])
    text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')

css = Path('assets/lesson-01-walkthrough.css')
css_text = css.read_text(encoding='utf-8')
if '.r1w-plain-note{' not in css_text:
    css_text += '\n.r1w-plain-note{margin:0 0 20px;padding:14px 16px;border:1px solid #dce5d9;border-radius:12px;background:#fff;color:#526b60;font-size:14px;line-height:1.6;}\n'
css.write_text(css_text, encoding='utf-8')

index = Path('index.html')
html = index.read_text(encoding='utf-8')
html, css_n = re.subn(r'assets/lesson-01-walkthrough\.css\?v=\d+', 'assets/lesson-01-walkthrough.css?v=2', html, count=1)
html, js_n = re.subn(r'assets/lesson-01-walkthrough\.js\?v=\d+', 'assets/lesson-01-walkthrough.js?v=2', html, count=1)
if css_n != 1 or js_n != 1:
    raise SystemExit(f'Could not bump walkthrough assets: css={css_n}, js={js_n}')
index.write_text(html, encoding='utf-8')

(assets / 'official-screenshots.json').write_text(json.dumps([
    {'file':'revit-home-2024.png','source':'https://help.autodesk.com/cloudhelp/2024/ENU/RevitLT-GetStarted/files/GUID-B6AD2298-C89C-4087-9C76-4759FEA8DB36.htm','image_url':shots['revit-home-2024.png'],'credit':'Autodesk screen shots reprinted courtesy of Autodesk, Inc.'},
    {'file':'revit-3d-example.png','source':'https://help.autodesk.com/cloudhelp/2024/ENU/RevitLT-DocumentPresent/files/GUID-D70048A8-71C4-47DB-9A7D-5463ADABAFF4.htm','image_url':shots['revit-3d-example.png'],'credit':'Autodesk screen shots reprinted courtesy of Autodesk, Inc.'}
], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
