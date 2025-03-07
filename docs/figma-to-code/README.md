# figma-to-code

## Описание

Данный проект представляет собой программу, которая позволяет правильно получать код из плагина [Figma to Code (HTML, Tailwind, Flutter, SwiftUI)](https://www.figma.com/community/plugin/842128343887142055). Этот плагин упрощает процесс преобразования дизайна в код, что позволяет разработчикам быстрее и эффективнее реализовывать проекты.

## Установка

1. Добавьте плагин [Figma to Code (HTML, Tailwind, Flutter, SwiftUI)](https://www.figma.com/community/plugin/842128343887142055) в Figma.
2. Откройте Figma и перейдите в раздел "Плагины", чтобы найти установленный плагин.

## Использование

1. Выделите фрейм, который вы хотите преобразовать в код.
2. Запустите плагин [Figma to Code (HTML, Tailwind, Flutter, SwiftUI)](https://www.figma.com/community/plugin/842128343887142055) в Figma.
3. Выберите `HTML`, `Optimize layout` и `Layer names`.
4. Скопируйте сгенерированный код и вставьте его в `input.html`.
5. Запустите `main.py` из корня проекта командой `python figma-to-code/main.py`.
6. Введите название префикса, которое автоматом проставится для всех тегов этого фрейма. К примеру: `userProfile`, `orderHistory`, `productReview`, `invoiceDetail`, `sessionToken`, `notificationAlert`, `dashboardStats`, `reportSummary`, `apiRequest`, `widgetConfig`.
7. Вы можете посмотреть получившийся результат, открыв `output.html` в браузере. После этого скопируйте весь код после `</head>` из `output.html` и вставьте его в свой основной код, где вы решаете свою задачу. Не забудьте также скопировать все содержимое `output.css`.

Для более подробного ознакомления с установкой и использованием плагина в комбинации с этим приложением, вы можете посмотреть видео-урок по [этой ссылке](https://www.google.com/).