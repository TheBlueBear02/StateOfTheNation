function createTimeline(ministers_history, totalDuration1, first_graph_date, lables, dates, type) {
    let currentDate = new Date().toJSON().slice(0, 7);
    console.log(currentDate);
    const colors = ["#FF6B6B", "#6EC1E4", "#90EE90", "#FFD56B", "#C9A0DC"];
 
    
    
    const labels_length = lables.length;

    let timeline;
    // Clear previous timeline content
    if (type == 'kpi') {
        timeline = document.getElementById("timeline");
    } else if (type == 'policy') {
        timeline = document.getElementById("timeline-p");
    } else {
        timeline = document.getElementById("timeline-office");
    }
    timeline.innerHTML = "";  // This removes all child elements

    // Check if the chart dates are years only or years and months
    // We'll check the length of the first label: "YYYY" is 4, "YYYY-MM" is 7
    let isYearOnly = false;
    if (lables.length > 0 && lables[0].length === 4) {
        isYearOnly = true;
    }

    if (type == 'office') {
        dates.push(currentDate);
    } else{
        if (isYearOnly){
            dates.push(lables[labels_length - 1] + "-12");
        } else {
            dates.push(lables[labels_length - 1]);
        }

        if (dates[0] < first_graph_date) {
            dates[0] = first_graph_date;
        }
    }    

    let widthPercent;
    let previous_date = 0;

    // Generate each era div
    for (let i = 0; i < dates.length - 1; i++) {
        // Check if its timeline for office or not
        if (type == 'office'){
             // Calculate the duration of this period
             const periodDuration = Date.parse(dates[i + 1]) - Date.parse(dates[i]);

             // Calculate width as a percentage of total duration
             widthPercent = (periodDuration / totalDuration1) * 100;
        } else {
            // If the labels are years and months, calculate the widths like this
            if (lables[0].length == 7) {
                for (let j = 0; j < labels_length; j++) {
                    if (lables[j] == dates[i + 1]) { // check if the current label equals the end of the era date
                        widthPercent = ((j - previous_date) / labels_length) * 100; // calculate the percentage of the number of labels in the era from the overall labels
                        previous_date = j; // set the previous date parameter to this label
                        break; // Once we find the matching label, we break out of the loop
                    }
                }
            } else { // If the labels are only years
                // Calculate the duration of this period
                const periodDuration = Date.parse(dates[i + 1]) - Date.parse(dates[i]);

                // Calculate width as a percentage of total duration
                widthPercent = (periodDuration / totalDuration1) * 100;
            }
        }

        // Set the era div info for the minister
        const ministerData = ministers_history[i];
        //  Get the color for the party
        let eraColor =  getPartyColor(ministerData["party"]);

        // Create div for this era
        const eraDiv = document.createElement("div");
        eraDiv.className = "era";
        eraDiv.style.width = widthPercent + "%";
        eraDiv.style.backgroundColor = eraColor;  // Cycle through colors

        // Add tooltip attribute
         eraDiv.setAttribute("data-tooltip", `${ministerData.name} - ${ministerData.party}`);
        // Only process the image and text if the width is above the threshold (5%)
        if (widthPercent >= 15) {
            // Convert the image URL to Base64 and then append it to the timeline
            convertToDataURL(ministerData["image"], (base64Image) => {
                // Create and append minister image with Base64 URL
                const ministerImage = document.createElement("img");
                ministerImage.src = base64Image; // Use the Base64-encoded image
                ministerImage.alt = `${ministerData.name} image`; // Alt text for accessibility
                ministerImage.style.width = "7vh"; // Adjust size as needed
                ministerImage.style.height = "auto"; // Maintain aspect ratio
                ministerImage.style.border = ".3vh solid " + eraColor; // Border color

                // Create a container for the minister's name and party
                const ministerInfoContainer = document.createElement("div");
                ministerInfoContainer.style.textAlign = "right"; // Aligns content to the right
                ministerInfoContainer.style.direction = "rtl"; // RTL for Hebrew or Arabic
                ministerInfoContainer.style.margin = 0;

                // Create and append minister name
                const ministerName = document.createElement("p");
                ministerName.textContent = ministerData["name"];
                ministerName.style.fontWeight = "bold";
                ministerName.style.margin = 0;
                ministerName.style.color = "white";

                // Create and append minister party
                const ministerParty = document.createElement("p");
                ministerParty.textContent = ministerData["party"];
                ministerParty.style.margin = 0;
                ministerParty.style.color = "white";


                // Create and append start and end dates
                const dateInfo = document.createElement("p");
                dateInfo.textContent = ` ${ministerData.start_date} `;
                dateInfo.style.position = "absolute";
                dateInfo.style.marginTop = "15vh";
                dateInfo.style.fontSize = "1.8vh";
                dateInfo.style.color = "grey";
                dateInfo.style.fontWeight = "bold";

                // Append the info container to the eraDiv
                eraDiv.appendChild(dateInfo);
                eraDiv.appendChild(ministerImage);
                ministerInfoContainer.appendChild(ministerName);
                ministerInfoContainer.appendChild(ministerParty);
                eraDiv.appendChild(ministerInfoContainer);
            });
        } else if (widthPercent >= 5 && widthPercent < 15) {
            // Process image and text if the width is between 5% and 10%
            convertToDataURL(ministerData["image"], (base64Image) => {
                const ministerImage = document.createElement("img");
                ministerImage.src = base64Image;
                ministerImage.alt = `${ministerData.name} image`;
                ministerImage.style.width = "7vh";
                ministerImage.style.height = "auto";
                ministerImage.style.border = ".3vh solid " + eraColor;

                const ministerInfoContainer = document.createElement("div");
                ministerInfoContainer.style.textAlign = "right";
                ministerInfoContainer.style.direction = "rtl";
                ministerInfoContainer.style.margin = 0;

      
                const dateInfo = document.createElement("p");
                dateInfo.textContent = ` ${ministerData.start_date} `;
                dateInfo.style.position = "absolute";
                dateInfo.style.marginTop = "15vh";
                dateInfo.style.fontSize = "1.8vh";
                dateInfo.style.color = "grey";
                dateInfo.style.fontWeight = "bold";

                eraDiv.appendChild(dateInfo);
                eraDiv.appendChild(ministerImage);
                ministerInfoContainer.appendChild(ministerName);
                ministerInfoContainer.appendChild(ministerParty);
                eraDiv.appendChild(ministerInfoContainer);
            });
        } else {
            // If width is smaller than 5%, we only show the date (no image)
            const dateInfo = document.createElement("p");
            dateInfo.style.position = "absolute";
            dateInfo.style.marginTop = "15vh";
            dateInfo.style.fontSize = "1.8vh";
            dateInfo.style.color = "grey";
            dateInfo.style.fontWeight = "bold";

            eraDiv.appendChild(dateInfo);
        }

        // Append to timeline container
        timeline.appendChild(eraDiv);
    }
}

// Convert image URL to Base64
function convertToDataURL(url, callback) {
    const img = new Image();
    img.crossOrigin = "Anonymous"; // Allow cross-origin loading
    img.onload = function () {
        const canvas = document.createElement("canvas");
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        const dataURL = canvas.toDataURL("image/png");
        callback(dataURL); // Return the Base64-encoded image
    };
    img.src = url;
}
