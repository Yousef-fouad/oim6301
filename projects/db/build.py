import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl

    return duckdb, mo, pl


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, database


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The Tables
    """)
    return


@app.cell
def _(database, duckdb, mo):

    database.unlink(missing_ok=True)

    with duckdb.connect(database) as _con:

        _con.execute("""
            CREATE TABLE members (
                member_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                school_email VARCHAR NOT NULL UNIQUE,
                class_year INTEGER,
                join_date DATE NOT NULL
            )
        """)

        _con.execute("""
            CREATE TABLE portfolios (
                portfolio_id INTEGER PRIMARY KEY,
                member_id INTEGER NOT NULL REFERENCES members(member_id),
                name VARCHAR NOT NULL,
                created_date DATE NOT NULL,
                strategy VARCHAR
            )
        """)

        _con.execute("""
            CREATE TABLE assets (
                asset_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL,
                asset_type VARCHAR NOT NULL
                    CHECK (asset_type IN ('stock', 'ETF', 'crypto')),
                sector VARCHAR,
                CHECK (asset_type != 'crypto' OR sector IS NULL)
            )
        """)

        _con.execute("""
            CREATE TABLE ticker_history (
                asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
                start_date DATE NOT NULL,
                ticker VARCHAR NOT NULL,
                end_date DATE,
                PRIMARY KEY (asset_id, start_date),
                CHECK (end_date IS NULL OR end_date >= start_date)
            )
        """)

        _con.execute("""
            CREATE TABLE closing_prices (
                asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
                price_date DATE NOT NULL,
                close_price DOUBLE NOT NULL CHECK (close_price > 0),
                PRIMARY KEY (asset_id, price_date)
            )
        """)

        _con.execute("""
            CREATE TABLE trades (
                trade_id INTEGER PRIMARY KEY,
                portfolio_id INTEGER NOT NULL REFERENCES portfolios(portfolio_id),
                asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
                trade_date DATE NOT NULL,
                side VARCHAR NOT NULL CHECK (side IN ('buy', 'sell')),
                quantity DOUBLE NOT NULL CHECK (quantity > 0),
                price_per_unit DOUBLE NOT NULL CHECK (price_per_unit > 0),
                fee DOUBLE NOT NULL DEFAULT 0 CHECK (fee >= 0),
                UNIQUE (portfolio_id, asset_id, trade_date)
            )
        """)

        _data_folder = mo.notebook_dir() / "data"

        for _table in [
            "members",
            "portfolios",
            "assets",
            "ticker_history",
            "closing_prices",
            "trades"
        ]:
            _csv = (_data_folder / f"{_table}.csv").as_posix()

            _con.execute(
                f"INSERT INTO {_table} SELECT * FROM read_csv_auto('{_csv}')"
            )

            print("Loaded", _table)
        
        _con.execute("""
            CREATE VIEW portfolio_holdings AS
            SELECT
                portfolio_id,
                asset_id,
                SUM(
                    CASE
                        WHEN side = 'buy' THEN quantity
                        ELSE -quantity
                    END
                ) AS units_held
            FROM trades
            GROUP BY portfolio_id, asset_id
        """)


    print("Created 6 database tables successfully.")


    return


@app.cell
def _(ask):
    for _table in [
        "members",
        "portfolios",
        "assets",
        "ticker_history",
        "closing_prices",
        "trades"
    ]:
        _result = ask(f"SELECT COUNT(*) AS total FROM {_table}")
        print(_table, _result["total"][0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A Look at the Data
    """)
    return


@app.cell
def _(mo, pl):
    _prices = pl.read_csv(
        mo.notebook_dir() / "data" / "closing_prices.csv",
        try_parse_dates=True
    )

    _apple_prices = _prices.filter(pl.col("asset_id") == 1)

    _apple_prices.plot.line(
        x="price_date",
        y="close_price"
    ).properties(
        title="Apple's Simulated Closing Prices Over 12 Months"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The simulated stock prices appear reasonably realistic because they fluctuate throughout the year rather than moving in a straight line. However, these are randomly generated prices and do not represent Apple's actual stock prices.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A Row It Refuses
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO trades (
                    trade_id, portfolio_id, asset_id,
                    trade_date, side, quantity,
                    price_per_unit, fee
                )
                VALUES (
                    99999, 1, 1,
                    '2026-11-10', 'buy', -3,
                    200, 0
                )
            """)

    except Exception as _error:
        print("Database rejected the invalid trade:")
        print(_error)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Answers You Already Knew

    **Question 1:** How many cryptocurrency assets does our club track?

    **My prediction:** 2 assets, Bitcoin and Ethereum.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT COUNT(*) AS crypto_assets
        FROM assets
        WHERE asset_type = 'crypto'
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 2:** How many members are registered in the Babson Investment Club?

    **My prediction:** 15 members, because our data generator created exactly 15 member records.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT COUNT(*) AS total_members
        FROM members
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 3:** How many ticker history records does Crescent Analytics have?

    **My prediction:** 2 records, because Crescent Analytics changed its ticker from CRSA to CRSB during the year.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT COUNT(*) AS ticker_records
        FROM ticker_history
        WHERE asset_id = 6
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT *
        FROM portfolio_holdings
        LIMIT 5
    """)
    return


if __name__ == "__main__":
    app.run()
