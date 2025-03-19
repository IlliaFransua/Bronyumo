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

  async initializeWorkingHours() {
    try {
      const map_hash = window.shareBookingLinkManager.getMapHash();
      const scriptUrl = `/bookings/api/object-working-hours-on-map/${map_hash}/`;
      const response = await fetch(scriptUrl, {
        method: 'GET',
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error('Failed to fetch the script');
      }

      const data = await response.json();

      if (!data.booking_availability) {
        throw new Error('Booking availability not found');
      }

      this.workingHours = {};

      for (const [day, hours] of Object.entries(data.booking_availability)) {
        this.workingHours[day] = hours.map(({open, close}) => ({
          open,
          close
        }));
      }

      console.log(JSON.stringify(this.workingHours, null, 2));
      await this.updateHtmlWithWorkingHours();
    } catch (error) {
      console.error('Ошибка при получении скрипта:', error);
    }
  }

  updateHtmlWithWorkingHours() {
    for (const [day, hours] of Object.entries(this.workingHours)) {
      const fromInput = document.getElementById(`dialog-add-for-booking_${day}_from`);
      const toInput = document.getElementById(`dialog-add-for-booking_${day}_to`);
      const closedCheckbox = document.getElementById(`dialog-add-for-booking_${day}_closed`);

      if (!fromInput || !toInput || !closedCheckbox) {
        console.warn(`Elements for ${day} not found.`);
        continue;
      }

      const isClosed = closedCheckbox.checked;

      if (hours.length === 0) {
        closedCheckbox.checked = true;
        fromInput.disabled = true;
        toInput.disabled = true;
      } else if (!isClosed) {
        fromInput.value = hours[0].open;
        toInput.value = hours[0].close;
        fromInput.disabled = false;
        toInput.disabled = false;
        closedCheckbox.checked = false;
      }
    }
    console.log('HTML updated with working hours');
  }

  extractWorkingHoursFromHtml() {
    const workingHours = {};

    const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];

    days.forEach(day => {
      const fromInput = document.getElementById(`dialog-add-for-booking_${day}_from`);
      const toInput = document.getElementById(`dialog-add-for-booking_${day}_to`);
      const closedCheckbox = document.getElementById(`dialog-add-for-booking_${day}_closed`);

      if (!fromInput || !toInput || !closedCheckbox) {
        console.warn(`Elements for ${day} not found.`);
        return;
      }

      const isClosed = closedCheckbox.checked;

      if (isClosed) {
        workingHours[day] = [];
      } else {
        workingHours[day] = [{
          open: fromInput.value,
          close: toInput.value
        }];
      }
    });

    console.log('Extracted working hours:', workingHours);
    this.workingHours = workingHours;
    return workingHours;
  }

  refreshWorkingHours() {
    this.extractWorkingHoursFromHtml();
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

  async saveWorkingHours(bookingObjectHash = null) {
    try {
      const mapHash = window.shareBookingLinkManager.getMapHash();
      let scriptUrl = `/bookings/api/object-working-hours-on-map/${mapHash}/`;

      if (bookingObjectHash) {
        scriptUrl += `${bookingObjectHash}/`;
      }

      const body = JSON.stringify({
        booking_availability: this.getRefreshedWorkingHours(),
      });

      console.log(body);

      const response = await fetch(scriptUrl, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: body
      });

      if (!response.ok) {
        throw new Error('Failed to save working hours');
      }

      const result = await response.json();
      console.log('Working hours updated successfully:', result);
    } catch (error) {
      console.error('Ошибка при сохранении времени:', error);
    }
  }

}

document.addEventListener("DOMContentLoaded", () => {
  window.workingHoursManager = new WorkingHoursManager();
  console.log('Изначальные часы:', workingHoursManager.getWorkingHours());

  workingHoursManager.refreshWorkingHours();
  console.log('Обновлённые часы:', workingHoursManager.getWorkingHours());
});
