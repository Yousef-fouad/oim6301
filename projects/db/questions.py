import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb

    return duckdb, mo


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell
def _():
    as_of = "2026-11-10"
    return (as_of,)


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. Business Questions

    ## Question 1 — Portfolio Trading Activity

    How many trades did each portfolio make in the last 30 days, and how much money did it spend on purchases and receive from sales?
    """)
    return


@app.cell
def _(as_of, ask):

    ask(f"""
        SELECT
            p.portfolio_id,
            p.name,
            COUNT(t.trade_id) AS number_of_trades,

            ROUND(SUM(
                CASE WHEN t.side = 'buy'
                THEN t.quantity * t.price_per_unit + t.fee
                ELSE 0 END
            ), 2) AS money_spent,

            ROUND(SUM(
                CASE WHEN t.side = 'sell'
                THEN t.quantity * t.price_per_unit - t.fee
                ELSE 0 END
            ), 2) AS money_received

        FROM portfolios p

        LEFT JOIN trades t
            ON p.portfolio_id = t.portfolio_id
            AND t.trade_date BETWEEN
                DATE '{as_of}' - INTERVAL 29 DAY
                AND DATE '{as_of}'

        GROUP BY p.portfolio_id, p.name
        ORDER BY p.portfolio_id
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** During the 30 days ending November 10, 2026, Portfolio 1 made 2 trades and spent $1,240.58 on purchases, while Portfolio 10 made 2 trades and spent $323,788.78. The query also calculates each portfolio's sales proceeds separately, after fees.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2 — Members and Their Portfolios

    How many portfolios does each member own, and what is the total value of investments they have purchased?
    """)
    return


@app.cell
def _(ask):

    ask("""
        SELECT
            m.member_id,
            m.first_name,
            m.last_name,
            COUNT(DISTINCT p.portfolio_id) AS number_of_portfolios,

            ROUND(SUM(
                CASE
                    WHEN t.side = 'buy'
                    THEN t.quantity * t.price_per_unit
                    ELSE 0
                END
            ), 2) AS total_value_bought

        FROM members m

        LEFT JOIN portfolios p
            ON m.member_id = p.member_id

        LEFT JOIN trades t
            ON p.portfolio_id = t.portfolio_id

        GROUP BY m.member_id, m.first_name, m.last_name
        ORDER BY m.member_id
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3 — Current Portfolio Holdings

    As of November 10, 2026, which investments does each portfolio hold, and how many units does it own?
    """)
    return


@app.cell
def _(as_of, ask):

    ask(f"""
        SELECT
            p.portfolio_id,
            p.name AS portfolio_name,
            a.name AS asset_name,

            SUM(
                CASE
                    WHEN t.side = 'buy' THEN t.quantity
                    ELSE -t.quantity
                END
            ) AS units_held

        FROM trades t

        JOIN portfolios p
            ON t.portfolio_id = p.portfolio_id

        JOIN assets a
            ON t.asset_id = a.asset_id

        WHERE t.trade_date <= DATE '{as_of}'

        GROUP BY p.portfolio_id, p.name, a.asset_id, a.name

        HAVING SUM(
            CASE
                WHEN t.side = 'buy' THEN t.quantity
                ELSE -t.quantity
            END
        ) > 0

        ORDER BY p.portfolio_id, a.asset_id
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 4 — Trade Prices vs. Closing Prices

    For every trade in the last 90 days, what was the asset's closing price, and how much did the trade price differ from it as a percentage?
    """)
    return


@app.cell
def _(as_of, ask):

    ask(f"""
        SELECT
            t.trade_id,
            p.name AS portfolio,
            a.name AS asset,
            t.trade_date,
            t.price_per_unit AS trade_price,
            c.close_price,

            ROUND(
                (t.price_per_unit - c.close_price)
                / c.close_price * 100, 2
            ) AS difference_percent

        FROM trades t

        JOIN portfolios p
            ON t.portfolio_id = p.portfolio_id

        JOIN assets a
            ON t.asset_id = a.asset_id

        LEFT JOIN closing_prices c
            ON t.asset_id = c.asset_id
            AND t.trade_date = c.price_date

        WHERE t.trade_date BETWEEN
            DATE '{as_of}' - INTERVAL 89 DAY
            AND DATE '{as_of}'

        ORDER BY t.trade_date, t.trade_id
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 5 — Assets Never Traded

    Which assets does the Investment Club track that have never been bought or sold by any portfolio?
    """)
    return


@app.cell
def _(ask):

    untraded_assets_sql = ask("""
        SELECT
            a.asset_id,
            a.name,
            a.asset_type
        FROM assets a
        LEFT JOIN trades t
            ON a.asset_id = t.asset_id
        WHERE t.trade_id IS NULL
        ORDER BY a.asset_id
    """)
    untraded_assets_sql
    return (untraded_assets_sql,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** The Vanguard Total Bond Market ETF is tracked by the Investment Club but has never been traded by any portfolio.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 6 — Asset Ticker Change

    What was the total value traded for Crescent Analytics over the year, combining trades under its old ticker (CRSA) and new ticker (CRSB)?
    """)
    return


