import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def calculate_bollinger_bands(data, window=20, num_std=2):
    # Calculate the rolling mean and standard deviation
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()

    # Calculate upper and lower bands
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)

    return upper_band, lower_band

# Example usage
# Assuming 'data' is a DataFrame with a 'Close' column
data['Upper Band'], data['Lower Band'] = calculate_bollinger_bands(data)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['Upper Band'], label='Upper Band')
plt.plot(data['Lower Band'], label='Lower Band')
plt.title('Bollinger Bands')
plt.legend()
plt.show()

def calculate_rsi(data, window=14):
    # Calculate price changes
    delta = data['Close'].diff(1)

    # Calculate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)

    # Calculate average gains and losses
    avg_gains = gains.rolling(window=window, min_periods=1).mean()
    avg_losses = losses.rolling(window=window, min_periods=1).mean()

    # Calculate relative strength (RS)
    rs = avg_gains / avg_losses

    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Example usage
# Assuming 'data' is a DataFrame with a 'Close' column
data['RSI'] = calculate_rsi(data)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(data['RSI'], label='RSI')
plt.axhline(70, color='r', linestyle='--', label='Overbought (70)')
plt.axhline(30, color='g', linestyle='--', label='Oversold (30)')
plt.title('Relative Strength Index (RSI)')
plt.legend()
plt.show()

def moving_average_crossover(data, short_window=50, long_window=200):
    # Calculate short-term and long-term moving averages
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

    # Generate signals
    data['Signal'] = 0
    data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1, 0)

    return data

# Example usage
# Assuming 'data' is a DataFrame with a 'Close' column
data = moving_average_crossover(data)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['Short_MA'], label='Short MA')
plt.plot(data['Long_MA'], label='Long MA')
plt.plot(data[data['Signal'] == 1]['Close'], '^', markersize=10, color='g', label='Buy Signal')
plt.plot(data[data['Signal'] == -1]['Close'], 'v', markersize=10, color='r', label='Sell Signal')
plt.title('Moving Average Crossover')
plt.legend()
plt.show()

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    # Calculate short-term and long-term exponential moving averages
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()

    # Calculate MACD line
    data['MACD'] = short_ema - long_ema

    # Calculate signal line
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()

    return data

# Example usage
# Assuming 'data' is a DataFrame with a 'Close' column
data = calculate_macd(data)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(data['MACD'], label='MACD Line')
plt.plot(data['Signal_Line'], label='Signal Line')
plt.title('MACD (Moving Average Convergence Divergence)')
plt.legend()
plt.show()

def moving_average_envelopes(data, window=20, percent=2):
    # Calculate the central moving average
    data['MA'] = data['Close'].rolling(window=window, min_periods=1).mean()

    # Calculate upper and lower envelopes
    data['Upper_Envelop'] = data['MA'] * (1 + percent / 100)
    data['Lower_Envelop'] = data['MA'] * (1 - percent / 100)

    return data

# Example usage
# Assuming 'data' is a DataFrame with a 'Close' column
data = moving_average_envelopes(data)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['MA'], label='Moving Average')
plt.plot(data['Upper_Envelop'], label='Upper Envelope')
plt.plot(data['Lower_Envelop'], label='Lower Envelope')
plt.title('Moving Average Envelopes')
plt.legend()
plt.show()

def calculate_stochastic_oscillator(data, window=14):
    # Calculate %K and %D
    data['Lowest_Low'] = data['Low'].rolling(window=window).min()
    data['Highest_High'] = data['High'].rolling(window=window).max()

    data['%K'] = ((data['Close'] - data['Lowest_Low']) / (data['Highest_High'] - data['Lowest_Low'])) * 100
    data['%D'] = data['%K'].rolling(window=3).mean()  # 3-period smoothing for %D

    return data

# Example usage
# Assuming 'data' is a DataFrame with 'Low', 'High', and 'Close' columns
data = calculate_stochastic_oscillator(data)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(data['%K'], label='%K')
plt.plot(data['%D'], label='%D')
plt.axhline(80, color='r', linestyle='--', label='Overbought (80)')
plt.axhline(20, color='g', linestyle='--', label='Oversold (20)')
plt.title('Stochastic Oscillator')
plt.legend()
plt.show()

