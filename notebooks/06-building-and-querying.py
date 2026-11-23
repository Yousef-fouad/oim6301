# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo[sql]",
#     "duckdb",
#     "polars",
#     "pyarrow",
#     "requests",
# ]
# ///
"""Building and querying a database.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb
    import polars as pl
    import requests

    return duckdb, pl, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Building and Querying a Database

    In this notebook you turn the design from the topic slides into a database: two tables with declared keys, filled from the towns file you saved in notebook 5. Then you ask it questions, the first few of them ones you already know the answer to.

    | | |
    |---|---|
    | ✏️ | Your turn. Add cells with the **+** button |
    | 🚀 | This week's work |

    For a written answer, add a cell under the question, open the cell's **⋯** menu and choose **Convert to Markdown**.

    Every ✏️ is part of this week's work. The **Going further** at the end of an exercise is optional; try it once the rest is done.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Work with your agent the same way as in notebook 5.** Try it yourself first, or write the steps in words. Then ask your agent, ask it to explain any line you could not have written, and ask which concepts its answer used. Do exercise A by hand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. From the Diagram to Tables

    The topic slides split the towns file into two tables, `counties` and `towns`, joined by the county's name. This section builds them.

    **The data.** The counties come from the course API, and the towns from `data/ma-towns.csv`, the file notebook 5 saved. If that file is not there, the cell fetches the towns again.
    """)
    return


