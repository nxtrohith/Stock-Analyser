# Stanalazify

**A Machine Learning-based Stock Trend Analyzer using the Latest News and Stock Trends**

## Overview

Stock Analyser is a Python-based project designed to predict stock trends using state-of-the-art machine learning techniques and a user-friendly graphical interface. By leveraging the latest stock market data and news articles, this tool provides insights into stock trend patterns, aiding investors and analysts in making informed decisions.

This project includes a GUI built with `Tkinter`, enabling users to interactively analyze stock trends and visualize results.

## Features

- **News Sentiment Analysis**: Analyzes the latest news to extract sentiment and correlate it with stock trends.
- **Historical Stock Data Analysis**: Utilizes historical stock data to identify patterns and predict future movements.
- **User-friendly GUI**: Built with `Tkinter`, the GUI allows users to fetch stock data, visualize charts, and predict trends with ease.
- **Integrated Charts**: Displays stock close price, volume, and high-low trends using `Matplotlib`.
- **Prediction Methods**:
  - Trend-Based Prediction
  - News-Based Prediction
  - Combined Approach

## Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- Pip (Python Package Manager)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/nxtrohith/Stock-Analyser.git
   cd Stock-Analyser
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python m.py
   ```

## Usage

1. **Launch the Application**: Run the `m.py` script to open the GUI.
2. **Input Stock Ticker**: Enter the stock ticker symbol (e.g., `AAPL` for Apple Inc.).
3. **Choose Analysis Parameters**:
   - Specify the number of days for analysis (default is 25).
   - Select the prediction method (Trend-Based, News-Based, or Combined).
   - Optionally, provide a company name for news-based predictions.
4. **Fetch Data**: Click "Fetch Stock Data" to retrieve historical stock data.
5. **Predict Trends**: Once data is fetched, click "Predict Trend" to generate predictions.
6. **Visualize Results**: View charts and prediction outcomes in the GUI.

## Project Structure

```
Stock-Analyser/
├── OUTPUTS/              # Stores generated charts for stock data
├── PREDICTED/            # Stores prediction-related outputs
├── data/                 # Contains historical stock data and news datasets
├── models/               # Machine learning models for trend prediction
├── scripts/              # Helper scripts for data processing
├── m.py                  # Main script for the Stock Analyser GUI
├── final.py              # Core functionality for fetching data and predictions
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Technologies

- **Programming Language**: Python
- **Libraries**:
  - `Tkinter`: For the graphical user interface (GUI)
  - `Matplotlib`: For visualizing stock trends
  - `Pandas` and `NumPy`: For data processing
  - `yFinance`: For fetching historical stock data
  - `Pillow`: For image processing in the GUI
  - `NewsAPI`: For fetching the latest news articles

## Future Enhancements

- Integration with real-time data streams for live predictions.
- Advanced machine learning models for more accurate predictions.
- A web-based dashboard for broader accessibility.
- Multi-language support for news analysis.

## Contributions

Contributions are welcome! If you have suggestions for improvements or new features, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Thanks to [NewsAPI](https://newsapi.org/) and [Yahoo Finance](https://finance.yahoo.com/) for providing data APIs.
- Inspired by the need for smarter tools in stock trend analysis.

---

Let me know if you'd like me to assist with adding this README directly to your repository or if you need further modifications!`
