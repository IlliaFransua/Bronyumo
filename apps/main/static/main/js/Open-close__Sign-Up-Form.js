(() => {
  const refs = {
    openModalBtns: document.querySelectorAll("[dlg-sign-up__data-modal-open]"),
    closeModalBtn: document.querySelector("[dlg-sign-up__data-modal-close]"),
    modal: document.querySelector("[dlg-sign-up__data-modal]"),
  };

  refs.openModalBtns.forEach(btn => {
      btn.addEventListener("click", (event) => {
          event.preventDefault();
          toggleModal();
      });
  });

  refs.closeModalBtn.addEventListener("click", toggleModal);

  function toggleModal() {
    refs.modal.classList.toggle("dlg-sign-up__is-hidden");
    document.body.classList.toggle("dlg-sign-up__no-scroll");
  }
})();
