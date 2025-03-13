class TableLayoutManager {
    constructor() {
        this.floorImage = document.querySelector('.section-floor-layout-floor-image');
        this.container = document.querySelector('.section-floor-layout');
        this.addBookingButton = document.querySelector('#add-booking-button');
        this.tables = [];

        this.initializeEventListeners();
        window.addEventListener('resize', this.repositionTables.bind(this));
    }

    initializeEventListeners() {
        if (this.addBookingButton) {
            this.addBookingButton.addEventListener('click', this.createNewTable.bind(this));
        }
    }

    createNewTable() {
        const table = document.createElement('div');
        table.classList.add('booking-rectangle');

        const defaultWidth = 100;
        const defaultHeight = 50;

        const imageRect = this.floorImage.getBoundingClientRect();
        const centerX = (imageRect.width - defaultWidth) / 2;
        const centerY = (imageRect.height - defaultHeight) / 2;

        table.style.width = `${defaultWidth}px`;
        table.style.height = `${defaultHeight}px`;
        table.style.left = `${centerX}px`;
        table.style.top = `${centerY}px`;

        const normalizedCoords = {
            x1: centerX / imageRect.width,
            y1: centerY / imageRect.height,
            x2: (centerX + defaultWidth) / imageRect.width,
            y2: (centerY + defaultHeight) / imageRect.height
        };
        table.dataset.normalizedCoords = JSON.stringify(normalizedCoords);

        this.container.appendChild(table);
        this.makeDraggable(table);
        this.tables.push(table);
    }

    makeDraggable(element) {
        let isDragging = false;
        let startX, startY, initialLeft, initialTop;

        const startDrag = (e) => {
            isDragging = true;

            e.preventDefault();

            startX = e.pageX;
            startY = e.pageY;

            initialLeft = parseFloat(element.style.left || 0);
            initialTop = parseFloat(element.style.top || 0);

            element.style.opacity = '0.7';
        };

        const drag = (e) => {
            if (!isDragging) return;

            const dx = e.pageX - startX;
            const dy = e.pageY - startY;

            const newLeft = initialLeft + dx;
            const newTop = initialTop + dy;

            const containerRect = this.container.getBoundingClientRect();
            const elementRect = element.getBoundingClientRect();

            const constrainedLeft = Math.max(
                0,
                Math.min(
                    newLeft,
                    containerRect.width - elementRect.width
                )
            );

            const constrainedTop = Math.max(
                0,
                Math.min(
                    newTop,
                    containerRect.height - elementRect.height
                )
            );

            element.style.left = `${constrainedLeft}px`;
            element.style.top = `${constrainedTop}px`;

            this.updateNormalizedCoordinates(element);
        };

        const stopDrag = () => {
            if (!isDragging) return;

            isDragging = false;
            element.style.opacity = '1';
        };

        this.addResizeHandles(element);

        element.addEventListener('mousedown', startDrag);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', stopDrag);
    }

    addResizeHandles(element) {
        const directions = ['se', 'sw', 'ne', 'nw'];

        directions.forEach(dir => {
            const handle = document.createElement('div');
            handle.classList.add('resize-handle', `resize-${dir}`);
            handle.style.position = 'absolute';
            handle.style.width = '10px';
            handle.style.height = '10px';
            handle.style.backgroundColor = 'blue';

            switch(dir) {
                case 'se':
                    handle.style.bottom = '0';
                    handle.style.right = '0';
                    handle.style.cursor = 'se-resize';
                    break;
                case 'sw':
                    handle.style.bottom = '0';
                    handle.style.left = '0';
                    handle.style.cursor = 'sw-resize';
                    break;
                case 'ne':
                    handle.style.top = '0';
                    handle.style.right = '0';
                    handle.style.cursor = 'ne-resize';
                    break;
                case 'nw':
                    handle.style.top = '0';
                    handle.style.left = '0';
                    handle.style.cursor = 'nw-resize';
                    break;
            }

            element.appendChild(handle);
            this.makeResizable(element, handle, dir);
        });
    }

    makeResizable(element, handle, direction) {
        let isResizing = false;
        let startX, startY, startWidth, startHeight, startLeft, startTop;

        const startResize = (e) => {
            e.stopPropagation();
            isResizing = true;

            startX = e.pageX;
            startY = e.pageY;

            startWidth = parseFloat(getComputedStyle(element).width);
            startHeight = parseFloat(getComputedStyle(element).height);

            startLeft = parseFloat(element.style.left || 0);
            startTop = parseFloat(element.style.top || 0);
        };

        const resize = (e) => {
            if (!isResizing) return;

            const dx = e.pageX - startX;
            const dy = e.pageY - startY;

            const containerRect = this.container.getBoundingClientRect();

            let newWidth, newHeight, newLeft, newTop;

            switch(direction) {
                case 'se':
                    newWidth = Math.max(50, startWidth + dx);
                    newHeight = Math.max(50, startHeight + dy);
                    break;
                case 'sw':
                    newWidth = Math.max(50, startWidth - dx);
                    newHeight = Math.max(50, startHeight + dy);
                    newLeft = startLeft + (startWidth - newWidth);
                    break;
                case 'ne':
                    newWidth = Math.max(50, startWidth + dx);
                    newHeight = Math.max(50, startHeight - dy);
                    newTop = startTop + (startHeight - newHeight);
                    break;
                case 'nw':
                    newWidth = Math.max(50, startWidth - dx);
                    newHeight = Math.max(50, startHeight - dy);
                    newLeft = startLeft + (startWidth - newWidth);
                    newTop = startTop + (startHeight - newHeight);
                    break;
            }

            if (newLeft !== undefined) {
                newLeft = Math.max(0, Math.min(newLeft, containerRect.width - newWidth));
                element.style.left = `${newLeft}px`;
            }

            if (newTop !== undefined) {
                newTop = Math.max(0, Math.min(newTop, containerRect.height - newHeight));
                element.style.top = `${newTop}px`;
            }

            element.style.width = `${newWidth}px`;
            element.style.height = `${newHeight}px`;

            this.updateNormalizedCoordinates(element);
        };

        const stopResize = () => {
            isResizing = false;
        };

        handle.addEventListener('mousedown', startResize);
        document.addEventListener('mousemove', resize);
        document.addEventListener('mouseup', stopResize);
    }

    updateNormalizedCoordinates(element) {
        const imageRect = this.floorImage.getBoundingClientRect();
        const elementRect = element.getBoundingClientRect();

        const normalizedCoords = {
            x1: (elementRect.left - imageRect.left) / imageRect.width,
            y1: (elementRect.top - imageRect.top) / imageRect.height,
            x2: (elementRect.right - imageRect.left) / imageRect.width,
            y2: (elementRect.bottom - imageRect.top) / imageRect.height
        };

        element.dataset.normalizedCoords = JSON.stringify(normalizedCoords);
    }

    repositionTables() {
        const imageRect = this.floorImage.getBoundingClientRect();

        this.tables.forEach(table => {
            const normalizedCoords = JSON.parse(table.dataset.normalizedCoords);

            const left = normalizedCoords.x1 * imageRect.width;
            const top = normalizedCoords.y1 * imageRect.height;
            const width = (normalizedCoords.x2 - normalizedCoords.x1) * imageRect.width;
            const height = (normalizedCoords.y2 - normalizedCoords.y1) * imageRect.height;

            table.style.left = `${left}px`;
            table.style.top = `${top}px`;
            table.style.width = `${width}px`;
            table.style.height = `${height}px`;
        });
    }

    // Method to get all table coordinates for saving
    getTableCoordinates() {
        return {
            path_to_object_map: "paste_the_url", // Replace with your actual URL
            objects_data: this.tables.map((table, index) => {
                const coords = JSON.parse(table.dataset.normalizedCoords);
                return {
                    object_id: index,
                    x1: coords.x1,
                    y1: coords.y1,
                    x2: coords.x2,
                    y2: coords.y2
                };
            })
        };
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.tableLayoutManager = new TableLayoutManager();
});