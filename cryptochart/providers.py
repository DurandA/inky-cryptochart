import requests

def quotes_historical_kraken_ohlc(pair, since, interval=15):
    unix_time = since.strftime("%s")
    payload = {'pair': pair, 'since': unix_time, 'interval': interval}
    r = requests.get('https://api.kraken.com/0/public/OHLC', params=payload)

    def parse_ohlc(data):
        return [[int(l[0]), float(l[1]), float(l[2]), float(l[3]), float(l[4])] for l in data]

    return parse_ohlc(r.json()['result'][pair])
