document.addEventListener('DOMContentLoaded', () => {
    let darkmode = localStorage.getItem('darkmode');
    const themeSwitch = document.getElementById('dark-mode-toggle');

    const imageSwitch = document.getElementById('DeskTop');
    const darkTop = themeSwitch.getAttribute('dark-image-top');
    const lightTop = themeSwitch.getAttribute('light-image-top');

    const enableDarkmode = () => {
        document.body.classList.add('darkmode');

        if (imageSwitch){
            imageSwitch.src = darkTop;
        }

        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.classList.add('dark-card');
        });

        localStorage.setItem('darkmode', 'active');
        console.log("Dark mode enabled");
    };

    const disableDarkmode = () => {
        document.body.classList.remove('darkmode');

        if (imageSwitch){
            imageSwitch.src = lightTop;
        }

        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.classList.remove('dark-card');
        });

        localStorage.setItem('darkmode', null);
        console.log("Dark mode disabled");
    };

    if (darkmode === "active") {
        console.log("Dark mode is active on page load");
        enableDarkmode();
    }

    themeSwitch.addEventListener("click", () => {
        darkmode = localStorage.getItem('darkmode');
        if (darkmode !== "active") {
            enableDarkmode();
        } else {
            disableDarkmode();
        }
    });
});