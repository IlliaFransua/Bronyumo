// Function to handle dropdown menu
function setupDropdownMenu() {
  // Get the dropdown button (the one with 'Normal' text)
  const dropdownButton = document.querySelector('.button-md');


  // Create dropdown menu element
  const dropdownMenu = document.createElement('div');
  dropdownMenu.className = 'dropdown-menu';
  dropdownMenu.style.borderColor = "#E9ECEF"
    dropdownMenu.style.borderWidth = "2px"

  // Create menu items
  const menuItems = [
      { text: 'Settings', icon: settingsIcon },
      { text: 'Logout', icon: logoutIcon }
  ];

  // Add menu items to dropdown
  menuItems.forEach(item => {
    const menuItem = document.createElement('a');
    menuItem.href = '#';
    menuItem.className = 'dropdown-item';

    // Create icon if provided
    if (item.icon) {
      const icon = document.createElement('img');
      icon.src = item.icon;
      icon.alt = `${item.text.toLowerCase()}-icon`;
      menuItem.appendChild(icon);
    }

    // Add text
    const text = document.createTextNode(item.text);
    menuItem.appendChild(text);

    dropdownMenu.appendChild(menuItem);
  });

  // Important: Add the dropdown to the button container for proper positioning
  dropdownButton.appendChild(dropdownMenu);

  // Toggle dropdown visibility on button click
  let isDropdownOpen = false;

  dropdownButton.addEventListener('click', function(e) {
    e.stopPropagation();
    isDropdownOpen = !isDropdownOpen;
    dropdownMenu.style.display = isDropdownOpen ? 'block' : 'none';
    dropdownButton.style.borderBottomLeftRadius = "0px";
    dropdownButton.style.borderBottomRightRadius = "0px";
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', function() {
    if (isDropdownOpen) {
      dropdownMenu.style.display = 'none';
      isDropdownOpen = false;
    }
  });
}

// Modal functionality
function openModal() {
  document.getElementById('modalOverlay').style.display = 'block';
  document.getElementById('modalDialog').style.display = 'block';
}

function closeModal() {
  document.getElementById('modalOverlay').style.display = 'none';
  document.getElementById('modalDialog').style.display = 'none';
}

// Initialize all components when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
  setupDropdownMenu();
});