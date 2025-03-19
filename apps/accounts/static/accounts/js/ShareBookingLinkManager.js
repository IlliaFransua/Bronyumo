class ShareBookingLinkManager {
  constructor() {
    this.modal = document.getElementById('modalShareLink_1234');
    this.linkInput = document.getElementById('bookingLinkInput_1234');
    this.copyButton = document.getElementById('copyLinkButton_1234');
    this.closeButton = document.getElementById('closeModalShareLink_1234');

    this.init();
  }

  init() {
    this.copyButton.addEventListener('click', this.copyBookingLink.bind(this));
    this.closeButton.addEventListener('click', this.closeModal.bind(this));
  }

  openBookingLink() {
    const mapHash = this.getMapHash();
    const bookingLink = `${window.location.origin}/bookings/client-booking-panel/${mapHash}/`;

    if (this.isValidUrl(bookingLink)) {
      this.showModalWithLink(bookingLink);
    } else {
      console.error('Invalid URL:', bookingLink);
      alert('Something went wrong with the URL.');
    }
  }

  getMapHash() {
    const url = window.location.href;
    const segments = url.split('/');
    return segments[segments.length - 2];
  }

  isValidUrl(url) {
    try {
      new URL(url);
      return true;
    } catch (e) {
      return false;
    }
  }

  showModalWithLink(link) {
    this.linkInput.value = link;
    this.modal.classList.remove('new-layout-img__is-hidden');
    document.body.classList.add('modal-open');
  }

  closeModal() {
    this.modal.classList.add('new-layout-img__is-hidden');
    document.body.classList.remove('modal-open');
    this.copyButton.removeEventListener('click', this.copyBookingLink.bind(this));
  }

  async copyBookingLink() {
    this.linkInput.select();

    try {
      await navigator.clipboard.writeText(this.linkInput.value);
      alert('Link copied to clipboard!');
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.shareBookingLinkManager = new ShareBookingLinkManager();
});
