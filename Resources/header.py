import os
import sys

def make_instruction(path, file_name):
    text = f"""
# Верстка шапки "{file_name}"

[Смотри видео-гайд по работе с тасками в Bronyumo](https://google.com)

## Описание задачи
Необходимо сверстать шапку **"{file_name}"** по предоставленному макету. Макет доступен в разделе `Ресурсы` в самом низу этого текста.

## Ожидаемый результат
Весь код этой задачи хранится в `Resources/{file_name}`. Шапка должна корректно отображаться на странице, соответствовать макету и использовать auto-layout (если таковой предусмотрен в макете).

## Требования

- **Статус задачи:**  
  Поставьте себя в качестве исполнителя и переместите задачу в статус `In progress`.

- **Коммуникация, вопросы и проблемы:**  
  Если при выполнении задачи у вас возникнут вопросы или проблемы (например, отсутствие доступа к макету, недостаток информации о содержимом и т.д.), пожалуйста, сообщите об этом в чат задания и установите метку `Help Wanted` в разделе `Labels`. Просьба не отправлять такие вопросы напрямую в личные сообщения управляющему проектом, чтобы избежать путаницы, когда таких вопросов будет много по разным заданиям. Если управляющий проекта долго не отвечает или задание срочное, вы можете отправить ему личное сообщение с просьбой просмотреть чат определённого задания или обсудить вопрос на митинге. Также можно обратиться за помощью к более опытному коллеге.
  При этом вы можете одновременно выполнять несколько заданий, если предыдущие ожидают проверки или требуют помощи.

- **Рабочая ветка:**  
  Переключитесь на ветку `feauture/{file_name}`, которая создана от `dev`.

- **Завершение задачи:**  
  После завершения работы переведите задачу в статус `In review`. После проверки:
  - Если задание требует доработки, оно будет возвращено ревьюером в статус `In progress` с комментариями.
  - Если задание выполнено, ревьюер переводит его в статус `Ready for Merge`. На этом этапе задачу может слить как исполнитель, так и ревьюер в родительскую ветку `dev`. Если задание уже слито, то оно будет находиться в статусе `Done`.

## Ресурсы
- **Макет шапки:** [ссылка на макет, ищи Layer с названием:](https://www.figma.com/design/XMX1W4mwttgUy8L0a4kzQe/Bronyumo.ua-(special-task-mockup)?node-id=0-1&t=wnXX2PPEWtIi002e-1)
    ```bash
    {file_name}
    ```
- **Рабочая ветка:** `feauture/{file_name}` от `dev`
- **Папка для ресурсов шапки:** `Resources/{file_name}`
    """

    script_dir = os.path.dirname(os.path.realpath(__file__))

    directory_path = os.path.join(script_dir, file_name)

    if os.path.isdir(directory_path):
        output_file_path = os.path.join(directory_path, f'{file_name}.md')

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text)

        print(f"Таска успешно сохранена в файл {output_file_path}")
    else:
        print(f"Каталог '{directory_path}' не найден.")


def print_directories_with_prefix(path, section):
    try:
        items = os.listdir(path)

        directories = [item for item in items if os.path.isdir(os.path.join(path, item)) and item.startswith(section)]

        if directories:
            print(f"Папки в каталоге '{path}', начинающиеся с '{section}':")
            for directory in directories:
                print(directory)
                make_instruction(path, directory)
        else:
            print(f"В указанном каталоге нет папок, начинающихся с '{section}'.")

    except FileNotFoundError:
        print("Указанный путь не найден")
    except PermissionError:
        print("Нет доступа к указанному пути")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    print_directories_with_prefix('Resources', 'guest-header')