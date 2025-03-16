function logButtonClick(buttonName) {
    console.log(`Button clicked: ${buttonName}`);
}

function shareBookingLink() {
    logButtonClick("SHARE BOOKING LINK");
}

function deleteLayout() {
    logButtonClick("DELETE THE LAYOUT");
}

function addForBooking() {
    logButtonClick("ADD FOR BOOKING");
}

function removeFromBooking() {
    logButtonClick("REMOVE FROM BOOKING");
}

function saveChanges() {
    logButtonClick("SAVE");
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.section-floor-settings .button-lg').forEach(button => {
        const buttonText = button.textContent.trim();

        if (buttonText === 'SHARE BOOKING LINK') {
            button.addEventListener('click', shareBookingLink);
        } else if (buttonText === 'DELETE THE LAYOUT') {
            button.addEventListener('click', deleteLayout);
        } else if (buttonText === 'ADD FOR BOOKING') {
            button.addEventListener('click', addForBooking);
        } else if (buttonText === 'REMOVE FROM BOOKING') {
            button.addEventListener('click', removeFromBooking);
        } else if (buttonText === 'SAVE') {
            button.addEventListener('click', saveChanges);
        }
    });
});