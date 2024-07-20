import os
import subprocess
import gdown
import time

def pause(
        seconds: float
)->None:
    time.sleep(seconds)


def directory_search(
) -> str:
    game_name: str = "Goose Goose Duck"
    possible_paths: list = []
    match os.name:
        case 'nt':
            possible_paths.extend([
                os.path.expandvars(fr'%ProgramFiles%\Steam\steamapps\common\{game_name}'),
                os.path.expandvars(fr'%ProgramFiles(x86)%\Steam\steamapps\common\{game_name}'),
                os.path.expandvars(fr'%LOCALAPPDATA%\Programs\{game_name}'),
            ])
        case 'posix':
            possible_paths.extend([
                os.path.expanduser(fr'~/.steam/steam/steamapps/common/{game_name}'),
                os.path.expanduser(fr'~/.local/share/Steam/steamapps/common/{game_name}'),
            ])
        case _:
            print("Не удалось определить операционную систему.\n")
            return ""

    for path in possible_paths:
        if os.path.exists(path):
            return path

    print(f"Не удалось найти корневую папку игры автоматически для системы: {os.name}.\n")
    return ""


def download_file_from_google_drive(
        file_id: str,
        destination: str
)->None:
    url = f"https://drive.google.com/uc?id={file_id}"

    try:
        gdown.download(url, destination, quiet=False)
        print(f"Файл {destination} успешно загружен.")
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")


def validate_game_directory(path: str) -> bool:
    game_name = "Goose Goose Duck"
    if not os.path.exists(path) or not os.path.isdir(path):
        return False

    if os.name == 'nt':
        return os.path.isfile(os.path.join(path, f"{game_name}.exe"))
    elif os.name == 'posix':
        return os.path.isdir(path)

    return False


def apply_reg_file(
        reg_file_path: str
)->None:
    if not os.path.exists(reg_file_path):
        print(f"Файл {reg_file_path} не найден.")
        return
    try:
        subprocess.run(
            ['regedit', '/s', reg_file_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print('Изменения успешно внесены в реестр.')
    except subprocess.CalledProcessError as e:
        print(f'Ошибка при внесении изменений: {e}')


def script_iterations(

):
    game_name: str = "Goose Goose Duck"
    file_id: str = "1IGENwFzLm8bBEboISadYSNEdxbnjz1fH"
    destination: str = 'settings.reg'

    while True:
        path_to_the_game: str = directory_search()
        if not path_to_the_game:
            path_to_the_game = input("Введите путь к игре вручную (или введите 'exit' для выхода):\n")
            if path_to_the_game.lower() == 'exit':
                print("Выход из программы.")
                return

        if validate_game_directory(path_to_the_game):
            print(f"Корневая папка игры найдена: {path_to_the_game}")
            pause(2)
            break
        else:
            print(f"Введённый путь не является корневой папкой игры {game_name}\n")
            pause(2)

    path_to_the_settings_reg = os.path.join(path_to_the_game, destination)
    download_file_from_google_drive(file_id, path_to_the_settings_reg)
    apply_reg_file(path_to_the_settings_reg)

    exe_path = os.path.join(path_to_the_game, f"{game_name}.exe")
    if os.path.isfile(exe_path):
        print(f"Запуск игры: {game_name}\n"
              f"Директория:{exe_path}")
        pause(3)
        os.system(f'"{exe_path}"')
    else:
        print(f"Не удалось найти исполняемый файл игры по пути: {exe_path}")


def main():
    script_iterations()


if __name__ == "__main__":
    main()
