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
def _():
    as_of = "2026-11-10"
    return


if __name__ == "__main__":
    app.run()
