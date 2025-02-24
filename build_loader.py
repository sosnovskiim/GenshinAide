""" Файл, содержащий класс для загрузки сборки персонажа. """
import os

from PIL import Image, ImageGrab
from PyQt6.QtCore import QObject, pyqtSignal
from ambr import Character
from easyocr import Reader
from jellyfish import levenshtein_distance

from client import Client
from constants import *


class BuildLoader(QObject):
    """
    Служит для распознавания персонажа и последующей инициализации
    загрузки сборки персонажа в отдельном от интерфейса потоке.
    """
    build_is_not_loaded = pyqtSignal(str)
    build_loaded = pyqtSignal(dict)

    reader: Reader
    client: Client
    character: Character
    build: dict

    def __init__(self, reader: Reader, client: Client) -> None:
        super().__init__()
        self.reader = reader
        self.client = client

    def load_build(self) -> None:
        """
        Загружает сборку персонажа. В случае неудачи в процессе
        загрузки подаёт сигнал с текстом сообщения о соответствующей
        ошибке. В случае успешной загрузки подаёт сигнал, содержащий
        словарь с полной информацией о сборке распознанного персонажа.
        """
        message = self.__grab_screenshot()
        if message:
            self.build_is_not_loaded.emit(message)
            return
        message = self.__recognize_character()
        if message:
            self.build_is_not_loaded.emit(message)
            return
        message = self.__get_character_build()
        if message:
            self.build_is_not_loaded.emit(message)
            return
        self.build_loaded.emit(self.build)

    @staticmethod
    def __grab_screenshot() -> str | None:
        """
        Получает скриншот из буфера обмена, обрезая его и сохраняя
        необходимые фрагменты во временные файлы.

        :return: Сообщение об ошибке или None при успешном выполнении.
        """
        screenshot = ImageGrab.grabclipboard()
        if (screenshot is None or
                not isinstance(screenshot, Image.Image)):
            return "Ошибка: не найден скриншот в буфере обмена"
        screenshot.crop((1440, 120, 1840, 190)).save(SCREENSHOT_1)
        screenshot.crop((1490, 870, 1890, 940)).save(SCREENSHOT_2)

    def __recognize_character(self) -> str | None:
        """
        Распознаёт имя персонажа с ранее сохранённого скриншота.

        :return: Сообщение об ошибке или None при успешном выполнении.
        """
        result = self.reader.readtext(
            SCREENSHOT_1, detail=0, paragraph=True
        )
        os.remove(SCREENSHOT_1)
        if not result:
            result = self.reader.readtext(
                SCREENSHOT_2, detail=0, paragraph=True
            )
            os.remove(SCREENSHOT_2)
            if not result:
                return "Ошибка: не найден текст на скриншоте"
        character = self.__find_character(result[0].lower())
        if character:
            self.character = character
            return
        return "Ошибка: не удалось определить персонажа"

    def __find_character(
            self, character_name_raw: str
    ) -> Character | None:
        """
        Находит персонажа, имя которого соответствует распознанному.
        Учитывает несовпадение имени на одну или две буквы, которое
        может быть вызвано анимациями персонажа или эффектами фона.

        :param character_name_raw: Распознанное имя персонажа.
        :return: Найденный персонаж или None в противном случае.
        """
        character_distance_1 = None
        character_distance_2 = None
        for character in self.client.characters_by_id.values():
            distance = levenshtein_distance(
                character.name.lower(), character_name_raw
            )
            if distance == 0:
                return character
            elif distance == 1:
                character_distance_1 = character
            elif distance == 2:
                character_distance_2 = character
        if character_distance_1:
            return character_distance_1
        if character_distance_2:
            return character_distance_2

    def __get_character_build(self) -> str | None:
        """
        Возвращает сборку персонажа, обращаясь к клиенту приложения.

        :return: Сообщение об ошибке или None при успешном выполнении.
        """
        build = self.client.get_character_build(self.character.name)
        if not build:
            return "Ошибка: нет доступа к wotpack.ru"
        if (build.get(KEY_DESCRIPTION) and
                build.get(KEY_WEAPONS) and
                build.get(KEY_PARTIES) and
                build.get(KEY_ARTIFACTS)):
            build[KEY_CHARACTER] = self.character
            self.build = build
            return
        return "Ошибка: не удалось загрузить сборку персонажа"
