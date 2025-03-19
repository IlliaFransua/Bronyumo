document.addEventListener("DOMContentLoaded", function () {
  window.bookingObjects = null;

  function getMapHashFromPath() {
    const pathSegments = window.location.pathname.split("/").filter(Boolean);
    return pathSegments[pathSegments.length - 1];
  }

  async function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async function fetchMapData(mapHash) {
    try {
      const mapResponse = await fetch(`/accounts/api/get_map_image/${mapHash}/`, {
        method: "GET",
        credentials: "include",
      });

      await wait(1000);

      if (!mapResponse.ok) throw new Error("Ошибка загрузки карты");

      const imageBlob = await mapResponse.blob();
      const imageUrl = URL.createObjectURL(imageBlob);

      const imageElement = document.querySelector(".section-floor-layout-floor-image");
      if (imageElement) {
        imageElement.src = imageUrl;
        imageElement.alt = "Map image";

        imageElement.onload = () => {
          window.bookingManager.loadBookingObjectsFromWindow();
        };
      }
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
    }
  }

  const mapHash = getMapHashFromPath();
  if (mapHash) {
    fetchMapData(mapHash);
  }
});
