""" Файл, содержащий класс для загрузки клиента приложения. """
import requests
from PIL import Image
from PyQt6.QtCore import QObject, pyqtSignal
from easyocr import Reader

from client import Client


class ClientLoader(QObject):
    """
    Служит для загрузки клиента приложения в отдельном от интерфейса
    потоке, а также для загрузки обновлений в случае их наличия.
    """
    client_loaded = pyqtSignal(Reader, Client)
    some_image_loaded = pyqtSignal(int)
    all_images_loaded = pyqtSignal()

    def load_client(self) -> None:
        """
        Инициализирует объект, использующийся для распознавания
        имён персонажей на скриншотах игры, а также клиент приложения.
        В случае наличия новых изображений персонажей и предметов,
        загружает их и сохраняет в папке с ресурсами приложения.
        """
        reader = Reader(["ru"])
        client = Client()
        # Подаётся сигнал, когда клиент загружен.
        self.client_loaded.emit(reader, client)
        if len(client.images_to_load) != 0:
            images = client.images_to_load
            image_index = 1
            images_number = len(images)
            for image_url, image_path in images.items():
                # Загружается изображение по имеющейся ссылке и
                # и сохраняется в нужную папку с изображениями.
                request = requests.get(image_url, stream=True)
                Image.open(request.raw).save(image_path)
                # Подаётся сигнал, когда каждое изображение загружено.
                self.some_image_loaded.emit(
                    int(image_index / images_number * 100)
                )
                image_index += 1
            # Подаётся сигнал, когда все изображения загружены.
            self.all_images_loaded.emit()
