document.addEventListener('click', function (event) {
    
    if (event.target.classList.contains('toggle-profile-btn')) {
        const button = event.target;
        const cardId = button.getAttribute('data-card-id');

        
        const profileName = prompt("Enter the profile name:");
        const profileHeight = prompt("Enter the height in cm:");

        if (!profileName || !profileHeight) {
            alert("Both name and height are required.");
            return;
        }

        
        const grid = document.querySelector('.height-profile-grid');
        const profileCard = document.createElement('div');
        profileCard.className = 'height-profile-card';
        profileCard.innerHTML = `
            <h3>${profileName}</h3>
            <p>Height: ${profileHeight} cm</p>
            <button class="apply-profile-btn" data-profile-name="${profileName}" data-profile-height="${profileHeight}">Apply</button>
            <button class="delete-profile-btn" data-card-id="${cardId}" data-profile-name="${profileName}" data-profile-height="${profileHeight}">Delete</button>
        `;
        grid.appendChild(profileCard);

        alert("Profile created successfully!");

        
        fetch('/save-profile/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ cardId, profileName, profileHeight }),
        })
            .then(response => response.json())
            .then(data => console.log(data.message))
            .catch(error => console.error('Error:', error));
    }

    
    if (event.target.classList.contains('apply-profile-btn')) {
        const button = event.target;
        const profileName = button.getAttribute('data-profile-name');
        const profileHeight = button.getAttribute('data-profile-height');

        alert(`Applying profile "${profileName}" with height ${profileHeight} cm`);

        
        fetch('/apply-profile/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ profileName, profileHeight }),
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => console.error('Error:', error));
    }

    
    if (event.target.classList.contains('delete-profile-btn')) {
        const button = event.target;
        const profileCard = button.closest('.height-profile-card');
        const grid = document.querySelector('.height-profile-grid');
        const profileName = button.getAttribute('data-profile-name');
        const profileHeight = button.getAttribute('data-profile-height');

        if (confirm(`Are you sure you want to delete the profile "${profileName}" with height ${profileHeight} cm?`)) { 
            grid.removeChild(profileCard);

            alert("Profile deleted successfully!");

            fetch('/delete-profile/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({ profileName, profileHeight }),
            })
                .then(response => response.json())
                .then(data => console.log(data.message))
                .catch(error => console.error('Error:', error));
        }
    }
});

function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            cookieValue = cookie.substring('csrftoken='.length, cookie.length);
            break;
        }
    }
    return cookieValue;
}
