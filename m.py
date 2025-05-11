import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import os
import yfinance as yf
from datetime import datetime, timedelta, date
import sys
from PIL import Image, ImageTk

default_days = 25
# Import your existing functionality
from final import fetch_stock_data, StockPredictor, GraPhs

class StockTrendAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Trend Analyzer")
        self.root.geometry("1077x966")
        self.root.configure(bg="#f4efbb")
        
        # Create directories if they don't exist
        if not os.path.exists("OUTPUTS"):
            os.makedirs("OUTPUTS")
        if not os.path.exists("PREDICTED"):
            os.makedirs("PREDICTED")
        
        self.create_gui()
        
    def create_gui(self):
        # Create frames
        self.input_frame = ttk.LabelFrame(self.root, text="Input Parameters")
        self.input_frame.pack(fill="x", expand=False, padx=10, pady=10)
        
        self.charts_frame = ttk.LabelFrame(self.root, text="Stock Charts")
        self.charts_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.prediction_frame = ttk.LabelFrame(self.root, text="Prediction Results")
        self.prediction_frame.pack(fill="x", expand=False, padx=10, pady=10)
        
        # Input frame widgets
        ttk.Label(self.input_frame, text="Stock Ticker:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ticker_entry = ttk.Entry(self.input_frame, width=10)
        self.ticker_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.input_frame, text="Days to Analyze:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.days_entry = ttk.Entry(self.input_frame, width=5)
        self.days_entry.insert(0, default_days)  # Default value
        self.days_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.input_frame, text="Company Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.company_entry = ttk.Entry(self.input_frame, width=20)
        self.company_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.input_frame, text="Prediction Method:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.prediction_method = ttk.Combobox(self.input_frame, values=["Trend Based", "News Based", "Combined"], width=15)
        self.prediction_method.current(2)  # Default to combined
        self.prediction_method.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        # API Key field (hidden by default)
        ttk.Label(self.input_frame, text="NEWSAPI Key:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.api_key_entry = ttk.Entry(self.input_frame, width=35)
        self.api_key_entry.insert(0, "c9c7b905272e46879386fb61ece03ab4")  # Default from your code
        self.api_key_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Buttons
        self.fetch_button = ttk.Button(self.input_frame, text="Fetch Stock Data", command=self.fetch_data)
        self.fetch_button.grid(row=3, column=0, padx=5, pady=5)
        
        self.predict_button = ttk.Button(self.input_frame, text="Predict Trend", command=self.predict_trend)
        self.predict_button.grid(row=3, column=1, padx=5, pady=5)
        self.predict_button.config(state="disabled")  # Disabled until data is fetched
        
        self.clear_button = ttk.Button(self.input_frame, text="Clear All", command=self.clear_all)
        self.clear_button.grid(row=3, column=2, padx=5, pady=5)
        
        # Charts frame
        self.charts_notebook = ttk.Notebook(self.charts_frame)
        self.charts_notebook.pack(fill="both", expand=True)
        
        # Close price tab
        self.close_tab = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(self.close_tab, text="Close Price")
        
        # Volume tab
        self.volume_tab = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(self.volume_tab, text="Volume")
        
        # High-Low tab
        self.highlow_tab = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(self.highlow_tab, text="High-Low")
        
        # Prediction tab
        self.prediction_tab = ttk.Frame(self.charts_notebook)
        self.charts_notebook.add(self.prediction_tab, text="Prediction")
        
        # Prediction results frame
        self.result_label = ttk.Label(self.prediction_frame, text="No prediction available yet.")
        self.result_label.pack(padx=10, pady=10)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Variables to store data
        self.stock_data = None
        self.trend_prediction = None
        self.prediction_date = None
        
    def fetch_data(self):
        print("Fetching data...")
        try:
            ticker = self.ticker_entry.get().upper()
            if not ticker:
                messagebox.showerror("Error", "Please enter a stock ticker.")
                return
                
            days = int(self.days_entry.get())
            if days < 10:
                messagebox.showerror("Error", "Please enter at least 10 days for reliable analysis.")
                return
                
            self.status_bar.config(text=f"Fetching data for {ticker}...")
            self.root.update()
            
            start = (date.today() - timedelta(days=days+4)).strftime("%Y-%m-%d")
            end = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")
            
            self.stock_data = fetch_stock_data(ticker, start, end)
            print(self.stock_data)
            if self.stock_data is None or self.stock_data.empty:
                messagebox.showerror("Error", f"No data available for {ticker}.")
                return
                
            self.display_charts(ticker)
            self.predict_button.config(state="normal")
            self.status_bar.config(text=f"Data fetched successfully for {ticker}.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_bar.config(text="Error fetching data.")
            
    def display_charts(self, ticker):
        # Clear previous charts
        for widget in self.close_tab.winfo_children():
            widget.destroy()
        for widget in self.volume_tab.winfo_children():
            widget.destroy()
        for widget in self.highlow_tab.winfo_children():
            widget.destroy()

        # Use GraPhs to generate and save the images
        graphs = GraPhs("OUTPUTS", gshow=False)
        graphs.stock_data_close(self.stock_data, ticker)
        graphs.stock_data_volume(self.stock_data, ticker)
        graphs.stock_data_high_low(self.stock_data, ticker)

        # Display saved images in the GUI
        close_img = Image.open(f"OUTPUTS/{ticker}_close_price.png")
        close_photo = ImageTk.PhotoImage(close_img)
        close_label = tk.Label(self.close_tab, image=close_photo)
        close_label.image = close_photo
        close_label.pack(fill=tk.BOTH, expand=True)

        volume_img = Image.open(f"OUTPUTS/{ticker}_volume.png")
        volume_photo = ImageTk.PhotoImage(volume_img)
        volume_label = tk.Label(self.volume_tab, image=volume_photo)
        volume_label.image = volume_photo
        volume_label.pack(fill=tk.BOTH, expand=True)

        highlow_img = Image.open(f"OUTPUTS/{ticker}_high_low.png")
        highlow_photo = ImageTk.PhotoImage(highlow_img)
        highlow_label = tk.Label(self.highlow_tab, image=highlow_photo)
        highlow_label.image = highlow_photo
        highlow_label.pack(fill=tk.BOTH, expand=True)

        
        
    def predict_trend(self):
        try:
            ticker = self.ticker_entry.get().upper()
            days = int(self.days_entry.get())
            company_name = self.company_entry.get()
            api_key = self.api_key_entry.get()
            
            prediction_type = self.prediction_method.current() + 1  # 1-based index
            
            if prediction_type in [2, 3] and not company_name:
                if messagebox.askyesno("Missing Company Name", "News-based prediction requires company name. Continue with just the ticker as the search term?"):
                    company_name = ticker
                else:
                    return
            
            self.status_bar.config(text="Generating prediction...")
            self.root.update()
            
            start = (date.today() - timedelta(days=days+4)).strftime("%Y-%m-%d")
            end = date.today().strftime("%Y-%m-%d")
            
            predictor = StockPredictor(ticker, start, end, api_key, company_name)
            
            if predictor.fetch_data():
                self.trend_prediction, self.prediction_date = predictor.predict(prediction_type=prediction_type)
                
                if self.trend_prediction is None:
                    messagebox.showerror("Error", "Could not generate prediction. Not enough data available.")
                    return
                    
                self.display_prediction(ticker)
                
                # Update result label with prediction details
                result_text = f"Prediction for {ticker} on {self.prediction_date.strftime('%Y-%m-%d')}: {self.trend_prediction}"
                self.result_label.config(text=result_text)
                
                # Switch to prediction tab
                self.charts_notebook.select(self.prediction_tab)
                
                self.status_bar.config(text=f"Prediction completed: {self.trend_prediction}")
            else:
                messagebox.showerror("Error", "Could not generate prediction. Not enough data available.")
                self.status_bar.config(text="Prediction failed.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during prediction: {str(e)}")
            self.status_bar.config(text="Prediction error.")
            
    def display_prediction(self, ticker):
        # Clear previous chart
        for widget in self.prediction_tab.winfo_children():
            widget.destroy()
            
        # Prediction chart
        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot historical data
        ax.plot(self.stock_data.index, self.stock_data['Close'], label=f"{ticker} Historical Close Price", color='blue')
        
        # Find the last date in stock data
        last_close = self.stock_data['Close'].iloc[-1]
        
        # Set color for prediction and calculate predicted price
        if self.trend_prediction == 'Up':
            marker_color = 'green'
            predicted_price = last_close * 1.01  # 1% increase
        else:
            marker_color = 'red'
            predicted_price = last_close * 0.99  # 1% decrease
            
        # Add prediction point
        ax.scatter([self.prediction_date], [predicted_price], color=marker_color, s=100, zorder=5)
        
        # Add annotation
        ax.annotate(f"Predicted: {self.trend_prediction}",
                   xy=(self.prediction_date, predicted_price),
                   xytext=(self.prediction_date - timedelta(days=2), 
                          predicted_price * 1.05 if self.trend_prediction == 'Up' else predicted_price * 0.95),
                   arrowprops=dict(facecolor=marker_color, shrink=0.05),
                   fontsize=10,
                   color=marker_color)
                   
        ax.set_title(f"{ticker} Stock Price with Prediction for {self.prediction_date.strftime('%Y-%m-%d')}")
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.prediction_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def clear_all(self):
        # Clear input fields
        self.ticker_entry.delete(0, tk.END)
        self.days_entry.delete(0, tk.END)
        self.days_entry.insert(0, default_days)
        self.company_entry.delete(0, tk.END)
        self.prediction_method.current(2)
        
        # Clear charts
        for tab in [self.close_tab, self.volume_tab, self.highlow_tab, self.prediction_tab]:
            for widget in tab.winfo_children():
                widget.destroy()
                
        # Reset labels and buttons
        self.result_label.config(text="No prediction available yet.")
        self.predict_button.config(state="disabled")
        
        # Reset variables
        self.stock_data = None
        self.trend_prediction = None
        self.prediction_date = None
        
        self.status_bar.config(text="Ready")

def main():
    root = tk.Tk()
    app = StockTrendAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()