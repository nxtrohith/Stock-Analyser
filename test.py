import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import yfinance as yf
from datetime import date, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class StockComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Comparison Tool")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame for input parameters
        input_frame = ttk.LabelFrame(self.root, text="Input Parameters")
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Stock 1 input
        ttk.Label(input_frame, text="Stock 1 Ticker:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.stock1_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.stock1_var).grid(row=0, column=1, padx=5, pady=5)
        
        # Stock 2 input
        ttk.Label(input_frame, text="Stock 2 Ticker:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.stock2_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.stock2_var).grid(row=1, column=1, padx=5, pady=5)
        
        # Time period input
        ttk.Label(input_frame, text="Days to lookback:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.days_var = tk.StringVar(value="30")
        ttk.Entry(input_frame, textvariable=self.days_var).grid(row=2, column=1, padx=5, pady=5)
        
        # Graph type selection
        ttk.Label(input_frame, text="Graph Type:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.graph_type_var = tk.StringVar(value="Close")
        ttk.Combobox(input_frame, textvariable=self.graph_type_var, 
                    values=["Close", "High", "Low", "Volume", "Adj Close"]).grid(row=3, column=1, padx=5, pady=5)
        
        # PDF filename
        ttk.Label(input_frame, text="PDF Filename:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.pdf_name_var = tk.StringVar(value="stock_comparison.pdf")
        ttk.Entry(input_frame, textvariable=self.pdf_name_var).grid(row=4, column=1, padx=5, pady=5)
        
        # Normalize checkbox
        self.normalize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Normalize Data (for better comparison)", 
                       variable=self.normalize_var).grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=10)
        
        ttk.Button(button_frame, text="Compare Stocks", command=self.compare_stocks).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save to PDF", command=self.save_to_pdf).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_data).pack(side="left", padx=5)
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self.root, text="Graph Preview")
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")
        
        # Store data for later use
        self.stock1_data = None
        self.stock2_data = None
        self.start_date = None
        self.end_date = None
        
        # Set default status
        self.status_var.set("Ready to compare stocks")
        
    def fetch_stock_data(self):
        try:
            stock1 = self.stock1_var.get().strip().upper()
            stock2 = self.stock2_var.get().strip().upper()
            
            if not stock1 or not stock2:
                messagebox.showerror("Input Error", "Please enter both stock tickers")
                return False
                
            days = int(self.days_var.get())
            if days <= 0:
                messagebox.showerror("Input Error", "Days must be a positive integer")
                return False
                
            self.status_var.set(f"Fetching data for {stock1} and {stock2}...")
            self.root.update_idletasks()
            
            # Calculate dates
            self.start_date = (date.today() - timedelta(days=days+4)).strftime("%Y-%m-%d")
            self.end_date = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")
            
            # Download data
            self.stock1_data = yf.download(stock1, self.start_date, self.end_date)
            if self.stock1_data.empty:
                messagebox.showerror("Data Error", f"No data found for ticker {stock1}")
                return False
                
            self.stock2_data = yf.download(stock2, self.start_date, self.end_date)
            if self.stock2_data.empty:
                messagebox.showerror("Data Error", f"No data found for ticker {stock2}")
                return False
                
            self.stock1_data.reset_index(inplace=True)
            self.stock2_data.reset_index(inplace=True)
            
            self.status_var.set(f"Data fetched successfully for {stock1} and {stock2}")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error fetching data")
            return False
    
    def compare_stocks(self):
        if not self.fetch_stock_data():
            return
            
        # Clear preview frame
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
            
        # Create figure and axes
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        stock1 = self.stock1_var.get().strip().upper()
        stock2 = self.stock2_var.get().strip().upper()
        graph_type = self.graph_type_var.get()
        normalize = self.normalize_var.get()
        
        # Prepare data
        if normalize:
            stock1_values = self.stock1_data[graph_type] / self.stock1_data[graph_type].iloc[0] * 100
            stock2_values = self.stock2_data[graph_type] / self.stock2_data[graph_type].iloc[0] * 100
            y_label = f"Normalized {graph_type} Price (%)"
        else:
            stock1_values = self.stock1_data[graph_type]
            stock2_values = self.stock2_data[graph_type]
            y_label = f"{graph_type} Price"
            
        # Plot data
        ax.plot(self.stock1_data['Date'], stock1_values, marker='o', linestyle='-', color='g', label=stock1)
        ax.plot(self.stock2_data['Date'], stock2_values, marker='s', linestyle='-', color='b', label=stock2)
        
        # Add labels and title
        ax.set_title(f'{stock1} vs {stock2} {graph_type} Price Comparison\n{self.start_date} to {self.end_date}')
        ax.set_xlabel('Date')
        ax.set_ylabel(y_label)
        ax.grid(True)
        ax.legend()
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        
        # Add figure to preview frame
        canvas = FigureCanvasTkAgg(fig, master=self.preview_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.status_var.set(f"Comparison complete. Click 'Save to PDF' to export.")
        
    def save_to_pdf(self):
        if self.stock1_data is None or self.stock2_data is None:
            messagebox.showinfo("Information", "Please compare stocks first before saving to PDF.")
            return
            
        try:
            pdf_filename = self.pdf_name_var.get()
            if not pdf_filename.endswith('.pdf'):
                pdf_filename += '.pdf'
                
            stock1 = self.stock1_var.get().strip().upper()
            stock2 = self.stock2_var.get().strip().upper()
            graph_type = self.graph_type_var.get()
            normalize = self.normalize_var.get()
            
            self.status_var.set(f"Creating PDF {pdf_filename}...")
            self.root.update_idletasks()
            
            with PdfPages(pdf_filename) as pdf:
                # Individual stock graphs
                for stock_name, stock_data in [(stock1, self.stock1_data), (stock2, self.stock2_data)]:
                    plt.figure(figsize=(10, 6))
                    plt.plot(stock_data['Date'], stock_data[graph_type], marker='o', linestyle='-', 
                            color='g', label=f'{stock_name} {graph_type} Price')
                    plt.title(f'{stock_name} {graph_type} Price from {self.start_date} to {self.end_date}')
                    plt.xlabel('Date')
                    plt.ylabel(f'{graph_type} Price')
                    plt.grid(True)
                    plt.legend()
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    pdf.savefig()
                    plt.close()
                
                # Comparison graph
                plt.figure(figsize=(10, 6))
                
                if normalize:
                    stock1_values = self.stock1_data[graph_type] / self.stock1_data[graph_type].iloc[0] * 100
                    stock2_values = self.stock2_data[graph_type] / self.stock2_data[graph_type].iloc[0] * 100
                    plt.ylabel(f"Normalized {graph_type} Price (%)")
                else:
                    stock1_values = self.stock1_data[graph_type]
                    stock2_values = self.stock2_data[graph_type]
                    plt.ylabel(f"{graph_type} Price")
                
                plt.plot(self.stock1_data['Date'], stock1_values, marker='o', linestyle='-', 
                        color='g', label=stock1)
                plt.plot(self.stock2_data['Date'], stock2_values, marker='s', linestyle='-', 
                        color='b', label=stock2)
                plt.title(f'{stock1} vs {stock2} {graph_type} Price Comparison\n{self.start_date} to {self.end_date}')
                plt.xlabel('Date')
                plt.grid(True)
                plt.legend()
                plt.xticks(rotation=45)
                plt.tight_layout()
                pdf.savefig()
                plt.close()
                
                # Volume comparison if available
                if graph_type != 'Volume':
                    plt.figure(figsize=(10, 6))
                    
                    if normalize:
                        vol1_values = self.stock1_data['Volume'] / self.stock1_data['Volume'].iloc[0] * 100
                        vol2_values = self.stock2_data['Volume'] / self.stock2_data['Volume'].iloc[0] * 100
                        plt.ylabel("Normalized Trading Volume (%)")
                    else:
                        vol1_values = self.stock1_data['Volume']
                        vol2_values = self.stock2_data['Volume']
                        plt.ylabel("Trading Volume")
                    
                    plt.plot(self.stock1_data['Date'], vol1_values, marker='o', linestyle='-', 
                            color='g', label=f'{stock1} Volume')
                    plt.plot(self.stock2_data['Date'], vol2_values, marker='s', linestyle='-', 
                            color='b', label=f'{stock2} Volume')
                    plt.title(f'{stock1} vs {stock2} Trading Volume Comparison\n{self.start_date} to {self.end_date}')
                    plt.xlabel('Date')
                    plt.grid(True)
                    plt.legend()
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    pdf.savefig()
                    plt.close()
            
            self.status_var.set(f"PDF saved successfully as {pdf_filename}")
            messagebox.showinfo("Success", f"PDF saved successfully as {pdf_filename}")
            
            # Open the PDF if possible
            try:
                os.startfile(pdf_filename)  # Windows
            except:
                try:
                    import subprocess
                    subprocess.call(["xdg-open", pdf_filename])  # Linux
                except:
                    try:
                        subprocess.call(["open", pdf_filename])  # macOS
                    except:
                        pass  # If can't open, just continue
                        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")
            self.status_var.set("Error saving PDF")
    
    def clear_data(self):
        self.stock1_var.set("")
        self.stock2_var.set("")
        self.days_var.set("30")
        self.graph_type_var.set("Close")
        self.pdf_name_var.set("stock_comparison.pdf")
        
        # Clear the preview
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
            
        # Reset data
        self.stock1_data = None
        self.stock2_data = None
        self.start_date = None
        self.end_date = None
        
        self.status_var.set("Ready to compare stocks")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockComparisonApp(root)
    root.mainloop()