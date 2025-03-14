document.addEventListener("DOMContentLoaded", function () {
  const modalReservation = document.getElementById("reservationModal");
  const modalOverlay = modalReservation.querySelector(".modal__overlay");
  const modalClose = document.getElementById("modalClose");

  document.addEventListener("click", function (e) {
    if (e.target.closest(".table__body-row-col-button img[alt='arrow']")) {
      modalReservation.style.display = "flex";
      document.body.classList.add("modal-reservation__no-scroll");
    }
  });

  modalClose.addEventListener("click", function () {
    modalReservation.style.display = "none";
    document.body.classList.remove("modal-reservation__no-scroll");
  });

  modalOverlay.addEventListener("click", function () {
    modalReservation.style.display = "none";
    document.body.classList.remove("modal-reservation__no-scroll");
  });
});
