""" Файл, содержащий класс основного окна приложения. """
import math
import sys
import time

from PyQt6.QtCore import QThread
from PyQt6.QtGui import (QIcon, QPixmap, QMovie, QColor,
                         QPainterPath, QPainter,
                         QKeySequence, QKeyEvent)
from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QLabel, QWidget, QGridLayout)
from ambr import Character, Weapon, ArtifactSet
from easyocr import Reader

# noinspection PyUnresolvedReferences
import resources
from build_loader import BuildLoader
from client import Client
from client_loader import ClientLoader
from constants import *
from main_window import MainWindowUI


class MainWindow(QMainWindow, MainWindowUI):
    """
    Реализует взаимодействие с пользователем и заполняет содержимым
    страницы основного окна приложения, в зависимости от действий
    пользователя.
    """
    loading_thread: QThread
    client_loader: ClientLoader
    build_loader: BuildLoader
    character: Character

    def __init__(self) -> None:
        super().__init__()
        # Устанавливается значок приложения.
        self.setWindowIcon(
            QIcon(f":/{DIRECTORY_ASSETS}/{IMAGE_APP_ICON}")
        )
        # Инициализируются все основные элементы интерфейса.
        self.setup_ui(self)
        # Подготавливается начальная страница приложения.
        self.__prepare_page_start()
        # Открывается начальная страница приложения.
        self.stacked_widget.setCurrentWidget(self.page_start)

    def __prepare_page_start(self) -> None:
        """
        Подготавливает к работе элементы интерфейса начальной страницы
        приложения и настраивает их внешний вид.
        """
        self.page_start.setStyleSheet(STYLE_PAGE_START)
        self.button_start.setStyleSheet(STYLE_BUTTON_START)
        self.button_start.clicked.connect(
            self.__on_click_button_start
        )
        self.movie_spinner = QMovie(
            f":/{DIRECTORY_ASSETS}/{IMAGE_LOADING_SPINNER}"
        )
        self.label_update_spinner.setMovie(self.movie_spinner)
        self.label_update_spinner.setScaledContents(True)
        self.label_update_spinner.setVisible(False)
        self.progress_bar_update.setStyleSheet(STYLE_PROGRESS_BAR)
        self.progress_bar_update.setVisible(False)
        self.label_update_title.setStyleSheet(STYLE_LABEL_TEXT)
        self.label_update_title.setVisible(False)

    def __on_click_button_start(self) -> None:
        """
        Обрабатывает нажатие на кнопку "Начать". Создаёт новый поток
        и помещает в него объект, служащий для загрузки клиента
        приложения и обновлений в случае их наличия. Затем запускает
        ранее созданный загрузочный поток и делает видимыми элементы,
        отображающие загрузку клиента.
        """
        self.loading_thread = QThread()
        self.client_loader = ClientLoader()
        self.client_loader.moveToThread(self.loading_thread)
        self.client_loader.client_loaded.connect(
            self.__init_build_loader
        )
        self.client_loader.some_image_loaded.connect(
            self.__update_progress_bar
        )
        self.client_loader.all_images_loaded.connect(
            self.__stop_image_loading
        )
        self.loading_thread.started.connect(
            self.client_loader.load_client
        )
        self.loading_thread.start()
        self.button_start.setVisible(False)
        self.label_update_spinner.setVisible(True)
        self.movie_spinner.start()

    def __init_build_loader(
            self, reader: Reader, client: Client
    ) -> None:
        """
        Создаёт объект, служащий для загрузки страницы персонажа, и
        помещает его в отдельный поток. В случае наличия обновлений
        делает видимыми элементы, отображающие их загрузку. В ином
        случае инициализирует подготовку основной страницы приложения.
        Затем скрывает элементы, отображающие загрузку клиента.

        :param reader: Объект, использующийся для распознавания имён
            персонажей на скриншотах игры.
        :param client: Клиент приложения.
        """
        self.build_loader = BuildLoader(reader, client)
        self.build_loader.moveToThread(self.loading_thread)
        self.build_loader.build_is_not_loaded.connect(
            self.__update_label_message
        )
        self.build_loader.build_loaded.connect(
            self.__update_page_character
        )
        self.loading_thread.started.disconnect()
        self.loading_thread.started.connect(
            self.build_loader.load_build
        )
        self.label_update_spinner.setVisible(False)
        self.movie_spinner.stop()
        if len(client.images_to_load) != 0:
            self.label_update_title.setVisible(True)
            self.progress_bar_update.setVisible(True)
        else:
            self.__update_page_main()

    def __update_progress_bar(self, progress: int) -> None:
        """
        Изменяет прогресс полосы загрузки во время обновления.

        :param progress: Целое число от 0 до 100.
        """
        self.progress_bar_update.setValue(progress)

    def __stop_image_loading(self) -> None:
        """
        Изменяет прогресс полосы загрузки на максимальный
        и инициализирует подготовку основной страницы приложения.
        """
        self.progress_bar_update.setValue(100)
        time.sleep(0.5)
        self.__update_page_main()

    def __update_page_main(self) -> None:
        """
        Завершает работу потока для загрузки клиента приложения.
        Подготавливает основную страницу приложения и страницу
        персонажа. Затем открывает основную страницу приложения.
        """
        self.loading_thread.quit()
        self.__prepare_page_main()
        self.__prepare_page_character()
        self.stacked_widget.setCurrentWidget(self.page_main)

    def __prepare_page_main(self) -> None:
        """
        Подготавливает к работе элементы интерфейса основной страницы
        приложения и настраивает их внешний вид.
        """
        self.page_main.setStyleSheet(STYLE_PAGE_MAIN)
        self.widget_info.setStyleSheet(STYLE_WIDGET_INFO)
        self.button_paste.setStyleSheet(STYLE_BUTTON_PASTE)
        self.button_paste.clicked.connect(
            self.__on_click_button_paste
        )
        self.label_info.setStyleSheet(STYLE_LABEL_TEXT)
        self.label_message.setStyleSheet(STYLE_LABEL_TEXT)
        self.label_build_spinner.setMovie(self.movie_spinner)
        self.label_build_spinner.setScaledContents(True)
        self.label_build_spinner.setVisible(False)

    def __prepare_page_character(self) -> None:
        """
        Подготавливает к работе элементы интерфейса основной страницы
        приложения и настраивает их внешний вид.
        """
        self.page_character.setStyleSheet(STYLE_PAGE_CHARACTER)
        self.scroll_area.setStyleSheet(STYLE_SCROLL_AREA)
        self.button_return.setStyleSheet(STYLE_BUTTON_RETURN)
        self.button_return.clicked.connect(
            self.__on_click_button_return
        )
        self.layout_title.addStretch()
        star_image = QPixmap(f"{DIRECTORY_ASSETS}/{IMAGE_STAR}")
        self.label_star_1.setPixmap(star_image)
        self.label_star_2.setPixmap(star_image)
        self.label_star_3.setPixmap(star_image)
        self.label_star_4.setPixmap(star_image)
        self.label_star_5.setPixmap(star_image)
        self.label_star_1.setScaledContents(True)
        self.label_star_2.setScaledContents(True)
        self.label_star_3.setScaledContents(True)
        self.label_star_4.setScaledContents(True)
        self.label_star_5.setScaledContents(True)
        self.label_name.setStyleSheet(STYLE_LABEL_TEXT)
        self.label_description.setStyleSheet(STYLE_LABEL_TEXT)
        self.label_weapon_title.setStyleSheet(STYLE_LABEL_TEXT)
        self.label_artifact_title.setStyleSheet(STYLE_LABEL_TEXT)
        self.label_party_title.setStyleSheet(STYLE_LABEL_TEXT)

    def keyPressEvent(self, a0) -> None:
        """
        Обрабатывает нажатие сочетания клавиш для вставки скриншота.

        :param a0: Событие нажатия на какие-либо клавиши.
        """
        if (self.stacked_widget.currentWidget() == self.page_main and
                a0.type() == QKeyEvent.Type.KeyPress and
                a0.matches(QKeySequence.StandardKey.Paste)):
            self.__on_click_button_paste()

    def __on_click_button_paste(self) -> None:
        """ Обрабатывает нажатие на кнопку "Вставить скриншот". """
        self.__start_loading_build()

    def __start_loading_build(self) -> None:
        """
        Запускает загрузочный поток и делает видимыми элементы,
        отображающие загрузку сборки персонажа.
        """
        self.loading_thread.start()
        self.button_paste.setVisible(False)
        self.label_message.setVisible(False)
        self.label_build_spinner.setVisible(True)
        self.movie_spinner.start()

    def __stop_loading_build(self) -> None:
        """
        Завершает работу загрузочного потока и скрывает элементы,
        отображающие загрузку сборки персонажа.
        """
        self.loading_thread.quit()
        self.button_paste.setVisible(True)
        self.label_message.setVisible(True)
        self.label_build_spinner.setVisible(False)
        self.movie_spinner.stop()

    def __update_label_message(self, message: str) -> None:
        """
        Завершает загрузку и обновляет сообщение об ошибке.

        :param message: Сообщение об ошибке.
        """
        self.__stop_loading_build()
        self.label_message.setText(message)

    def __update_page_character(self, build: dict) -> None:
        """
        Обновляет содержимое страницы персонажа и завершает загрузку.
        Затем открывает страницу персонажа.

        :param build: Словарь со сборкой персонажа.
        """
        self.character = build[KEY_CHARACTER]
        self.__update_label_element()
        self.__update_label_name()
        self.__update_label_rarity()
        self.__update_label_gacha()
        self.__update_label_description(build.get(KEY_DESCRIPTION))
        self.__update_weapon_list(build.get(KEY_WEAPONS))
        self.__update_artifact_list(build.get(KEY_ARTIFACTS))
        self.__update_party_list(build.get(KEY_PARTIES))
        self.__stop_loading_build()
        self.stacked_widget.setCurrentWidget(self.page_character)

    def __update_label_element(self) -> None:
        """ Обновляет элемент, отображающий стихию персонажа. """
        self.label_element.setPixmap(
            QPixmap(f"{DIRECTORY_ASSETS}/"
                    f"{self.character.element.lower()}.png")
        )
        self.label_element.setScaledContents(True)

    def __update_label_name(self) -> None:
        """ Обновляет элемент, содержащий имя персонажа. """
        self.label_name.setText(f"{self.character.name} |")

    def __update_label_rarity(self) -> None:
        """ Обновляет элемент, отображающий редкость персонажа. """
        self.label_star_5.setVisible(self.character.rarity == 5)

    def __update_label_gacha(self) -> None:
        """ Обновляет элемент, отображающий сплэш-арт персонажа. """
        self.label_gacha.setPixmap(
            QPixmap(f"{DIRECTORY_GACHA}/{self.character.id}.png")
        )
        self.label_gacha.setScaledContents(True)

    def __update_label_description(self, description: str) -> None:
        """
        Обновляет элемент, содержащий описание персонажа.

        :param description: Описание персонажа.
        """
        self.label_description.setText(description)

    def __update_weapon_list(
            self, weapons: list[list[Weapon]]
    ) -> None:
        """
        Обновляет макет, содержащий список оружия.

        :param weapons: Список, содержащий одну или две рекомендуемые
            сборки оружия.
        """
        if len(weapons) == 1:
            self.__update_weapon_list_with_one_build(weapons[0])
        else:
            self.__update_weapon_list_with_two_builds(weapons[:2])

    def __update_weapon_list_with_one_build(
            self, weapons: list[Weapon]
    ) -> None:
        """
        Обновляет макет, содержащий список оружия, в случае, когда
        персонаж имеет одну рекомендуемую сборку оружия.

        :param weapons: Список оружия.
        """
        # Цикл по i от 0 до количества элементов в макете, которое
        # определяется таким образом, чтобы уместились все
        # изображения оружий, а оставшееся пространство было заполнено
        # пустыми элементами, чтобы элементы макета не "разъезжались".
        for i in range(
                math.ceil(len(weapons) / COLUMNS_NUMBER) *
                COLUMNS_NUMBER
        ):
            # Определяются строка и столбец добавляемого элемента.
            row = int(i / COLUMNS_NUMBER)
            column = i % COLUMNS_NUMBER
            # Если индекс не вышел за границу списка, то на
            # соответствующую позицию в макете добавляется элемент
            # с изображением оружия, стоящего на позиции i.
            if i < len(weapons):
                self.__add_label_weapon(
                    weapons[i], row, column
                )
            # Иначе, на соответствующую позицию в макете
            # добавляется пустой элемент.
            else:
                self.__add_label_blank(
                    self.layout_weapon_list, row, column
                )

    def __update_weapon_list_with_two_builds(
            self, weapons: list[list[Weapon]]
    ) -> None:
        """
        Обновляет макет, содержащий список оружия, в случае, когда
        персонаж имеет две рекомендуемые сборки оружия.

        :param weapons: Списки оружия.
        """
        # Считается количество элементов, которое может быть размещено
        # в строке одной из половин макета, визуально обозначающих две
        # рекомендуемые сборки оружия.
        columns_number_half = COLUMNS_NUMBER // 2
        # Количество элементов, необходимое для корректного
        # отображения первой половины макета.
        rows_number_1 = math.ceil(
            len(weapons[0]) / columns_number_half
        )
        # Количество элементов, необходимое для корректного
        # отображения второй половины макета.
        rows_number_2 = math.ceil(
            len(weapons[1]) / columns_number_half
        )
        # Количество пустых элементов, которые должны занимать
        # центральный столбец между двумя половинами макета.
        blanks_number = max(rows_number_1, rows_number_2)
        row, column, i, j = 0, 0, 0, 0
        # Цикл, тело которого выполнится столько раз, сколько
        # элементов необходимо добавить в макет.
        for _ in range(blanks_number * COLUMNS_NUMBER):
            # Проверяется, что текущий индекс столбца относится
            # к первой половине макета.
            if column < columns_number_half:
                # Если индекс не вышел за границу списка, то на
                # соответствующую позицию в макете добавляется элемент
                # с изображением оружия, стоящего на позиции i.
                if i < len(weapons[0]):
                    self.__add_label_weapon(
                        weapons[0][i], row, column
                    )
                    # Индекс, указывающий на оружие в списке,
                    # увеличивается на 1.
                    i += 1
                # Иначе, на соответствующую позицию в макете
                # добавляется пустой элемент.
                else:
                    self.__add_label_blank(
                        self.layout_weapon_list, row, column
                    )
            # Иначе проверяется, что текущий индекс столбца совпадает
            # с индексом центрального столбца макета.
            elif column == columns_number_half:
                # На соответствующую позицию в макете добавляется
                # пустой элемент.
                self.__add_label_blank(
                    self.layout_weapon_list, row, column
                )
            # Иначе текущий индекс столбца однозначно относится
            # к второй половине макета.
            else:
                # Если индекс не вышел за границу списка, то на
                # соответствующую позицию в макете добавляется элемент
                # с изображением оружия, стоящего на позиции j.
                if j < len(weapons[1]):
                    self.__add_label_weapon(
                        weapons[1][j], row, column
                    )
                    # Индекс, указывающий на набор артефактов
                    # в списке, увеличивается на 1.
                    j += 1
                # Иначе, на соответствующую позицию в макете
                # добавляется пустой элемент.
                else:
                    self.__add_label_blank(
                        self.layout_weapon_list, row, column
                    )
            # Индекс, указывающий на столбец, увеличивается на 1.
            column += 1
            # Если индекс столбца вышел за границу макета, то
            # производится переход на следующую строку.
            if column == COLUMNS_NUMBER:
                column = 0
                row += 1

    def __update_artifact_list(
            self, artifacts: list[list[
                ArtifactSet | tuple[ArtifactSet, ArtifactSet]]]
    ) -> None:
        """
        Обновляет макет, содержащий список наборов артефактов.

        :param artifacts: Список, содержащий одну или две
            рекомендуемые сборки наборов артефактов.
        """
        if len(artifacts) == 1:
            self.__update_artifact_list_with_one_build(artifacts[0])
        else:
            self.__update_artifact_list_with_two_builds(artifacts[:2])

    def __update_artifact_list_with_one_build(
            self, artifacts: list[
                ArtifactSet | tuple[ArtifactSet, ArtifactSet]]
    ) -> None:
        """
        Обновляет макет, содержащий список наборов артефактов,
        в случае, когда персонаж имеет одну рекомендуемую сборку
        наборов артефактов.

        :param artifacts: Список наборов артефактов.
        """
        row, column = 0, 0
        # Цикл по i от 0 до количества элементов в списке.
        for i in range(len(artifacts)):
            # Проверяется, что очередным элементом списка является
            # так называемая "сборка артефактов 2+2".
            if isinstance(artifacts[i], tuple):
                # Если в строке макета не осталось места, чтобы
                # разместить два изображения артефактов, то
                # производится переход на следующую строку.
                if COLUMNS_NUMBER - column < 2:
                    column = 0
                    row += 1
                # На соответствующую позицию в макете добавляется
                # виджет, содержащий два элемента с изображениями
                # артефактов, полученных из кортежа, стоящего
                # в списке на позиции i.
                self.__add_widget_artifact(
                    artifacts[i], row, column
                )
                # Индекс, указывающий на столбец, увеличивается на 1.
                column += 1
            # Иначе элемент списка является одним набором артефактов.
            else:
                # На соответствующую позицию в макете добавляется
                # элемент с изображением артефакта, стоящего
                # в списке на позиции i.
                self.__add_label_artifact(
                    artifacts[i], row, column
                )
            # Индекс, указывающий на столбец, увеличивается на 1.
            column += 1
            # Если индекс столбца вышел за границу макета, то
            # производится переход на следующую строку.
            if column == COLUMNS_NUMBER:
                column = 0
                row += 1
        # Если последняя строка макета не была полностью заполнена
        # элементами, то в её конец добавляются пустые элементы.
        if column != 0:
            for column in range(column, COLUMNS_NUMBER):
                self.__add_label_blank(
                    self.layout_artifact_list, row, column
                )

    def __update_artifact_list_with_two_builds(
            self, artifacts: list[list[
                ArtifactSet | tuple[ArtifactSet, ArtifactSet]]]
    ) -> None:
        """
        Обновляет макет, содержащий список наборов артефактов,
        в случае, когда персонаж имеет две рекомендуемые сборки
        наборов артефактов.

        :param artifacts: Списки наборов артефактов.
        """
        # Считается количество элементов, которое может быть размещено
        # в строке одной из половин макета, визуально обозначающих две
        # рекомендуемые сборки артефактов.
        columns_number_half = COLUMNS_NUMBER // 2
        row, column, i, j = 0, 0, 0, 0
        # Цикл до тех пор, пока не закончатся элементы в обоих списках
        # рекомендуемых сборок наборов артефактов.
        while i < len(artifacts[0]) or j < len(artifacts[1]):
            # Проверяется, что текущий индекс столбца относится
            # к первой половине макета.
            if column < columns_number_half:
                # Проверяется, что индекс не вышел за границу списка.
                if i < len(artifacts[0]):
                    # Проверяется, что очередным элементом списка
                    # является так называемая "сборка артефактов 2+2".
                    if isinstance(artifacts[0][i], tuple):
                        # Проверяется, что в строке макета есть место,
                        # чтобы разместить два изображения артефактов.
                        if columns_number_half - column >= 2:
                            # На соответствующую позицию в макете
                            # добавляется виджет, содержащий два
                            # элемента с изображениями артефактов,
                            # полученных из кортежа, стоящего
                            # в списке на позиции i.
                            self.__add_widget_artifact(
                                artifacts[0][i], row, column
                            )
                            # Индекс, указывающий на столбец,
                            # увеличивается на 1.
                            column += 1
                            # Индекс, указывающий на кортеж наборов
                            # артефактов в списке, увеличивается на 1.
                            i += 1
                        # Иначе, на соответствующую позицию в макете
                        # добавляется пустой элемент.
                        else:
                            self.__add_label_blank(
                                self.layout_artifact_list,
                                row, column
                            )
                    # Иначе элемент списка является одним набором
                    # артефактов.
                    else:
                        # На соответствующую позицию в макете
                        # добавляется элемент с изображением
                        # артефакта, стоящего в списке на позиции i.
                        self.__add_label_artifact(
                            artifacts[0][i], row, column
                        )
                        # Индекс, указывающий на набор артефактов
                        # в списке, увеличивается на 1.
                        i += 1
                # Иначе, на соответствующую позицию в макете
                # добавляется пустой элемент.
                else:
                    self.__add_label_blank(
                        self.layout_artifact_list, row, column
                    )
            # Иначе проверяется, что текущий индекс столбца совпадает
            # с индексом центрального столбца макета.
            elif column == columns_number_half:
                # На соответствующую позицию в макете добавляется
                # пустой элемент.
                self.__add_label_blank(
                    self.layout_artifact_list, row, column
                )
            # Иначе текущий индекс столбца однозначно относится
            # к второй половине макета.
            else:
                # Проверяется, что индекс не вышел за границу списка.
                if j < len(artifacts[1]):
                    # Проверяется, что очередным элементом списка
                    # является так называемая "сборка артефактов 2+2".
                    if isinstance(artifacts[1][j], tuple):
                        # Проверяется, что в строке макета есть место,
                        # чтобы разместить два изображения артефактов.
                        if COLUMNS_NUMBER - column >= 2:
                            # На соответствующую позицию в макете
                            # добавляется виджет, содержащий два
                            # элемента с изображениями артефактов,
                            # полученных из кортежа, стоящего
                            # в списке на позиции i.
                            self.__add_widget_artifact(
                                artifacts[1][j], row, column
                            )
                            # Индекс, указывающий на столбец,
                            # увеличивается на 1.
                            column += 1
                            # Индекс, указывающий на кортеж наборов
                            # артефактов в списке, увеличивается на 1.
                            j += 1
                        # Иначе, на соответствующую позицию в макете
                        # добавляется пустой элемент.
                        else:
                            self.__add_label_blank(
                                self.layout_artifact_list,
                                row, column
                            )
                    # Иначе элемент списка является одним набором
                    # артефактов.
                    else:
                        self.__add_label_artifact(
                            artifacts[1][j], row, column
                        )
                        # Индекс, указывающий на набор артефактов
                        # в списке, увеличивается на 1.
                        j += 1
                # Иначе, на соответствующую позицию в макете
                # добавляется пустой элемент.
                else:
                    self.__add_label_blank(
                        self.layout_artifact_list, row, column
                    )
            # Индекс, указывающий на столбец, увеличивается на 1.
            column += 1
            # Если индекс столбца вышел за границу макета, то
            # производится переход на следующую строку.
            if column == COLUMNS_NUMBER:
                column = 0
                row += 1

    def __update_party_list(
            self, parties: list[list[Character]]
    ) -> None:
        """
        Обновляет макет, содержащий список отрядов.

        :param parties: Список, содержащий рекомендуемые отряды.
        """
        # Количество элементов в одной строке макета.
        columns_number = 9
        # Количество элементов в одной половине макета (количество
        # персонажей в полноценном отряде).
        columns_number_half = 4
        row, column, i, j = 0, 0, 0, 0
        # Цикл, тело которого выполнится столько раз, сколько
        # элементов необходимо добавить в макет.
        for _ in range(
                math.ceil(len(parties) / 2) * columns_number
        ):
            # Проверяется, что текущий индекс столбца не совпадает
            # с индексом центрального столбца макета.
            if column != columns_number_half:
                # Проверяется, что индекс не вышел за границу списка.
                if i < len(parties):
                    # На соответствующую позицию в макете добавляется
                    # элемент с изображением персонажа, стоящего
                    # в отряде на позиции j.
                    self.__add_label_character(
                        parties[i][j], row, column
                    )
                    # Индекс, указывающий на отряд в списке,
                    # увеличивается на 1.
                    j += 1
                    # Если персонажи в отряде закончились, то индекс,
                    # указывающий на отряд в списке увеличивается
                    # на 1, а индекс, указывающий на персонажа
                    # в отряде обнуляется.
                    if j == columns_number_half:
                        i += 1
                        j = 0
                # Иначе на соответствующую позицию в макете
                # добавляется пустой элемент.
                else:
                    self.__add_label_blank(
                        self.layout_party_list, row, column
                    )
            # Иначе на соответствующую позицию в макете добавляется
            # пустой элемент.
            else:
                self.__add_label_blank(
                    self.layout_party_list, row, column
                )
            # Индекс, указывающий на столбец, увеличивается на 1.
            column += 1
            # Если индекс столбца вышел за границу макета, то
            # производится переход на следующую строку.
            if column == columns_number:
                column = 0
                row += 1

    def __add_label_weapon(
            self, weapon: Weapon, row: int, column: int
    ) -> None:
        """
        Добавляет элемент с изображением оружия в соответствующий
        макет.

        :param weapon: Добавляемое оружие.
        :param row: Индекс строки в макете.
        :param column: Индекс столбца в макете.
        """
        label_weapon = QLabel(parent=self.scroll_area_content)
        label_weapon.setMinimumSize(LABEL_SIZE, LABEL_SIZE)
        label_weapon.setMaximumSize(LABEL_SIZE, LABEL_SIZE)
        # Изменяется фон элемента в зависимости от редкости оружия.
        if weapon.rarity == 5:
            label_weapon.setStyleSheet(STYLE_WEAPON_RARITY_5)
        elif weapon.rarity == 4:
            label_weapon.setStyleSheet(STYLE_WEAPON_RARITY_4)
        else:
            label_weapon.setStyleSheet(STYLE_WEAPON_RARITY_3)
        # Скругляются края элемента.
        icon_weapon = f"{DIRECTORY_WEAPON}/{weapon.id}.png"
        pixmap_weapon = QPixmap(icon_weapon)
        pixmap_weapon.fill(QColor(COLOR_TRANSPARENT))
        painter_path = QPainterPath()
        painter_path.addRoundedRect(
            0, 0, ICON_SIZE, ICON_SIZE, ICON_RADIUS, ICON_RADIUS
        )
        painter = QPainter(pixmap_weapon)
        painter.setClipPath(painter_path)
        painter.drawPixmap(0, 0, QPixmap(icon_weapon))
        painter.end()
        label_weapon.setPixmap(pixmap_weapon)
        label_weapon.setScaledContents(True)
        # Созданный элемент добавляется в соответствующий макет.
        self.layout_weapon_list.addWidget(
            label_weapon, row, column
        )

    def __add_widget_artifact(
            self, artifacts: tuple[ArtifactSet, ArtifactSet],
            row: int, column: int
    ) -> None:
        """
        Добавляет виджет, содержащий два элемента с изображениями
        артефактов в соответствующий макет.

        :param artifacts: Добавляемые наборы артефактов.
        :param row: Индекс строки в макете.
        :param column: Индекс столбца в макете.
        """
        widget_artifact = QWidget(parent=self.scroll_area_content)
        widget_artifact.setMinimumSize(LABEL_SIZE * 2, LABEL_SIZE)
        widget_artifact.setMaximumSize(LABEL_SIZE * 2, LABEL_SIZE)
        # Изменяется фон элемента в зависимости от максимальной
        # редкости набора артефактов.
        if artifacts[0].rarity_list[-1] == 5:
            widget_artifact.setStyleSheet(STYLE_ARTIFACT_RARITY_5)
        elif artifacts[0].rarity_list[-1] == 4:
            widget_artifact.setStyleSheet(STYLE_ARTIFACT_RARITY_4)
        else:
            widget_artifact.setStyleSheet(STYLE_ARTIFACT_RARITY_3)
        # В созданный виджет добавляется элемент с изображением
        # первого набора артефактов.
        self.__add_label_artifact(
            artifacts[0], widget_artifact=widget_artifact
        )
        # В созданный виджет добавляется элемент с изображением
        # второго набора артефактов.
        self.__add_label_artifact(
            artifacts[1], widget_artifact=widget_artifact,
            is_artifact_paired=True
        )
        # Созданный виджет добавляется в соответствующий макет.
        self.layout_artifact_list.addWidget(
            widget_artifact, row, column, 1, 2
        )

    def __add_label_artifact(
            self, artifact: ArtifactSet,
            row: int = 0, column: int = 0,
            widget_artifact: QWidget = None,
            is_artifact_paired: bool = False
    ) -> None:
        """
        Добавляет элемент с изображением набора артефактов
        в соответствующий макет.

        :param artifact: Добавляемый набор артефактов.
        :param row: Индекс строки в макете.
        :param column: Индекс столбца в макете.
        :param widget_artifact: Виджет для пары наборов артефактов.
        :param is_artifact_paired: Указывает, является ли набор
            артефактов вторым в паре.
        """
        label_artifact = QLabel()
        label_artifact.setMinimumSize(LABEL_SIZE, LABEL_SIZE)
        label_artifact.setMaximumSize(LABEL_SIZE, LABEL_SIZE)
        label_artifact.setPixmap(
            QPixmap(f"{DIRECTORY_ARTIFACT}/{artifact.id}.png")
        )
        label_artifact.setScaledContents(True)
        # Проверяется, имеет ли набор артефактов пару.
        if widget_artifact is not None:
            label_artifact.setParent(widget_artifact)
            label_artifact.setStyleSheet(STYLE_ARTIFACT_TRANSPARENT)
            label_artifact.setGeometry(
                LABEL_SIZE if is_artifact_paired else 0,
                0, LABEL_SIZE, LABEL_SIZE
            )
        # Иначе, набор артефактов не имеет пары.
        else:
            # Изменяется фон элемента в зависимости от максимальной
            # редкости набора артефактов.
            if artifact.rarity_list[-1] == 5:
                label_artifact.setStyleSheet(STYLE_ARTIFACT_RARITY_5)
            elif artifact.rarity_list[-1] == 4:
                label_artifact.setStyleSheet(STYLE_ARTIFACT_RARITY_4)
            elif artifact.rarity_list[-1] == 3:
                label_artifact.setStyleSheet(STYLE_ARTIFACT_RARITY_3)
            label_artifact.setParent(self.scroll_area_content)
            # Созданный элемент добавляется в соответствующий макет.
            self.layout_artifact_list.addWidget(
                label_artifact, row, column
            )

    def __add_label_character(
            self, character: Character, row: int, column: int
    ) -> None:
        """
        Добавляет элемент с изображением персонажа в соответствующий
        макет.

        :param character: Добавляемый персонаж.
        :param row: Индекс строки в макете.
        :param column: Индекс столбца в макете.
        """
        label_character = QLabel(parent=self.scroll_area_content)
        label_character.setMinimumSize(LABEL_SIZE, LABEL_SIZE)
        label_character.setMaximumSize(LABEL_SIZE, LABEL_SIZE)
        # Изменяется фон элемента в зависимости от стихии персонажа.
        if character.element == character.element.PYRO:
            label_character.setStyleSheet(STYLE_CHARACTER_PYRO)
        elif character.element == character.element.HYDRO:
            label_character.setStyleSheet(STYLE_CHARACTER_HYDRO)
        elif character.element == character.element.ANEMO:
            label_character.setStyleSheet(STYLE_CHARACTER_ANEMO)
        elif character.element == character.element.ELECTRO:
            label_character.setStyleSheet(STYLE_CHARACTER_ELECTRO)
        elif character.element == character.element.DENDRO:
            label_character.setStyleSheet(STYLE_CHARACTER_DENDRO)
        elif character.element == character.element.CRYO:
            label_character.setStyleSheet(STYLE_CHARACTER_CRYO)
        elif character.element == character.element.GEO:
            label_character.setStyleSheet(STYLE_CHARACTER_GEO)
        # Скругляются края элемента.
        icon_character = f"{DIRECTORY_AVATAR}/{character.id}.png"
        pixmap_character = QPixmap(icon_character)
        pixmap_character.fill(QColor(COLOR_TRANSPARENT))
        painter_path = QPainterPath()
        painter_path.addRoundedRect(
            0, 0, ICON_SIZE, ICON_SIZE, ICON_RADIUS, ICON_RADIUS
        )
        painter = QPainter(pixmap_character)
        painter.setClipPath(painter_path)
        painter.drawPixmap(0, 0, QPixmap(icon_character))
        painter.end()
        label_character.setPixmap(pixmap_character)
        label_character.setScaledContents(True)
        # Созданный элемент добавляется в соответствующий макет.
        self.layout_party_list.addWidget(
            label_character, row, column
        )

    def __add_label_blank(
            self, layout: QGridLayout, row: int, column: int
    ) -> None:
        """
        Добавляет пустой элемент в нужный макет.

        :param layout: Макет, в который необходимо добавить элемент.
        :param row: Индекс строки в макете.
        :param column: Индекс столбца в макете.
        """
        label_blank = QLabel(parent=self.scroll_area_content)
        label_blank.setMinimumSize(LABEL_SIZE, LABEL_SIZE)
        label_blank.setMaximumSize(LABEL_SIZE, LABEL_SIZE)
        layout.addWidget(label_blank, row, column)

    def __on_click_button_return(self) -> None:
        """ Обрабатывает нажатие на кнопку "Назад". """
        # Очищается элемент, содержащий сообщение об ошибке.
        self.label_message.clear()
        # Открывается основная страница приложения.
        self.stacked_widget.setCurrentWidget(self.page_main)
        # Устанавливается полоса прокрутки в верхнее положение.
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().minimum()
        )
        # Очищаются макеты, содержащие списки рекомендуемого оружия,
        # наборов артефактов и отрядов.
        for i in reversed(range(self.layout_weapon_list.count())):
            (self.layout_weapon_list
             .itemAt(i).widget().setParent(None))
        for i in reversed(range(self.layout_artifact_list.count())):
            (self.layout_artifact_list
             .itemAt(i).widget().setParent(None))
        for i in reversed(range(self.layout_party_list.count())):
            (self.layout_party_list
             .itemAt(i).widget().setParent(None))


if __name__ == "__main__":
    # Создаётся экземпляр класса приложения.
    app = QApplication(sys.argv)
    # Создаётся экземпляр класса основного окна приложения.
    main = MainWindow()
    # Подготовленное окно приложения выводится на экран.
    main.show()
    # Выход из программы привязывается к событию закрытия приложения.
    sys.exit(app.exec())
