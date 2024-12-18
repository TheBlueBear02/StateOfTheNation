function createTimeline(ministers_history, totalDuration1,first_graph_date,lables,dates) {
        
    let currentDate = new Date().toJSON().slice(0, 7);

    const colors = ["#FF6B6B", "#6EC1E4", "#90EE90", "#FFD56B", "#C9A0DC"];
    const labels_length = lables.length;

    // Clear previous timeline content
    const timeline = document.getElementById("timeline");
    timeline.innerHTML = "";  // This removes all child elements

   
    // Adding today's date to the end of the dates array
    dates.push(lables[labels_length - 1]+"-12")

    
    if (dates[0] < first_graph_date){
        dates[0] = first_graph_date
    }
    
    let widthPercent;
    let previous_date = 0;

   
    // Generate each era div
    for (let i = 0; i < dates.length - 1; i++) {
        
        
        
        
        // if the labales are years and months calculate the widths like this
        if (lables[0].length == 7){
            for(let j = 0; j < labels_length; j++){
            if (lables[j] == dates[i + 1]){ // check if the current label queal to the end of the era date
                widthPercent = (j - previous_date) / labels_length * 100; // calculate the precentage of the number of labales in the era from the overall labales 
                previous_date = j; // set the previous date parameter to the this label
                }
            }
        }
        else{ // if the labales are only years
            // Calculate the duration of this period
            const periodDuration = Date.parse(dates[i + 1]) - Date.parse(dates[i]);

            // Calculate width as a percentage of total duration
            widthPercent = (periodDuration / totalDuration1) * 100;
        }
       
        // Create div for this era
        const eraDiv = document.createElement("div");
        eraDiv.className = "era";
        eraDiv.style.width = widthPercent + "%";
        eraDiv.style.backgroundColor = colors[i % colors.length];  // Cycle through colors
        
        // Set the era div info for the minister
        const ministerData = ministers_history[i];

        // Create and append minister image
        const ministerImage = document.createElement("img");
        ministerImage.src = ministerData["image"]; // Replace with actual image property
        ministerImage.alt = `${ministerData.name} image`; // Alt text for accessibility
        ministerImage.style.width = "7vh"; // Adjust size as needed
        ministerImage.style.height = "auto"; // Maintain aspect ratio
        ministerImage.style.border = ".3vh solid "+colors[i % colors.length]; // Maintain aspect ratio
    
    
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

        // Create and append minister party
        const ministerParty = document.createElement("p");
        ministerParty.textContent = ministerData["party"];
        ministerParty.style.margin = 0;

        // Create and append start and end dates
        const dateInfo = document.createElement("p");
        dateInfo.textContent = ` ${ministerData.start_date} `; // Adjust as necessary
        dateInfo.style.position = "absolute";
        dateInfo.style.marginTop = "15vh";
        dateInfo.style.fontSize = "1.8vh";
        dateInfo.style.color = "grey";
        dateInfo.style.fontWeight = "bold";


        // Append the info container to the eraDiv
        if (widthPercent < 5) {

        } else if (widthPercent >= 5 && widthPercent < 10) {
            eraDiv.appendChild(dateInfo);
            eraDiv.appendChild(ministerImage);
            
        } else {
            eraDiv.appendChild(dateInfo);
            eraDiv.appendChild(ministerImage);
            ministerInfoContainer.appendChild(ministerName);
            ministerInfoContainer.appendChild(ministerParty);
            eraDiv.appendChild(ministerInfoContainer);

        }
        
        

        // Append to timeline container
        timeline.appendChild(eraDiv);
    }
}
