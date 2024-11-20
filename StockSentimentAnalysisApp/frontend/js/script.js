// frontend/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // Fetch market trends
    fetch('http://localhost:5000/api/market-trends')
    .then(response => response.json())
    .then(data => {
        displayMarketTrends(data.trends);
    })
    .catch(error => console.error('Error fetching market trends:', error));

    // Fetch top news headlines
    fetch('http://localhost:5000/api/news/top-news')
    .then(response => response.json())
    .then(data => {
        displayTopNews(data.articles);
    })
    .catch(error => console.error('Error fetching news:', error));

    // Search button click event
    document.getElementById('search-button').addEventListener('click', function() {
        const symbol = document.getElementById('search-input').value.trim().toUpperCase();
        if (symbol) {
            window.location.href = `stock.html?symbol=${symbol}`;
        } else {
            alert('Please enter a stock symbol.');
        }
    });
});

function displayMarketTrends(trends) {
    const trendsDiv = document.getElementById('trends');
    trends.forEach(trend => {
        const trendCard = document.createElement('div');
        trendCard.className = 'trend-card';
        trendCard.innerHTML = `
            <h3>${trend.name}</h3>
            <p>Index: ${trend.symbol}</p>
            <p>Current Price: $${trend.current_price}</p>
            <p>Change: ${trend.change_percent}%</p>
        `;
        trendsDiv.appendChild(trendCard);
    });
}

function displayTopNews(articles) {
    const newsList = document.getElementById('news-headlines');
    articles.slice(0, 5).forEach(article => {
        const li = document.createElement('li');
        li.innerHTML = `<a href="${article.url}" target="_blank">${article.title}</a>`;
        newsList.appendChild(li);
    });
}
