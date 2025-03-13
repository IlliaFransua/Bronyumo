function showModal() {
  document.getElementById('modalOverlay').style.display = 'block';
  document.getElementById('modalDialog').style.display = 'block';
  document.body.classList.add('modal-open');
}

function closeModal() {
  document.getElementById('modalOverlay').style.display = 'none';
  document.getElementById('modalDialog').style.display = 'none';
  document.body.classList.remove('modal-open');
}

setTimeout(showModal, 0);