class ObjectsMapLoaderAPI {
  constructor() {
  }

  async loadAvailableObjects(fromTime, toTime) {
    if (!fromTime || !toTime) {
      console.error("Missing 'from' or 'to' parameters.");
      return null;
    }

    try {
      const url = `/utils/api/objects-map-loader/${parseMapHash()}?from=${encodeURIComponent(fromTime)}&to=${encodeURIComponent(toTime)}`;
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log("Available booking objects:", data.booking_objects);
      return data.booking_objects;
    } catch (error) {
      console.error("Failed to load available objects:", error);
      return null;
    }
  }
}
