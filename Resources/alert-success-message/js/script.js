function openModal(message) {
  document.getElementById('modalOverlay').style.display = 'block';
  document.getElementById('modalDialog').style.display = 'block';
  document.getElementById('errorMessage').textContent = message;
}

setTimeout(openModal, 3000);

function closeModal() {
  document.getElementById('modalOverlay').style.display = 'none';
  document.getElementById('modalDialog').style.display = 'none';
}