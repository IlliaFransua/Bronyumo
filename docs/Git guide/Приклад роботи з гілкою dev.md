Перед початком роботи ознайомтеся з усім файлом, оскільки він не структурований для покрокового виконання в реальному часі.
#### 1. Переключення на гілку `dev`

```bash
git checkout main     # переключаємось на main
git branch dev        # dev створюємо від main
git checkout dev      # переключаємось на dev
```

Якщо гілка `dev` вже існує, команда `git branch dev` видасть помилку:

```
fatal: A branch named 'dev' already exists.
```

Щоб переключитися на існуючу гілку dev, виконайте команду:

```bash
git checkout dev
```

#### 2. Створення нової функції

Створимо нову гілку `feature/new-feature` для роботи над новою функцією:

```bash
git branch feature/new-feature    # створюємо
git checkout feature/new-feature  # переключаємось
```

#### 3. Внесення змін

Внесіть необхідні зміни у ваш код. Це може бути редагування файлів, додавання нової функції тощо.

#### 4. Додавання змін до індексу

```bash
git add .                 # підготовка всіх змін до коміту
```

```bash
git add index.html style/style.css   # або конкретні файли
```

#### 5. Коміт змін (фіксація змін)

```bash
git commit -m "Added new script about ..."
```

```bash
git commit  # відкриває текстовий редактор для введення опису змін
```

#### 6. Повернення до гілки `dev` після закінчення роботи над функцією

```bash
git checkout dev
```

#### 7. Злиття змін з гілки `feature/new-feature` в `dev`

```bash
git merge feature/new-feature
```

#### 8. Відправка змін на GitHub після злиття гілок

```bash
git push origin dev
```

### Повна послідовність команд для роботи з гілкою `dev`

```bash
# Переключіться на гілку dev
git checkout main     # переключаємось на main
git branch dev        # dev створюємо від main
git checkout dev      # переключаємось на dev

# Створіть нову гілку для функції
git branch feature/new-feature    # створюємо
git checkout feature/new-feature  # переключаємось

# Внесіть зміни у код

# Додайте зміни до індексу
git add .

# Зафіксуйте зміни
git commit -m "Added new script about ..."

# Поверніться до гілки dev
git checkout dev

# Злийте зміни з гілки feature/new-feature в dev
git merge feature/new-feature

# Відправте зміни на GitHub
git push origin dev
```

### Додаткові поради

- Якщо під час злиття виникають конфлікти, Git повідомить вас про це. Вам потрібно буде вручну вирішити конфлікти в файлах, а потім завершити злиття, виконавши `git commit` команду. Якщо ви такого ніколи не робили, то попросить допомоги.
- Після завершення роботи над гілкою `feature/new-feature`, ви можете видалити її, якщо вона більше не потрібна:
  ```bash
  git branch -d feature/new-feature
  ```
- Якщо ваша робота ще не готова, тобто ще рано зливати `feature/new-feature` з `dev`, просто закомітьте зміни у `feature/new-feature` та відправте їх на оригінальний репозиторій замість `dev` (крок 8 `git push origin feature/new-feature`).