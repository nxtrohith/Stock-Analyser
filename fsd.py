import yfinance as yf
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Fetch historical stock data
data = yf.download('JMFINANCIL.BO', start='2025-03-25', end='2025-04-30')
df = data.copy()  # Preserve all columns

# Compute daily returns using 'Close' price
df['return'] = df['Close'].pct_change()

# Create lagged return features (past 5 days)
for i in range(1, 6):
    df[f'return_t-{i}'] = df['return'].shift(i)

# Create target variable: 1 if next day's return is positive, 0 otherwise
df['target'] = (df['return'].shift(-1) > 0).astype(int)

# Drop rows with missing values
df.dropna(inplace=True)

# Define feature columns
feature_cols = [f'return_t-{i}' for i in range(1, 6)]
X = df[feature_cols]
y = df['target']

# Split data into training (80%) and testing (20%) sets
train_size = int(len(df) * 0.8)
X_train = X.iloc[:train_size]
y_train = y.iloc[:train_size]
X_test = X.iloc[train_size:]
y_test = y.iloc[train_size:]

# Train logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')

# Example prediction for the last available day
latest_data = X.iloc[-1:].values
prediction = model.predict(latest_data)
trend = 'Up' if prediction[0] == 1 else 'Down'
print(f'Predicted trend for the next day: {trend}')
