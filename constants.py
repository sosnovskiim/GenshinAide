""" Файл со строковыми и числовыми константами. """
# noinspection PyUnresolvedReferences
import resources

# Название приложения.
APP_NAME = "Genshin Aide"

# Символ звезды, обозначающей редкость персонажей и предметов.
CHAR_STAR = "\u2b50"

# Названия файлов, хранящих временные обрезанные скриншоты игры.
SCREENSHOT_1 = "screenshot-1.png"
SCREENSHOT_2 = "screenshot-2.png"

# Ключи словаря, содержащего информацию о сборке персонажа.
KEY_CHARACTER = "character"
KEY_DESCRIPTION = "description"
KEY_WEAPONS = "weapons"
KEY_ARTIFACTS = "artifacts"
KEY_PARTIES = "parties"

# Числовые константы, используемые при заполнении страницы персонажа.
COLUMNS_NUMBER = 11
LABEL_SIZE = 80
ICON_SIZE = 256
ICON_RADIUS = 32

# Названия папок с необходимыми изображениями.
DIRECTORY_CONTENTS = "contents"
DIRECTORY_ASSETS = "assets"
DIRECTORY_GACHA = "gacha"
DIRECTORY_AVATAR = "avatar"
DIRECTORY_WEAPON = "weapon"
DIRECTORY_ARTIFACT = "artifact"

# Названия основных файлов изображений.
IMAGE_APP_ICON = "app-icon.png"
IMAGE_LOADING_SPINNER = "loading-spinner.gif"
IMAGE_BACKGROUND_START = "background-start.jpeg"
IMAGE_BACKGROUND_MAIN = "background-main.jpeg"
IMAGE_BUTTON_RETURN = "button-return.png"
IMAGE_STAR = "star-of-rarity.png"

# Числовые константы для таблиц стилей.
BORDER_RADIUS_2 = "2px"
BORDER_RADIUS_3 = "3px"
BORDER_RADIUS_10 = "10px"
BORDER_RADIUS_20 = "20px"
MARGIN_5 = "5px"
MARGIN_20 = "20px"
WIDTH_10 = "10px"

# Основные цвета.
COLOR_TRANSPARENT = "transparent"
COLOR_WHITE = "white"
COLOR_MAIN = "rgba(220, 135, 114, 120)"

# Цвета конкретных элементов интерфейса.
COLOR_BUTTON_START = "rgba(180, 180, 180, 120)"
COLOR_BUTTON_PASTE = "rgba(255, 255, 255, 60)"
COLOR_SCROLL_BAR = "rgba(255, 255, 255, 40)"

# Цвета редкости персонажей и предметов.
COLOR_RARITY_5 = "rgb(191, 120, 39)"
COLOR_RARITY_4 = "rgb(142, 108, 181)"
COLOR_RARITY_3 = "rgb(86, 128, 165)"

# Цвета элементов персонажей.
COLOR_PYRO = "rgb(216, 93, 53)"
COLOR_HYDRO = "rgb(64, 131, 217)"
COLOR_ANEMO = "rgb(0, 225, 141)"
COLOR_ELECTRO = "rgb(152, 112, 217)"
COLOR_DENDRO = "rgb(142, 166, 70)"
COLOR_CRYO = "rgb(74, 208, 239)"
COLOR_GEO = "rgb(209, 169, 26)"

# Таблицы стилей для страниц приложения.
STYLE_PAGE_START = (
    f"QWidget#page_start {{ background-image: "
    f"url(:/{DIRECTORY_ASSETS}/{IMAGE_BACKGROUND_START}); }}"
)
STYLE_PAGE_MAIN = (
    f"QWidget#page_main {{ background-image: "
    f"url(:/{DIRECTORY_ASSETS}/{IMAGE_BACKGROUND_MAIN}); }}"
)
STYLE_PAGE_CHARACTER = (
    f"QWidget#page_character {{ background-image: "
    f"url(:/{DIRECTORY_ASSETS}/{IMAGE_BACKGROUND_MAIN}); }}"
)

# Таблица стилей для полосы загрузки.
STYLE_PROGRESS_BAR = (
    f"QProgressBar {{ "
    f"background-color: {COLOR_TRANSPARENT}; "
    f"border: {COLOR_TRANSPARENT}; }}"
    "\n"
    f"QProgressBar::chunk {{ "
    f"background-color: {COLOR_WHITE}; "
    f"border-radius: {BORDER_RADIUS_3}; }}"
)