@app.cell
def _(mo, pl, requests):
    county_rows = pl.DataFrame(
        requests.get("https://oim.zhili.dev/ma/counties", timeout=10).json()
    )

    town_columns = [
        "name",
        "county",
        "population",
        "income_per_capita_dollars",
        "average_single_family_bill_dollars",
    ]
    _towns_file = mo.notebook_dir().parent / "data" / "ma-towns.csv"
    if _towns_file.exists():
        town_rows = pl.read_csv(_towns_file).select(town_columns)
    else:
        _records = []
        for _county in county_rows["name"]:
            _reply = requests.get(
                "https://oim.zhili.dev/ma/towns",
                params={"county": _county, "per_page": 100},
                timeout=10,
            )
            _records += _reply.json()["items"]
        town_rows = pl.DataFrame(_records).select(town_columns)

    county_rows.shape, town_rows.shape
    return county_rows, town_rows


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The database is a file**, `data/ma-towns.duckdb`. It keeps the tables after this notebook stops, and any program that can read DuckDB can open it.

    Before you run the next cell, open `.gitignore` in the root folder of your repository and add this line, then commit it:

    ```
    *.duckdb*
    ```

    This notebook rebuilds the database from the data every time it runs, so the file itself does not belong in your repository.

    **One cell builds it.** It deletes the old file, opens a new one, creates the tables and loads them, and closes the file when the `with` block ends. Read the two `CREATE TABLE` statements against the diagram:

    - `name` is the **primary key** of each table. A county's name or a town's name names exactly one row, and the database refuses a second row with the same name.
    - `county` in `towns` is a **foreign key**. `REFERENCES counties(name)` makes the database refuse a town whose county is not in `counties`, so `counties` has to be filled first. This rule is called **referential integrity**.
    - `NOT NULL` and `CHECK` are rules about one column. A population has to be there and has to be more than zero.
    - `fips_code` is `UNIQUE`: it is not the key, and still no two counties can share one.
    - `government_abolished_year` has no `NOT NULL`. For the six counties that still have a county government, the year is empty, and that is a real answer.

    The last statement, `CREATE VIEW`, saves a query for later. Section 5 explains it.
    """)
    return


@app.cell
def _(county_rows, duckdb, mo, town_rows):
    _file = mo.notebook_dir().parent / "data" / "ma-towns.duckdb"
    _file.parent.mkdir(exist_ok=True)
    _file.unlink(missing_ok=True)

    with duckdb.connect(_file) as _con:
        _con.register("county_rows", county_rows)
        _con.register("town_rows", town_rows)
        _con.execute("""
            CREATE TABLE counties (
                name                      VARCHAR PRIMARY KEY,
                fips_code                 VARCHAR NOT NULL UNIQUE,
                towns                     INTEGER NOT NULL,
                population                INTEGER NOT NULL CHECK (population > 0),
                founded_year              INTEGER NOT NULL,
                government_abolished_year INTEGER
            )
        """)
        _con.execute("""
            CREATE TABLE towns (
                name                               VARCHAR PRIMARY KEY,
                county                             VARCHAR NOT NULL REFERENCES counties(name),
                population                         INTEGER NOT NULL CHECK (population > 0),
                income_per_capita_dollars          INTEGER,
                average_single_family_bill_dollars INTEGER CHECK (average_single_family_bill_dollars >= 0)
            )
        """)
        _con.execute("""
            INSERT INTO counties
            SELECT name, fips_code, towns, population, founded_year, government_abolished_year
            FROM county_rows
        """)
        _con.execute("INSERT INTO towns SELECT * FROM town_rows")
        _con.execute("""
            CREATE VIEW high_bill_towns_by_county AS
                SELECT county, count(*) AS towns
                FROM towns
                WHERE average_single_family_bill_dollars > 10000
                GROUP BY county
        """)

    database = _file
    database.name
    return (database,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Every other cell asks through `ask`.** It opens the file only to read, runs one query, hands back the result as a table, and closes the file again. Nothing keeps the database open, so you can rebuild it at any time. Your database project's notebooks use the same function.
    """)
    return


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell
def _(ask):
    ask("SELECT (SELECT count(*) FROM counties) AS counties, (SELECT count(*) FROM towns) AS towns")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ A · A Table of Your Own

    **No agent for this one**, and no code completion either. When the editor suggests code in grey as you type, press `Esc` and keep typing your own.

    The course API keeps each town's figures for every year. Open [oim.zhili.dev/ma/towns/317/history](https://oim.zhili.dev/ma/towns/317/history), Wellesley's, in your browser and read what comes back.

    1. Write a `CREATE TABLE` for a table `town_bills`: one row for one town in one fiscal year, with the town's name, the year and the average single-family bill. Make the town's name a foreign key to `towns`.
    2. Choose the primary key, which takes two columns. A key of two columns goes on a line of its own at the end of the table, in the form `PRIMARY KEY (order_id, product_id)`.
    3. Insert two of Wellesley's years by hand.
    4. Run all of it inside `with duckdb.connect(database) as _con:`, in a cell of its own, after the cell that builds the database.

    *Check yourself: inserting the same town and year a second time is refused with `Duplicate key`, and a town that is not in `towns` is refused with `foreign key`.*

    **Going further.** Load every year for one county's towns from the API, and find the town whose bill grew the most over 10 years.
    """)
    return


@app.cell
def _(database, duckdb):


    with duckdb.connect(database) as _con:

        _con.execute("""
            CREATE TABLE IF NOT EXISTS town_bills (
                name VARCHAR NOT NULL REFERENCES towns(name),
                fiscal_year INTEGER NOT NULL,
                average_single_family_bill_dollars INTEGER,
                PRIMARY KEY (name, fiscal_year)
            )
        """)

        _con.execute("""
            INSERT OR IGNORE INTO town_bills
            VALUES ('Wellesley', 2025, 19792)
        """)

        _con.execute("""
            INSERT OR IGNORE INTO town_bills
            VALUES ('Wellesley', 2026, 20551)
        """)
    return


@app.cell
def _(ask):

    ask("""
        SELECT *
        FROM town_bills
        WHERE name = 'Wellesley'
          AND fiscal_year IN (2025, 2026)
        ORDER BY fiscal_year
    """)
    return


@app.cell
def _(ask, database, duckdb, requests):
    response = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"county": "Norfolk", "per_page": 100},
        timeout=20,
    )
    response.raise_for_status()
    norfolk_towns = response.json()["items"]

    # 2. Collect historical bills for every town
    bill_records = []

    for town in norfolk_towns:
        town_code = town.get("dor_code") or town.get("id")

        if town_code is None:
            raise ValueError(f"Missing town code: {town}")

        response = requests.get(
            f"https://oim.zhili.dev/ma/towns/{town_code}/history",
            timeout=20,
        )
        response.raise_for_status()
        history = response.json()

        for year in history["years"]:
            bill = year["average_single_family_bill_dollars"]

            if bill is not None:
                bill_records.append((
                    history["name"],
                    year["fiscal_year"],
                    bill,
                ))

    # 3. Create the table and load the records
    with duckdb.connect(database) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS town_bills (
                name VARCHAR REFERENCES towns(name),
                fiscal_year INTEGER,
                average_single_family_bill_dollars INTEGER,
                PRIMARY KEY (name, fiscal_year)
            )
        """)

        con.executemany("""
            INSERT OR REPLACE INTO town_bills
            VALUES (?, ?, ?)
        """, bill_records)

    # 4. Compare bills from 2016 and 2026
    ask("""
        SELECT
            newer.name,
            older.average_single_family_bill_dollars AS bill_2016,
            newer.average_single_family_bill_dollars AS bill_2026,
            newer.average_single_family_bill_dollars
                - older.average_single_family_bill_dollars
                AS dollar_increase,
            ROUND(
                100.0 * (
                    newer.average_single_family_bill_dollars
                    - older.average_single_family_bill_dollars
                ) / NULLIF(
                    older.average_single_family_bill_dollars, 0
                ),
                2
            ) AS percentage_increase
        FROM town_bills AS older
        JOIN town_bills AS newer
            ON older.name = newer.name
        JOIN towns AS t
            ON t.name = older.name
        WHERE t.county = 'Norfolk'
            AND older.fiscal_year = 2016
            AND newer.fiscal_year = 2026
        ORDER BY dollar_increase DESC
        LIMIT 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. What the Database Refuses

    A constraint checks every row that arrives, without anybody remembering to. Here is a town in a county that does not exist. `try` and `except` catch the refusal, so the rest of the notebook keeps running, and the cell shows the message.
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute("INSERT INTO towns VALUES ('Nowhere', 'Atlantis', 10, 0, 0)")
        refused = "accepted"
    except duckdb.ConstraintException as _error:
        refused = str(_error).splitlines()[0]
    refused
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ B · Breaking the Rules

    Write three inserts into `towns`, each breaking a different rule: a name that is already there, a population of zero, and a county that does not exist. Show the message each one gets.

    *Check yourself: the three messages contain `Duplicate key`, `CHECK constraint failed` and `foreign key`.*

    **Going further.** Find a rule the scenario of your database project states that a constraint cannot hold, and write the query that checks it instead.
    """)
    return


