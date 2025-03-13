document.addEventListener('DOMContentLoaded', () => {
    const tableLayoutManager = window.tableLayoutManager;

    function setupTableCoordinatesSave() {
        const sendUrl = '/accounts/save-table-layout/'
        const saveButton = document.querySelector('.section-floor-settings button:last-child');

        if (saveButton) {
            saveButton.addEventListener('click', (event) => {
                const tableCoordinates = tableLayoutManager.getTableCoordinates();
                console.log('Sending data:', tableCoordinates);

                const xhr = new XMLHttpRequest();
                xhr.open('POST', sendUrl, true);

                // Set up CSRF token
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                if (csrfToken) {
                    xhr.setRequestHeader('X-CSRFToken', csrfToken.value);
                }

                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        console.log('Success! Server response:', xhr.responseText);
                    } else {
                        console.error('Error saving coordinates. Status:', xhr.status);
                        console.error('Response:', xhr.responseText);
                    }
                };

                xhr.send(JSON.stringify(tableCoordinates));
            });
        } else {
            console.error('Save button not found');
        }
    }
    setupTableCoordinatesSave();
});