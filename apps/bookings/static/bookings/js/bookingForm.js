document.addEventListener('DOMContentLoaded', function () {
  let date = new Date();
  let monthIndex = date.getMonth();
  let day = date.getDate();
  console.log('Current month:', monthIndex);
  const dropdownData = {
    months: [
      {value: 'january', display: 'January'},
      {value: 'february', display: 'February'},
      {value: 'march', display: 'March'},
      {value: 'april', display: 'April'},
      {value: 'may', display: 'May'},
      {value: 'june', display: 'June'},
      {value: 'july', display: 'July'},
      {value: 'august', display: 'August'},
      {value: 'september', display: 'September'},
      {value: 'october', display: 'October'},
      {value: 'november', display: 'November'},
      {value: 'december', display: 'December'}
    ],
    days: Array.from({length: 31}, (_, i) => ({
      value: i + 1,
      display: i + 1,
      selected: i + 1 === day + 3
    })),
    years: [
      {value: '2025', display: '2025', selected: true},
      {value: '2026', display: '2026'}
    ]
  };
  dropdownData.months[monthIndex].selected = true;
  dropdownData.days[day].selected = true;
  const timeSettings = {
    startHour: 8,
    endHour: 22,
    interval: 15,
    defaultTime: '18:25'
  };

  const durationSettings = {
    minDuration: 1,
    maxDuration: 4,
    interval: 1,
    defaultDuration: 2,
    suffix: ' hour',
  };

  function populateDropdown(selectId, options) {
    const selectElement = document.getElementById(selectId);
    if (!selectElement) return;

    selectElement.innerHTML = '';

    options.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option.value;
      optionElement.textContent = option.display;
      if (option.selected) {
        optionElement.selected = true;
      }
      selectElement.appendChild(optionElement);
    });
  }

  function generateTimeOptions(settings) {
    const times = [];
    for (let hour = settings.startHour; hour <= settings.endHour; hour++) {
      for (let minute = 0; minute < 60; minute += settings.interval) {
        const hourStr = hour.toString().padStart(2, '0');
        const minuteStr = minute.toString().padStart(2, '0');
        const timeStr = `${hourStr}:${minuteStr}`;
        times.push({
          value: timeStr,
          display: timeStr,
          selected: timeStr === settings.defaultTime
        });
      }
    }
    return times;
  }

  function generateDurationOptions(settings) {
    const durations = [];
    for (let i = settings.minDuration; i <= settings.maxDuration; i += settings.interval) {
      const suffix = i === 1 ? settings.suffix : `${settings.suffix}s`;
      durations.push({
        value: i,
        display: `${i}${suffix}`,
        selected: i === settings.defaultDuration
      });
    }
    return durations;
  }

  const timeOptions = generateTimeOptions(timeSettings);
  const durationOptions = generateDurationOptions(durationSettings);

  populateDropdown('month', dropdownData.months);
  populateDropdown('day', dropdownData.days);
  populateDropdown('year', dropdownData.years);
  populateDropdown('startTime', timeOptions);
  populateDropdown('duration', durationOptions);

  document.getElementById('month').addEventListener('change', function () {
    console.log('Selected month:', this.value);
    updateDaysInMonth();
  });

  document.getElementById('year').addEventListener('change', function () {
    console.log('Selected year:', this.value);
    updateDaysInMonth();
  });

  function updateDaysInMonth() {
    const monthSelect = document.getElementById('month');
    const yearSelect = document.getElementById('year');
    const daySelect = document.getElementById('day');
    const selectedDay = daySelect.value; // Save current selection

    const monthNames = dropdownData.months.map(m => m.value);
    const selectedMonth = monthNames.indexOf(monthSelect.value);
    const selectedYear = parseInt(yearSelect.value);

    const lastDay = new Date(selectedYear, selectedMonth + 1, 0).getDate();

    const days = Array.from({length: lastDay}, (_, i) => {
      const day = i + 1;
      return {
        value: day,
        display: day,
        selected: day.toString() === selectedDay
      };
    });

    populateDropdown('day', days);
  }
});

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('year').addEventListener('change', ScanAndParseData);
  document.getElementById('month').addEventListener('change', ScanAndParseData);
  document.getElementById('day').addEventListener('change', ScanAndParseData);
  document.getElementById('startTime').addEventListener('change', ScanAndParseData);
  document.getElementById('duration').addEventListener('change', ScanAndParseData);
});

async function ScanAndParseData() {
  if (isDateValid() && isTimeValid()) {
    let duration = document.getElementById('duration').value;
    let month = document.getElementById('month').selectedIndex;
    let day = document.getElementById('day').value;
    let year = document.getElementById('year').value;
    let startTime = document.getElementById('startTime').value;

    hours = duration.split(' ')[0];
    startTime = document.getElementById('startTime').value;
    let from = new Date(parseInt(year), month, parseInt(day), parseInt(startTime.split(':')[0]), parseInt(startTime.split(':')[1]));
    let to = new Date(parseInt(year), month, parseInt(day), parseInt(startTime.split(':')[0]) + parseInt(hours), parseInt(startTime.split(':')[1]));

    correct_format_from = formatUTCDate(from);
    correct_format_to = formatUTCDate(to);
    console.log('from:', from);
    console.log('to:', to);
    let data = {
      to: correct_format_to,
      from: correct_format_from,
    };

    console.log('ScanAndParseData', data);

    const fromTime = new Date(data.from);
    const toTime = new Date(data.to);

    window.booking_objects = await window.objectsMapLoaderAPI.loadAvailableObjects(fromTime.toISOString(), toTime.toISOString());
    console.log('Loaded booking objects:', window.booking_objects);

    return data;
  } else {
    return null;
  }
}

function formatUTCDate(date) {
  return date.getUTCFullYear() + "-" +
    String(date.getUTCMonth() + 1).padStart(2, '0') + "-" +
    String(date.getUTCDate()).padStart(2, '0') + " " +
    String(date.getUTCHours()).padStart(2, '0') + ":" +
    String(date.getUTCMinutes()).padStart(2, '0');
}

function isDateValid() {
  const year = parseInt(document.getElementById('year').value);
  const month = document.getElementById('month').selectedIndex; // індекс від 0 (січень) до 11 (грудень)
  const day = parseInt(document.getElementById('day').value);

  const selectedDate = new Date(year, month, day);
  const today = new Date();
  today.setDate(today.getDate() + 3);  // Додаємо 3 дні до вибраної дати
  today.setHours(0, 0, 0, 0); // Обнуляємо час для коректного порівняння

  if (selectedDate < today) {
    console.log('❌ Оформити бронювання можна тільки на третій день після сьогоднішньої дати!');
    alert('Оформити бронювання можна тільки на третій день після сьогоднішньої дати!');
    return false;
  } else {
    console.log('✅ Дата коректна!');
    return true;
  }
}

function isTimeValid() {

  const startTime = document.getElementById('startTime').value;
  const duration = parseInt(document.getElementById('duration').value.split(' ')[0]);
  const startHour = parseInt(startTime.split(':')[0]);
  const startMinute = parseInt(startTime.split(':')[1]);

  const endHour = startHour + duration;
  const endMinute = startMinute;

  if (endHour > 22 || (endHour === 22 && endMinute > 0)) {
    console.log('❌ Часовий проміжок може бути від 8:00 до 22:00!');
    alert('Часовий проміжок може бути від 8:00 до 22:00!');
    return false;
  } else {
    console.log('✅ Час коректний!');
    return true;
  }
}