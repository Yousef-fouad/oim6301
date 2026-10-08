# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *This tool is designed for investors or financial advisors who want to keep their portfolios balanced. Since stock prices change over time, the percentage invested in each stock can move away from the original target. This tool will calculate how many shares need to be bought or sold to get the portfolio closer to its target weights.

    Who? An investor or financial advisor managing a stock portfolio.

    What's the problem? Stock prices change, causing the portfolio percentages to move away from their targets.

    What's the decision? How many shares of each stock should be bought or sold to get closer to the target percentages.

    *
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *First, I will calculate the total value of the portfolio by multiplying the number of shares by their prices and adding the $5,000 cash.

    Next, I will use the target percentages to calculate how much money should be invested in each stock.

    Then, I will divide each target amount by the stock's price to find how many whole shares the investor should own.

    After that, I will compare the current shares with the target shares to determine how many shares need to be bought or sold.

    Finally, I will calculate the remaining cash, find the new percentage of each stock, and print a table showing the results.

    What does my loop carry from one step to the next?

    My loop will go through each stock and keep track of the total portfolio value. I will also use a running calculation to track how much cash remains after buying and selling shares.

    Which check will I use in Section 6, and which two numbers should agree?

    I will calculate the total portfolio value before and after rebalancing. Both values should be the same because buying and selling stocks does not change the total value of the portfolio when there are no trading fees.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    # Your inputs.
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]

    cash = 5000.00

    target_weights = {
        "AAPL": 0.20,
        "MSFT": 0.20,
        "GOOG": 0.15,
        "AMZN": 0.15,
        "NVDA": 0.15,
        "TSLA": 0.15
    }
    return cash, holdings, target_weights


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(cash, holdings):
    total_value = cash

    for stock in holdings:
        stock_value = stock[1] * stock[2]
        total_value = total_value + stock_value

    print(f"Total portfolio value: ${total_value:,.2f}")
    return (total_value,)


@app.cell
def _(holdings, target_weights, total_value):
    target_shares = {}

    for _holding in holdings:
        _ticker = _holding[0]
        _price = _holding[2]
        _target_amount = total_value * target_weights[_ticker]
        _shares = int(_target_amount // _price)

        target_shares[_ticker] = _shares

    print(target_shares)
    return (target_shares,)


@app.cell
def _(holdings, target_shares):
    shares_to_trade = {}

    for _stock in holdings:
        _ticker = _stock[0]
        _current_shares = _stock[1]
        _difference = target_shares[_ticker] - _current_shares

        shares_to_trade[_ticker] = _difference

    print(shares_to_trade)

    return (shares_to_trade,)


@app.cell
def _(cash, holdings, shares_to_trade):
    cash_left = cash

    for _stock in holdings:
        _ticker = _stock[0]
        _price = _stock[2]
        _trade = shares_to_trade[_ticker]

        cash_left = cash_left - (_trade * _price)

    print(f"Cash remaining: ${cash_left:,.2f}")
    return (cash_left,)


@app.cell
def _(holdings, target_shares, target_weights, total_value):
    new_values = {}
    new_weights = {}
    weight_gaps = {}

    for _stock in holdings:
        _ticker = _stock[0]
        _price = _stock[2]
        _shares = target_shares[_ticker]

        _value = _shares * _price
        _weight = _value / total_value
        _gap = (_weight - target_weights[_ticker]) * 100

        new_values[_ticker] = _value
        new_weights[_ticker] = _weight
        weight_gaps[_ticker] = _gap

        print(f"{_ticker}: {_weight * 100:.2f}% (Difference: {_gap:+.2f} points)")
    return new_values, new_weights, weight_gaps


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(
    cash_left,
    holdings,
    new_values,
    new_weights,
    shares_to_trade,
    target_shares,
    weight_gaps,
):
    print(f"{'Ticker':<8} {'Now':>7} {'Target':>8} {'Trade':>8} {'Value After':>15} {'Weight':>9} {'Gap':>10}")
    print("-" * 75)

    for _stock in holdings:
        _ticker = _stock[0]

        print(f"{_ticker:<8} {_stock[1]:>7} {target_shares[_ticker]:>8} {shares_to_trade[_ticker]:>+8} ${new_values[_ticker]:>14,.2f} {new_weights[_ticker]*100:>8.2f}% {weight_gaps[_ticker]:>+9.2f}")

    print("-" * 75)
    print(f"Cash remaining: ${cash_left:,.2f}")
    return


@app.cell
def _():
    # The portfolio can be brought close to its target weights by buying and selling the calculated number of shares, with all six stocks ending within 0.24 percentage points of their targets and $725.62 remaining in cash.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