@app.cell
def _(database, duckdb, pl):
    _tests = [
        (
            "Duplicate name",
            ("Wellesley", "Norfolk", 100, 0, 0)
        ),
        (
            "Population of zero",
            ("Test Zero Pop", "Norfolk", 0, 0, 0)
        ),
        (
            "Nonexistent county",
            ("Test Missing County", "Atlantis", 100, 0, 0)
        )
    ]

    constraint_results = []

    for _label, _values in _tests:
        try:
            with duckdb.connect(database) as _con:
                _con.execute("""
                    INSERT INTO towns
                    (name, county, population,
                     income_per_capita_dollars,
                     average_single_family_bill_dollars)
                    VALUES (?, ?, ?, ?, ?)
                """, _values)

            constraint_results.append(
                (_label, "Insert accepted")
            )

        except duckdb.ConstraintException as _error:
            constraint_results.append(
                (_label, str(_error).splitlines()[0])
            )

    pl.DataFrame(
        constraint_results,
        schema=["Test", "Error Message"],
        orient="row"
    )
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            c.name AS county,
            c.towns AS expected_towns,
            COUNT(t.name) AS actual_towns
        FROM counties AS c
        LEFT JOIN towns AS t
            ON c.name = t.county
        GROUP BY c.name, c.towns
        HAVING COUNT(t.name) <> c.towns
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. Asking One Table

    `SELECT` names the columns, `FROM` the table, `WHERE` keeps the rows that pass a condition, `ORDER BY` sorts and `LIMIT` cuts the list short. Read it as a sentence: the towns in Norfolk County, the highest bill first.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT name, population, average_single_family_bill_dollars
        FROM towns
        WHERE county = 'Norfolk'
        ORDER BY average_single_family_bill_dollars DESC
        LIMIT 5
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ C · An Answer You Already Know

    In notebook 5, exercise B found the five towns of more than 50,000 people with the highest average bill, in polars. Ask the database the same question.

    *Check yourself: Brookline, Newton, Cambridge, Somerville, Quincy.*

    **Going further.** Ask the same question of `counties` and `towns` together: which county is each of those five in, and what share of its county's people does each hold? That needs both tables at once, which the topic slides call a join.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            name,
            population,
            average_single_family_bill_dollars
        FROM towns
        WHERE population > 50000
        ORDER BY average_single_family_bill_dollars DESC
        LIMIT 5
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            t.name AS town,
            c.name AS county,
            t.population AS town_population,
            c.population AS county_population,
            ROUND(
                100.0 * t.population / c.population, 2
            ) AS percent_of_county_population,
            t.average_single_family_bill_dollars
        FROM towns AS t
        JOIN counties AS c
            ON t.county = c.name
        WHERE t.population > 50000
        ORDER BY t.average_single_family_bill_dollars DESC
        LIMIT 5
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. `GROUP BY`

    Notebook 5 counted the million-dollar towns in each county in polars, with `.filter()`, `.group_by()` and `.agg()`. The same kind of question in SQL asks how many towns in each county have an average bill over $10,000. `WHERE` is the filter, `GROUP BY` makes one group per county, and `count(*)` counts the rows in each.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT county, count(*) AS towns
        FROM towns
        WHERE average_single_family_bill_dollars > 10000
        GROUP BY county
        ORDER BY towns DESC
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            county,
            COUNT(*) AS town_count,
            SUM(population) AS total_pop, round(avg(population)) AS avg_pop
        FROM towns
        GROUP BY county
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `WHERE` keeps rows before they are grouped. To keep **groups** after they are counted, use `HAVING`: the counties with more than five such towns.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT county, count(*) AS towns
        FROM towns
        WHERE average_single_family_bill_dollars > 10000
        GROUP BY county
        HAVING count(*) > 5
        ORDER BY towns DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ D · A Count You Can Check

    1. Count the towns in each county with `GROUP BY`, and compare each count with the `towns` column of `counties`. *Check yourself: Worcester 60, Middlesex 54, Essex 34, and all 14 agree.*
    2. Add the counts up. Write in a markdown cell why the sum has to equal the number of rows in `towns`. *Check yourself: 351.*
    3. For each county, the total population of its towns, and the share of those people living in towns with a bill over $10,000. Use `sum()` and a `CASE WHEN` inside it, or two queries. *Check yourself: the totals add up to 7,136,171.*

    **Going further.** Answer one question of your own about the towns with `GROUP BY`, and check it in polars on `town_rows`. Or download the TV show database from [Downloads](https://oim6301.github.io/downloads/), keep it out of your repository, and answer the two TV show questions from the topic slides.
    """)
    return


@app.cell
def _(ask):

    ask("""
        SELECT
            c.name AS county,
            c.towns AS expected_towns,
            COUNT(t.name) AS actual_towns,
            CASE
                WHEN c.towns = COUNT(t.name)
                THEN 'Match'
                ELSE 'Mismatch'
            END AS validation
        FROM counties AS c
        LEFT JOIN towns AS t
            ON c.name = t.county
        GROUP BY c.name, c.towns
        ORDER BY actual_towns DESC
    """)

    return


@app.cell
def _(ask):

    ask("""
        SELECT
            (SELECT SUM(towns)
             FROM counties) AS total_county_towns,
            (SELECT COUNT(*)
             FROM towns) AS total_town_rows
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise D — Question 2: Verifying Town Counts

    The sum of the town counts across all 14 counties is 351, which matches the total number of rows in the towns table.

    This equality holds because every town belongs to exactly one county. When towns are grouped by county, each town is counted once, with no duplication or omission.

    The matching totals confirm that the county-level counts reconcile with the overall number of towns in the database.
    """)
    return


@app.cell
def _(ask):

    ask("""
        SELECT
            county,
            SUM(population) AS total_population,
            SUM(
                CASE
                    WHEN average_single_family_bill_dollars > 10000
                    THEN population
                    ELSE 0
                END
            ) AS high_bill_population,
            ROUND(
                100.0 * SUM(
                    CASE
                        WHEN average_single_family_bill_dollars > 10000
                        THEN population
                        ELSE 0
                    END
                ) / SUM(population),
                2
            ) AS high_bill_population_percent
        FROM towns
        GROUP BY county
        ORDER BY county
    """)

    return


@app.cell
def _(ask):

    ask("""
        SELECT
            SUM(population) AS total_population,
            SUM(
                CASE
                    WHEN average_single_family_bill_dollars > 10000
                    THEN population
                    ELSE 0
                END
            ) AS high_bill_population,
            ROUND(
                100.0 * SUM(
                    CASE
                        WHEN average_single_family_bill_dollars > 10000
                        THEN population
                        ELSE 0
                    END
                ) / SUM(population),
                2
            ) AS statewide_high_bill_percent
        FROM towns
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise D — Question 3: Population Analysis

    This analysis calculates each county's total town population
    and the percentage living in towns where the average
    single-family bill exceeds $10,000.

    SUM(population) calculates the total population, while
    CASE WHEN includes only the population of towns meeting
    the bill threshold.

    Dividing the qualifying population by the total population
    gives the percentage for each county.

    The statewide population check should equal 7,136,171,
    confirming that the county populations reconcile with
    the underlying towns data.
    """)
    return


@app.cell
def _(ask):

    ask("""
        SELECT
            county,
            COUNT(*) AS town_count,
            ROUND(
                AVG(average_single_family_bill_dollars), 2
            ) AS average_bill
        FROM towns
        GROUP BY county
        ORDER BY average_bill DESC
    """)

    return


@app.cell
def _(pl, town_rows):
    town_rows.group_by("county").agg(
        pl.len().alias("town_count"),
        pl.col("average_single_family_bill_dollars")
          .mean()
          .round(2)
          .alias("average_bill")
    ).sort("average_bill", descending=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise D — Going Further: Average Bills by County

    This analysis identifies which Massachusetts counties have the highest average single-family bills across their towns.

    The SQL query uses GROUP BY to calculate the number of towns and average bill for each county. The results show that Middlesex has the highest average at $11,327.04, followed by Norfolk at $11,148.46.

    To verify the calculations, I repeated the analysis using Polars on the original town_rows dataset.

    Both methods return the same 14 counties, town counts, and average bills, confirming that the SQL aggregation is consistent with the source data.

    These are unweighted averages across towns, not population-weighted averages.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 5. Views

    A **view** is a query with a name. The cell that builds the database saved the first query of section 4 as `high_bill_towns_by_county`. Asking for it by name runs that query again, on the rows as they are at that moment, so a view stores no rows of its own and is never out of date. Section 4's query listed the counties in order; a view keeps no order, so put the `ORDER BY` in the question you ask of it.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM high_bill_towns_by_county ORDER BY towns DESC")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It returns the same rows as section 4's first query. In your database project, save the question the business asks every week the same way, in the cell that builds your database.

    Full reference: [SQL §28](https://oim6301.github.io/handbooks/sql/04-building-and-loading/#28-views)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ E · Northwind's Orders

    Northwind, the company in the topic slides and the SQL handbook, keeps its 16,282 orders in one file on the course site. The cell below downloads the file to your `data` folder, once, and counts the orders. A query can read a file directly, with the file's path in place of a table name; write each query below the same way, with `orders_file`.
    """)
    return


