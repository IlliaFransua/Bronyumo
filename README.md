# Bronyumo

This repository contains the **Bronyumo** project, a simple platform for booking restaurant tables, featuring an intuitive interface with detailed info and an interactive map for listing table locations. Follow this guide to set up your development environment, install the needed tools, set up PostgreSQL, and run the server.

For the visual design of the project, check the [Figma model](https://www.figma.com/design/XMX1W4mwttgUy8L0a4kzQe/Bronyumo.ua?node-id=0-1&t=R0HweH7mP9Udk7mT-1).

## 1. Prerequisites

Make sure you have the following installed:

### Git

- **How to Install:** Check the [official Git website](https://git-scm.com/).

### Python

- **How to Install:** Download and install Python from the [official Python website](https://www.python.org/).  
  **Note for Windows 11 users:** Be sure to check **"Add python.exe to PATH"** during installation.

## 2. Cloning the Repository

Open your terminal and run:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/IlliaFransua/Bronyumo.git
   ```

2. **Go to the project folder:**

   ```bash
   cd Bronyumo
   ```

## 3. Creating a Virtual Environment

### 3.1 Create the Environment

- **On Linux and macOS:**

  ```bash
  python3 -m venv env
  ```

- **On Windows:**

  ```bash
  python -m venv env
  ```

### 3.2 Activate the Virtual Environment

- **On Linux and macOS:**

  ```bash
  source env/bin/activate
  ```

- **On Windows:**

  ```bash
  env\Scripts\activate
  ```

> **Important (Windows 11):**  
> If you get a security policy error when activating, run the following command in an administrator command prompt:
> 
> ```bash
> Set-ExecutionPolicy RemoteSigned
> ```
> Then close and reopen the command prompt, navigate to your project folder (right-click the folder, copy the path, and paste it after `cd`), and try activating again.

## 4. Installing PostgreSQL and Restoring the Database

**Note:** The project needs a running database.

### 4.1 Installing PostgreSQL

**Required:** PostgreSQL 14

- **Windows:**  
  Follow this [installation guide](https://www.geeksforgeeks.org/install-postgresql-on-windows/).

- **macOS/Linux:**  
  Use your package manager:
  
  - **macOS:**
  
    ```bash
    brew install postgresql@14
    ```
  
  - **Ubuntu/Debian:**
  
    ```bash
    sudo apt install postgresql-14
    ```
  
  - **Arch Linux:**
  
    ```bash
    sudo pacman -S postgresql
    ```

### 4.2 Restoring the Database

A backup file is provided in the project root. Restore the database by following these steps:

1. Open the PostgreSQL shell:

   ```bash
   psql postgres
   ```

2. Create the database:

   ```sql
   create database bronyumo;
   ```

3. Exit the shell:

   ```bash
   \q
   ```

4. **Restore the backup:**  
   Use this command:

   ```bash
   pg_restore -U <username> -W -d bronyumo -v <path_to_backup>
   ```

   **Example:**

   ```bash
   pg_restore -U illiafransua -W -d bronyumo -v "C:\Users\<Your_Username>\Documents\Telegram Desktop\bronyumo.backup"
   ```

5. Check that the tables are restored:

   ```bash
   psql postgres
   \c bronyumo
   \dt
   ```

   You should see tables like:

   ```
   Schema |            Name            | Type  |    Owner     
   --------+----------------------------+-------+--------------
    public | auth_group                 | table | illiafransua
    public | auth_group_permissions     | table | illiafransua
    public | auth_permission            | table | illiafransua
    public | auth_user                  | table | illiafransua
    public | auth_user_groups           | table | illiafransua
    public | auth_user_user_permissions | table | illiafransua
    public | django_admin_log           | table | illiafransua
    public | django_content_type        | table | illiafransua
    public | django_migrations          | table | illiafransua
    public | django_session             | table | illiafransua
   (10 rows)
   ```

> **Tip:** To create your own backup later, use:
>
> ```bash
> pg_dump -U illiafransua -W -F c -b -v -f ~/bronyumo.backup bronyumo
> ```

## 5. Configuring the Database Connection

Create a file named `.env.db.config` **outside** the project folder. This file should include your PostgreSQL connection details. **Remember:**

- The file is **not** included in the repository.
- Save it on your local device near the project folder.
- Use your own username and password from the PostgreSQL installation.

Below is an example of the contents for the `.env.db.config` file:

```env
DATABASE_NAME=bronyumo
DATABASE_USERNAME=illiafransua
DATABASE_PASSWORD=1234
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Make sure to update the values as necessary for your environment.

## 6. Installing Dependencies

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

## 7. Running the Server

Start the server by running:

```bash
python manage.py runserver
```

Then open your browser and go to:  
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 8. Shutting Down

When you are done, deactivate the virtual environment with:

```bash
deactivate
```

## Conclusion

With these steps completed, your Bronyumo development environment is now ready. You have:

- Cloned the repository
- Set up a virtual environment
- Installed PostgreSQL and restored the database
- Configured the database connection via the `.env.db.config` file
- Installed all necessary dependencies
- Started the development server

You're now ready to further develop and test the project. Remember to secure your configuration files and update any credentials as needed. Happy coding!
