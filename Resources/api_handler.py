import os
import sys

def make_instruction(file_name):
    text_en = f"""
# 🇺🇸 Create an API handler "{file_name}"

## Task Description
You need to implement the API handler **"{file_name}"** according to the comments provided in the layout. The layout can be viewed at the following link:
[Go to the Figma layout](https://www.figma.com/design/XMX1W4mwttgUy8L0a4kzQe/Bronyumo.ua-(special-task-mockup)?node-id=0-1&t=wnXX2PPEWtIi002e-1).

## Requirements for the API Handler
- The API should correctly handle requests (e.g., GET, POST, PUT, DELETE).
- All responses must be in JSON format with the appropriate HTTP status codes (200, 201, 400, 404, etc.).
- It is mandatory to test the API to verify that it correctly processes both valid and invalid data. In cases of invalid data, return the appropriate status codes.
- The API handler must verify user authorization, if required.

## Task Execution Requirements
- **Task Status:**  
  Assign yourself as the executor and move the task to the `In progress` status.
- **Communication, Questions, and Issues:**  
  If you encounter any questions or problems (for example, if the layout is unavailable or there is insufficient information), notify the team in the task chat and set the `Help Wanted` label under `Labels`. Do not send questions directly to the project manager to avoid confusion. If the manager does not respond for a long time or the task is urgent, send them a personal message asking them to review the task chat or discuss the issue in a meeting. You may also seek help from a more experienced colleague.  
  You can work on several tasks simultaneously if previous ones are awaiting review or require assistance.
- **Working Branch:**  
  Switch to the branch `feature/apps/{file_name}`, which was created from `dev`.
- **Task Completion:**  
  Once you have finished your work, move the task to the `In review` status. After the review:  
  - If the task requires revisions, the reviewer will return it to the `In progress` status with comments.  
  - If the task is complete, the reviewer will move it to the `Ready for Merge` status. At this stage, the task can be merged into the parent `dev` branch by either the executor or the reviewer. If the task has already been merged, it will change to the `Done` status.

## Resources
- [In the layout, look for comments that mention:](https://www.figma.com/design/XMX1W4mwttgUy8L0a4kzQe/Bronyumo.ua-(special-task-mockup)?node-id=0-1&t=wnXX2PPEWtIi002e-1)  
    ```bash
    {file_name}
    ```
- **Working Branch:**  
  `feature/apps/{file_name}` from `dev`
"""

    text_ua = f"""
# 🇺🇦 Створити API-обробник "{file_name}"

## Опис завдання
Необхідно реалізувати API-обробник **"{file_name}"** відповідно до коментарів наданих у макеті. Макет можна переглянути за посиланням:
[Перейти до макету у Figma](https://www.figma.com/design/XMX1W4mwttgUy8L0a4kzQe/Bronyumo.ua-(special-task-mockup)?node-id=0-1&t=wnXX2PPEWtIi002e-1).

## Вимоги до API-обробника
- API повинен коректно обробляти запити (наприклад GET, POST, PUT, DELETE).
- Всі відповіді мають бути у форматі JSON з відповідними HTTP статус-кодами (200, 201, 400, 404 тощо).
- Обов’язково проведення тестування API для перевірки обробки як валідних, так і невалідних даних. У випадку невідповідних даних повернути відповідні статус-коди.
- API-обробник має перевіряти авторизацію користувача, якщо це необхідно.

## Вимоги до виконання завдання
- **Статус завдання:**  
  Призначте себе виконавцем та перемістіть завдання в статус `In progress`.
- **Комунікація, питання та проблеми:**  
  Якщо у вас виникнуть питання або проблеми (наприклад, недоступність макету або недостатня інформація), повідомте про це в чаті завдання та встановіть мітку `Help Wanted` у розділі `Labels`. Не надсилайте питання безпосередньо менеджеру проєкту, щоб уникнути плутанини. Якщо менеджер довго не відповідає або завдання термінове, напишіть йому особисте повідомлення з проханням переглянути чат завдання або обговорити питання на мітингу. Також можна звернутися за допомогою до більш досвідченого колеги.  
  Ви можете працювати над кількома завданнями одночасно, якщо попередні очікують на перевірку або потребують допомоги.
- **Робоча гілка:**  
  Перейдіть на гілку `feature/apps/{file_name}`, створену від `dev`.
- **Завершення завдання:**  
  Після завершення роботи переведіть завдання в статус `In review`. Після перевірки:  
  - Якщо завдання потребує доопрацювання, рецензент поверне його в статус `In progress` із коментарями.  
  - Якщо завдання виконано, рецензент переведе його в статус `Ready for Merge`. На цьому етапі завдання може бути злите як виконавцем, так і рецензентом у батьківську гілку `dev`. Якщо завдання вже злите, воно перейде в статус `Done`.

## Ресурси
- [У макеті шукайте коментарі, в яких згадується:](https://www.figma.com/design/XMX1W4mwttgUy8L0a4kzQe/Bronyumo.ua-(special-task-mockup)?node-id=0-1&t=wnXX2PPEWtIi002e-1)  
    ```bash
    {file_name}
    ```
- **Робоча гілка:**  
  `feature/apps/{file_name}` від `dev`
    """

    text = text_ua.strip() + "\n---\n" + text_en.strip()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(script_dir, "backend")

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    output_file_path = os.path.join(output_dir, f'{file_name}.md')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f"Таска успешно сохранена в файл {output_file_path}")


if __name__ == "__main__":
    file_names = [
        "check_booking_availability",
        "create_booking",
        "sign_up",
        "sign_in",
        "set_preview_image",
        "upload_and_delete_bookings",
        "share_booking",
        "upload_and_preserve_bookings",
        "save_map",
        "add_for_booking",
        "remove_from_booking",
        "delete_booking_entry",
        "object_map_loader"
    ]

    for file_name in file_names:
        make_instruction(file_name)