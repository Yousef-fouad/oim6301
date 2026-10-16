import marimo

__generated_with = "0.24.2"
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

    My fellow students, clubs, committees, and event organizers in Massachusetts, who want to plan outdoor events and activities. My tool helps them decide which day has the best suitable weather for their event and examines the next seven days of weather for their selected town. My tool will also be able to recommend a more suitable day based on variables like temperature, rain probability, and wind speed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    Before writing code, I will open the Open-Meteo API in my browser and examine the response.

    ### My Steps

    Write at least five lines explaining how you plan to solve the problem, in order.

    1. I will use the Open-Meteo API provided to find the coordinates of the towns entered by the user. If several places have the same name, I will match the town to the state to find a match and correctly identify the user's town.

    2. I will use those coordinates to request the weather forecast from the Open-Meteo API for the next seven days, including the day they are asking in. I need the high and low temperature for each day, the chance of rain, and the maximum wind speed.

    3. I will organize the weather data into a list of records, with one record for each day; each record will contain the date and all four weather measurements.

    4. I will compare each day's forecast against the user's weather limits. A day will pass my test only if the high temperature, rain probability, and wind speeds don't exceed their limits.

    5. If multiple days qualify, I will recommend the day that sits on the lowest ends of my limits to break the tie. If no days qualify, I will recommend the day that breaks the fewest limits to break the tie.

    6. I will display a seven-day table showing all weather conditions and whether each day passes my limits. I will also use 'f' to print a sentence explaining why I recommended that day.

    7. I will save the weather records as a JSON or CSV file and check that all seven days were collected.

    8. I will check one of the days' results to ensure accuracy


    ### Functions I Will Need

    Which functions will my tool need? For each function, describe what goes in and what comes out.

    Function 1: get_forecast(place, state)

    Inputs: Town name and state.

    Purpose: Find the town's coordinates, request the weather forecast, and organize the results.

    Output: A list of seven daily weather records, including the selected location.

    Function 2: check_weather(day, limits)

    Inputs: One day's weather record and the allowed weather limits.

    Purpose:It determines the best day that fits my limits.

    Output: Whether the day passes and the number of broken rules.

    Function 3: find_best_day(records, limits)

    Inputs: The weather records and limits.

    Purpose: It compares the days and selects the best one out of my table.

    Output: The recommended day's record.

    ### API Addresses

    Which addresses will my functions request?

    - Geocoding: https://geocoding-api.open-meteo.com/v1/search
    - Forecast: https://api.open-meteo.com/v1/forecast

    ### Checking Completeness

    How will I know that I have collected every required record?

    I will confirm that I collected exactly seven daily records and that the dates and weather measurements correspond to the seven days returned by Open-Meteo.

    ### My Verification Plan

    Which independent check will I use in Section 6?

    I will independently calculate the weather for one day and ensure that it meets all four requirements using the original forecasted data. I will compare the results with a pass/fail output; both results should agree, and I will display the results.
    """)
    return


if __name__ == "__main__":
    app.run()
