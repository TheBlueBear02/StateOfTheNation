// Declare variables at the top level
let correctAnswers = 0;
let wrongAnswers = 0;

  // Function to update the time left until midnight
  function updateTimeLeft() {
    const now = new Date();
    const midnight = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1); // Next midnight
    const timeLeft = midnight - now; // Time left in milliseconds

    // Calculate hours, minutes, and seconds
    const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

    // Update the display
    const timeDisplay = document.getElementById("time-left");
    timeDisplay.textContent = `חברי כנסת חדשים בעוד ${hours} שעות ו${minutes} דקות `;
}

document.addEventListener("DOMContentLoaded", function () {
    const difficultyButtons = document.querySelectorAll(".difficulty-btn");
    const submitButton = document.getElementById("submit-btn");
    const userInput = document.getElementById("user-answer");
    const resultMessage = document.getElementById("result-message");
    const skipButton = document.getElementById("skip-btn");
    const startButton = document.getElementById("start-btn");
    const openingScreen = document.querySelector(".openingScreen");
    const gameContainer = document.getElementById("game-container");
    let correctName = "";
    
    // Function to load Knesset members from JSON
    function loadKnessetMembers() {
        fetch("static/json/knesset_members.json") // Adjust the path as necessary
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const datalist = document.getElementById("knesset-members");
                datalist.innerHTML = ""; // Clear existing options

                // Check if data is an array and has members
                if (Array.isArray(data)) {
                    data.forEach(level => {
                        if (level.members && level.members.length > 0) {
                            level.members.forEach(member => {
                                const option = document.createElement("option");
                                option.value = member.name; // Assuming member has a 'name' property
                                datalist.appendChild(option);
                            });
                        } else {
                            console.warn(`No members found for difficulty level: ${level.difficulty}`);
                        }
                    });
                } else {
                    console.error("Data is not in the expected format:", data);
                }
            })
            .catch(error => {
                console.error("Error loading Knesset members:", error);
            });
    }

    function loadQuestion(difficulty) {
        return fetch("/api/question", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ difficulty })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Check if the expected fields are present in the data
            if (data.name_hidden && data.year_first && data.year_last && data.important_role && data.career_before && data.party) {
                correctName = data.name_hidden;
                document.getElementById("year-first").textContent = data.year_first;
                document.getElementById("year-last").textContent = (data.year_last === new Date().getFullYear()) ? "עדיין מכהן" : data.year_last;
                document.getElementById("important-role").textContent = data.important_role;
                document.getElementById("career-before").textContent = data.career_before;
                document.getElementById("party").textContent = data.party;

                // Update the current-level class
                difficultyButtons.forEach(button => {
                    button.classList.remove("current-level");
                    if (button.getAttribute("data-level") === difficulty) {
                        button.classList.add("current-level");
                    }
                });
            } else {
                console.error("Received data does not contain the expected fields:", data);
            }
        })
        .catch(error => {
            console.error("Error loading question:", error);
        });
    }
    
    // Load initial question and Knesset members when page loads
    loadKnessetMembers(); // Load Knesset members
    loadQuestion("קל"); // Load initial question
    
    // Disable difficulty buttons to prevent interaction
    difficultyButtons.forEach(button => {
        button.disabled = true; // Disable the button
    });
    
    submitButton.addEventListener("click", function () {
        const answer = userInput.value.trim();
        fetch("/api/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answer, correct_name: correctName })
        })
        .then(response => response.json())
        .then(data => {
            resultMessage.textContent = data.correct ? "נכון!" : "לא נכון, נסה שוב.";
            resultMessage.style.color = data.correct ? "green" : "red";
            if (data.correct) {
                correctAnswers++; // Increment correct answers
                setTimeout(() => {
                    // Get the current difficulty level
                    let currentDifficulty = document.querySelector(".current-level").getAttribute("data-level");
                    
                    difficultyButtons.forEach(button => {
                        if (button.getAttribute("data-level") === currentDifficulty) {
                            button.style.backgroundColor = "green"; // Change to green
                            button.style.color = "white"; // Change text color to white
                            button.style.opacity = "0.5";
                            button.disabled = true; // Disable the button
                        }
                    });
                    // Determine the next difficulty level
                    let nextDifficulty;
                    if (currentDifficulty === "קל") {
                        nextDifficulty = "בינוני"; // Change to medium
                    } else if (currentDifficulty === "בינוני") {
                        nextDifficulty = "קשה"; // Change to hard
                    } else {
                        // Show summary screen after completing the hardest difficulty
                        showSummaryScreen();
                        return; // Exit the function
                    }

                    // Load the next question with the new difficulty
                    loadQuestion(nextDifficulty).then(() => {
                        // Update the current-level class
                        difficultyButtons.forEach(button => {
                            button.classList.remove("current-level"); // Remove current-level from all buttons
                            if (button.getAttribute("data-level") === nextDifficulty) {
                                button.classList.add("current-level"); // Add current-level to the new difficulty button
                                button.disabled = false; // Enable the button for the next question
                            }
                        });

                        userInput.value = "";
                        resultMessage.textContent = "";
                    });
                }, 1500);
            } else {
                wrongAnswers++; // Increment wrong answers
            }
        })
        .catch(error => {
            console.error("Error checking answer:", error);
        });
    });

    skipButton.addEventListener("click", function() {
        // Get the current difficulty level
        const currentDifficulty = document.querySelector(".current-level").getAttribute("data-level");
        wrongAnswers++; // Increment correct answers

        // Change the button color to red
        difficultyButtons.forEach(button => {
            if (button.getAttribute("data-level") === currentDifficulty) {
                button.style.backgroundColor = "red"; // Change to red
                button.style.color = "white"; // Change text color to white
                button.style.opacity = "0.5";
                button.disabled = true; // Disable the button
            }
        });

        // Determine the next difficulty level
        let nextDifficulty;
        if (currentDifficulty === "קל") {
            nextDifficulty = "בינוני"; // Change to medium
        } else if (currentDifficulty === "בינוני") {
            nextDifficulty = "קשה"; // Change to hard
        } else {
            showSummaryScreen(); // Show summary screen
            return; // Exit the function
        }

        // Load the next question with the new difficulty
        loadQuestion(nextDifficulty);
        
        // Update the current-level class
        difficultyButtons.forEach(button => {
            button.classList.remove("current-level"); // Remove current-level from all buttons
            if (button.getAttribute("data-level") === nextDifficulty) {
                button.classList.add("current-level"); // Add current-level to the new difficulty button
                button.disabled = false; // Enable the button for the next question
            }
        });

        // Clear user input and result message
        userInput.value = "";
        resultMessage.textContent = "";
    });

    // Add event listener for the start button
    startButton.addEventListener("click", function () {
        openingScreen.style.display = "none"; // Hide the opening screen
        gameContainer.style.display = "block"; // Show the game container
    });

    // Add event listener for the share button
    document.getElementById("share-btn").addEventListener("click", function() {
        captureScreenshot();
    });

  
  

    // Update the time every second
});

