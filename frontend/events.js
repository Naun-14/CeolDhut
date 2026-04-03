document.addEventListener("DOMContentLoaded", () => {
    // DOM elements
    const likeButtons = document.querySelectorAll(".like-btn");
    const filterButtons = document.querySelectorAll(".location-filter button");
    const favoritesButton = document.getElementById("favorites-btn");
    const cards = document.querySelectorAll(".card");
    const modal = document.getElementById("event-modal");
    const modalTitle = document.getElementById("modal-title");
    const modalDescription = document.getElementById("modal-description");
    const modalDetails = document.getElementById("modal-details");
    const modalLink = document.getElementById("modal-link"); 
    const closeButton = document.querySelector(".close-btn");
    const displayButton = document.getElementById("display-btn");
   
    // like button 
    likeButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            console.log("like button clicked");
            const liked = btn.classList.toggle("liked");
            btn.innerHTML = liked ? "favorite" : "heart_plus"; 
        });
    });

    // filter buttons staying coloured
    filterButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            filterButtons.forEach((b) => b.classList.remove("active-filter"));
            btn.classList.add("active-filter");
        });
    });

    // filter for liked events
    favoritesButton.addEventListener("click", () => {
        cards.forEach((card) => {
            const likeBtn = card.querySelector(".like-btn");
            if (likeBtn.classList.contains("liked")) {
                card.style.display = "block"; 
            } else {
                card.style.display = "none"; 
            }
        });
    });

    // display events button, to show all cards again
    if(displayButton) {
    displayButton.addEventListener("click", () => {
        cards.forEach((card) => {
            card.style.display = "block";
        });
    });
} else {
     console.error("Not working at all");
}


    // MODAL
    cards.forEach((card) => {
        card.addEventListener("click", (e) => {
            // Skip click if like button is clicked
            if (e.target.classList.contains("like-btn")) return;
            modalTitle.textContent = card.dataset.title;
            modalDescription.textContent = card.dataset.description;
            modalDetails.textContent = `Date: ${card.dataset.date} | Location: ${card.dataset.location}`;
            modalLink.href = card.dataset.link;
            modal.style.display = "flex";
        });
    });

    // closes modal with button
    closeButton.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // closes modal
    window.addEventListener("click", (e) => {
        if (e.target === modal) modal.style.display = "none";
    });


    function checkEmail(email) { 
    // Email regex that covers most common email formats 
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; 
        if (emailRegex.test(email.value.trim())) { 
            showSuccess(email); 
            return true; 
        } else { 
            showError(email, "Email is not valid"); 
            return false; 
        } 
    } 

});
