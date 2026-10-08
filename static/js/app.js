document.addEventListener("DOMContentLoaded", () => {

    // Add a small visual effect when an item is added to cart
    const addButtons = document.querySelectorAll(".add-btn");

    addButtons.forEach((button) => {

        button.addEventListener("click", () => {

            const originalText = button.textContent;

            button.textContent = "✓ Added";

            button.style.background = "#58dba4";

            setTimeout(() => {
                button.textContent = originalText;
                button.style.background = "";
            }, 900);

        });

    });


    // Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach((link) => {

        link.addEventListener("click", (event) => {

            const targetId = link.getAttribute("href");

            if (targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (target) {
                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth"
                });
            }

        });

    });

});