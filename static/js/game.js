document.addEventListener("DOMContentLoaded", function () {
    const difficultyButtons = document.querySelectorAll(".difficulty-btn");
    const submitButton = document.getElementById("submit-btn");
    const userInput = document.getElementById("user-answer");
    const resultMessage = document.getElementById("result-message");
    const skipButton = document.getElementById("skip-btn");
    let correctName = "";
    
    // Variables to track scores
    let correctAnswers = 0;
    let wrongAnswers = 0;

    // Function to load Knesset members from JSON
    function loadKnessetMembers() {
        fetch("static/json/knesset_members.json") // Adjust the path as necessary
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(members => {
                const datalist = document.getElementById("knesset-members");
                datalist.innerHTML = ""; // Clear existing options
                members.forEach(member => {
                    const option = document.createElement("option");
                    option.value = member.name; // Assuming member has a 'name' property
                    datalist.appendChild(option);
                });
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
            correctName = data.name_hidden;
            document.getElementById("year-first").textContent = data.year_first;
            document.getElementById("year-last").textContent = data.year_last;
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
        console.log("Skip button clicked"); // Debugging line
        // Get the current difficulty level
        const currentDifficulty = document.querySelector(".current-level").getAttribute("data-level");
        
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
});

// Function to show the summary screen
function showSummaryScreen() {
    const gameContainer = document.getElementById("game-container");

    // Replace the content of the game container with the summary results
    gameContainer.innerHTML = `
        <h1>סיכום המשחק</h1>
        <p id="summary-results"></p>
        <button id="restart-btn">התחל מחדש</button>
    `;

    // Display the results
    const summaryResults = document.getElementById("summary-results");
    summaryResults.textContent = `סיימת את המשחק! 
    מספר תשובות נכונות: ${correctAnswers} 
    מספר תשובות שגויות: ${wrongAnswers}`;

    // Restart button functionality
    document.getElementById("restart-btn").addEventListener("click", function () {
        window.location.reload(); // Reload the game page
    });
}
    