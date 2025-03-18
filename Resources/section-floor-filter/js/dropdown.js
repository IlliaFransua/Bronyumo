document.addEventListener('DOMContentLoaded', function() {
    const dropdownData = {
        months: [
            { value: 'january', display: 'January' },
            { value: 'february', display: 'February', selected: true },
            { value: 'march', display: 'March' },
            { value: 'april', display: 'April' },
            { value: 'may', display: 'May' },
            { value: 'june', display: 'June' },
            { value: 'july', display: 'July' },
            { value: 'august', display: 'August' },
            { value: 'september', display: 'September' },
            { value: 'october', display: 'October' },
            { value: 'november', display: 'November' },
            { value: 'december', display: 'December' }
        ],
        days: Array.from({ length: 31 }, (_, i) => ({
            value: i + 1,
            display: i + 1,
            selected: i + 1 === 22
        })),
        years: [
            { value: '2025', display: '2025', selected: true },
            { value: '2026', display: '2026' }
        ]
    };

    const timeSettings = {
        startHour: 8,
        endHour: 22,
        interval: 15,
        defaultTime: '18:25'
    };

    const durationSettings = {
        minDuration: 1,
        maxDuration: 8,
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

    document.getElementById('month').addEventListener('change', function() {
        console.log('Selected month:', this.value);
        updateDaysInMonth();
    });

    document.getElementById('year').addEventListener('change', function() {
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

        const days = Array.from({ length: lastDay }, (_, i) => {
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