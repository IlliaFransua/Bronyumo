
| Flag               | Description                                            | Path Linux     | Path MacOS     | Path Windows                |
| ------------------ | ------------------------------------------------------ | -------------- | -------------- | --------------------------- |
| --system           | for the whole operating system (Linux, MacOS, Windows) | /etc/gitconfig | /etc/gitconfig | C:\ProgramData\Git\config   |
| -- global          | for the current user                                   | ~/.gitconfig   | ~/.gitconfig   | C:\Users\Username.gitconfig |
| -- local (default) | for the current repository                             | .git/config    | .git/config    | .git\config                 |

### <span style="color: red;">Setting Git configurations</span>

#### Local level
```bash
# Set user name for the current repository
git config --local user.name "Your Name"

# Set email address for the current repository
git config --local user.email "your.email@example.com"
```
#### Global level
```bash
# Set user name for all repositories of the current user
git config --global user.name "Your Name"

# Set email address for all repositories of the current user
git config --global user.email "your.email@example.com"
```
#### System level
```bash
# Set user name for all repositories on the system
sudo git config --system user.name "Your Name"

# Set email address for all repositories on the system
sudo git config --system user.email "your.email@example.com"
```
### <span style="color: red;">Removing Git configurations</span>

#### Local level
```bash
# Remove the user name setting for the current repository
git config --local --unset user.name

# Remove the email address setting for the current repository
git config --local --unset user.email
```
#### Global level
```bash
# Remove the user name setting for all repositories of the current user
git config --global --unset user.name

# Remove the email address setting for all repositories of the current user
git config --global --unset user.email
```
#### System level
```bash
# Remove the user name setting for all users on the system
sudo git config --system --unset user.name

# Remove the email address setting for all users on the system
sudo git config --system --unset user.email
```
### <span style="color: red;">Displaying Git configurations</span>

```bash
# List local configuration for the current repository
git config --list --local

# List global configuration for the current user
git config --list --global

# List system configuration for all users on the system
git config --list --system
```
### <span style="color: red;">Removing a configuration section</span>

This can be useful if you want to delete, for example, all settings of the `user`.
#### Local level
```bash
# Remove the 'user' section from the local repository configuration
git config --local --remove-section user
```
#### Global level
```bash
# Remove the 'user' section from the global configuration
git config --global --remove-section user
```
#### System level
```bash
# Remove the 'user' section from the system configuration
sudo git config --system --remove-section user
```

### <span style="color: red;">Setting the core.editor configuration</span>

This lets you choose your favorite text editor for Git commit messages and other editing tasks. The `--wait` option allows Git to wait until you finish editing the file before continuing. [More about associating text editors with Git](https://stackoverflow.com/questions/2596805/how-do-i-make-git-use-the-editor-of-my-choice-for-editing-commit-messages).
#### Visual Studio Code
```bash
# Set Visual Studio Code as the default editor for Git
git config --global core.editor "code --wait"
```
#### Neovim
```bash
# Set Neovim as the default editor for Git
git config --global core.editor "nvim"
```
#### Sublime Text
```bash
# Set Sublime Text as the default editor for Git
git config --global core.editor "subl --wait"
```
### Atom
```bash
# Set Atom as the default editor for Git
git config --global core.editor "atom --wait"
```
#### IntelliJ IDEA
```bash
# Set IntelliJ IDEA as the default editor for Git
git config --global core.editor "'/path/to/idea/bin/idea' --wait"
```
#### PyCharm
```bash
# Set PyCharm as the default editor for Git
git config --global core.editor "'/path/to/pycharm/bin/pycharm' --wait"
```
#### WebStorm
```bash
# Set WebStorm as the default editor for Git
git config --global core.editor "'/path/to/webstorm/bin/webstorm' --wait"
```
#### Notepad++
```bash
# Set Notepad++ as the default editor for Git on Windows
git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -nosession"
```
