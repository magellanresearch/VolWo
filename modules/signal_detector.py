def detect_signals(data):
    signals = []
    for ticker, df in data.items():
        df["SMA_20"] = df["Close"].rolling(20).mean()
        df["SMA_50"] = df["Close"].rolling(50).mean()
        crossover = df["SMA_20"] > df["SMA_50"]
        if crossover.iloc[-1]:
            signals.append({"ticker": ticker, "signal": "Bullish SMA crossover"})
    return signals
