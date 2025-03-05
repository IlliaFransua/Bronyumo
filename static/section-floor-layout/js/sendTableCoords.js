document.addEventListener('DOMContentLoaded', () => {
    const tableLayoutManager = window.tableLayoutManager;

    function setupTableCoordinatesSave() {
        const sendUrl = '/accounts/save-table-layout/'
        const saveButton = document.querySelector('.section-floor-settings button:last-child');

        if (saveButton) {
            saveButton.addEventListener('click', (event) => {
                const tableCoordinates = tableLayoutManager.getTableCoordinates();
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
                        console.log('Extracted coordinates:', tableCoordinates);
                        console.log(xhr.responseText);
                    } else {
                        console.error('Error saving coordinates');
                    }
                };

                const payload = JSON.stringify({
                    table_coordinates: tableCoordinates
                });
                xhr.send(payload);
            });
        } else {
            console.error('Save button not found');
        }
    }
    setupTableCoordinatesSave();
});