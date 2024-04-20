from tradingview_ta import TA_Handler, Interval

import time
import sqlite3

try:
    f = open("trackBTC.db", 'a')
except:
    pass


class sqldb:
    def __init__(self, nama_file):
        self.conn = sqlite3.connect(nama_file)
        self.cursor = self.conn.cursor()
        self.buat_table()
    def jalankan(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print("Data Berhasil di input")
        except:
            print("Data Gagal di input")
    def insert(self, buka, rendah, tinggi, volum, rsi):
        query = f"INSERT INTO harga_btc (open, low, high, volume, rsi) VALUES ({buka}, {rendah}, {tinggi}, {volum}, {rsi})"
        self.jalankan(query)
    def buat_table(self):
        query = "CREATE TABLE IF NOT EXISTS harga_btc (id INTEGER PRIMARY KEY, open FLOAT, low FLOAT, high FLOAT, volume FLOAT, rsi FLOAT)"
        self.jalankan(query)


db = sqldb("trackBTC.db")


while True:
    symbol = "BTCUSDT"
    interval = Interval.INTERVAL_1_MINUTE
    handler = TA_Handler()

    handler.set_symbol_as(symbol)
    handler.set_exchange_as_crypto_or_stock("BINANCE")
    handler.set_screener_as_crypto()
    handler.set_interval_as(interval)

    analisys = handler.get_analysis()
    
    buka = analisys.indicators['open']
    rendah = analisys.indicators['low']
    tinggi = analisys.indicators['high']
    volume = analisys.indicators['volume']
    rsi = analisys.indicators['RSI']
    print("Open:", buka)
    print("Low:", rendah)
    print("High:", tinggi)
    print("Volume BTC:", volume)
    print("RSI:", rsi)
    db.insert(buka, rendah, tinggi, volume, rsi)
    time.sleep(60)
    print()