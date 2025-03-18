function toggleInput(day) {
  const fromInput = document.getElementById(`dialog-add-for-booking_${day}_from`);
  const toInput = document.getElementById(`dialog-add-for-booking_${day}_to`);
  const isClosed = document.getElementById(`dialog-add-for-booking_${day}_closed`).checked;

  if (isClosed) {
    fromInput.disabled = true;
    toInput.disabled = true;
    fromInput.style.opacity = "0.5";
    toInput.style.opacity = "0.5";
  } else {
    fromInput.disabled = false;
    toInput.disabled = false;
    fromInput.style.opacity = "1";
    toInput.style.opacity = "1";
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
  days.forEach(day => toggleInput(day));
  days.forEach(day => {
    const checkbox = document.getElementById(`dialog-add-for-booking_${day}_closed`);
    checkbox.addEventListener('change', () => {
      toggleInput(day);
      workingHoursManager.refreshWorkingHours();
    });
  });
});

function openWorkingHoursModal() {
  const modal = document.getElementById('modalSetWorkingHours');
  const overlay = document.getElementById('modalOverlay');
  modal.classList.remove('new-layout-img__is-hidden');
  // overlay.classList.remove('new-layout-img__is-hidden');
  workingHoursManager.refreshWorkingHours();
}

function closeWorkingHoursModal() {
  const modal = document.getElementById('modalSetWorkingHours');
  const overlay = document.getElementById('modalOverlay');
  modal.classList.add('new-layout-img__is-hidden');
  // overlay.classList.add('new-layout-img__is-hidden');
  workingHoursManager.refreshWorkingHours();
}