# Таблицы стилей для основных виджетов.
STYLE_WIDGET_INFO = (
    f"QWidget#widget_info {{ "
    f"background-color: {COLOR_MAIN}; "
    f"border-radius: {BORDER_RADIUS_20}; }}"
)
STYLE_SCROLL_AREA = (
    f"QScrollArea {{ "
    f"background-color: {COLOR_MAIN}; "
    f"border-radius: {BORDER_RADIUS_20}; }}"
    "\n"
    f"QScrollArea > QWidget > QWidget "
    f"{{ background-color: {COLOR_TRANSPARENT}; }}"
    "\n"
    f"QScrollBar:vertical {{ "
    f"background: {COLOR_TRANSPARENT}; "
    f"margin: {MARGIN_20} {MARGIN_5} {MARGIN_20} 0; "
    f"width: {WIDTH_10}; }}"
    "\n"
    f"QScrollBar::handle:vertical {{ "
    f"background-color: {COLOR_SCROLL_BAR}; "
    f"border-radius: {BORDER_RADIUS_2}; }}"
    "\n"
    "QScrollBar::add-line:vertical, "
    "QScrollBar::sub-line:vertical, "
    "QScrollBar::add-page:vertical, "
    "QScrollBar::sub-page:vertical "
    f"{{ background: {COLOR_TRANSPARENT}; }}"
)

# Таблицы стилей для кнопок.
STYLE_BUTTON_START = (
    f"QPushButton#button_start {{ "
    f"background-color: {COLOR_BUTTON_START}; "
    f"border-radius: {BORDER_RADIUS_10}; "
    f"color: {COLOR_WHITE}; }}"
)
STYLE_BUTTON_PASTE = (
    f"QPushButton#button_paste {{ "
    f"background-color: {COLOR_BUTTON_PASTE}; "
    f"border-radius: {BORDER_RADIUS_10}; "
    f"color: {COLOR_WHITE}; }}"
)
STYLE_BUTTON_RETURN = (
    f"QToolButton#button_return {{ "
    f"background-color: {COLOR_TRANSPARENT}; "
    f"image: url({DIRECTORY_ASSETS}/{IMAGE_BUTTON_RETURN}); }}"
)

# Таблица стилей для элементов, отображающих текст.
STYLE_LABEL_TEXT = f"color: {COLOR_WHITE};"

# Таблицы стилей для элементов, содержащих изображения оружия и
# обозначающих их редкость в виде цвета фона.
STYLE_WEAPON_RARITY_5 = (
    f"background-color: {COLOR_RARITY_5}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
STYLE_WEAPON_RARITY_4 = (
    f"background-color: {COLOR_RARITY_4}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
STYLE_WEAPON_RARITY_3 = (
    f"background-color: {COLOR_RARITY_3}; "
    f"border-radius: {BORDER_RADIUS_10};"
)

# Таблицы стилей для элементов, содержащих изображения артефактов и
# обозначающих их редкость в виде цвета фона.
STYLE_ARTIFACT_RARITY_5 = (
    f"background-color: {COLOR_RARITY_5}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
STYLE_ARTIFACT_RARITY_4 = (
    f"background-color: {COLOR_RARITY_4}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
STYLE_ARTIFACT_RARITY_3 = (
    f"background-color: {COLOR_RARITY_3}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
STYLE_ARTIFACT_TRANSPARENT = (
    f"background-color: {COLOR_TRANSPARENT};"
)

# Таблицы стилей для элементов, содержащих изображения персонажей и
# обозначающих их принадлежность к элементу в виде цвета фона.
STYLE_CHARACTER_PYRO = (
    f"background-color: {COLOR_PYRO}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
STYLE_CHARACTER_HYDRO = (
    f"background-color: {COLOR_HYDRO}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
STYLE_CHARACTER_ANEMO = (
    f"background-color: {COLOR_ANEMO}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
STYLE_CHARACTER_ELECTRO = (
    f"background-color: {COLOR_ELECTRO}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
STYLE_CHARACTER_DENDRO = (
    f"background-color: {COLOR_DENDRO}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
STYLE_CHARACTER_CRYO = (
    f"background-color: {COLOR_CRYO}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
STYLE_CHARACTER_GEO = (
    f"background-color: {COLOR_GEO}; "
    f"border-radius: {BORDER_RADIUS_10};"
)
