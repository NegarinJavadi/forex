import pandas as pd

def BollingerBands(df: pd.DataFrame, n=20, s=2):
    #df_an = df.copy()
    typical_p = ( df['mid-c'] + df['mid-h'] +df['mid-l'] ) / 3
    stddev = typical_p.rolling(window=n).std()
    df['BB_MA'] = typical_p.rolling(window=n).mean()
    df['BB_UP'] = df['BB_MA'] + stddev * s
    df['BB_LW'] = df['BB_MA'] - stddev * s
    return df

def ATR(df: pd.DataFrame, n=14):
    #df_an = df.copy()
    prev_c = df['mid-c'].shift(1)
    tr1 = df['mid-h'] - df['mid-l']
    tr2 = df['mid-h'] - prev_c
    tr3 = prev_c - df['mid-l']
    tr = pd.DataFrame({'tr1':tr1, 'tr2':tr2, 'tr3':tr3}).max(axis=1)
    df[f"ATR_{n}"] = tr.rolling(window=n).mean()
    return df

def KeltnerChannels(df: pd.DataFrame, n_ema=20, n_atr=10):
    #df_an = df.copy()
    df['EMA'] = df['mid-c'].ewm(span=n_ema, min_periods=n_ema).mean()
    df = ATR(df, n=n_atr)
    c_atr = f"ATR_{n_atr}"
    df['KeUp'] = df[c_atr] * 2 + df.EMA
    df['KeLo'] = df.EMA - df[c_atr] * 2
    df.drop(c_atr, inplace=True, axis=1)
    return df

def RSI(df: pd.DataFrame, n=14):
    alpha = 1.0 / n
    gains = df['mid-c'].diff()

    wins = pd.Series([ x if x>=0 else 0.0 for x in gains ], name="wins")
    losses = pd.Series([ x * -1 if x < 0 else 0.0 for x in gains ], name="losses")

    wins_rma = wins.ewm(min_periods=n, alpha=alpha).mean()
    losses_rma = losses.ewm(min_periods=n, alpha=alpha).mean()

    rs = wins_rma / losses_rma

    df[f"RSI_{n}"] = 100.0 - (100.0 / (1 + rs))
    return df

def MACD(df: pd.DataFrame, n_slow=26, n_fast=12, n_signal=9):
    ema_long = df['mid-c'].ewm(min_periods=n_slow, span=n_slow).mean()
    ema_short = df['mid-c'].ewm(min_periods=n_fast, span=n_fast).mean()

    df['MACD'] = ema_short - ema_long
    df['SIGNAL'] = df.MACD.ewm(min_periods=n_signal, span=n_signal).mean()
    df['HIST'] = df.MACD - df.SIGNAL
    
    return df