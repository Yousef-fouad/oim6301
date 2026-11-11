
# The Scenario

**Scenario B — Babson Investment Club**

The Babson Investment Club manages paper portfolios for its members. The club needs a database to track members, portfolios, assets, trades, and historical closing prices.

The database will help the club understand what each portfolio owns, its trading history, and the value of its investments.

# The ERD

```mermaid
erDiagram
    MEMBERS ||--o{ PORTFOLIOS : owns
    PORTFOLIOS ||--o{ TRADES : makes
    ASSETS ||--o{ TRADES : traded_in
    ASSETS ||--o{ CLOSING_PRICES : has
    ASSETS ||--|{ TICKER_HISTORY : uses

    MEMBERS {
        int member_id PK
        string first_name
        string last_name
        string school_email
        int class_year
        date join_date
    }

    PORTFOLIOS {
        int portfolio_id PK
        int member_id FK
        string name
        date created_date
        string strategy
    }

    ASSETS {
        int asset_id PK
        string name
        string asset_type
        string sector
    }

    TICKER_HISTORY {
        int asset_id PK,FK
        date start_date PK
        string ticker
        date end_date
    }

    TRADES {
        int trade_id PK
        int portfolio_id FK
        int asset_id FK
        date trade_date
        string side
        double quantity
        double price_per_unit
        double fee
    }

    CLOSING_PRICES {
        int asset_id PK,FK
        date price_date PK
        double close_price
    }
```

# What One Row Means
- MEMBERS: One row represents one member of the Babson Investment Club and their personal and membership information.

- PORTFOLIOS: One row represents one investment portfolio owned by a club member.

- ASSETS: One row represents one investment asset, such as a stock, ETF, or cryptocurrency.

- TICKER_HISTORY: One row represents the ticker symbol used by an asset during a specific period.

- TRADES: One row represents one transaction in which a portfolio buys or sells an asset.

- CLOSING_PRICES: One row represents the closing price of one asset on a specific date.

# Design Choices