@app.cell
def _(as_of, ask):

    ask(f"""
        SELECT
            a.name AS asset_name,

            ROUND(SUM(
                CASE WHEN h.ticker = 'CRSA'
                THEN t.quantity * t.price_per_unit
                ELSE 0 END
            ), 2) AS old_ticker_value,

            ROUND(SUM(
                CASE WHEN h.ticker = 'CRSB'
                THEN t.quantity * t.price_per_unit
                ELSE 0 END
            ), 2) AS new_ticker_value,

            ROUND(SUM(t.quantity * t.price_per_unit), 2)
                AS total_traded_value

        FROM trades t

        JOIN assets a
            ON t.asset_id = a.asset_id

        JOIN ticker_history h
            ON t.asset_id = h.asset_id
            AND t.trade_date >= h.start_date
            AND (h.end_date IS NULL OR t.trade_date <= h.end_date)

        WHERE a.asset_id = 6
            AND t.trade_date BETWEEN
                DATE '{as_of}' - INTERVAL 364 DAY
                AND DATE '{as_of}'

        GROUP BY a.name
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 7 — Trades Without Closing Prices

    Which trades happened on dates when their assets had no recorded closing price?
    """)
    return


@app.cell
def _(ask):

    ask("""
        SELECT
            t.trade_id,
            p.name AS portfolio,
            a.name AS asset,
            t.trade_date

        FROM trades t

        JOIN portfolios p
            ON t.portfolio_id = p.portfolio_id

        JOIN assets a
            ON t.asset_id = a.asset_id

        LEFT JOIN closing_prices c
            ON t.asset_id = c.asset_id
            AND t.trade_date = c.price_date

        WHERE c.asset_id IS NULL

        ORDER BY t.trade_id
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** Out of 344 trades, 2 violated the closing-price rule. Trades 341 and 342 were made on dates when their assets had no recorded closing prices. These are the two intentional violations created in the dataset.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 8 — Trades That Exceed Available Holdings

    Which sell transactions exceeded the number of units available in their portfolios?
    """)
    return


