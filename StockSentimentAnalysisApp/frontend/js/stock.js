// frontend/js/stock.js

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const symbol = urlParams.get('symbol');

    if (!symbol) {
        alert('No stock symbol provided.');
        window.location.href = 'index.html';
    }

    document.getElementById('stock-symbol').textContent = symbol.toUpperCase();

    // Fetch stock chart data
    fetch(`http://localhost:5000/api/stock-chart/${symbol}`)
    .then(response => response.json())
    .then(data => {
        displayStockChart(data);
    })
    .catch(error => console.error('Error fetching stock chart data:', error));

    // Fetch news and sentiment
    fetch(`http://localhost:5000/api/news/${symbol}`)
    .then(response => response.json())
    .then(data => {
        displayNews(data.news);
        return fetch(`http://localhost:5000/api/predict/${symbol}`);
    })
    .then(response => response.json())
    .then(data => {
        displayPrediction(data);
        displaySentimentChart(data.sentiment);
    })
    .catch(error => console.error('Error fetching stock prediction or sentiment analysis:', error));
});

function displayStockChart(data) {
    const ctx = document.getElementById('stock-chart').getContext('2d');

    const labels = data.dates;
    const prices = data.prices;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Closing Price',
                data: prices,
                borderColor: 'green',
                fill: false
            }]
        },
        options: {
            responsive: true
        }
    });
}

function displayNews(newsList) {
    const newsUl = document.getElementById('news-list');
    newsList.forEach(news => {
        const li = document.createElement('li');
        li.textContent = news;
        newsUl.appendChild(li);
    });
}

function displayPrediction(data) {
    if (data.error) {
        console.error('Error in prediction:', data.error);
        return;
    }
    const predictionP = document.getElementById('prediction-result');
    predictionP.innerHTML = `
        Predicted Price: $${data.predicted_price.toFixed(2)}<br>
        Current Price: $${data.current_price.toFixed(2)}<br>
        Trend: ${data.trend}<br>
        Confidence: ${data.confidence.toFixed(2)}%
    `;
}

function displaySentimentChart(sentiment) {
    const ctx = document.getElementById('sentiment-chart').getContext('2d');
    const sentimentData = {
        labels: ['Positive', 'Neutral', 'Negative'],
        datasets: [{
            data: [
                sentiment.positive * 100,
                sentiment.neutral * 100,
                sentiment.negative * 100
            ],
            backgroundColor: ['green', 'gray', 'red']
        }]
    };

    new Chart(ctx, {
        type: 'pie',
        data: sentimentData,
        options: {
            responsive: true
        }
    });
}
