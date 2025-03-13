(() => {
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

  // Modal window opening function
  const openModal = (modal) => {
      modal.classList.remove("new-layout-img__is-hidden");
      document.body.classList.add("modal-open"); // Disable scrolling
  };

  // Function to close modal window
  const closeModal = (modal) => {
      modal.classList.add("new-layout-img__is-hidden");
      if (!document.querySelector(".new-layout-img__backdrop:not(.new-layout-img__is-hidden)")) {
          document.body.classList.remove("modal-open"); // Enable scrolling if all modals are closed
      }
  };

  // Function to close all modal windows
  const closeAllModals = () => {
      Object.values(modals).forEach(closeModal);
  };

  // Opening modal windows
  buttons.openModalBtn?.addEventListener("click", () => openModal(modals.modal1));
  buttons.openModal2Btn?.addEventListener("click", () => {
      openModal(modals.modal2);
      closeModal(modals.modal1);
  });
  buttons.deleteAllBtn?.addEventListener("click", () => {
      openModal(modals.modal3);
      closeModal(modals.modal1);
  });

  // Confirm and close all modal windows
  buttons.option1Btn?.addEventListener("click", closeAllModals);
  buttons.option1BtnModal3?.addEventListener("click", () => {
      closeAllModals();
      console.log("Confirmed and closed all modals");
  });

  // Close using Cancel buttons
  buttons.cancelOptionBtn?.addEventListener("click", () => {
      closeModal(modals.modal2);
      openModal(modals.modal1);
  });

  buttons.cancelDeleteBtn?.addEventListener("click", () => {
      closeModal(modals.modal3);
      openModal(modals.modal1);
  });

  // Close with cross in first modal window
  buttons.closeModal1?.addEventListener("click", () => closeModal(modals.modal1));
})();
