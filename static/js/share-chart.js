function copyElementAsPngToClipboard(elementId) {
    const element = document.getElementById(elementId);

    if (!element) {
        console.error(`Element with id '${elementId}' not found.`);
        return;
    }

    // Create a watermark div
    const watermarkDiv = document.createElement("div");
    watermarkDiv.style.position = "absolute";
    watermarkDiv.style.top = ".5vw";
    watermarkDiv.style.left = ".5vw";
    watermarkDiv.style.backgroundColor = "rgba(255, 255, 255)";
    watermarkDiv.style.padding = "1vw";
    watermarkDiv.style.borderRadius = "5px";
    watermarkDiv.style.display = "flex";
    watermarkDiv.style.alignItems = "center";
    watermarkDiv.style.gap = "10px";
    watermarkDiv.style.zIndex = "1000";
    watermarkDiv.style.visibility = "hidden"; // Make it invisible to the user
    watermarkDiv.style.pointerEvents = "none"; // Ensure it doesn't interfere with user interactions

    // Create a container for text content
    const textContainer = document.createElement("div");
    textContainer.style.display = "flex";
    textContainer.style.flexDirection = "column";
    textContainer.style.textAlign = "left"; // Align text to the left of the container

    // Add site name
    const siteName = document.createElement("span");
    siteName.textContent = "מתוך האתר מצב האומה"; // Replace with your site's name
    siteName.style.fontWeight = "bold";
    siteName.style.fontSize = "16px";
    siteName.style.color = "#000";
    siteName.style.fontFamily = 'Arial, sans-serif';
    textContainer.appendChild(siteName);

    // Add site URL
    const siteUrl = document.createElement("a");
    siteUrl.textContent = "www.stateofthenation.co.il";
    siteUrl.style.fontSize = "14px";
    siteUrl.style.color = "#4890FD"; // Example link color
    siteUrl.style.textDecoration = "none";
    siteUrl.target = "_blank"; // Open the URL in a new tab
    textContainer.appendChild(siteUrl);

    // Add logo
    const logoImg = document.createElement("img");
    logoImg.src = "static/images/header/header-logo.png"; // Replace with your logo URL
    logoImg.alt = "Site Logo";
    logoImg.style.width = "100px"; // Adjust logo size
    logoImg.style.height = "50px";

    // Add logo and text container to the watermark div
    watermarkDiv.appendChild(logoImg);
    watermarkDiv.appendChild(textContainer);

    // Temporarily append the watermark to the element
    element.style.position = "relative"; // Ensure the element has relative positioning
    watermarkDiv.style.visibility = "visible"; // Make it visible during capture
    element.appendChild(watermarkDiv);

    // Configure html2canvas options
    const options = {
        backgroundColor: null, // Ensure transparent background
        scale: 2, // Higher quality
        useCORS: true, // Enable CORS for images
        allowTaint: true, // Allow cross-origin images
        logging: false, // Disable logging
        onclone: (clonedDoc) => {
            // Ensure timeline elements are properly rendered in the clone
            const timeline = clonedDoc.querySelector('.timeline');
            if (timeline) {
                timeline.style.backgroundColor = 'transparent';
            }
        }
    };

    html2canvas(element, options).then(canvas => {
        // Remove the watermark after capturing
        watermarkDiv.remove();

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
                // Show custom popup message
                showMessage();
                showMessageP();
            }).catch(error => {
                console.error("Failed to copy image to clipboard:", error);
            });
        }, "image/png");
    }).catch(error => {
        console.error("Error capturing element:", error);
    });
}
