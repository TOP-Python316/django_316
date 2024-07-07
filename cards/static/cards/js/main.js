// cards/static/cards/js/main.js
// Главный файл для всего приложения, подключается в шаблоне base.html


// Листнер при клике на заголовок H1 добавляет/убирает класс бутсрап 5
// желтый фон и красный текст
document.querySelector('h1').addEventListener('click', () => {
    document.querySelector('h1').classList.toggle('text-danger');
    document.querySelector('h1').classList.toggle('bg-warning');
});