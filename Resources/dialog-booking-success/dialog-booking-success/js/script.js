function showModal() {
  document.getElementById('modalOverlay').style.display = 'block';
  document.getElementById('modalDialog').style.display = 'block';
}

function closeModal() {
  document.getElementById('modalOverlay').style.display = 'none';
  document.getElementById('modalDialog').style.display = 'none';
}

setTimeout(showModal, 0);