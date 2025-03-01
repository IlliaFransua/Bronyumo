document.querySelectorAll(".faq__question").forEach((question) => {
  question.addEventListener("click", () => {
    const faqItem = question.closest(".faq__item");
    faqItem.classList.toggle("active");
  });
});
