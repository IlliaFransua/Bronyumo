(() => {
  const modals = {
    modal1: document.getElementById("modal1"),
    modal2: document.getElementById("modal2")
  };

  const buttons = {
    openModalBtn: document.querySelectorAll(".table__body-row-col-button img[alt='basket']"),
    option1Btn: document.getElementById("option1Btn"),
    cancelOptionBtn: document.getElementById("cancelOptionBtn"),
    confirmModal2Btn: document.getElementById("confirmModal2Btn"),
    cancelModal2Btn: document.getElementById("cancelModal2Btn")
  };

  const closeAllModals = () => {
    Object.values(modals).forEach(modal => modal.classList.add("dlg-del-entry__is-hidden"));
  };

  buttons.openModalBtn.forEach(button => {
    button.addEventListener("click", () => {
      modals.modal1.classList.remove("dlg-del-entry__is-hidden");
    });
  });

  buttons.option1Btn.addEventListener("click", () => {
    modals.modal1.classList.add("dlg-del-entry__is-hidden");
    modals.modal2.classList.remove("dlg-del-entry__is-hidden");
  });

  buttons.cancelOptionBtn.addEventListener("click", () => {
    modals.modal1.classList.add("dlg-del-entry__is-hidden");
  });

  buttons.cancelModal2Btn?.addEventListener("click", () => {
    modals.modal2.classList.add("dlg-del-entry__is-hidden");
  });

  buttons.confirmModal2Btn.addEventListener("click", () => {
    closeAllModals();
    console.log("Confirmed and closed all modals");
  });
})();
