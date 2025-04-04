import os
import sys

def make_instruction(path, file_name):
    text_en = f"""
# 🇺🇸 Converting the markup of the dialog window "{file_name}" into code

[Watch the video guide on working with tasks in Bronyumo](https://google.com)

## Task Description
You need to implement the dialog window **"{file_name}"** according to the provided design. The design is available in the `Resources` section at the bottom of this text.

## Expected Result
All the code for this task is stored in `Resources/{file_name}`. The dialog window should display correctly on the page, match the design, and use auto-layout (if specified in the design).

## Requirements

- **Task Status:**  
  Assign yourself as the executor and move the task to the `In progress` status.

- **Communication, Questions, and Issues:**  
  If you encounter any questions or issues while executing the task (for example, lack of access to the design, insufficient information about the content, etc.), please report it in the task chat and set the `Help Wanted` label in the `Labels` section. Please do not send such questions directly as personal messages to the project manager to avoid confusion when there are many such inquiries across different tasks. If the project manager does not respond for a long time or the task is urgent, you may send him a personal message asking him to review the chat for that specific task or to discuss the issue in a meeting. You may also ask a more experienced colleague for assistance.  
  At the same time, you can work on several tasks concurrently if previous ones are awaiting review or require help.

- **Working Branch:**  
  Switch to the branch `feauture/{file_name}`, which is created from `dev`.

- **Task Completion:**  
  After finishing your work, move the task to the `In review` status. After review:
  - If the task requires further revisions, it will be returned by the reviewer to the `In progress` status with comments.
  - If the task is completed, the reviewer will move it to the `Ready for Merge` status. At this stage, the task can be merged by either the executor or the reviewer into the parent branch `dev`. If the task has already been merged, it will be in the `Done` status.

## Resources
- **Dialog Window Design:** [link to the design, look for the Layer named:](https://www.figma.com/design/XMX1W4mwttgUy8L0a4kzQe/Bronyumo.ua-(special-task-mockup)?node-id=0-1&t=wnXX2PPEWtIi002e-1)
    ```bash
    {file_name}
    ```
- **Working Branch:** `feauture/{file_name}` from `dev`
- **Folder for Dialog Window Resources:** `Resources/{file_name}`
    """

    text_ua = f"""
# 🇺🇦 Верстка діалогового вікна "{file_name}"

[Дивись відео-гайд щодо роботи з тасками в Bronyumo](https://google.com)

## Опис завдання
Необхідно зверстати діалогове вікно **"{file_name}"** за наданим макетом. Макет доступний у розділі `Ресурси` внизу цього тексту.

## Очікуваний результат
Весь код цього завдання зберігається в `Resources/{file_name}`. Діалогове вікно повинно коректно відображатися на сторінці, відповідати макету та використовувати auto-layout (якщо це передбачено макетом).

## Вимоги

- **Статус завдання:**  
  Призначте себе виконавцем і перемістіть завдання в статус `In progress`.

- **Комунікація, питання та проблеми:**  
  Якщо під час виконання завдання у вас виникнуть питання або проблеми (наприклад, відсутність доступу до макета, нестача інформації про зміст тощо), будь ласка, повідомте про це в чаті завдання та встановіть мітку `Help Wanted` у розділі `Labels`. Прохання не надсилати такі питання напряму в особисті повідомлення менеджеру проєкту, щоб уникнути плутанини, коли таких питань буде багато по різних завданнях. Якщо менеджер проєкту довго не відповідає або завдання термінове, ви можете написати йому особисте повідомлення з проханням переглянути чат конкретного завдання або обговорити питання на мітингу. Також можна звернутися по допомогу до більш досвідченого колеги.
  При цьому ви можете одночасно виконувати кілька завдань, якщо попередні очікують перевірки або потребують допомоги.

- **Робоча гілка:**  
  Переключіться на гілку `feauture/{file_name}`, яка створена від `dev`.

- **Завершення завдання:**  
  Після завершення роботи переведіть завдання в статус `In review`. Після перевірки:
  - Якщо завдання вимагає доопрацювання, воно буде повернуто рев’юером у статус `In progress` з коментарями.
  - Якщо завдання виконане, рев’юер переводить його в статус `Ready for Merge`. На цьому етапі завдання може бути об’єднане як виконавцем, так і рев’юером у батьківську гілку `dev`. Якщо завдання вже об’єднано, то воно буде знаходитися у статусі `Done`.

## Ресурси
- **Макет діалогового вікна:** [посилання на макет, шукай Layer з назвою:](https://www.figma.com/design/XMX1W4mwttgUy8L0a4kzQe/Bronyumo.ua-(special-task-mockup)?node-id=0-1&t=wnXX2PPEWtIi002e-1)
    ```bash
    {file_name}
    ```
- **Робоча гілка:** `feauture/{file_name}` від `dev`
- **Папка для ресурсів діалогового вікна:** `Resources/{file_name}`
    """

    text = text_en.strip() + "\n---\n" + text_ua.strip()

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
    print_directories_with_prefix('Resources', 'dialog')