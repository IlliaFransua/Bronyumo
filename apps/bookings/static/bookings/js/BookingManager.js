class BookingManager {
  constructor(imageSelector) {
    this.image = document.querySelector(imageSelector);
    if (!this.image) {
      console.error('Image not found!');
      return;
    }
    this.imageContainer = this.image.parentElement;
    this.imageContainer.style.position = 'relative';
    this.overlays = [];

    this.imageContainer.addEventListener('click', (e) => {
      if (!e.target.closest('.overlay-box')) {
        this.clearSelection();
      }
    });

    document.addEventListener('keydown', this.handleKeyDown.bind(this));
  }

  handleKeyDown(e) {
    if (e.key === 'Delete' || e.key === 'Backspace') {
      openModal(modals.modalDeleteObject);
    }
  }

  loadBookingObjectsFromWindow() {
    if (!parseMapHash() && !Array.isArray(window.booking_objects)) {
      console.error('Ошибка: данные в window.booking_objects отсутствуют или неверного формата');
      return;
    }

    console.log(`Загружаем объекты бронирования из window.booking_objects...`);

    window.booking_objects.forEach((obj, index) => {
      console.log(`Обрабатываем объект ${index + 1}:`, obj);
      this.createOverlayFromData(obj);
    });

    console.log(`Загружено ${window.booking_objects.length} объектов`);
  }

  createOverlayFromData(obj) {
    const overlay = document.createElement('div');
    overlay.classList.add('overlay-box');
    overlay.style.position = 'absolute';
    overlay.style.background = 'rgba(32, 108, 252, 0.4)';
    overlay.style.cursor = 'pointer';
    overlay.style.borderRadius = '8px';
    overlay.style.userSelect = 'none';
    overlay.style.border = '3px solid #206CFC';
    overlay.setAttribute('data-booking-hash', obj.booking_object_hash);

    const containerRect = this.imageContainer.getBoundingClientRect();

    const x_min = Math.max(0, Math.min(1, obj.x_min));
    const y_min = Math.max(0, Math.min(1, obj.y_min));
    const x_max = Math.max(x_min, Math.min(1, obj.x_max));
    const y_max = Math.max(y_min, Math.min(1, obj.y_max));

    const leftPx = x_min * containerRect.width;
    const topPx = y_min * containerRect.height;
    const widthPx = (x_max - x_min) * containerRect.width;
    const heightPx = (y_max - y_min) * containerRect.height;

    overlay.style.left = `${leftPx}px`;
    overlay.style.top = `${topPx}px`;
    overlay.style.width = `${widthPx}px`;
    overlay.style.height = `${heightPx}px`;

    overlay.addEventListener('click', (e) => {
      e.stopPropagation();
      console.log("Overlay clicked", obj);
      this.selectOverlayExisting(overlay, obj);
      console.log(obj.booking_object_hash)
      window.isSubmitting = true;
      createBookingForm(obj.booking_object_hash);
    });

    this.imageContainer.appendChild(overlay);
    this.overlays.push(overlay);
  }

  selectOverlayExisting(overlay, obj) {
    this.clearSelection();
    overlay.classList.add('selected-existing');
    this.redrawOverlayFromData(overlay, obj);
  }

  redrawOverlayFromData(overlay, obj) {
    const containerRect = this.imageContainer.getBoundingClientRect();

    console.log("Container dimensions:", containerRect);

    const x_min = Math.max(0, Math.min(1, obj.x_min));
    const y_min = Math.max(0, Math.min(1, obj.y_min));
    const x_max = Math.max(x_min, Math.min(1, obj.x_max));
    const y_max = Math.max(y_min, Math.min(1, obj.y_max));

    const leftPx = x_min * containerRect.width;
    const topPx = y_min * containerRect.height;
    const widthPx = (x_max - x_min) * containerRect.width;
    const heightPx = (y_max - y_min) * containerRect.height;

    overlay.style.left = `${leftPx}px`;
    overlay.style.top = `${topPx}px`;
    overlay.style.width = `${widthPx}px`;
    overlay.style.height = `${heightPx}px`;
  }

  clearSelection(event = null) {
    if (event && event.target.closest('.overlay-box')) return;
    this.overlays.forEach(overlay => {
      overlay.classList.remove('selected');
      overlay.innerHTML = '';
    });
  }

  getCurrentOverlays() {
    return this.overlays.map(overlay => {
      const bookingObjectHash = overlay.getAttribute('data-booking-hash');

      const style = overlay.style;
      const x_min = parseFloat(style.left) / this.imageContainer.clientWidth;
      const y_min = parseFloat(style.top) / this.imageContainer.clientHeight;
      const x_max = x_min + 100 / this.imageContainer.clientWidth;
      const y_max = y_min + 100 / this.imageContainer.clientHeight;

      return {
        booking_object_hash: bookingObjectHash,
        x_min: x_min,
        x_max: x_max,
        y_min: y_min,
        y_max: y_max
      };
    });
  }

  printOverlays() {
    this.overlays.forEach(overlay => {
      const bookingHash = overlay.getAttribute('data-booking-hash');
      console.log(`Overlay с хешем: ${bookingHash}`);
    });
  }
}
