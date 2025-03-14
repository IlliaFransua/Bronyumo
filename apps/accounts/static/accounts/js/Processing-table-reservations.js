const store = [
  { fullName: 'Alyvia Kelley', email: 'a.kelley@gmail.com', date: '2025-02-22', startTime: '18:00', endTime: '19:10' },
  { fullName: 'Jackson Wright', email: 'j.wright@gmail.com', date: '2025-03-10', startTime: '09:30', endTime: '10:30' },
  { fullName: 'Emma Johnson', email: 'e.johnson@gmail.com', date: '2025-03-14', startTime: '13:15', endTime: '14:00' },
  { fullName: 'Noah Brown', email: 'n.brown@gmail.com', date: '2025-02-25', startTime: '15:00', endTime: '16:10' },
  { fullName: 'Sophia Smith', email: 's.smith@gmail.com', date: '2025-03-01', startTime: '11:00', endTime: '12:00' },
  { fullName: 'James Williams', email: 'j.williams@gmail.com', date: '2025-03-05', startTime: '10:00', endTime: '11:15' },
  { fullName: 'Olivia Martinez', email: 'o.martinez@gmail.com', date: '2025-02-28', startTime: '16:30', endTime: '17:45' },
  { fullName: 'Liam Davis', email: 'l.davis@gmail.com', date: '2025-03-08', startTime: '14:00', endTime: '15:10' },
  { fullName: 'Mia Moore', email: 'm.moore@gmail.com', date: '2025-03-12', startTime: '17:30', endTime: '18:30' },
  { fullName: 'Ethan Taylor', email: 'e.taylor@gmail.com', date: '2025-03-04', startTime: '08:00', endTime: '09:00' },
];

const bodyHtml = document.querySelector('#tableBody');

const renderTableBody = (store) => {
  bodyHtml.innerHTML = '';
  store.forEach((item, index) => {
    const rowHtml = `
      <tr class="table__body-row">
        <td class="table__body-row-col">${index + 1}</td>
        <td class="table__body-row-col">${item.fullName}</td>
        <td class="table__body-row-col">${item.email}</td>
        <td class="table__body-row-col">${item.date}</td>
        <td class="table__body-row-col">${item.startTime}</td>
        <td class="table__body-row-col">${item.endTime}</td>
        <td class="table__body-row-col">
          <button class="table__body-row-col-button">
            <img src="/apps/accounts/static/accounts/images/arrow.svg" alt="arrow">
          </button>
          <button class="table__body-row-col-button">
            <img src="/apps/accounts/static/accounts/images/basket.svg" alt="basket">
          </button>
        </td>
      </tr>
    `;
    bodyHtml.innerHTML += rowHtml;
  });
}

renderTableBody(store);
