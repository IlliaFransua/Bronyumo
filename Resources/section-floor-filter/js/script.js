const selectorsStore = [
  {
    id: "month",
    name: "Month",
    options: [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ],
    value: "January",
  },
  {
    id: "day",
    name: "Day",
    options: Array.from({ length: 31 }, (_, i) => i + 1),
    value: "1",
  },
  {
    id: "year",
    name: "Year",
    options: Array.from({ length: 10 }, (_, i) => 2025 - i),
    value: "2025",
  },
  {
    id: "start-time",
    name: "Start Time",
    options: Array.from({ length: 24 }, (_, i) => i),
    value: "00:00",
  },
  {
    id: "duration",
    name: "Duration",
    options: Array.from({ length: 12 }, (_, i) => i + 1),
    value: "1",
  },
];

const footerList = document.getElementById("footer__list");

const clearDropdowns = () => {
  const dropdows = document.querySelectorAll(".footer__list-item-dropdown");
  dropdows.forEach((dropdown) => {
    dropdown.style.display = "none";
  });
};

const clearArrows = () => {
  const arrows = document.querySelectorAll(".footer__list-item-icon");
  arrows.forEach((arrow) => {
    arrow.style.transform = "rotate(0deg)";
  });
};

const generateSelectors = (store) => {
  footerList.innerHTML = "";
  store.forEach((selector) => {
    footerList.innerHTML += `
    <li class="footer__list-item">
        <h3 class="footer__list-item-title">${selector.name}</h3>
        <button class="footer__list-item-container" data-id="${
          selector.id
        }" id="button-${selector.id}">
            <p class="footer__list-item-value" id="value-${selector.id}">${
      selector.value
    }</p>
            <img
              class="footer__list-item-icon"
              src="../../../static/section-floor-filter/arrow.svg"
              alt="arrow"
              id="arrow-${selector.id}"
            />
        </button>
         <div class="footer__list-item-dropdown" id="dropdown-${selector.id}">
            <ul class="footer__list-item-dropdown-list" id="dropdown-list-${
              selector.id
            }">
                ${selector.options
                  .map(
                    (option) =>
                      `<li class="footer__list-item-dropdown-list-item" data-value="${option}">${option}</li>`
                  )
                  .join("")}
            </ul>
        </div>
    </li>
    `;
  });

  const allButtons = document.querySelectorAll(".footer__list-item-container");

  allButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const id = button.getAttribute("data-id");
      const dropdown = document.querySelector(`#dropdown-${id}`);
      if (dropdown.getAttribute("status") === "active") {
        dropdown.setAttribute("status", "inactive");
        dropdown.style.display = "none";
      } else {
        clearDropdowns();
        clearArrows();
        dropdown.setAttribute("status", "active");
        const arrow = document.querySelector(`#arrow-${id}`);
        if (dropdown.style.display === "block") {
          dropdown.style.display = "none";
          arrow.style.transform = "rotate(0deg)";
        } else {
          dropdown.style.display = "block";
          arrow.style.transform = "rotate(180deg)";
        }
      }
      const options = document.querySelectorAll(
        ".footer__list-item-dropdown-list-item"
      );
      options.forEach((option) => {
        option.addEventListener("click", () => {
          const value = option.getAttribute("data-value");

          const newStore = selectorsStore.map((selector) => {
            if (selector.id === id) {
              selector.value = value;
            }
            return selector;
          });

          generateSelectors(newStore);
        });
      });
    });
  });
};

generateSelectors(selectorsStore);
