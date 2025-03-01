function showModal() {
  document.getElementById('modalOverlay').style.display = 'block';
  document.getElementById('modalDialog').style.display = 'block';
}

function closeModal() {
  document.getElementById('modalOverlay').style.display = 'none';
  document.getElementById('modalDialog').style.display = 'none';
}

setTimeout(showModal, 2000);

//Натискання кнопки в guest-header1 -> переходимо на Entreprenuer Page
document.addEventListener("DOMContentLoaded", function() {
  const button = document.querySelector(".entrepreneurs-button");
  button.addEventListener("click", function() {
      window.location.href = "#"; // Замініть # на шлях до потрібного файлу
  });
});
