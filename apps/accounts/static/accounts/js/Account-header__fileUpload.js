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

        sendToBackend(file);
    });


    function sendToBackend(file) {
        const uploadFileUrl = '/utils/api/map-upload/';
        const formData = new FormData();
        formData.append('floorPlanImage', file);

        const canvasDiv = document.querySelector('.section-upload-floor-plan__canvas');
        let uploadStatus = document.getElementById('upload-status');
        if (!uploadStatus) {
            uploadStatus = document.createElement('p');
            uploadStatus.id = 'upload-status';
            canvasDiv.appendChild(uploadStatus);
        }

        fetch(uploadFileUrl, {
            method: 'POST',
            body: formData,
            credentials: 'include',
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(errorData.error || 'Network response was not ok');
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                uploadStatus.textContent = 'Successfully sent to server!';
                uploadStatus.style.color = 'green';
                if (data.redirect_url) {
                    console.log('Redirect URL:', data.redirect_url);
                    window.location.href = data.redirect_url;
                } else {
                    location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                uploadStatus.textContent = 'Failed to send to server. ' + error.message;
                uploadStatus.style.color = 'red';
                alert('Error: ' + error.message);
            });
    }
});