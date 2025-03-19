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

  handleKeyDown(e) {
    if (e.key === 'Delete' || e.key === 'Backspace') {
      openModal(modals.modalDeleteObject);
    }
  }

  deleteSelectedOverlay() {
    const selectedOverlay = this.imageContainer.querySelector('.overlay-box.selected');

    if (selectedOverlay) {
      const bookingHash = selectedOverlay.getAttribute('data-booking-hash');

      fetch(`/bookings/api/delete-booking-object/${window.shareBookingLinkManager.getMapHash()}/${bookingHash}/`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.message) {
            window.booking_objects = window.booking_objects.filter(obj => obj.booking_object_hash !== bookingHash);
            console.log('Удален объект с хешом:', bookingHash);

            selectedOverlay.remove();
            this.overlays = this.overlays.filter(item => item !== selectedOverlay);

            this.clearSelection();

            closeModal(modals.modalFinalDelete);
          } else {
            alert('Ошибка: объект не был удален.');
          }
        })
        .catch(error => {
          console.error('Ошибка при отправке запроса:', error);
          alert('Ошибка: не удалось удалить объект.');
        });
    } else {
      console.log('No selected overlay found');
    }
  }

  printOverlays() {
    this.overlays.forEach(overlay => {
      const bookingHash = overlay.getAttribute('data-booking-hash');
      console.log(`Overlay с хешем: ${bookingHash}`);
    });
  }

  loadBookingObjectsFromWindow() {
    if (!window.shareBookingLinkManager.getMapHash() && !Array.isArray(window.booking_objects)) {
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
    overlay.style.cursor = 'grab';
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
      this.selectOverlayExisting(overlay);
    });

    this.imageContainer.appendChild(overlay);
    this.overlays.push(overlay);
  }


  createOverlay() {
    const overlay = document.createElement('div');
    overlay.classList.add('overlay-box');
    overlay.style.position = 'absolute';
    overlay.style.width = '100px';
    overlay.style.height = '100px';
    overlay.style.background = 'rgba(32, 108, 252, 0.4)';
    overlay.style.cursor = 'grab';
    overlay.style.borderRadius = '8px';
    overlay.style.userSelect = 'none';
    overlay.style.border = '3px solid #206CFC';

    const containerRect = this.imageContainer.getBoundingClientRect();
    const x_min = ((containerRect.width / 2) - 50) / containerRect.width;
    const y_min = ((containerRect.height / 2) - 50) / containerRect.height;
    const x_max = ((containerRect.width / 2) + 50) / containerRect.width;
    const y_max = ((containerRect.height / 2) + 50) / containerRect.height;

    overlay.style.left = `${(containerRect.width / 2) - 50}px`;
    overlay.style.top = `${(containerRect.height / 2) - 50}px`;

    overlay.addEventListener('click', (e) => {
      e.stopPropagation();
      this.selectOverlay(overlay);
    });

    const booking_availability = workingHoursManager.getWorkingHours();

    fetch(`/bookings/api/add-for-booking/${window.shareBookingLinkManager.getMapHash()}/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({x_min, x_max, y_min, y_max, booking_availability})
    })
      .then(response => response.json())
      .then(data => {
        if (data.booking_object_hash) {
          overlay.setAttribute('data-booking-hash', data.booking_object_hash);

          if (!window.booking_objects) {
            window.booking_objects = [];
          }

          const newObject = {
            booking_object_hash: data.booking_object_hash,
            x_min,
            x_max,
            y_min,
            y_max
          };

          window.booking_objects.push(newObject);

          this.imageContainer.appendChild(overlay);
          this.overlays.push(overlay);
          this.selectOverlay(overlay);

          console.log('Добавлен новый объект:', newObject);
          this.printOverlays()
        } else {
          console.error('Ошибка: в ответе нет booking_object_hash', data);
        }
      })
      .catch(error => {
        console.error('Ошибка при отправке запроса:', error);
      });
  }

  selectOverlay(overlay) {
    this.clearSelection();
    overlay.classList.add('selected');
    this.addResizeHandles(overlay);
    this.addResizeBars(overlay);
    this.setupDrag(overlay);
  }

  selectOverlayExisting(overlay) {
    this.clearSelection();
    overlay.classList.add('selected-existing');
    this.addResizeHandlesExisting(overlay);
    this.addResizeBarsExisting(overlay);
    this.setupDragExisting(overlay);
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

  addResizeHandlesExisting(overlay) {
    const handles = ['nw', 'ne', 'sw', 'se'];
    handles.forEach(handle => {
      const resizeHandle = document.createElement('div');
      resizeHandle.classList.add('resize-handle-existing', handle);
      resizeHandle.style.position = 'absolute';
      resizeHandle.style.width = '16px';
      resizeHandle.style.height = '16px';
      resizeHandle.style.background = 'blue';
      resizeHandle.style.borderRadius = '50%';
      resizeHandle.style.cursor = `${handle}-resize`;

      if (handle.includes('n')) resizeHandle.style.top = '-18px';
      if (handle.includes('s')) resizeHandle.style.bottom = '-18px';
      if (handle.includes('w')) resizeHandle.style.left = '-18px';
      if (handle.includes('e')) resizeHandle.style.right = '-18px';

      overlay.appendChild(resizeHandle);
      this.setupResizeExisting(resizeHandle, overlay, handle);
    });
  }

  addResizeBarsExisting(overlay) {
    const bars = ['n', 's', 'w', 'e'];

    bars.forEach(bar => {
      const resizeBar = document.createElement('div');
      resizeBar.classList.add('resize-bar-existing', bar);
      resizeBar.style.position = 'absolute';
      resizeBar.style.background = 'blue';
      resizeBar.style.opacity = '0.0';
      resizeBar.style.cursor = `${bar}-resize`;

      if (bar === 'n' || bar === 's') {
        resizeBar.style.height = '18px';
        resizeBar.style.width = '80%';
        resizeBar.style.left = '10%';
      } else {
        resizeBar.style.width = '18px';
        resizeBar.style.height = '80%';
        resizeBar.style.top = '10%';
      }

      if (bar === 'n') resizeBar.style.top = '-10px';
      if (bar === 's') resizeBar.style.bottom = '-10px';
      if (bar === 'w') resizeBar.style.left = '-10px';
      if (bar === 'e') resizeBar.style.right = '-10px';

      overlay.appendChild(resizeBar);
      this.setupResizeExisting(resizeBar, overlay, bar);
    });

  }

  setupResizeExisting(handle, overlay, direction) {
    handle.addEventListener('mousedown', (e) => {
      e.stopPropagation();
      let startX = e.clientX;
      let startY = e.clientY;
      let startWidth = overlay.offsetWidth;
      let startHeight = overlay.offsetHeight;
      let startLeft = overlay.offsetLeft;
      let startTop = overlay.offsetTop;

      const onMouseMove = (e) => {
        let newWidth = startWidth;
        let newHeight = startHeight;
        let newLeft = startLeft;
        let newTop = startTop;

        if (direction.includes('e')) newWidth = Math.max(20, startWidth + (e.clientX - startX));
        if (direction.includes('s')) newHeight = Math.max(20, startHeight + (e.clientY - startY));
        if (direction.includes('w')) {
          newWidth = Math.max(20, startWidth - (e.clientX - startX));
          newLeft = startLeft + (startWidth - newWidth);
        }
        if (direction.includes('n')) {
          newHeight = Math.max(20, startHeight - (e.clientY - startY));
          newTop = startTop + (startHeight - newHeight);
        }

        overlay.style.width = `${newWidth}px`;
        overlay.style.height = `${newHeight}px`;
        overlay.style.left = `${newLeft}px`;
        overlay.style.top = `${newTop}px`;
      };

      const onMouseUp = () => {
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
      };

      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    });
  }

  setupDragExisting(overlay) {
    let isDragging = false;
    let offsetX = 0, offsetY = 0;

    overlay.addEventListener('mousedown', (e) => {
      if (e.target.classList.contains('resize-handle-existing') || e.target.classList.contains('resize-bar-existing')) return;
      if (!overlay.classList.contains('selected-existing')) return;

      isDragging = true;
      const rect = overlay.getBoundingClientRect();
      offsetX = e.clientX - rect.left;
      offsetY = e.clientY - rect.top;
      overlay.style.cursor = 'grabbing';

    });

    const onMouseMove = (e) => {
      if (!isDragging) return;

      const containerRect = this.imageContainer.getBoundingClientRect();
      let newX = e.clientX - containerRect.left - offsetX;
      let newY = e.clientY - containerRect.top - offsetY;

      newX = Math.max(0, Math.min(newX, containerRect.width - overlay.clientWidth));
      newY = Math.max(0, Math.min(newY, containerRect.height - overlay.clientHeight));

      overlay.style.left = `${newX}px`;
      overlay.style.top = `${newY}px`;
    };

    const onMouseUp = () => {
      isDragging = false;
      overlay.style.cursor = 'grab';
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    };

    overlay.addEventListener('mousedown', (e) => {
      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    });
  }

  clearSelection(event = null) {
    if (event && event.target.closest('.overlay-box')) return;
    this.overlays.forEach(overlay => {
      overlay.classList.remove('selected');
      overlay.innerHTML = '';
    });
  }

  addResizeHandles(overlay) {
    const handles = ['nw', 'ne', 'sw', 'se'];
    handles.forEach(handle => {
      const resizeHandle = document.createElement('div');
      resizeHandle.classList.add('resize-handle', handle);
      resizeHandle.style.position = 'absolute';
      resizeHandle.style.width = '16px';
      resizeHandle.style.height = '16px';
      resizeHandle.style.background = 'blue';
      resizeHandle.style.borderRadius = '50%';
      resizeHandle.style.cursor = `${handle}-resize`;

      if (handle.includes('n')) resizeHandle.style.top = '-18px';
      if (handle.includes('s')) resizeHandle.style.bottom = '-18px';
      if (handle.includes('w')) resizeHandle.style.left = '-18px';
      if (handle.includes('e')) resizeHandle.style.right = '-18px';

      overlay.appendChild(resizeHandle);
      this.setupResize(resizeHandle, overlay, handle);
    });
  }

  addResizeBars(overlay) {
    const bars = ['n', 's', 'w', 'e'];
    bars.forEach(bar => {
      const resizeBar = document.createElement('div');
      resizeBar.classList.add('resize-bar', bar);
      resizeBar.style.position = 'absolute';
      resizeBar.style.background = 'blue';
      resizeBar.style.opacity = '0.0';
      resizeBar.style.cursor = `${bar}-resize`;

      if (bar === 'n' || bar === 's') {
        resizeBar.style.height = '18px';
        resizeBar.style.width = '80%';
        resizeBar.style.left = '10%';
      } else {
        resizeBar.style.width = '18px';
        resizeBar.style.height = '80%';
        resizeBar.style.top = '10%';
      }

      if (bar === 'n') resizeBar.style.top = '-10px';
      if (bar === 's') resizeBar.style.bottom = '-10px';
      if (bar === 'w') resizeBar.style.left = '-10px';
      if (bar === 'e') resizeBar.style.right = '-10px';

      overlay.appendChild(resizeBar);
      this.setupResize(resizeBar, overlay, bar);
    });
  }

  setupResize(handle, overlay, direction) {
    handle.addEventListener('mousedown', (e) => {
      e.stopPropagation();
      let startX = e.clientX;
      let startY = e.clientY;
      let startWidth = overlay.offsetWidth;
      let startHeight = overlay.offsetHeight;
      let startLeft = overlay.offsetLeft;
      let startTop = overlay.offsetTop;

      const onMouseMove = (e) => {
        let newWidth = startWidth;
        let newHeight = startHeight;
        let newLeft = startLeft;
        let newTop = startTop;

        if (direction.includes('e')) newWidth = Math.max(20, startWidth + (e.clientX - startX));
        if (direction.includes('s')) newHeight = Math.max(20, startHeight + (e.clientY - startY));
        if (direction.includes('w')) {
          newWidth = Math.max(20, startWidth - (e.clientX - startX));
          newLeft = startLeft + (startWidth - newWidth);
        }
        if (direction.includes('n')) {
          newHeight = Math.max(20, startHeight - (e.clientY - startY));
          newTop = startTop + (startHeight - newHeight);
        }

        overlay.style.width = `${newWidth}px`;
        overlay.style.height = `${newHeight}px`;
        overlay.style.left = `${newLeft}px`;
        overlay.style.top = `${newTop}px`;
      };

      const onMouseUp = () => {
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
      };

      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    });
  }

  setupDrag(overlay) {
    let isDragging = false;
    let offsetX = 0, offsetY = 0;

    overlay.addEventListener('mousedown', (e) => {
      if (e.target.classList.contains('resize-handle') || e.target.classList.contains('resize-bar')) return;

      if (!overlay.classList.contains('selected')) return;

      isDragging = true;
      const rect = overlay.getBoundingClientRect();
      offsetX = e.clientX - rect.left;
      offsetY = e.clientY - rect.top;
      overlay.style.cursor = 'grabbing';
    });

    const onMouseMove = (e) => {
      if (!isDragging) return;

      const containerRect = this.imageContainer.getBoundingClientRect();
      let newX = e.clientX - containerRect.left - offsetX;
      let newY = e.clientY - containerRect.top - offsetY;

      newX = Math.max(0, Math.min(newX, containerRect.width - overlay.clientWidth));
      newY = Math.max(0, Math.min(newY, containerRect.height - overlay.clientHeight));

      overlay.style.left = `${newX}px`;
      overlay.style.top = `${newY}px`;
    };

    const onMouseUp = () => {
      isDragging = false;
      overlay.style.cursor = 'grab';
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    };

    overlay.addEventListener('mousedown', (e) => {
      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.bookingManager = new BookingManager('.section-floor-layout-floor-image');
});