@app.cell
def _(ask):

    ask("""
        WITH trade_balances AS (
            SELECT
                trade_id,
                portfolio_id,
                asset_id,
                trade_date,
                side,
                quantity,

                SUM(
                    CASE
                        WHEN side = 'buy' THEN quantity
                        ELSE -quantity
                    END
                ) OVER (
                    PARTITION BY portfolio_id, asset_id
                    ORDER BY trade_date, trade_id
                ) AS units_after_trade

            FROM trades
        )

        SELECT
            t.trade_id,
            p.name AS portfolio,
            a.name AS asset,
            t.trade_date,
            t.quantity AS units_sold,
            t.units_after_trade + t.quantity AS units_before_sale

        FROM trade_balances t

        JOIN portfolios p
            ON t.portfolio_id = p.portfolio_id

        JOIN assets a
            ON t.asset_id = a.asset_id

        WHERE t.side = 'sell'
            AND t.units_after_trade < 0

        ORDER BY t.trade_id
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** Two trades violated the rule against overselling. Trades 343 and 344 each sold 50 units of Ethereum despite their respective portfolios having no Ethereum holdings before the transactions. These are the two intentional violations in the dataset.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 9 — Cryptocurrency Exposure

    Which portfolios have the highest cryptocurrency holdings by market value as of November 10, 2026?
    """)
    return


@app.cell
def _(as_of, ask):

    ask(f"""
        SELECT
            p.portfolio_id,
            p.name AS portfolio_name,

            ROUND(SUM(
                CASE
                    WHEN a.asset_type = 'crypto'
                         AND h.units_held > 0
                    THEN h.units_held * c.close_price
                    ELSE 0
                END
            ), 2) AS crypto_market_value

        FROM portfolios p

        LEFT JOIN portfolio_holdings h
            ON p.portfolio_id = h.portfolio_id

        LEFT JOIN assets a
            ON h.asset_id = a.asset_id

        LEFT JOIN closing_prices c
            ON h.asset_id = c.asset_id
            AND c.price_date = DATE '{as_of}'

        GROUP BY p.portfolio_id, p.name

        ORDER BY crypto_market_value DESC, p.portfolio_id
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** As of November 10, 2026, Portfolio 10 has the highest cryptocurrency market value at $1,449,753.25, followed by Portfolio 13 at $1,333,772.99. This helps the Investment Club identify which portfolios have the largest cryptocurrency exposure.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 10 — Trading Fees by Asset Type

    How much has the Investment Club paid in trading fees for stocks, ETFs, and cryptocurrencies over the year?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # How I Know These Numbers Are Right

    ## Check 1 — Trading Fees

    I independently calculated the total trading fees directly from the CSV file using Python and compared the result with Question 10's SQL output.
    """)
    return


@app.cell
def _(as_of, ask):

    fees_by_type = ask(f"""
        SELECT
            a.asset_type,
            COUNT(t.trade_id) AS number_of_trades,
            ROUND(SUM(t.fee), 2) AS total_trading_fees

        FROM trades t

        JOIN assets a
            ON t.asset_id = a.asset_id

        WHERE t.trade_date BETWEEN
            DATE '{as_of}' - INTERVAL 364 DAY
            AND DATE '{as_of}'

        GROUP BY a.asset_type
        ORDER BY total_trading_fees DESC
    """)
    fees_by_type
    return (fees_by_type,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** During the year ending November 10, 2026, stocks generated the highest trading fees at $432 across 167 trades, followed by cryptocurrencies at $211.50 across 100 trades and ETFs at $160.50 across 77 trades. The Investment Club paid a total of $804 in trading fees.
    """)
    return


@app.cell
def _(fees_by_type, mo):
    import csv

    csv_total_fees = 0
    csv_trade_count = 0

    with open(mo.notebook_dir() / "data" / "trades.csv", newline="") as _file:
        _reader = csv.DictReader(_file)

        for _trade in _reader:
            csv_total_fees += float(_trade["fee"])
            csv_trade_count += 1

    csv_total_fees = round(csv_total_fees, 2)

    sql_total_fees = round(sum(fees_by_type["total_trading_fees"]), 2)
    sql_trade_count = sum(fees_by_type["number_of_trades"])

    print("SQL total fees:", sql_total_fees)
    print("CSV total fees:", csv_total_fees)
    print("SQL trade count:", sql_trade_count)
    print("CSV trade count:", csv_trade_count)
    print("Do they agree?", sql_total_fees == csv_total_fees and sql_trade_count == csv_trade_count)

    assert sql_total_fees == csv_total_fees
    assert sql_trade_count == csv_trade_count
    return (csv,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check 2 — Assets Never Traded

    I independently checked Question 5 by comparing the assets in assets.csv against the asset IDs in trades.csv. I used Python to find assets that never appeared in the trading records, then compared that result with my SQL answer.
    """)
    return


