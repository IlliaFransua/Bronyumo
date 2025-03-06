(() => {
  const refs = {
    openModalBtn: document.querySelector("[dlg-sign-up__data-modal-open]"),
    closeModalBtn: document.querySelector("[dlg-sign-up__data-modal-close]"),
    modal: document.querySelector("[dlg-sign-up__data-modal]"),
  };

  refs.openModalBtn.addEventListener("click", toggleModal);
  refs.closeModalBtn.addEventListener("click", toggleModal);

  function toggleModal() {
    refs.modal.classList.toggle("dlg-sign-up__is-hidden");
    document.body.classList.toggle("dlg-sign-up__no-scroll");
  }
})();