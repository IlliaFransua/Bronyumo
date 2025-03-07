(() => {
  // Масиви для кнопок та модальних вікон
  const modals = {
    modal1: document.getElementById("modal1"),
    modal2: document.getElementById("modal2"),
    modal3: document.getElementById("modal3")
  };

  const buttons = {
    openModalBtn: document.getElementById("openModalBtn"),
    openModal2Btn: document.getElementById("openModal2Btn"),
    deleteAllBtn: document.getElementById("deleteAllBtn"),
    option1Btn: document.getElementById("option1Btn"),
    cancelOptionBtn: document.getElementById("cancelOptionBtn"),
    cancelDeleteBtn: document.getElementById("cancelDeleteBtn"),
    option1BtnModal3: document.getElementById("option1BtnModal3"),
    closeModal1: document.getElementById("closeModal1")
  };

  // Загальна функція для закриття всіх модальних вікон
  const closeAllModals = () => {
    Object.values(modals).forEach(modal => modal.classList.add("new-layout-img__is-hidden"));
  };

  // Відкриття модальних вікон
  buttons.openModalBtn.addEventListener("click", () => modals.modal1.classList.remove("new-layout-img__is-hidden"));
  buttons.openModal2Btn.addEventListener("click", () => {
    modals.modal2.classList.remove("new-layout-img__is-hidden");
    modals.modal1.classList.add("new-layout-img__is-hidden");
  });
  buttons.deleteAllBtn.addEventListener("click", () => {
    modals.modal3.classList.remove("new-layout-img__is-hidden");
    modals.modal1.classList.add("new-layout-img__is-hidden");
  });

  // Підтвердження та закриття всіх модальних вікон
  buttons.option1Btn.addEventListener("click", closeAllModals);

  // Закриття за допомогою кнопок Cancel
  buttons.cancelOptionBtn.addEventListener("click", () => {
    modals.modal2.classList.add("new-layout-img__is-hidden");
    modals.modal1.classList.remove("new-layout-img__is-hidden");
  });

  buttons.cancelDeleteBtn.addEventListener("click", () => {
    modals.modal3.classList.add("new-layout-img__is-hidden");
    modals.modal1.classList.remove("new-layout-img__is-hidden");
  });

  // Закриття через хрестик у першому модальному вікні
  buttons.closeModal1.addEventListener("click", () => modals.modal1.classList.add("new-layout-img__is-hidden"));

  // Підтвердження для третього модального вікна
  buttons.option1BtnModal3.addEventListener("click", () => {
    closeAllModals();
    console.log("Confirmed and closed all modals");
  });
})();
