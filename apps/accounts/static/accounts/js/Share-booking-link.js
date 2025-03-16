function openBookingLink() {
    const mapHash = getMapHash();
    const bookingLink = `${window.location.origin}/bookings/client-booking-panel/${mapHash}/`;

    if (isValidUrl(bookingLink)) {
        showModalWithLink(bookingLink);
    } else {
        console.error('Invalid URL:', bookingLink);
        alert('Something went wrong with the URL.');
    }
}

function getMapHash() {
    const url = window.location.href;
    const segments = url.split('/');
    return segments[segments.length - 2];
}

function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch (e) {
        return false;
    }
}

function showModalWithLink(link) {
    const modal = document.getElementById('modalShareLink_1234');
    const linkInput = document.getElementById('bookingLinkInput_1234');
    const copyButton = document.getElementById('copyLinkButton_1234');

    linkInput.value = link;

    modal.classList.remove('new-layout-img__is-hidden');
    document.body.classList.add('modal-open');

    copyButton.onclick = copyBookingLink;

    document.getElementById('closeModalShareLink_1234').addEventListener('click', () => {
        modal.classList.add('new-layout-img__is-hidden');
        document.body.classList.remove('modal-open');

        copyButton.onclick = null;
    });
}

async function copyBookingLink() {
    const linkInput = document.getElementById('bookingLinkInput_1234');
    linkInput.select();

    try {
        await navigator.clipboard.writeText(linkInput.value);
        alert('Link copied to clipboard!');
    } catch (err) {
        console.error('Failed to copy: ', err);
    }
}
