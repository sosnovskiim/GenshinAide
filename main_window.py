""" Файл интерфейса, сгенерированный с помощью библиотеки PyQt6. """
from PyQt6.QtCore import (QSize, QRect, Qt,
                          QMetaObject, QCoreApplication)
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QWidget, QStackedWidget, QScrollArea,
                             QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QToolButton,
                             QProgressBar, QLabel, QFrame)


class MainWindowUI(object):
    """ Содержит в виде полей все основные элементы интерфейса. """
    widget_main: QWidget
    stacked_widget: QStackedWidget
    page_start: QWidget
    page_main: QWidget
    widget_info: QWidget
    page_character: QWidget
    scroll_area: QScrollArea
    scroll_area_content: QWidget
    layout_scroll_area: QVBoxLayout
    layout_weapon_list: QGridLayout
    layout_artifact_list: QGridLayout
    layout_party_list: QGridLayout
    layout_title: QHBoxLayout
    button_start: QPushButton
    button_paste: QPushButton
    button_return: QToolButton
    progress_bar_update: QProgressBar
    label_update_title: QLabel
    label_update_spinner: QLabel
    label_message: QLabel
    label_info: QLabel
    label_build_spinner: QLabel
    label_element: QLabel
    label_name: QLabel
    label_star_1: QLabel
    label_star_2: QLabel
    label_star_3: QLabel
    label_star_4: QLabel
    label_star_5: QLabel
    label_gacha: QLabel
    label_description: QLabel
    label_weapon_title: QLabel
    label_artifact_title: QLabel
    label_party_title: QLabel

    def setup_ui(self, main_window):
        """
        Инициализирует все основные элементы интерфейса.

        :param main_window: Основное окно приложения.
        """
        font_family = "Bahnschrift Light Condensed"
        font_size_16 = QFont(font_family, 16)
        font_size_20 = QFont(font_family, 20)
        font_size_24 = QFont(font_family, 24)
        font_size_30 = QFont(font_family, 30)
        main_window.setObjectName("main_window")
        main_window.setMinimumSize(QSize(1280, 720))
        main_window.setMaximumSize(QSize(1280, 720))
        self.widget_main = QWidget(parent=main_window)
        self.widget_main.setObjectName("widget_main")
        self.stacked_widget = QStackedWidget(parent=self.widget_main)
        self.stacked_widget.setGeometry(QRect(0, 0, 1280, 720))
        self.stacked_widget.setObjectName("stacked_widget")
        self.page_start = QWidget()
        self.page_start.setObjectName("page_start")
        self.button_start = QPushButton(parent=self.page_start)
        self.button_start.setGeometry(QRect(570, 430, 140, 40))
        self.button_start.setFont(font_size_20)
        self.button_start.setObjectName("button_start")
        self.progress_bar_update = QProgressBar(
            parent=self.page_start
        )
        self.progress_bar_update.setGeometry(QRect(490, 470, 300, 6))
        self.progress_bar_update.setTextVisible(False)
        self.progress_bar_update.setObjectName("progress_bar_update")
        self.label_update_title = QLabel(parent=self.page_start)
        self.label_update_title.setGeometry(QRect(540, 430, 200, 30))
        self.label_update_title.setFont(font_size_16)
        self.label_update_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.label_update_title.setObjectName("label_update_title")
        self.label_update_spinner = QLabel(parent=self.page_start)
        self.label_update_spinner.setGeometry(QRect(615, 430, 50, 50))
        self.label_update_spinner.setObjectName(
            "label_update_spinner"
        )
        self.stacked_widget.addWidget(self.page_start)
        self.page_main = QWidget()
        self.page_main.setObjectName("page_main")
        self.widget_info = QWidget(parent=self.page_main)
        self.widget_info.setGeometry(QRect(140, 200, 1000, 300))
        self.widget_info.setObjectName("widget_info")
        self.button_paste = QPushButton(parent=self.widget_info)
        self.button_paste.setGeometry(QRect(380, 190, 240, 40))
        self.button_paste.setFont(font_size_20)
        self.button_paste.setObjectName("button_paste")
        self.label_message = QLabel(parent=self.widget_info)
        self.label_message.setGeometry(QRect(0, 250, 1000, 30))
        self.label_message.setFont(font_size_16)
        self.label_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_message.setObjectName("label_message")
        self.label_info = QLabel(parent=self.widget_info)
        self.label_info.setGeometry(QRect(0, 70, 1000, 100))
        self.label_info.setFont(font_size_20)
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_info.setObjectName("label_info")
        self.label_build_spinner = QLabel(parent=self.widget_info)
        self.label_build_spinner.setGeometry(QRect(475, 210, 50, 50))
        self.label_build_spinner.setObjectName("label_build_spinner")
        self.stacked_widget.addWidget(self.page_main)
        self.page_character = QWidget()
        self.page_character.setObjectName("page_character")
        self.scroll_area = QScrollArea(parent=self.page_character)
        self.scroll_area.setGeometry(QRect(100, 20, 1080, 680))
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_content = QWidget()
        self.scroll_area_content.setGeometry(QRect(0, 0, 1080, 911))
        self.scroll_area_content.setObjectName("scroll_area_content")
        self.layout_scroll_area = QVBoxLayout(
            self.scroll_area_content
        )
        self.layout_scroll_area.setContentsMargins(40, 20, 40, 20)
        self.layout_scroll_area.setSpacing(20)
        self.layout_scroll_area.setObjectName("layout_scroll_area")
        self.layout_title = QHBoxLayout()
        self.layout_title.setSpacing(10)
        self.layout_title.setObjectName("layout_title")
        self.label_element = QLabel(parent=self.scroll_area_content)
        self.label_element.setMinimumSize(QSize(50, 50))
        self.label_element.setMaximumSize(QSize(50, 50))
        self.label_element.setObjectName("label_element")
        self.layout_title.addWidget(self.label_element)
        self.label_name = QLabel(parent=self.scroll_area_content)
        self.label_name.setMinimumSize(QSize(0, 50))
        self.label_name.setMaximumSize(QSize(690, 50))
        self.label_name.setFont(font_size_30)
        self.label_name.setAlignment(
            Qt.AlignmentFlag.AlignBottom |
            Qt.AlignmentFlag.AlignLeading |
            Qt.AlignmentFlag.AlignLeft
        )
        self.label_name.setObjectName("label_name")
        self.layout_title.addWidget(self.label_name)
        self.label_star_1 = QLabel(parent=self.scroll_area_content)
        self.label_star_1.setMinimumSize(QSize(40, 40))
        self.label_star_1.setMaximumSize(QSize(40, 40))
        self.label_star_1.setObjectName("label_star_1")
        self.layout_title.addWidget(self.label_star_1)
        self.label_star_2 = QLabel(parent=self.scroll_area_content)
        self.label_star_2.setMinimumSize(QSize(40, 40))
        self.label_star_2.setMaximumSize(QSize(40, 40))
        self.label_star_2.setObjectName("label_star_2")
        self.layout_title.addWidget(self.label_star_2)
        self.label_star_3 = QLabel(parent=self.scroll_area_content)
        self.label_star_3.setMinimumSize(QSize(40, 40))
        self.label_star_3.setMaximumSize(QSize(40, 40))
        self.label_star_3.setObjectName("label_star_3")
        self.layout_title.addWidget(self.label_star_3)
        self.label_star_4 = QLabel(parent=self.scroll_area_content)
        self.label_star_4.setMinimumSize(QSize(40, 40))
        self.label_star_4.setMaximumSize(QSize(40, 40))
        self.label_star_4.setObjectName("label_star_4")
        self.layout_title.addWidget(self.label_star_4)
        self.label_star_5 = QLabel(parent=self.scroll_area_content)
        self.label_star_5.setMinimumSize(QSize(40, 40))
        self.label_star_5.setMaximumSize(QSize(40, 40))
        self.label_star_5.setObjectName("label_star_5")
        self.layout_title.addWidget(self.label_star_5)
        self.layout_scroll_area.addLayout(self.layout_title)
        self.label_gacha = QLabel(parent=self.scroll_area_content)
        self.label_gacha.setMinimumSize(QSize(1000, 500))
        self.label_gacha.setMaximumSize(QSize(1000, 500))
        self.label_gacha.setObjectName("label_gacha")
        self.layout_scroll_area.addWidget(self.label_gacha)
        self.label_description = QLabel(
            parent=self.scroll_area_content
        )
        self.label_description.setMinimumSize(QSize(1000, 0))
        self.label_description.setMaximumSize(QSize(1000, 16777215))
        self.label_description.setFont(font_size_20)
        self.label_description.setWordWrap(True)
        self.label_description.setObjectName("label_description")
        self.layout_scroll_area.addWidget(self.label_description)
        self.label_weapon_title = QLabel(
            parent=self.scroll_area_content
        )
        self.label_weapon_title.setMinimumSize(QSize(1000, 40))
        self.label_weapon_title.setMaximumSize(QSize(1000, 40))
        self.label_weapon_title.setFont(font_size_24)
        self.label_weapon_title.setObjectName("label_weapon_title")
        self.layout_scroll_area.addWidget(self.label_weapon_title)
        self.layout_weapon_list = QGridLayout()
        self.layout_weapon_list.setSpacing(12)
        self.layout_weapon_list.setObjectName("layout_weapon_list")
        self.layout_scroll_area.addLayout(self.layout_weapon_list)
        self.label_artifact_title = QLabel(
            parent=self.scroll_area_content
        )
        self.label_artifact_title.setMinimumSize(QSize(1000, 40))
        self.label_artifact_title.setMaximumSize(QSize(1000, 40))
        self.label_artifact_title.setFont(font_size_24)
        self.label_artifact_title.setObjectName(
            "label_artifact_title"
        )
        self.layout_scroll_area.addWidget(self.label_artifact_title)
        self.layout_artifact_list = QGridLayout()
        self.layout_artifact_list.setSpacing(12)
        self.layout_artifact_list.setObjectName(
            "layout_artifact_list"
        )
        self.layout_scroll_area.addLayout(self.layout_artifact_list)
        self.label_party_title = QLabel(
            parent=self.scroll_area_content
        )
        self.label_party_title.setMinimumSize(QSize(1000, 40))
        self.label_party_title.setMaximumSize(QSize(1000, 40))
        self.label_party_title.setFont(font_size_24)
        self.label_party_title.setObjectName("label_party_title")
        self.layout_scroll_area.addWidget(self.label_party_title)
        self.layout_party_list = QGridLayout()
        self.layout_party_list.setContentsMargins(92, -1, 92, -1)
        self.layout_party_list.setHorizontalSpacing(12)
        self.layout_party_list.setVerticalSpacing(24)
        self.layout_party_list.setObjectName("layout_party_list")
        self.layout_scroll_area.addLayout(self.layout_party_list)
        self.scroll_area.setWidget(self.scroll_area_content)
        self.button_return = QToolButton(parent=self.page_character)
        self.button_return.setGeometry(QRect(10, 10, 25, 25))
        self.button_return.setObjectName("button_return")
        self.stacked_widget.addWidget(self.page_character)
        main_window.setCentralWidget(self.widget_main)
        self.translate_ui(main_window)
        self.stacked_widget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(main_window)

    def translate_ui(self, main_window):
        """
        Задаёт текст для основных элементов интерфейса.

        :param main_window: Основное окно приложения.
        """
        _translate = QCoreApplication.translate
        main_window.setWindowTitle(_translate(
            "main_window", "Genshin Aide"
        ))
        self.button_start.setText(_translate(
            "main_window", "НАЧАТЬ"
        ))
        self.label_update_title.setText(_translate(
            "main_window", "ЗАГРУЗКА ОБНОВЛЕНИЯ"
        ))
        self.button_paste.setText(_translate(
            "main_window", "ВСТАВИТЬ СКРИНШОТ"
        ))
        self.label_info.setText(_translate(
            "main_window",
            "Находясь в игре, "
            "войдите в меню персонажа или галерею персонажей,\n"
            "выберите интересующего вас персонажа "
            "и сделайте скриншот игры (Alt + Print Screen).\n"
            "Затем используйте сочетание клавиш Ctrl + V "
            "или нажмите на кнопку ниже."
        ))
        self.label_weapon_title.setText(_translate(
            "main_window", "Лучшее оружие"
        ))
        self.label_artifact_title.setText(_translate(
            "main_window", "Лучшие артефакты"
        ))
        self.label_party_title.setText(_translate(
            "main_window", "Примеры отрядов"
        ))
