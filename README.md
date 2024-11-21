# Stock Sentiment Analysis Web Application

## Overview

The **Stock Sentiment Analysis Web Application** is a comprehensive tool that provides real-time stock market insights, sentiment analysis, and stock price predictions based on news headlines. The application allows users to:

- Search for specific stocks and view detailed information.
- View historical stock charts.
- Read related news articles.
- See sentiment analysis results.
- Get next-day stock price predictions.

![Stock Sentiment Analysis App Screenshot](screenshot.png) <!-- Replace with an actual screenshot of your application -->

---

## Features

### 1. Home Page

- **Search Functionality**: Enter a stock ticker symbol (e.g., AAPL, GOOGL) to get detailed information.
- **Current Market Trends**: Displays real-time trends for major indices like Dow Jones, NASDAQ, and S&P 500.
- **Top News Headlines**: Fetches and displays the latest news headlines.

### 2. Stock Details Page

- **Stock Chart**: Interactive line chart of the stock's historical closing prices.
- **Related News Articles**: Recent news headlines related to the selected stock.
- **Sentiment Analysis**: Sentiment analysis on news headlines using FinBERT to determine positive, neutral, and negative sentiments.
- **Stock Prediction**: Predicts the next day's stock closing price using an LSTM neural network model.

### 3. News & Blogs Page

- **Latest Business News**: List of recent business news articles with links to original sources.

---

## Technologies Used

### Backend

- **Python 3.8/3.9**
- **Flask**: Web framework for building the RESTful API.
- **Flask-CORS**: Handling Cross-Origin Resource Sharing (CORS).
- **TensorFlow & Keras**: For building and training the LSTM neural network model.
- **PyTorch & Transformers**: For loading and running the FinBERT model for sentiment analysis.
- **yfinance**: Fetching historical stock data from Yahoo Finance.
- **NewsAPI**: Fetching news articles.
- **scikit-learn**: Data preprocessing and scaling.
- **pandas & NumPy**: Data manipulation and numerical operations.
- **python-dotenv**: Loading environment variables from a `.env` file.

### Frontend

- **HTML5 & CSS3**: Building the structure and style of the web pages.
- **JavaScript (ES6+)**: Implementing interactivity and API calls.
- **Chart.js**: Creating interactive charts.
- **Fetch API**: Making asynchronous HTTP requests to the backend API.

---

## Project Structure

```
StockSentimentAnalysisApp/
├── backend/
│   ├── app.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── sentiment_model.py
│   │   └── stock_model.py
│   ├── saved_model/
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── index.html
│   ├── stock.html
│   ├── news.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── script.js
│       ├── stock.js
│       └── news.js
├── README.md
└── LICENSE
```

---

## Setup Instructions

### Prerequisites

- **Python 3.8 or 3.9**: Ensure you have a compatible Python version installed.
- **Node.js and npm**: Optional, if you prefer using a package manager for frontend dependencies.

### Backend Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/StockSentimentAnalysisApp.git
   ```

2. **Navigate to the Backend Directory**

   ```bash
   cd StockSentimentAnalysisApp/backend
   ```

3. **Create a Virtual Environment (Recommended)**

   ```bash
   python -m venv venv
   ```

   - Activate the virtual environment:

     - On Windows:

       ```bash
       venv\Scripts\activate
       ```

     - On macOS/Linux:

       ```bash
       source venv/bin/activate
       ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   **Contents of `requirements.txt`:**

   ```
   Flask
   flask-cors
   requests
   transformers
   torch
   tensorflow
   yfinance
   numpy
   pandas
   scikit-learn
   python-dotenv
   ```

