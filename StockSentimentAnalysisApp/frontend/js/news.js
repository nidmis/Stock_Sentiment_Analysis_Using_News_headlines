// frontend/js/news.js

document.addEventListener('DOMContentLoaded', function() {
    // Fetch recent news articles
    fetch('http://localhost:5000/api/news/top-news')
    .then(response => response.json())
    .then(data => {
        displayArticles(data.articles);
    })
    .catch(error => console.error('Error fetching news articles:', error));
});

function displayArticles(articles) {
    const articlesList = document.getElementById('articles-list');
    articles.forEach(article => {
        const li = document.createElement('li');
        li.innerHTML = `<a href="${article.url}" target="_blank">${article.title}</a>`;
        articlesList.appendChild(li);
    });
}
