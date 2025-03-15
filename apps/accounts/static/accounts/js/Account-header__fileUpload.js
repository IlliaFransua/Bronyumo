document.addEventListener('DOMContentLoaded', function () {
    const uploadButton = document.querySelector('.button-lg');

    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.png,.jpg,.jpeg';
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);

    uploadButton.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (!file) {
            return;
        }

        const fileType = file.type.toLowerCase();
        if (fileType !== 'image/png' && fileType !== 'image/jpeg') {
            alert('Please upload only PNG or JPG files.');
            return;
        }

        if (file.size > 52428800) {
            alert('File size exceeds 50MB limit.');
            return;
        }

        console.log('File uploaded:', {
            name: file.name,
            type: file.type,
            size: `${(file.size / 1024 / 1024).toFixed(2)} MB`
        });

        // Send the file to the backend
        sendToBackend(file);
    });


    function sendToBackend(file) {
        //Paste the url to Django view
        const uploadFileUrl = '/utils/api/map-upload/';
        const formData = new FormData();
        formData.append('floorPlanImage', file);

        const canvasDiv = document.querySelector('.section-upload-floor-plan__canvas');
        const uploadStatus = document.createElement('p');
        uploadStatus.id = 'upload-status';

        const existingStatus = document.getElementById('upload-status');
        if (existingStatus) {
            canvasDiv.removeChild(existingStatus);
        }

        canvasDiv.appendChild(uploadStatus);

        // Send the file to the backend
        fetch(uploadFileUrl, {
            method: 'POST',
            body: formData,
            credentials: 'include',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                uploadStatus.textContent = 'Successfully sent to server!';
                uploadStatus.style.color = 'green';
            })
            .catch(error => {
                console.error('Error:', error);
                uploadStatus.textContent = 'Failed to send to server. ' + error.message;
                uploadStatus.style.color = 'red';
            });
    }
});