5. **Set Up Environment Variables**

   - Create a `.env` file in the `backend/` directory.
   - Add your NewsAPI key:

     ```env
     NEWS_API_KEY=your_actual_news_api_key
     ```

     - Replace `your_actual_news_api_key` with your NewsAPI key obtained from [NewsAPI.org](https://newsapi.org/register).

6. **Run the Backend Application**

   ```bash
   python app.py
   ```

   - The backend server will start running at `http://localhost:5000`.

### Frontend Setup

1. **Navigate to the Frontend Directory**

   ```bash
   cd ../frontend
   ```

2. **Serve the Frontend Files**

   - Using Python's HTTP server:

     ```bash
     python -m http.server 8000
     ```

   - Alternatively, use any web server or live server extension in your code editor.

3. **Access the Application**

   - Open your web browser and navigate to:

     ```
     http://localhost:8000/index.html
     ```

---

## Usage Instructions

1. **Home Page**

   - **Search for a Stock**: Enter a stock ticker symbol (e.g., AAPL, GOOGL) in the search bar and click "Search".
   - **View Market Trends**: Check the current market trends for Dow Jones, NASDAQ, and S&P 500.
   - **Read Top News**: Browse the latest top news headlines.

2. **Stock Details Page**

   - **View Stock Chart**: See the historical closing prices of the selected stock in an interactive chart.
   - **Read Related News**: Access recent news articles related to the stock.
   - **Sentiment Analysis**: View the sentiment breakdown (positive, neutral, negative) of the related news.
   - **Stock Prediction**: Check the predicted next-day closing price, trend, and confidence level.

3. **News & Blogs Page**

   - **Browse News Articles**: Explore the latest business news articles.
   - **Read Full Articles**: Click on headlines to read the full articles on their respective websites.

---

## Important Notes

- **API Keys**

  - Replace the placeholder in the `.env` file with your actual NewsAPI key.
  - Ensure your API key is valid and has not exceeded its usage limits.
  - Do not share your API key publicly or commit it to version control.

- **Dependencies**

  - Install all the required Python packages listed in `requirements.txt`.
  - Packages like `transformers` and `torch` are large; ensure you have a stable internet connection.

- **Model Training**

  - The LSTM model is trained on the fly for each stock prediction to improve accuracy.
  - Training may take some time; consider adding a loading indicator in the frontend.
  - The model incorporates sentiment analysis results into the prediction.

- **Python Version Compatibility**

  - Use Python 3.8 or 3.9 for better compatibility with the libraries used.

- **Error Handling**

  - Detailed error logging is included. Check the backend console output if you encounter issues.
  - Common issues may relate to invalid stock symbols or insufficient historical data.

- **Security**

  - Do not expose your API keys in any public repositories.
  - Add the `.env` file to your `.gitignore` file to prevent accidental commits.

---

## Project Structure Details

### Backend Files

- **`app.py`**: The main Flask application file that defines API endpoints.

  - **Key Endpoints:**

    - `/api/market-trends`: Fetches current trends for major indices.
    - `/api/news/<symbol>`: Fetches recent news for a specific stock symbol.
    - `/api/news/top-news`: Fetches top news headlines.
    - `/api/stock-chart/<symbol>`: Fetches stock chart data.
    - `/api/predict/<symbol>`: Predicts stock price trends and confidence levels.

- **`model/`**

  - **`sentiment_model.py`**: Contains the `SentimentModel` class for performing sentiment analysis using FinBERT.
  - **`stock_model.py`**: Contains the `StockModel` class for fetching historical data and predicting stock prices.

- **`saved_model/`**

  - Placeholder for any saved models if you choose to implement model saving.

- **`requirements.txt`**: Lists all the Python dependencies needed for the backend.

- **`.env`**: Contains environment variables like `NEWS_API_KEY`.

### Frontend Files

- **`index.html`**: The home page of the application.

- **`stock.html`**: The stock details page.

- **`news.html`**: The news and blogs page.

- **`css/style.css`**: Contains all the CSS styles for the application.

- **`js/`**

  - **`script.js`**: Handles JavaScript for the home page.
  - **`stock.js`**: Handles JavaScript for the stock details page.
  - **`news.js`**: Handles JavaScript for the news and blogs page.

---

## How to Run the Project

### Step-by-Step Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/StockSentimentAnalysisApp.git
   ```

2. **Set Up the Backend**

   - Navigate to the backend directory:

     ```bash
     cd StockSentimentAnalysisApp/backend
     ```

   - Create and activate a virtual environment:

     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

   - Install dependencies:

     ```bash
     pip install -r requirements.txt
     ```

   - Create a `.env` file and add your NewsAPI key:

     ```env
     NEWS_API_KEY=your_actual_news_api_key
     ```

   - Run the backend application:

     ```bash
     python app.py
     ```

3. **Set Up the Frontend**

   - In a new terminal window, navigate to the frontend directory:

     ```bash
     cd StockSentimentAnalysisApp/frontend
     ```

   - Serve the frontend files:

     ```bash
     python -m http.server 8000
     ```

   - Open your web browser and navigate to:

     ```
     http://localhost:8000/index.html
     ```

4. **Use the Application**

   - Use the search bar to find information about specific stocks.
   - Explore market trends and news articles.
   - View sentiment analysis and stock predictions.

---

## Contact

- **Author**: Your Name
- **Email**: your.email@example.com
- **GitHub**: [yourusername](https://github.com/yourusername)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **FinBERT**: Financial Sentiment Analysis Pretrained Language Model.
- **NewsAPI**: For providing news data.
- **Yahoo Finance**: For providing historical stock data via `yfinance`.
- **Chart.js**: For the charting library used in the frontend.
- **TensorFlow & Keras**: For building and training the LSTM neural network.
- **PyTorch & Transformers**: For loading and running the FinBERT model.

---

## Future Enhancements

- **User Authentication**: Implement user login and registration for personalized experiences.
- **Portfolio Tracking**: Enable users to create and manage a portfolio of stocks.
- **Advanced Analytics**: Incorporate more advanced analytical tools and visualizations.
- **Notifications**: Implement email or SMS notifications for significant market events or stock changes.
- **Deployment**: Deploy the application to a cloud platform for wider accessibility.

---

## Additional Information

### Understanding the Machine Learning Components

#### Sentiment Analysis with FinBERT

- **Model**: `yiyanghkust/finbert-tone` from Hugging Face.
- **Purpose**: Analyze financial news headlines to determine sentiment.
- **Implementation**:
  - Fetch news headlines related to the stock.
  - Use FinBERT to classify each headline as positive, negative, or neutral.
  - Aggregate the results to get overall sentiment scores.

#### Stock Price Prediction with LSTM

- **Model**: Long Short-Term Memory (LSTM) neural network.
- **Purpose**: Predict the next day's closing price of a stock.
- **Features Used**:
  - Closing price (`Close`)
  - Percentage change (`Change`)
  - Volatility (`Volatility`)
  - Volume percentage change (`Volume`)
  - Moving averages (`MA7`, `MA14`, `MA30`)
  - Sentiment score (`Sentiment`)
- **Implementation**:
  - Fetch historical stock data for the specific stock.
  - Preprocess and scale the data.
  - Prepare sequences of past 60 days to use as input.
  - Train the LSTM model on the historical data.
  - Use the trained model to predict the next day's closing price.

---

### Common Issues and Solutions

- **Invalid API Key Error**:
  - Ensure your NewsAPI key is correct and hasn't exceeded rate limits.
- **Model Training Time**:
  - Training may take time; consider adding a loading indicator.
- **Errors During Prediction**:
  - Check backend logs for detailed error messages.
  - Ensure sufficient historical data is available for the stock.

---

**Note**: This README provides all necessary information to understand, set up, and run the Stock Sentiment Analysis Web Application. For any issues or questions, please contact the author.
