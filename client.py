""" Файл, содержащий класс-клиент приложения. """
import asyncio
import os
import sys
import urllib.parse

import bs4.element
import requests
from ambr import AmbrAPI, Language, Character, Weapon, ArtifactSet
from bs4 import BeautifulSoup
from jellyfish import levenshtein_distance

from constants import *


class Client:
    """
    Служит для обращения к AmbrAPI с целью получения основных данных
    о персонажах и предметах игры, а также для парсинга страниц сайта
    Wotpack.ru с целью получения информации о сборках персонажей.
    """
    images_to_load: dict[str, str] = dict()
    characters_by_id: dict[str, Character]
    weapons_by_name: dict[str, Weapon]
    artifacts_by_name: dict[str, ArtifactSet]

    def __init__(self):
        # Если приложение запущено из exe-файла, то текущая рабочая
        # директория изменяется на папку с ресурсами приложения.
        if getattr(sys, "frozen", False):
            os.chdir(DIRECTORY_CONTENTS)
        self.characters_by_id = asyncio.run(self.__fetch_characters())
        self.weapons_by_name = asyncio.run(self.__fetch_weapons())
        self.artifacts_by_name = asyncio.run(self.__fetch_artifacts())

    async def __fetch_characters(self) -> dict[str, Character]:
        """
        Асинхронно загружает основные данные о персонажах игры.

        :return: Словарь, ключами которого являются id персонажей,
            а значениями экземпляры класса Character библиотеки ambr.
        """
        async with AmbrAPI(lang=Language.RU) as api:
            characters = await api.fetch_characters()
            result = dict()
            os.makedirs(DIRECTORY_GACHA, exist_ok=True)
            os.makedirs(DIRECTORY_AVATAR, exist_ok=True)
            gacha_images = set(os.listdir(DIRECTORY_GACHA))
            avatar_images = set(os.listdir(DIRECTORY_AVATAR))
            for character in characters:
                # Добавляется персонаж в словарь по id.
                result[character.id] = character
                # Если в папке с ресурсами отсутствуют его
                # изображения, то ссылки на их скачивание
                # добавляются в словарь для обновления приложения.
                if f"{character.id}.png" not in gacha_images:
                    self.images_to_load[character.gacha] = (
                        f"{DIRECTORY_GACHA}/{character.id}.png"
                    )
                if f"{character.id}.png" not in avatar_images:
                    self.images_to_load[character.icon] = (
                        f"{DIRECTORY_AVATAR}/{character.id}.png"
                    )
            return result

    async def __fetch_weapons(self) -> dict[str, Weapon]:
        """
        Асинхронно загружает основные данные об оружии игры.

        :return: Словарь, ключами которого являются названия оружия,
            а значениями экземпляры класса Weapon библиотеки ambr.
        """
        async with AmbrAPI(lang=Language.RU) as api:
            weapons = await api.fetch_weapons()
            result = dict()
            os.makedirs(DIRECTORY_WEAPON, exist_ok=True)
            weapon_images = set(os.listdir(DIRECTORY_WEAPON))
            for weapon in weapons:
                # Добавляется оружие в словарь по названию.
                result[weapon.name] = weapon
                # Если в папке с ресурсами отсутствует его
                # изображение, то ссылка на его скачивание
                # добавляется в словарь для обновления приложения.
                if f"{weapon.id}.png" not in weapon_images:
                    self.images_to_load[weapon.icon] = (
                        f"{DIRECTORY_WEAPON}/{weapon.id}.png"
                    )
            return result

    async def __fetch_artifacts(self) -> dict[str, ArtifactSet]:
        """
        Асинхронно загружает основные данные об артефактах игры.

        :return: Словарь, ключами которого являются названия
            наборов артефактов, а значениями экземпляры класса
            ArtifactSet библиотеки ambr.
        """
        async with AmbrAPI(lang=Language.RU) as api:
            artifacts = await api.fetch_artifact_sets()
            result = dict()
            os.makedirs(DIRECTORY_ARTIFACT, exist_ok=True)
            artifact_images = set(os.listdir(DIRECTORY_ARTIFACT))
            for artifact in artifacts:
                # Добавляется набор артефактов в словарь по названию.
                result[artifact.name] = artifact
                # Если в папке с ресурсами отсутствует его
                # изображение, то ссылка на его скачивание
                # добавляется в словарь для обновления приложения.
                if f"{artifact.id}.png" not in artifact_images:
                    self.images_to_load[artifact.icon] = (
                        f"{DIRECTORY_ARTIFACT}/{artifact.id}.png"
                    )
            return result

    def get_character_build(self, character_name: str) -> dict | None:
        """
        Возвращает информацию о сборке персонажа.

        :param character_name: Имя рассматриваемого персонажа.
        :return: Словарь с информацией о сборке персонажа или None
            в случае отсутствия доступа к сайту со статьями.
        """
        soup = self.__get_character_soup(character_name)
        if not soup:
            return
        description = ""
        weapons = list()
        artifacts = list()
        parties = list()
        # В цикле ищется заголовок, за которым следует краткое
        # описание боевых навыков персонажа.
        for header2 in soup.find_all("h2"):
            if "Лучш" in header2.text and "билд" in header2.text:
                tag = header2.find_next("p")
                # Сохраняется первый непустой абзац текста.
                while not description:
                    description = tag.text
                    tag = tag.find_next("p")
        # В цикле ищутся заголовки, за которыми следуют списки лучших
        # оружий, артефактов и отрядов для данного персонажа.
        for header3 in soup.find_all("h3"):
            if "Лучшее оружие" in header3.text:
                # Сохраняется каждый список рекомендуемого оружия.
                weapons.extend(
                    self.__get_character_weapons(header3)
                )
            if "Лучшие артефакты" in header3.text:
                # Сохраняется каждый список рекомендуемых артефактов.
                artifacts.extend(
                    self.__get_character_artifacts(header3)
                )
            if ("Лучшие команды" in header3.text
                    or "Примеры групп" in header3.text
                    or "Примеры отрядов" in header3.text):
                # Сохраняется каждый список рекомендуемых отрядов.
                parties.extend(
                    self.__get_character_parties(header3)
                )
        # Если текущим персонажем является Барбара, то рекомендуемые
        # отряды для неё получаются особенным образом.
        if character_name == "Барбара":
            parties.append(self.__get_barbara_parties())
        # Перегруппируется список отрядов для лучшей визуализации.
        parties = self.__group_character_parties(
            parties, character_name
        )
        return {
            KEY_DESCRIPTION: description,
            KEY_WEAPONS: weapons,
            KEY_ARTIFACTS: artifacts,
            KEY_PARTIES: parties
        }

    @staticmethod
    def __get_character_soup(
            character_name: str
    ) -> bs4.BeautifulSoup | None:
        """
        Возвращает загруженную страницу со статьёй о персонаже.

        :param character_name: Имя рассматриваемого персонажа.
        :return: Статья о персонаже или None в противном случае.
        """
        headers = {
            "Accept": "text/html",
            "User-Agent": (
                "Mozilla/5.0 "
                "(Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Mobile Safari/537.36"
            )
        }
        character_name = (character_name
                          .replace("Ё", "Е")
                          .replace("ё", "е"))
        keywords = ["билд", "сборк", "оруж"]
        # Цикл по всем ключевым словам для поиска статей.
        for keyword in keywords:
            # Формируется поисковый запрос с именем персонажа,
            # названием игры и одним из ключевых слов.
            search_query = urllib.parse.quote_plus(
                f"{character_name} в Genshin Impact {keyword}",
                encoding="utf-8"
            )
            url = "https://wotpack.ru/?s=" + search_query
            # Запрашиваются результаты поиска по созданному запросу.
            request = requests.get(url, headers)
            # Проверяется, что страница успешно загружена.
            if request.status_code == 200:
                # Парсинг страницы с результатами поиска.
                soup = BeautifulSoup(
                    request.text, features="html.parser"
                )
                # В цикле проверяются карточки всех найденных статей.
                for card in soup.find_all(
                        name="div", class_='post-card'
                ):
                    meta = card.find_next("meta").find_next("meta")
                    text = meta.get("content")
                    # Проверяется, что заголовок статьи на карточке
                    # содержит имя персонажа и ключевое слово.
                    if character_name in text and keyword in text:
                        url = meta.get("itemid")
                        # Запрашивается страница со статьей.
                        request = requests.get(url, headers)
                        # Проверяется, что страница успешно загружена.
                        if request.status_code == 200:
                            # Парсинг страницы со статьёй о персонаже.
                            soup = BeautifulSoup(
                                request.text, features="html.parser"
                            )
                            return soup

    def __get_character_weapons(
            self, header3: bs4.element.PageElement
    ) -> list[list[Weapon]]:
        """
        Возвращает списки оружия, рекомендуемого для персонажа.

        :param header3: Заголовок, за которым должна следовать
            таблица с рекомендуемым оружием.
        :return: Списки оружия.
        """
        result = list()
        # Находится следующая таблица.
        table = header3.find_next("tbody")
        # Считываются данные об оружии из неё.
        weapons = self.__read_weapons_table(table)
        # Если результат непустой, то он сохраняется.
        if weapons:
            result.append(weapons)
        # Находится следующий подзаголовок.
        header4 = table.find_next("h4")
        # Находится следующая таблица.
        table = table.find_next("tbody")
        # Проверяется, что заголовок, находящийся перед этой таблицей,
        # соответствует изначальному, так как в ином случае данная
        # таблица не содержит информацию об оружии.
        if table.find_previous("h3").text == header3.text:
            # Считываются данные об оружии из неё.
            weapons = self.__read_weapons_table(table)
            # Если между этими таблицами существует подзаголовок, то
            # вторая таблица относится к альтернативной сборке
            # персонажа и её данные добавляются отдельным списком.
            # В ином случае обе таблицы относятся к одной и той же
            # сборке персонажа и данные сохраняются в один список.
            if (header4 is not None and
                    table.find_previous("h4").text == header4.text):
                if weapons:
                    result.append(weapons)
            else:
                for weapon in weapons:
                    result[0].append(weapon)
        return result

    def __read_weapons_table(
            self, table: bs4.element.Tag
    ) -> list[Weapon]:
        """
        Возвращает список оружия, считанный из полученной таблицы.

        :param table: Таблица, содержащая рекомендуемое оружие.
        :return: Список оружия.
        """
        result = list()
        # Цикл по всем строкам таблицы.
        for row in table.find_all("tr"):
            # Считывается первая ячейка строки таблицы.
            tag = row.find_next("td")
            # Если текст в ячейке слишком короткий, значит в ней
            # содержится номер строки таблицы или изображение.
            # В таком случае осуществляется переход к следующей ячейке
            # таблицы до тех пор, пока не будет найдена нужная ячейка.
            text = ""
            while len(text) < 4:
                text = tag.text
                tag = tag.find_next()
            # Если текст ячейки содержит звезду редкости,
            # то она и весь текст после неё обрезаются.
            star_index = text.find(CHAR_STAR)
            if star_index != -1:
                text = text[:star_index]
            # Если текст ячейки содержит открывающуюся скобку,
            # то она и весь текст после неё обрезаются.
            bracket_index = text.find("(")
            if bracket_index != -1:
                text = text[:bracket_index]
            # Исправляется грубая ошибка в названии одного из оружий,
            # если в ячейке содержится именно его название.
            if text == "Переправа Флев Сандре ":
                text = "Перевозчик Флёв Сандр"
            # Считывается оружие, содержащееся в данной ячейке.
            weapon = self.__read_weapon(text.strip())
            # Если результат непустой, то он сохраняется.
            if weapon:
                result.append(weapon)
            else:
                # Иначе текст в ячейке делится на слова. После чего,
                # функции, считывающей название оружия, передаются
                # сначала первое слово, затем первое и второе слово,
                # и так далее. Тем самым обеспечивается определение
                # оружия в том случае, когда после него следует
                # ещё какой-то текст, не относящийся к его названию.
                words = text.split()
                text = ""
                for i in range(min(len(words), 5)):
                    text += words[i] + " "
                    weapon = self.__read_weapon(text.strip())
                    if weapon:
                        result.append(weapon)
                        break
        return result

    def __read_weapon(
            self, weapon_name_raw: str
    ) -> Weapon | None:
        """
        Возвращает оружие, найденное в полученном тексте.

        :param weapon_name_raw: Часть текста из ячейки таблицы.
        :return: Найденное оружие или None в противном случае.
        """
        # Если текст уже является названием, то сразу же возвращается
        # оружие с соответствующим названием.
        if weapon_name_raw in self.weapons_by_name:
            return self.weapons_by_name[weapon_name_raw]
        weapon_distance_1 = None
        weapon_distance_2 = None
        weapon_distance_3 = None
        weapon_distance_4 = None
        # Цикл по всем названиям оружий.
        for weapon_name in self.weapons_by_name.keys():
            # Считается расстояние Левенштейна между названием
            # в списке и текстом, полученным в качестве параметра.
            distance = levenshtein_distance(
                weapon_name, weapon_name_raw
            )
            # Если расстояние Левенштейна находится в диапазоне 1-4,
            # то название из списка сохраняется в переменную,
            # обозначающую соответствующее расстояние.
            if distance == 1:
                weapon_distance_1 = weapon_name
            elif distance == 2:
                weapon_distance_2 = weapon_name
            elif distance == 3:
                weapon_distance_3 = weapon_name
            elif distance == 4:
                weapon_distance_4 = weapon_name
        # Если в списке найдены названия, расстояния Левенштейна
        # до которых в диапазоне 1-4, то возвращается оружие
        # с минимальным расстоянием до его названия.
        if weapon_distance_1:
            return self.weapons_by_name[weapon_distance_1]
        if weapon_distance_2:
            return self.weapons_by_name[weapon_distance_2]
        if weapon_distance_3:
            return self.weapons_by_name[weapon_distance_3]
        if weapon_distance_4:
            return self.weapons_by_name[weapon_distance_4]

    def __get_character_artifacts(
            self, header3: bs4.element.PageElement
    ) -> list[list[ArtifactSet | tuple[ArtifactSet, ArtifactSet]]]:
        """
        Возвращает списки наборов артефактов, рекомендуемых
        для персонажа.

        :param header3: Заголовок, за которым должна следовать
            таблица с рекомендуемыми наборами артефактов.
        :return: Списки наборов артефактов.
        """
        result = list()
        # Находится следующая таблица.
        table = header3.find_next("tbody")
        # Считываются данные об артефактах из неё.
        artifacts = self.__read_artifacts_table(table)
        # Если результат непустой, то он сохраняется.
        if artifacts:
            result.append(artifacts)
        # Находится следующий подзаголовок.
        header4 = table.find_next("h4")
        # Находится следующая таблица.
        table = table.find_next("tbody")
        # Проверяется, что заголовок, находящийся перед этой таблицей,
        # соответствует изначальному, так как в ином случае данная
        # таблица не содержит информацию об артефактах.
        if (table.find_previous("h3").text == header3.text and
                table.find_previous("h2").text ==
                header3.find_previous("h2").text):
            # Считываются данные об артефактах из неё.
            artifacts = self.__read_artifacts_table(table)
            # Если между этими таблицами существует подзаголовок, то
            # вторая таблица относится к альтернативной сборке
            # персонажа и её данные добавляются отдельным списком.
            # В ином случае обе таблицы относятся к одной и той же
            # сборке персонажа и данные сохраняются в один список.
            if (header4 is not None and
                    table.find_previous("h4").text == header4.text):
                if artifacts:
                    result.append(artifacts)
            else:
                for artifact in artifacts:
                    result[0].append(artifact)
        return result

    def __read_artifacts_table(self, table: bs4.element.Tag) -> (
            list[ArtifactSet | tuple[ArtifactSet, ArtifactSet]]
    ):
        """
        Возвращает список наборов артефактов, считанный из полученной
        таблицы.

        :param table: Таблица, содержащая рекомендуемые наборы
            артефактов.
        :return: Список наборов артефактов.
        """
        result = list()
        # Цикл по всем строкам таблицы.
        for row in table.find_all("tr"):
            # Считывается первая ячейка строки таблицы.
            tag = row.find_next("td")
            # Если текст в ячейке слишком короткий, значит в ней
            # содержится номер строки таблицы или изображение.
            # В таком случае осуществляется переход к следующей ячейке
            # таблицы до тех пор, пока не будет найдена нужная ячейка.
            while len(tag.text) < 4:
                tag = tag.find_next()
            artifacts = list()
            # Так как в одной ячейки таблицы может быть перечислено
            # несколько наборов артефактов, то отдельные фрагменты
            # текста ячейки разделяются с помощью точки с запятой.
            raw = tag.get_text(separator=";", strip=True)
            # Цикл по всем фрагментам текста ячейки.
            for text in raw.split(";"):
                # Если фрагмент текста слишком короткий или содержит
                # открывающуюся скобку, то он не рассматривается.
                if len(text) < 4 or "(" in text:
                    continue
                # Фрагмент текста разделяется на ещё меньшие фрагменты
                # по символам "+", так как ими могут быть разделены
                # так называемые "сборки артефактов 2+2".
                text_sep_by_pluses = text.split("+")
                # Цикл по фрагментам, разделённым по символам "+".
                for text_without_pluses in text_sep_by_pluses:
                    # Меньший фрагмент текста, разделяется на ещё
                    # меньшие фрагменты по символам "/", так как
                    # ими могут быть разделены наборы артефактов,
                    # имеющие одинаковый эффект от двух частей набора.
                    text_sep_by_slashes = (
                        text_without_pluses.split("/")
                    )
                    # Цикл по фрагментам, разделённым по символам "/".
                    for text_without_slashes in text_sep_by_slashes:
                        if CHAR_STAR not in text_without_slashes:
                            # Если фрагмент текста не содержит
                            # звезды редкости, то считывается
                            # набор артефактов, записанный в нём.
                            artifact = self.__read_artifact(
                                text_without_slashes.strip()
                            )
                            # Если результат непустой,
                            # то он сохраняется.
                            if artifact:
                                artifacts.append(artifact)
            # Полученный из данной ячейки список артефактов
            # передаётся функции, которая выделит необходимые
            # один или два набора артефактов из этого списка.
            artifact_row = self.__read_artifact_row(artifacts)
            # Если результат непустой, то он сохраняется.
            if artifact_row:
                result.append(artifact_row)
        return result

    def __read_artifact(
            self, artifact_name_raw: str
    ) -> ArtifactSet | None:
        """
        Возвращает набор артефактов, найденный в полученном тексте.

        :param artifact_name_raw: Часть текста из ячейки таблицы.
        :return: Найденный набор артефактов или
            None в противном случае.
        """
        # Если текст уже является названием, то сразу же возвращается
        # набор артефактов с соответствующим названием.
        if artifact_name_raw in self.artifacts_by_name:
            return self.artifacts_by_name[artifact_name_raw]
        artifact_distance_1 = None
        artifact_distance_2 = None
        artifact_distance_3 = None
        artifact_distance_4 = None
        # Цикл по всем названиям наборов артефактов.
        for artifact_name in self.artifacts_by_name.keys():
            # Считается расстояние Левенштейна между названием
            # в списке и текстом, полученным в качестве параметра.
            distance = levenshtein_distance(
                artifact_name, artifact_name_raw
            )
            # Если расстояние Левенштейна находится в диапазоне 1-4,
            # то название из списка сохраняется в переменную,
            # обозначающую соответствующее расстояние.
            if distance == 1:
                artifact_distance_1 = artifact_name
            elif distance == 2:
                artifact_distance_2 = artifact_name
            elif distance == 3:
                artifact_distance_3 = artifact_name
            elif distance == 4:
                artifact_distance_4 = artifact_name
        # Если в списке найдены названия, расстояния Левенштейна
        # до которых в диапазоне 1-4, то возвращается набор артефактов
        # с минимальным расстоянием до его названия.
        if artifact_distance_1:
            return self.artifacts_by_name[artifact_distance_1]
        if artifact_distance_2:
            return self.artifacts_by_name[artifact_distance_2]
        if artifact_distance_3:
            return self.artifacts_by_name[artifact_distance_3]
        if artifact_distance_4:
            return self.artifacts_by_name[artifact_distance_4]

    @staticmethod
    def __read_artifact_row(artifacts: list[ArtifactSet]) -> (
            ArtifactSet | tuple[ArtifactSet, ArtifactSet] | None
    ):
        """
        Возвращает один или два набора артефактов, логически
        выделяемых из списка наборов артефактов.

        :param artifacts: Список наборов артефактов.
        :return: Набор артефактов, или кортеж из двух наборов, или
            None в противном случае.
        """
        artifact_1 = None
        artifact_2 = None
        # Цикл по всем наборам артефактов в списке.
        for artifact in artifacts:
            if not artifact_1:
                # Сохранение первого набора артефактов в списке.
                artifact_1 = artifact
            elif not artifact_2:
                # Сохранение второго набора артефактов в списке.
                artifact_2 = artifact
            else:
                effect = artifact.affix_list[0].effect
                effect_1 = artifact_1.affix_list[0].effect
                effect_2 = artifact_2.affix_list[0].effect
                # Если наборов артефактов в списке более двух и
                # эффект от двух частей очередного набора не совпадает
                # ни с эффектом первого набора, ни с эффектом второго,
                # то второй набор артефактов заменяется данным,
                # после чего цикл завершается.
                if effect != effect_1 and effect != effect_2:
                    artifact_2 = artifact
                    break
        if artifact_1:
            if artifact_2:
                return artifact_1, artifact_2
            return artifact_1

    def __get_character_parties(
            self, header3: bs4.element.PageElement
    ) -> list[list[list[Character]]]:
        """
        Возвращает списки отрядов, рекомендуемых для персонажа.

        :param header3: Заголовок, за которым должна следовать
            таблица с рекомендуемыми отрядами.
        :return: Списки отрядов.
        """
        result = list()
        # Находится следующая таблица.
        table = header3.find_next("tbody")
        # Цикл до тех пор, пока существует очередная таблица,
        # и заголовок, находящийся перед этой таблицей,
        # соответствует изначальному, так как в ином случае данная
        # таблица не содержит информацию об отрядах.
        while (table is not None and
               table.find_previous("h3").text == header3.text):
            # Считываются данные об отрядах из неё.
            parties = self.__read_parties_table(table)
            # Если результат непустой, то он сохраняется.
            if parties:
                result.append(parties)
            # Находится следующая таблица.
            table = table.find_next("tbody")
        return result

    def __read_parties_table(
            self, table: bs4.element.Tag
    ) -> list[list[Character]]:
        """
        Возвращает список отрядов, считанный из полученной таблицы.

        :param table: Таблица, содержащая рекомендуемые отряды.
        :return: Список отрядов.
        """
        result = list()
        # Цикл по всем строкам таблицы.
        for row in table.find_all("tr"):
            party = list()
            # Считывается первая ячейка строки таблицы.
            tag = row.find_next("td")
            # Цикл, тело которого выполняется 4 раза, так как
            # полноценный отряд всегда состоит из 4 персонажей и
            # таблицы с отрядами во всех статьях единообразны.
            for _ in range(4):
                # Так как в одной ячейки таблицы может быть
                # перечислено несколько взаимозаменяемых персонажей,
                # то отдельные фрагменты текста ячейки разделяются
                # с помощью точки с запятой.
                text = tag.get_text(separator=";", strip=True)
                # Если в ячейке перечислено несколько персонажей, то
                # текст ячейки обрезается, включая точку с запятой.
                semicolon_index = text.find(";")
                if semicolon_index != -1:
                    text = text[:semicolon_index]
                # Считывается персонаж, содержащийся в данной ячейке.
                character = self.__read_character(text.strip())
                # Если результат непустой, то он сохраняется.
                if character:
                    party.append(character)
                # Считывается следующая ячейка строки таблицы.
                tag = tag.find_next("td")
            # Если удалось считать всех 4 персонажей для составления
            # полноценного отряда, то такой отряд сохраняется.
            if len(party) == 4:
                result.append(party)
        return result

    def __read_character(
            self, character_name_raw: str
    ) -> Character | None:
        """
        Возвращает персонажа, найденного в полученном тексте.

        :param character_name_raw: Часть текста из ячейки таблицы.
        :return: Найденный персонаж или None в противном случае.
        """
        character_distance_1 = None
        character_distance_2 = None
        character_distance_3 = None
        character_distance_4 = None
        # Если в ячейке написана фамилия Куки персонажа Куки Синобу,
        # то сразу же возвращается персонаж Синобу.
        if "Куки" in character_name_raw:
            return self.characters_by_id["10000065"]
        # Если в ячейке написан один из семи элементов, то сразу же
        # возвращается путешественница соответствующего элемента.
        if "Пиро" in character_name_raw:
            return self.characters_by_id["10000007-pyro"]
        if "Гидро" in character_name_raw:
            return self.characters_by_id["10000007-hydro"]
        if "Анемо" in character_name_raw:
            return self.characters_by_id["10000007-anemo"]
        if "Электро" in character_name_raw:
            return self.characters_by_id["10000007-electro"]
        if "Дендро" in character_name_raw:
            return self.characters_by_id["10000007-dendro"]
        if "Гео" in character_name_raw:
            return self.characters_by_id["10000007-geo"]
        # Цикл по всем именам персонажей.
        for character in self.characters_by_id.values():
            # Считается расстояние Левенштейна между именем
            # в списке и текстом, полученным в качестве параметра.
            distance = levenshtein_distance(
                character.name, character_name_raw
            )
            # Если найдено точное совпадение имени, то сразу же
            # возвращается персонаж с соответствующим именем.
            # Если расстояние Левенштейна находится в диапазоне 1-4,
            # то имя из списка сохраняется в переменную,
            # обозначающую соответствующее расстояние.
            if distance == 0:
                return character
            elif distance == 1:
                character_distance_1 = character
            elif distance == 2:
                character_distance_2 = character
            elif distance == 3:
                character_distance_3 = character
            elif distance == 4:
                character_distance_4 = character
        # Если в списке найдены имена, расстояния Левенштейна
        # до которых в диапазоне 1-4, то возвращается персонаж
        # с минимальным расстоянием до его имени.
        if character_distance_1:
            return character_distance_1
        if character_distance_2:
            return character_distance_2
        if character_distance_3:
            return character_distance_3
        if character_distance_4:
            return character_distance_4

    @staticmethod
    def __group_character_parties(
            temp_parties: list[list[list[Character]]],
            character_name: str
    ) -> list[list[Character]]:
        """
        Возвращает список отрядов, готовый к визуализации.
        Оптимизирует число отрядов и объединяет их в единый список.

        :param temp_parties: Считанные списки рекомендуемых отрядов.
        :param character_name: Имя рассматриваемого персонажа.
        :return: Список отрядов.
        """
        # Оптимальное максимальное число отрядов для визуализации.
        parties_max_number = 12
        # Считается оптимальное максимальное число отрядов, которое
        # следует брать из каждого списка, полученного из таблицы.
        parties_per_table = int(
            parties_max_number / len(temp_parties)
        )
        # Проверяется, что из статьи о персонаже было считано всего
        # две таблицы с отрядами и хотя бы в одной из них число
        # отрядов меньше оптимального.
        if (len(temp_parties) == 2 and (
                len(temp_parties[0]) < parties_per_table or
                len(temp_parties[1]) < parties_per_table
        )):
            # Если в первом списке отрядов больше, чем во втором, то
            # оптимальным числом отрядов считается минимальное из
            # значений длины первого списка и разности максимального
            # числа отрядов и длины второго списка.
            if len(temp_parties[0]) > len(temp_parties[1]):
                parties_per_table = min(
                    len(temp_parties[0]),
                    parties_max_number - len(temp_parties[1])
                )
            # Иначе, если во втором списке отрядов больше, чем
            # в первом, то оптимальным числом отрядов считается
            # минимальное из значений длины второго списка и разности
            # максимального числа отрядов и длины первого списка.
            else:
                parties_per_table = min(
                    len(temp_parties[1]),
                    parties_max_number - len(temp_parties[0])
                )
        parties_where_main = list()
        parties_where_sub = list()
        # Цикл по всем спискам отрядов.
        for parties in temp_parties:
            # Цикл по i до минимального из значений длины списка
            # отрядов и оптимального числа отрядов из одной таблицы.
            for i in range(min(len(parties), parties_per_table)):
                # Если рассматриваемый персонаж стоит на первой
                # позиции в отряде, то считается, что в этом отряде
                # персонаж играет главную роль. Иначе считается, что
                # в этом отряде персонаж играет второстепенную роль.
                if parties[i][0].name == character_name:
                    parties_where_main.append(parties[i])
                else:
                    parties_where_sub.append(parties[i])
        # Если персонаж в отрядах чаще стоит на главной позиции, то
        # возвращаемый список отрядов будет начинаться именно с таких
        # отрядов. Иначе, возвращаемый список отрядов будет начинаться
        # с отрядов, где персонаж стоит на второстепенной позиции.
        if len(parties_where_main) > len(parties_where_sub):
            return parties_where_main + parties_where_sub
        return parties_where_sub + parties_where_main

    # Если текущим персонажем является Барбара, то рекомендуемые
    # отряды для неё получаются особенным образом.
    def __get_barbara_parties(self) -> list[list[Character]]:
        """
        Возвращает список отрядов, рекомендуемых для Барбары. В связи
        с тем, что в статье о Барбаре отсутствуют подписи с именами
        персонажей, в текущей реализации алгоритма парсинга считать
        отряды с ней не представляется возможным, поэтому
        рекомендуемые отряды для данного персонажа заданы вручную.

        :return: Список отрядов для Барбары.
        """
        return [
            [
                self.characters_by_id["10000016"],
                self.characters_by_id["10000032"],
                self.characters_by_id["10000043"],
                self.characters_by_id["10000014"]
            ],
            [
                self.characters_by_id["10000033"],
                self.characters_by_id["10000024"],
                self.characters_by_id["10000043"],
                self.characters_by_id["10000014"]
            ],
            [
                self.characters_by_id["10000036"],
                self.characters_by_id["10000030"],
                self.characters_by_id["10000031"],
                self.characters_by_id["10000014"]
            ],
            [
                self.characters_by_id["10000042"],
                self.characters_by_id["10000031"],
                self.characters_by_id["10000043"],
                self.characters_by_id["10000014"]
            ],
            [
                self.characters_by_id["10000002"],
                self.characters_by_id["10000022"],
                self.characters_by_id["10000014"],
                self.characters_by_id["10000039"]
            ],
            [
                self.characters_by_id["10000014"],
                self.characters_by_id["10000031"],
                self.characters_by_id["10000024"],
                self.characters_by_id["10000043"]
            ],
            [
                self.characters_by_id["10000070"],
                self.characters_by_id["10000014"],
                self.characters_by_id["10000073"],
                self.characters_by_id["10000077"]
            ],
            [
                self.characters_by_id["10000014"],
                self.characters_by_id["10000065"],
                self.characters_by_id["10000007-dendro"],
                self.characters_by_id["10000073"]
            ],
            [
                self.characters_by_id["10000073"],
                self.characters_by_id["10000014"],
                self.characters_by_id["10000039"],
                self.characters_by_id["10000047"]
            ],
            [
                self.characters_by_id["10000050"],
                self.characters_by_id["10000014"],
                self.characters_by_id["10000067"],
                self.characters_by_id["10000007-dendro"]
            ]
        ]
