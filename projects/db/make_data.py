
import csv
import random
from pathlib import Path
from datetime import date, timedelta

random.seed(1234)

data_folder = Path(__file__).parent / "data"
data_folder.mkdir(exist_ok=True)

as_of = date(2026, 11, 10)

first_names = ["Adam", "Sarah", "Omar", "Emma", "James",
               "Maya", "Daniel", "Sophia", "Noah", "Layla",
               "Ethan", "Olivia", "Ali", "Chloe", "Ryan"]

last_names = ["Smith", "Johnson", "Hassan", "Brown", "Wilson",
              "Khan", "Davis", "Martin", "Anderson", "Ahmed",
              "Taylor", "Lee", "Patel", "White", "Clark"]

members = []

for _i in range(15):
    member = {
        "member_id": _i + 1,
        "first_name": first_names[_i],
        "last_name": last_names[_i],
        "school_email": f"member{_i + 1}@student.example.edu",
        "class_year": 2026 + (_i % 4),
        "join_date": (as_of - timedelta(days=500 + _i * 10)).isoformat()
    }
    members.append(member)

with open(data_folder / "members.csv", "w", newline="") as _file:
    writer = csv.DictWriter(_file, fieldnames=members[0].keys())
    writer.writeheader()
    writer.writerows(members)

print("Created", len(members), "members.")


portfolios = []

for _i in range(18):
    portfolio = {
        "portfolio_id": _i + 1,
        "member_id": (_i % 12) + 1,
        "name": f"Portfolio {_i + 1}",
        "created_date": (as_of - timedelta(days=375)).isoformat(),
        "strategy": ["Growth", "Value", "Balanced"][_i % 3]
    }

    portfolios.append(portfolio)

with open(data_folder / "portfolios.csv", "w", newline="") as _file:
    writer = csv.DictWriter(_file, fieldnames=portfolios[0].keys())
    writer.writeheader()
    writer.writerows(portfolios)

print("Created", len(portfolios), "portfolios.")

assets = [
    {"asset_id": 1, "name": "Apple", "asset_type": "stock", "sector": "Technology"},
    {"asset_id": 2, "name": "Microsoft", "asset_type": "stock", "sector": "Technology"},
    {"asset_id": 3, "name": "Alphabet", "asset_type": "stock", "sector": "Technology"},
    {"asset_id": 4, "name": "Amazon", "asset_type": "stock", "sector": "Consumer"},
    {"asset_id": 5, "name": "NVIDIA", "asset_type": "stock", "sector": "Technology"},
    {"asset_id": 6, "name": "Crescent Analytics", "asset_type": "stock", "sector": "Technology"},
    {"asset_id": 7, "name": "Vanguard Total Stock Market ETF", "asset_type": "ETF", "sector": "Diversified"},
    {"asset_id": 8, "name": "SPDR S&P 500 ETF", "asset_type": "ETF", "sector": "Diversified"},
    {"asset_id": 9, "name": "Invesco QQQ ETF", "asset_type": "ETF", "sector": "Technology"},
    {"asset_id": 10, "name": "Vanguard Total Bond Market ETF", "asset_type": "ETF", "sector": "Fixed Income"},
    {"asset_id": 11, "name": "Bitcoin", "asset_type": "crypto", "sector": None},
    {"asset_id": 12, "name": "Ethereum", "asset_type": "crypto", "sector": None}
]

with open(data_folder / "assets.csv", "w", newline="") as _file:
    writer = csv.DictWriter(_file, fieldnames=assets[0].keys())
    writer.writeheader()
    writer.writerows(assets)

print("Created", len(assets), "assets.")

ticker_history = []

tickers = {
    1: "AAPL",
    2: "MSFT",
    3: "GOOGL",
    4: "AMZN",
    5: "NVDA",
    7: "VTI",
    8: "SPY",
    9: "QQQ",
    10: "BND",
    11: "BTC",
    12: "ETH"
}

for _asset_id in tickers:
    ticker_history.append({
        "asset_id": _asset_id,
        "start_date": "2025-11-11",
        "ticker": tickers[_asset_id],
        "end_date": ""
    })

# Fictional asset 6 changes ticker during the year
ticker_history.append({
    "asset_id": 6,
    "start_date": "2025-11-11",
    "ticker": "CRSA",
    "end_date": "2026-04-30"
})