@app.cell
def _(ask, mo, requests):
    _path = mo.notebook_dir().parent / "data" / "northwind-orders.parquet"
    if not _path.exists():
        _reply = requests.get(
            "https://oim7510.github.io/data/northwind/orders.parquet",
            timeout=30,
        )
        _reply.raise_for_status()
        _path.write_bytes(_reply.content)
    orders_file = _path.as_posix()
    ask(f"SELECT count(*) AS orders FROM '{orders_file}'")
    return (orders_file,)


@app.cell
def _(ask, orders_file):

    ask(f"""
        SELECT
            COUNT(DISTINCT ShipCountry) AS total_countries
        FROM '{orders_file}'
    """)

    return


@app.cell
def _(ask, orders_file):

    ask(f"""
        SELECT
            ShipCountry AS country,
            COUNT(*) AS total_orders,
            ROUND(SUM(Freight), 2) AS total_freight
        FROM '{orders_file}'
        GROUP BY ShipCountry
        ORDER BY total_freight DESC
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise E — Northwind Freight by Country

    The query groups Northwind orders by shipping country
    and calculates the number of orders and total freight
    for each destination.

    COUNT(*) calculates the order count, while SUM(Freight)
    calculates total shipping freight. ORDER BY sorts the
    countries from highest to lowest total freight.

    The USA has the highest total freight at $573,251.00,
    followed by Germany at $537,189.75 and France at
    $442,055.75.

    The results cover 21 shipping countries.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. How many different countries did Northwind ship orders to? Use the column `ShipCountry`. *Check yourself: 21.*
    2. For each country, the number of orders and the total of `Freight`, the most freight first. *Check yourself: USA with 2,328 orders and 573,251 in freight, then Germany with 2,193 and 537,189.75, then France with 1,778 and 442,055.75.*

    **Going further.** Rank the countries by freight per order instead, and see which countries move.
    """)
    return


