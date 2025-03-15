(() => {
    const refs = {
        openModalBtns: document.querySelectorAll("[dlg-sign-in__data-modal-open]"),
        closeModalBtn: document.querySelector("[dlg-sign-in__data-modal-close]"),
        modal: document.querySelector("[dlg-sign-in__data-modal]"),
    };

    refs.openModalBtns.forEach(btn => {
        btn.addEventListener("click", (event) => {
            event.preventDefault();
            toggleModal();
        });
    });

    refs.closeModalBtn.addEventListener("click", toggleModal);

    function toggleModal() {
        refs.modal.classList.toggle("dlg-sign-in__is-hidden");
        document.body.classList.toggle("dlg-sign-in__no-scroll");
    }
})();

document.addEventListener("DOMContentLoaded", function () {
    const signInForm = document.querySelector("#sign-in-form");

    signInForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("sign-in-email").value.trim();
        const password = document.getElementById("sign-in-password").value.trim();

        if (!email || !password) {
            alert("Please fill out all fields.");
            return;
        }

        const formData = {
            email: email,
            password: password
        };

        try {
            const response = await fetch("/accounts/api/sign-in/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
                credentials: "include",
            });

            if (!response.ok) {
                const errorData = await response.json();
                const errorMessage = errorData.error || "Authentication failed. Try again later.";
                throw new Error(errorMessage);
            }

            window.location.href = "/accounts/entrepreneur-panel/";

        } catch (error) {
            console.error("Login error:", error);
            alert(error.message || "Unexpected error occurred.");
        }
    });
});

