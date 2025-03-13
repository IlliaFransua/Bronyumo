document.addEventListener('DOMContentLoaded', function() {
    // Data for dropdown options
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

    // Time settings - easier to configure
    const timeSettings = {
        startHour: 8,     // 8:00 AM
        endHour: 22,      // 10:00 PM
        interval: 15,     // 15-minute intervals
        defaultTime: '18:25' // Default selected time
    };

    // Duration settings - easier to configure
    const durationSettings = {
        minDuration: 1,   // 1 hour
        maxDuration: 8,   // 8 hours
        interval: 1,      // 1-hour intervals
        defaultDuration: 2, // Default selected duration (2 hours)
        suffix: ' hour',  // Text to append (will add 's' for plural)
    };

    // Helper function to populate a dropdown
    function populateDropdown(selectId, options) {
        const selectElement = document.getElementById(selectId);
        if (!selectElement) return;

        // Clear existing options
        selectElement.innerHTML = '';

        // Add new options
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

    // Generate time options based on settings
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

    // Generate duration options based on settings
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

    // Generate the time and duration options
    const timeOptions = generateTimeOptions(timeSettings);
    const durationOptions = generateDurationOptions(durationSettings);

    // Populate all dropdowns
    populateDropdown('month', dropdownData.months);
    populateDropdown('day', dropdownData.days);
    populateDropdown('year', dropdownData.years);
    populateDropdown('startTime', timeOptions);
    populateDropdown('duration', durationOptions);

    // Optional: Add event listeners for dropdown changes
    document.getElementById('month').addEventListener('change', function() {
        console.log('Selected month:', this.value);
        updateDaysInMonth();
    });

    document.getElementById('year').addEventListener('change', function() {
        console.log('Selected year:', this.value);
        updateDaysInMonth();
    });

    // Function to update days based on selected month and year
    function updateDaysInMonth() {
        const monthSelect = document.getElementById('month');
        const yearSelect = document.getElementById('year');
        const daySelect = document.getElementById('day');
        const selectedDay = daySelect.value; // Save current selection

        // Get month index (0-11) from month name
        const monthNames = dropdownData.months.map(m => m.value);
        const selectedMonth = monthNames.indexOf(monthSelect.value);
        const selectedYear = parseInt(yearSelect.value);

        // Get the last day of the selected month
        const lastDay = new Date(selectedYear, selectedMonth + 1, 0).getDate();

        // Create new days array with the correct number of days
        const days = Array.from({ length: lastDay }, (_, i) => {
            const day = i + 1;
            return {
                value: day,
                display: day,
                selected: day.toString() === selectedDay
            };
        });

        // Update the days dropdown
        populateDropdown('day', days);
    }
});