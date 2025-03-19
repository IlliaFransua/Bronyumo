const modals = {
    modalDeleteObject: document.getElementById("modalDeleteObject"),
    modalFinalDelete: document.getElementById("modalFinalDelete")
};

const buttons = {
    openFinalDeleteObject: document.getElementById("openFinalDeleteObject"),
    cancelDeleteObject: document.getElementById("canselDeleteObject"),
    deleteFinalDelete: document.getElementById("deleteFinalDelete"),
    closeModalFinalDelete: document.getElementById("closeModalFinalDelete")
};

const openModal = (modal) => {
    modal.classList.remove("new-layout-img__is-hidden");
    document.body.classList.add("modal-open");
};

const closeModal = (modal) => {
    modal.classList.add("new-layout-img__is-hidden");
    if (!document.querySelector(".new-layout-img__backdrop:not(.new-layout-img__is-hidden)")) {
        document.body.classList.remove("modal-open");
    }
};

buttons.openFinalDeleteObject?.addEventListener("click", () => {
    openModal(modals.modalFinalDelete);
    closeModal(modals.modalDeleteObject);
});

buttons.deleteFinalDelete?.addEventListener("click", () => {
    closeModal(modals.modalFinalDelete);
    console.log("Object deleted permanently");
});

buttons.cancelDeleteObject?.addEventListener("click", () => {
    closeModal(modals.modalDeleteObject);
});

buttons.closeModalFinalDelete?.addEventListener("click", () => {
    closeModal(modals.modalFinalDelete);
});

