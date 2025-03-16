function saveBookingObjects() {
    const bookingObjects = window.booking_objects;
    const mapHash = window.map_hash;
    const bookingAvailability = window.booking_availability;

    const requestData = {
        booking_availability: bookingAvailability,
        booking_objects: bookingObjects
    };

    fetch(`/bookings/api/save-booking-objects/${mapHash}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(requestData)
    })
        .then(response => response.json())
        .then(data => {
            console.log("Ответ от сервера:", data);
            if (data.message) {
                alert(data.message);
            } else if (data.error) {
                alert("Ошибка: " + data.error);
            }
        })
        .catch(error => {
            console.error("Ошибка при отправке данных:", error);
            alert("Произошла ошибка при отправке данных.");
        });
}

document.getElementById("save-booking-btn").onclick = saveBookingObjects;
