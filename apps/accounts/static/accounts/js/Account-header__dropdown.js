function setupDropdownMenu() {
    const dropdownButton = document.querySelector('.button-md');

    const dropdownMenu = document.createElement('div');
    dropdownMenu.className = 'dropdown-menu';
    dropdownMenu.style.borderColor = "#E9ECEF"
    dropdownMenu.style.borderWidth = "2px"

    const menuItems = [
        // { text: 'Settings', icon: settingsIcon },
        {text: 'Logout', icon: window.logoutIcon}
    ];

    const logout = async () => {
        try {
            const response = await fetch('/accounts/api/logout/', {
                method: 'GET',
                credentials: 'same-origin',
            });

            if (response.ok) {
                const result = await response.json();
                window.location.href = '/';
            } else {
                const error = await response.json();
                alert(error.error || 'An error occurred during logout.');
            }
        } catch (error) {
            alert('An error occurred while logging out.');
        }
    };

    menuItems.forEach(item => {
        const menuItem = document.createElement('a');
        menuItem.href = '#';
        menuItem.className = 'dropdown-item';

        if (item.icon) {
            const icon = document.createElement('img');
            icon.src = item.icon;
            icon.alt = `${item.text.toLowerCase()}-icon`;
            menuItem.appendChild(icon);
        }

        const text = document.createTextNode(item.text);
        menuItem.appendChild(text);

        if (item.text === 'Logout') {
            menuItem.addEventListener('click', function (e) {
                e.preventDefault();
                logout();
            });
        }

        dropdownMenu.appendChild(menuItem);
    });

    dropdownButton.appendChild(dropdownMenu);

    let isDropdownOpen = false;

    dropdownButton.addEventListener('click', function (e) {
        e.stopPropagation();
        isDropdownOpen = !isDropdownOpen;
        dropdownMenu.style.display = isDropdownOpen ? 'block' : 'none';
        dropdownButton.style.borderBottomLeftRadius = "0px";
        dropdownButton.style.borderBottomRightRadius = "0px";
    });

    document.addEventListener('click', function () {
        if (isDropdownOpen) {
            dropdownMenu.style.display = 'none';
            isDropdownOpen = false;
        }
    });
}

setupDropdownMenu();
