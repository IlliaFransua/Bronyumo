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

document.addEventListener("DOMContentLoaded", function () {
    const signUpForm = document.querySelector("#sign-up-form");
    signUpForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const companyName = document.getElementById("sign-up-company").value.trim();
        const address = document.getElementById("sign-up-address").value.trim();
        const email = document.getElementById("sign-up-email").value.trim();
        const password = document.getElementById("sign-up-password").value.trim();

        if (!companyName || !address || !email || !password) {
            alert("Please fill out all fields.");
            return;
        }

        const formData = {
            companyName: companyName,
            address: address,
            email: email,
            password: password
        };

        try {
            const response = await fetch("/accounts/api/sign-up/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
                credentials: "include",
            });

            if (!response.ok) {
                const errorData = await response.json();
                const errorMessage = errorData.error || "Registration failed. Try again later.";
                throw new Error(errorMessage);
            }

            window.location.href = "/accounts/entrepreneur-panel/";

        } catch (error) {
            console.error("Registration error:", error);
            alert(error.message || "Unexpected error occurred.");
        }
    });
});