@app.cell
def _(csv, mo, untraded_assets_sql):

    # Read all assets
    _assets = {}

    with open(mo.notebook_dir() / "data" / "assets.csv", newline="") as _file:
        for _row in csv.DictReader(_file):
            _assets[_row["asset_id"]] = _row["name"]

    # Find which assets were traded
    _traded_ids = set()

    with open(mo.notebook_dir() / "data" / "trades.csv", newline="") as _file:
        for _row in csv.DictReader(_file):
            _traded_ids.add(_row["asset_id"])

    # Find assets with no trades
    _csv_untraded = []

    for _id in _assets:
        if _id not in _traded_ids:
            _csv_untraded.append(_assets[_id])

    _sql_untraded = list(untraded_assets_sql["name"])

    print("SQL result:", sorted(_sql_untraded))
    print("Python result:", sorted(_csv_untraded))
    print("Do they agree?", sorted(_sql_untraded) == sorted(_csv_untraded))

    assert sorted(_sql_untraded) == sorted(_csv_untraded)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Working With the Agent

    I used AI to help write the SQL queries for my database project. However, I wanted to make sure the results were accurate rather than simply accepting them.

    For Question 10, I independently calculated the trading fees using Python and the original CSV file. Both methods returned $804 in fees across 344 trades.

    I also verified Question 5 using Python to identify assets that were never traded. Both methods identified the Vanguard Total Bond Market ETF.

    These checks confirmed that the SQL queries produced the expected results. The relevant code is in Question 10, Question 5, and the two verification cells under "How I Know These Numbers Are Right."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. Reading It Back

    **Chosen question:** How many portfolios does each club member own, and how much money have they spent buying investments?

    **My prediction before grouping:**
    """)
    return


@app.cell
def _(ask):
    joined_rows = ask("""
        SELECT
            m.member_id,
            p.portfolio_id,
            t.trade_id
        FROM members m
        LEFT JOIN portfolios p
            ON m.member_id = p.member_id
        LEFT JOIN trades t
            ON p.portfolio_id = t.portfolio_id
    """)

    print("Predicted rows:", 347)
    print("Actual rows:", len(joined_rows))
    print("Do they agree?", len(joined_rows) == 347)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Did My Prediction Match?

    Yes, my prediction matched the actual result of 347 rows. There were 344 trades, and the three members without portfolios each added one extra row because I used a LEFT JOIN.

    ### What One Row Means

    One row in the final Question 2 result represents one club member, the number of portfolios they own, and the total value of investments purchased across those portfolios.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. Going Further

    I created a bar chart to compare the trading fees paid for stocks, ETFs, and cryptocurrencies.
    """)
    return


@app.cell
def _(fees_by_type, mo):
    import altair as alt

    fees_chart = mo.ui.altair_chart(
        fees_by_type.plot.bar(
            x=alt.X("asset_type", title="Asset Type"),
            y=alt.Y("total_trading_fees", title="Total Trading Fees ($)")
        ).properties(
            title="Trading Fees by Investment Type"
        )
    )

    fees_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What I Found:**

    Stocks generated the highest trading fees at $432, followed by cryptocurrencies at $211.50 and ETFs at $160.50. The chart makes it easier to compare the trading costs across the three investment types.

    **Where My Work Is Located:**

    The chart is located in Section 4 — Going Further, directly below the ten business questions and verification sections.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 5. Time Spent

    Approximate hours spent working on this project outside class:

    12
    """)
    return


if __name__ == "__main__":
    app.run()
