const carrossel = document.querySelector('.carrossel');
const imagens = document.querySelectorAll('.carrossel img');
const botaoAnterior = document.querySelector('.anterior');
const botaoProximo = document.querySelector('.proximo');

let currentIndex = 0;

function atualizaCarrossel() {
    const imageWidth = imagens[0].clientWidth;
    carrossel.style.transform = `translateX(${-currentIndex * imageWidth}px)`;
}

botaoProximo.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % imagens.length; // Vai para a próxima imagem
    atualizaCarrossel();
});

botaoAnterior.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + imagens.length) % imagens.length; // Volta para a imagem anterior
    atualizaCarrossel();
});

window.addEventListener('resize', atualizaCarrossel); // Ajusta se a janela for redimensionada
