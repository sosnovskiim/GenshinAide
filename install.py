""" Файл, служащий для сборки в самостоятельное приложение. """
import PyInstaller.__main__

from constants import *

# Упаковывает программу и все необходимые компоненты
# в полноценное приложение, запускаемое из exe-файла, не требующее
# установленного интерпретатора Python на компьютере.
#
# Функции передаётся следующий список параметров:
# - main.py: файл, являющийся отправной точкой приложения;
# --name: название папки и exe-файла приложения;
# --contents-directory: название папки, в которой будут храниться все
# необходимые ресурсы приложения (изображения, исполняемые файлы
# использующихся библиотек и прочее);
# --add-data: дополнительные папки с ресурсами, которые будут
# перенесены из текущего проекта в папку с ресурсами после сборки;
# --windowed: указывает, что это приложение с графическим интерфейсом,
# не требующее запуска командной строки;
# --icon: файл, который впоследствии станет иконкой приложения.
PyInstaller.__main__.run([
    "main.py",
    f"--name={APP_NAME}",
    f"--contents-directory={DIRECTORY_CONTENTS}",
    f"--add-data={DIRECTORY_ASSETS}:{DIRECTORY_ASSETS}",
    f"--add-data={DIRECTORY_GACHA}:{DIRECTORY_GACHA}",
    f"--add-data={DIRECTORY_AVATAR}:{DIRECTORY_AVATAR}",
    f"--add-data={DIRECTORY_WEAPON}:{DIRECTORY_WEAPON}",
    f"--add-data={DIRECTORY_ARTIFACT}:{DIRECTORY_ARTIFACT}",
    "--windowed",
    f"--icon={DIRECTORY_ASSETS}/{IMAGE_APP_ICON}"
])