@app.cell
def _(ask, orders_file):

    ask(f"""
        WITH country_freight AS (
            SELECT
                ShipCountry AS country,
                COUNT(*) AS total_orders,
                SUM(Freight) AS total_freight,
                AVG(Freight) AS freight_per_order
            FROM '{orders_file}'
            GROUP BY ShipCountry
        ),
        ranked_countries AS (
            SELECT
                country,
                total_orders,
                total_freight,
                freight_per_order,
                ROW_NUMBER() OVER (
                    ORDER BY total_freight DESC, country
                ) AS total_freight_rank,
                ROW_NUMBER() OVER (
                    ORDER BY freight_per_order DESC, country
                ) AS freight_per_order_rank
            FROM country_freight
        )
        SELECT
            country,
            total_orders,
            ROUND(total_freight, 2) AS total_freight,
            ROUND(freight_per_order, 2) AS freight_per_order,
            total_freight_rank,
            freight_per_order_rank,
            total_freight_rank - freight_per_order_rank
                AS rank_change
        FROM ranked_countries
        ORDER BY freight_per_order_rank
    """)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise E — Going Further: Freight per Order

    This analysis compares country rankings based on total freight
    and average freight per order.

    Total freight measures the overall shipping costs associated
    with each country, while average freight per order measures
    the shipping cost of a typical order.

    ROW_NUMBER() assigns rankings for both measures. Subtracting
    the average-freight ranking from the total-freight ranking
    shows which countries move up or down.

    A country with many orders may rank highly in total freight
    but lower in average freight per order. Conversely, a country
    with fewer orders may rank higher when comparing freight per
    order rather than total freight.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🚀 This Week's Work

    1. **What is due is listed under *Before next session* in the post-class notes.** I post them on the session page after each class, with the sections we reached, and the checkpoint on Canvas lists the same items.
    2. **[The database project](https://oim6301.github.io/assignments/database-project/)**, Part A, due Sunday 11/08
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Self-check:**

    - [ ] I can turn a diagram into `CREATE TABLE` statements with the keys declared
    - [ ] I can explain what a primary key, a foreign key, `NOT NULL` and `CHECK` each refuse
    - [ ] I can build a database file from data and read it with a function that closes it again
    - [ ] I can ask one table a question with `SELECT`, `WHERE`, `ORDER BY` and `LIMIT`
    - [ ] I can count groups with `GROUP BY`, keep some of them with `HAVING`, and check the counts against a total I know
    - [ ] I can save a query as a view and ask for it by name
    """)
    return


if __name__ == "__main__":
    app.run()
