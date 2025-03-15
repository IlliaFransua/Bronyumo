// Function to handle dropdown menu
function setupDropdownMenu() {
    // Get the dropdown button (the one with 'Normal' text)
    const dropdownButton = document.querySelector('.button-md');


    // Create dropdown menu element
    const dropdownMenu = document.createElement('div');
    dropdownMenu.className = 'dropdown-menu';
    dropdownMenu.style.borderColor = "#E9ECEF"
    dropdownMenu.style.borderWidth = "2px"

    // Define menu items
    const menuItems = [
        // { text: 'Settings', icon: settingsIcon },
        {text: 'Logout', icon: logoutIcon}
    ];

    // Function to handle user logout
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

    // Populate dropdown menu with items
    menuItems.forEach(item => {
        const menuItem = document.createElement('a');
        menuItem.href = '#';
        menuItem.className = 'dropdown-item';

        // Add icon if available
        if (item.icon) {
            const icon = document.createElement('img');
            icon.src = item.icon;
            icon.alt = `${item.text.toLowerCase()}-icon`;
            menuItem.appendChild(icon);
        }

        // Add text label
        const text = document.createTextNode(item.text);
        menuItem.appendChild(text);

        // Attach logout functionality to "Logout" menu item
        if (item.text === 'Logout') {
            menuItem.addEventListener('click', function (e) {
                e.preventDefault();
                logout();
            });
        }

        dropdownMenu.appendChild(menuItem);
    });

    // Attach dropdown menu to the button container
    dropdownButton.appendChild(dropdownMenu);

    // Toggle dropdown visibility when clicking the button
    let isDropdownOpen = false;

    dropdownButton.addEventListener('click', function (e) {
        e.stopPropagation();
        isDropdownOpen = !isDropdownOpen;
        dropdownMenu.style.display = isDropdownOpen ? 'block' : 'none';
        dropdownButton.style.borderBottomLeftRadius = "0px";
        dropdownButton.style.borderBottomRightRadius = "0px";
    });

    // Close dropdown when clicking outside of it
    document.addEventListener('click', function () {
        if (isDropdownOpen) {
            dropdownMenu.style.display = 'none';
            isDropdownOpen = false;
        }
    });
}

function openModal() {
    document.getElementById('modalOverlay').style.display = 'block';
    document.getElementById('modalDialog').style.display = 'block';
}

function closeModal() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.getElementById('modalDialog').style.display = 'none';
}

// Initialize components when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    setupDropdownMenu();
});