ticker_history.append({
    "asset_id": 6,
    "start_date": "2026-05-01",
    "ticker": "CRSB",
    "end_date": ""
})

with open(data_folder / "ticker_history.csv", "w", newline="") as _file:
    writer = csv.DictWriter(_file, fieldnames=ticker_history[0].keys())
    writer.writeheader()
    writer.writerows(ticker_history)

print("Created", len(ticker_history), "ticker history records.")

base_prices = {
    1: 175, 2: 320, 3: 140, 4: 130,
    5: 410, 6: 85, 7: 230, 8: 450,
    9: 370, 10: 72, 11: 65000, 12: 3500
}

closing_prices = []

for _asset in assets:
    _asset_id = _asset["asset_id"]
    _price = base_prices[_asset_id]

    for _i in range(365):
        _day = as_of - timedelta(days=364 - _i)

        if _asset["asset_type"] != "crypto" and _day.weekday() >= 5:
            continue

        if _asset["asset_type"] == "crypto":
            _change = random.uniform(-0.04, 0.04)
        else:
            _change = random.uniform(-0.02, 0.02)

        _price = round(_price * (1 + _change), 2)

        closing_prices.append({
            "asset_id": _asset_id,
            "price_date": _day.isoformat(),
            "close_price": _price
        })

with open(data_folder / "closing_prices.csv", "w", newline="") as _file:
    writer = csv.DictWriter(_file, fieldnames=closing_prices[0].keys())
    writer.writeheader()
    writer.writerows(closing_prices)

print("Created", len(closing_prices), "closing price records.")

# Look up closing prices for each asset and date
price_lookup = {}

for _record in closing_prices:
    _key = (_record["asset_id"], _record["price_date"])
    price_lookup[_key] = _record["close_price"]

trades = []
units_held = {}

# Create 340 normal trades
for _i in range(340):
    _day = as_of - timedelta(days=339 - _i)
    _date = _day.isoformat()
    _portfolio_id = (_i % 18) + 1

    if _day.weekday() >= 5:
        _asset_id = 11
    else:
        _asset_id = ((_i // 18) % 9) + 1

    _key = (_portfolio_id, _asset_id)
    _held = units_held.get(_key, 0)

    if _held > 0 and random.random() < 0.35:
        _side = "sell"
        _quantity = random.randint(1, min(5, _held))
        units_held[_key] = _held - _quantity
    else:
        _side = "buy"
        _quantity = random.randint(2, 8)
        units_held[_key] = _held + _quantity

    _price = price_lookup[(_asset_id, _date)]

    trades.append({
        "trade_id": _i + 1,
        "portfolio_id": _portfolio_id,
        "asset_id": _asset_id,
        "trade_date": _date,
        "side": _side,
        "quantity": _quantity,
        "price_per_unit": round(_price * random.uniform(0.98, 1.02), 2),
        "fee": random.choice([0, 1.50, 5])
    })

# Two trades on days without closing prices
trades.append({
    "trade_id": 341,
    "portfolio_id": 1,
    "asset_id": 1,
    "trade_date": "2026-11-07",
    "side": "buy",
    "quantity": 3,
    "price_per_unit": 200,
    "fee": 0
})

trades.append({
    "trade_id": 342,
    "portfolio_id": 2,
    "asset_id": 2,
    "trade_date": "2026-11-08",
    "side": "buy",
    "quantity": 2,
    "price_per_unit": 350,
    "fee": 0
})

# Two sells that exceed the portfolio's holdings
for _id, _portfolio, _date in [
    (343, 17, "2026-11-09"),
    (344, 18, "2026-11-10")
]:
    trades.append({
        "trade_id": _id,
        "portfolio_id": _portfolio,
        "asset_id": 12,
        "trade_date": _date,
        "side": "sell",
        "quantity": 50,
        "price_per_unit": price_lookup[(12, _date)],
        "fee": 0
    })

with open(data_folder / "trades.csv", "w", newline="") as _file:
    writer = csv.DictWriter(_file, fieldnames=trades[0].keys())
    writer.writeheader()
    writer.writerows(trades)

print("Created", len(trades), "trades.")
print("Missing-price rule violations: 341, 342")
print("Oversell rule violations: 343, 344")
