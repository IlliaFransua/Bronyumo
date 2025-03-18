class WorkingHoursManager {
  constructor() {
    this.workingHours = this.createEmptyWorkingHours();
    this.initializeWorkingHours();
  }

  createEmptyWorkingHours() {
    return {
      monday: [],
      tuesday: [],
      wednesday: [],
      thursday: [],
      friday: [],
      saturday: [],
      sunday: []
    };
  }

  initializeWorkingHours() {
    for (const day of Object.keys(this.workingHours)) {
      this.workingHours[day] = this.getDayHours(day);
    }
  }

  refreshWorkingHours() {
    this.initializeWorkingHours();
  }

  getDayHours(day) {
    const fromInput = document.getElementById(`dialog-add-for-booking_${day}_from`);
    const toInput = document.getElementById(`dialog-add-for-booking_${day}_to`);
    const closedCheckbox = document.getElementById(`dialog-add-for-booking_${day}_closed`);

    if (!fromInput || !toInput || !closedCheckbox) {
      // console.error(`Elements for ${day} not found.`);
      return [];
    }

    if (closedCheckbox.checked) {
      // console.log(`${day} is closed.`);
      return [];
    }

    const fromTime = fromInput.value;
    const toTime = toInput.value;

    if (!fromTime || !toTime) {
      // console.error(`Time inputs for ${day} are not filled. From: ${fromTime}, To: ${toTime}`);
      return [];
    }

    // console.log(`Hours for ${day}: Open at ${fromTime}, Close at ${toTime}`);
    return [{open: fromTime, close: toTime}];
  }

  getFormattedWorkingHours() {
    const formattedHours = {};
    for (const day of Object.keys(this.workingHours)) {
      formattedHours[day] = this.workingHours[day].length > 0 ? this.workingHours[day] : [];
    }
    return formattedHours;
  }

  getWorkingHours() {
    return this.workingHours;
  }

  getRefreshedWorkingHours() {
    this.refreshWorkingHours();
    return this.getWorkingHours();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.workingHoursManager = new WorkingHoursManager();
  console.log('Изначальные часы:', workingHoursManager.getWorkingHours());

  workingHoursManager.refreshWorkingHours();
  console.log('Обновлённые часы:', workingHoursManager.getWorkingHours());
});
