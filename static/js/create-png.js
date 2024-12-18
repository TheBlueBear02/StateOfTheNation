
function copyElementAsPngToClipboard(elementId) {
    const element = document.getElementById(elementId);

    if (!element) {
        console.error(`Element with id '${elementId}' not found.`);
        return;
    }

    html2canvas(element).then(canvas => {
        // Convert the canvas to a Blob
        canvas.toBlob(blob => {
            if (!blob) {
                console.error("Failed to create Blob from canvas.");
                return;
            }

            // Create a ClipboardItem with the Blob
            const item = new ClipboardItem({ "image/png": blob });

            // Write the item to the clipboard
            navigator.clipboard.write([item]).then(() => {
                console.log("Image copied to clipboard successfully!");
            }).catch(error => {
                console.error("Failed to copy image to clipboard:", error);
            });
        }, "image/png");
    }).catch(error => {
        console.error("Error capturing element:", error);
    });
}
