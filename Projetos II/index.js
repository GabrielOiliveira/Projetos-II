document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".card-carro button");

    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            const card = button.closest(".card-carro");
            card.classList.toggle("expanded");
        });
    });
});