// Function to show the summary screen
function showSummaryScreen() {
    const gamefunctionContainer = document.getElementById("game-function-container");
    const gameContainer = document.getElementById("game-container");
    
    // Define arrays of messages based on the number of correct answers
    const messages = {
        0: [
            "אם תמשיך ככה אין דלת שלא תיסגר בפניך!",
            "אין ספק שאתה תגיע קרוב מאוד בחיים!"
        ],
        1: [
            "נסיון יפה! יש לך מספיק ידע בשביל לריב עם אנשים בטוויטר"
        ],
        2: [
            "יפה! רק 28% מהמתמשים הצליחו לנחש 2 מתוך ה3! (עכשיו המצאתי)"
        ],
        3: [
            "תגיע מחר בשמונה למהדורה המרכזית שמור לך מקום בין עמית סגל לקושמרו"
        ]
    };

    // Select a random message based on the number of correct answers
    const correctMessageArray = messages[correctAnswers] || [""];
    const randomMessage = correctMessageArray[Math.floor(Math.random() * correctMessageArray.length)];

    // Replace the content of the game container with the summary results
    gamefunctionContainer.innerHTML = `
        <p>הצלחת לנחש ${correctAnswers} מתוך 3 חברי הכנסת</p>
        <p id="summary-results">${randomMessage}</p>
        <button id="share-btn">שתף</button>
        <div id="time-left"></div>
    `;

    // Update the time left immediately
    updateTimeLeft(); // Call this to set the initial time left

    // Add event listener for the share button
    document.getElementById("share-btn").addEventListener("click", function() {
        captureScreenshot();
    });
}

// Function to capture screenshot of the body element
function captureScreenshot() {
    html2canvas(document.body).then(canvas => {
        // Convert the canvas to a data URL
        const dataURL = canvas.toDataURL("image/png");

        // Create a temporary link element to copy the image
        const link = document.createElement("a");
        link.href = dataURL;
        link.download = "screenshot.png"; // Set the filename

        // Append the link to the body
        document.body.appendChild(link);
        
        // Trigger the download
        link.click();
        
        // Remove the link from the document
        document.body.removeChild(link);

        // Optionally, show a message to the user
        alert("הסקרין שוט הועתק!");
    });
}

