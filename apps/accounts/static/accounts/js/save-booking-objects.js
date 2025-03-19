function saveBookingObjects() {
  const bookingObjects = window.bookingManager.getCurrentOverlays();
  const mapHash = window.shareBookingLinkManager.getMapHash();
  const bookingAvailability = window.workingHoursManager.getRefreshedWorkingHours();

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
      console.log("Response from the server:", data);
      if (data.message) {
        alert(data.message);
      } else if (data.error) {
        alert("Error: " + data.error);
      }
    })
    .catch(error => {
      console.error("Error sending data:", error);
      alert("Error occurred while sending data.");
    });
}

document.getElementById("save-booking-btn").onclick = saveBookingObjects;
