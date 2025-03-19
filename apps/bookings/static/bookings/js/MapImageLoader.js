class MapImageLoader {
  constructor() {
    this.mapHash = parseMapHash();
    this.imageElement = document.querySelector(".section-floor-layout-floor-image");
  }

  async wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async fetchMapData() {
    try {
      if (!this.mapHash) throw new Error("Map hash not found");

      const mapResponse = await fetch(`/accounts/api/get_map_image/${this.mapHash}/`, {
        method: "GET",
        credentials: "include",
      });

      await this.wait(1000);

      if (!mapResponse.ok) throw new Error("Card download error");

      const imageBlob = await mapResponse.blob();
      const imageUrl = URL.createObjectURL(imageBlob);

      if (this.imageElement) {
        this.imageElement.src = imageUrl;
        this.imageElement.alt = "Map image";
      }
      return imageUrl;
    } catch (error) {
      console.error("Data upload error:", error);
      throw error;
    }
  }

  async start() {
    if (this.mapHash) {
      try {
        const imageUrl = await this.fetchMapData();
        console.log('Image URL:', imageUrl);
      } catch (error) {
        console.error("Ошибка при загрузке карты:", error);
      }
    } else {
      console.error("Map hash is missing");
    }
  }
}
