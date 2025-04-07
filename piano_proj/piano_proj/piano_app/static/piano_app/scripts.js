document.addEventListener('DOMContentLoaded', () => {

    // Show/hide error message
    const showVoteErrorMsg = (msg, id) => {
        const msgDiv = document.querySelector(`.vote-msg[data-piano="${id}"]`);
        msgDiv.textContent = msg;
        msgDiv.style.display = "block";

        setTimeout(() => {
            msgDiv.style.display = "none";
        }, 2500)
    }

    
    document.querySelectorAll(".vote-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {

            // If user tries to click disabled button
            if (btn.classList.contains("disabled-button")) {
                alert("You already voted this way")
                return
            }
    
            const pianoId = btn.dataset.piano;
            // Convert to integer (base 10 default)
            const voteValue = parseInt(btn.dataset.vote, 10);
            const url = `/pianos/vote/${pianoId}`;
            const token = document.querySelector('[name="csrfmiddlewaretoken"]').value;

            console.log(`Vote value:  ${voteValue}`)
    
            try {
                const response = await fetch(url, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": token,
                    },
                    body: JSON.stringify({
                        vote_type: voteValue,
                        piano_id: pianoId
                    })
                });

                if (!response.ok) {
                    throw new Error(`Response status: ${response.status}`);
                }
    
                const json = await response.json();

                if (json.error) {
                    alert(json.error);
                    return;
                }
    
                const voteDisplay = document.querySelector(`.vote-num[data-piano="${pianoId}"]`);
                // Update vote count
                if (voteDisplay) {
                    voteDisplay.textContent = `${json.vote_count}`;
                }

                toggleVoteButton(json, pianoId);

                console.log(json)      
    
            } catch (err) {
                console.error(err.message);
                alert("An error occurred while processing your vote.")
            }
    
        });
    }); // Vote button query selector


    // Disable vote button according to returned response
    function toggleVoteButton(data, id) {
        // Select upvote and downvote buttons
        const upVoteBtn = document.querySelector(`.vote-btn[data-piano="${id}"][data-vote="1"]`);
        const downVoteBtn = document.querySelector(`.vote-btn[data-piano="${id}"][data-vote="-1"]`);

        if (data.vote_type == "1") {
            upVoteBtn.classList.add("disabled-button");
            downVoteBtn.classList.remove("disabled-button");
        } else if (data.vote_type == "-1") {
            upVoteBtn.classList.remove("disabled-button");
            downVoteBtn.classList.add("disabled-button");
        } else {
            upVoteBtn.classList.remove("disabled-button");
            downVoteBtn.classList.add("disabled-button");
        }
    }
    


   // Delete piano
    const deleteLinks = document.querySelectorAll('.piano_delete_links');
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const confirmation = confirm("Are you really sure you want to delete this wonderful piano?")

            if (confirmation) {
                // Get the URL from the dataset
                const url = this.dataset.url;
                // Find the parent card element
                const pianoCard = this.closest('.card.mb-3');

                fetch (url, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrf_token,
                        'Content-Type': 'application/json'
                    },
                }).then(response => {
                    if (response.ok) {
                        alert('Piano has been successfully deleted.');
                        // Remove the card element from the DOM
                        pianoCard.remove();
                    } else {
                        alert("Houston, we have a problem.")
                    }
                }).catch(err => console.error("Error", err))
            }
        })
    })

    console.log("DOMContentLoaded");
});
// End DOMContentLoaded

