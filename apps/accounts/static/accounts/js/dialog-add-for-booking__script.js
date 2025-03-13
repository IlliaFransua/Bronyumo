function showModal() {
  document.getElementById('modalOverlay').style.display = 'block';
  document.getElementById('modalDialog').style.display = 'block';
  document.body.classList.add('modal-open'); // Disable scrolling
}

function closeModal() {
  document.getElementById('modalOverlay').style.display = 'none';
  document.getElementById('modalDialog').style.display = 'none';
  document.body.classList.remove('modal-open'); // Enable scroll back
}

setTimeout(showModal, 0);