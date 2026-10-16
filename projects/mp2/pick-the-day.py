
import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 2 — Pick the Day

    ## 1. The Question

    Who would use this tool, and what decision does it help them make?

    Write two or three sentences in words that someone outside this course would understand.

    **My answer:**

    [Write your answer here.]
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    Before writing code, I will open the Open-Meteo API in my browser and examine the response.

    ### My Steps

    Write at least five lines explaining how you plan to solve the problem, in order.

    1. [Your first step]
    2. [Your second step]
    3. [Your third step]
    4. [Your fourth step]
    5. [Your fifth step]

    ### Functions I Will Need

    Which functions will my tool need? For each function, describe what goes in and what comes out.

    [Write your answer here.]

    ### API Addresses

    Which addresses will my functions request?

    - Geocoding: https://geocoding-api.open-meteo.com/v1/search
    - Forecast: https://api.open-meteo.com/v1/forecast

    ### Checking Completeness

    How will I know that I have collected every required record?

    [Write your answer here.]

    ### My Verification Plan

    Which independent check will I use in Section 6?

    Which two numbers or results should agree?

    [Write your answer here.]
    """)
    return


if __name__ == "__main__":
    app.run()
