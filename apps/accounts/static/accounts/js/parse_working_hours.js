function getWorkingHours() {
    const workingHours = {
        monday: getDayHours('Monday'),
        tuesday: getDayHours('Tuesday'),
        wednesday: getDayHours('Wednesday'),
        thursday: getDayHours('Thursday'),
        friday: getDayHours('Friday'),
        saturday: getDayHours('Saturday'),
        sunday: getDayHours('Sunday')
    };

    return workingHours;
}

function getDayHours(day) {
    const fromInput = document.getElementById(`dialog-add-for-booking_${day}_from`);
    const toInput = document.getElementById(`dialog-add-for-booking_${day}_to`);
    const closedCheckbox = document.getElementById(`dialog-add-for-booking_${day}_closed`);

    if (closedCheckbox.checked) {
        return [];
    }

    const fromTime = fromInput.value;
    const toTime = toInput.value;

    return [{open: fromTime, close: toTime}];
}
