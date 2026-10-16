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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every changeable input must be together in one cell at the top of the working code.

    **Option C Inputs:**

    - Town: Wellesley
    - State: Massachusetts
    - Lowest allowed high temperature: 55°F
    - Highest allowed high temperature: 80°F
    - Maximum rain probability: 30%
    - Maximum wind speed: 15 mph

    The inputs will be defined in a Python cell below this section.
    """)
    return


@app.cell
def _():
    place = "Wellesley"
    state = "Massachusetts"

    lowest_high_f = 55
    highest_high_f = 80

    max_rain_chance = 30
    max_wind_mph = 15
    return place, state


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    This section contains the functions and code used to complete the main task.

    **Required tasks:**

    1. Search Open-Meteo for the requested town.
    2. Select the first matching location in the correct state.
    3. Request seven days of weather forecasts.
    4. Collect high temperature, low temperature, rain probability, and maximum wind speed.
    5. Organize the forecast into a list of daily records.
    6. Check each day against all four weather rules.
    7. Select the best day using the assignment's ranking rules.
    8. Save the fetched records to CSV or JSON in projects/mp2/data/.

    At least one function must use requests to fetch data and return a list of records.

    I will use basic Python with functions, lists, dictionaries, loops, and conditions.
    """)
    return


@app.cell
def _(place, state):
    import requests

    def find_coordinates(place, state):
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": place, "count": 100, "country_code": "US"}

        reply = requests.get(url, params=params, timeout=10)
        data = reply.json()

        if "results" not in data:
            return None

        for _town in data["results"]:
            if _town["admin1"] == state:
                return _town["latitude"], _town["longitude"]

        return None

    print(find_coordinates(place, state))
    return find_coordinates, requests


@app.cell
def _(find_coordinates, place, requests, state):
    def get_forecast(place, state):
        coordinates = find_coordinates(place, state)

        if coordinates is None:
            return []

        latitude = coordinates[0]
        longitude = coordinates[1]

        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "America/New_York",
            "forecast_days": 7
        }

        reply = requests.get(url, params=params, timeout=10)
        data = reply.json()

        daily = data["daily"]
        records = []

        for _i in range(len(daily["time"])):
            record = {
                "date": daily["time"][_i],
                "high_f": daily["temperature_2m_max"][_i],
                "low_f": daily["temperature_2m_min"][_i],
                "rain_chance": daily["precipitation_probability_max"][_i],
                "wind_mph": daily["wind_speed_10m_max"][_i]
            }

            records.append(record)

        return records


    weather_records = get_forecast(place, state)

    print("Number of days:", len(weather_records))
    print("First day:", weather_records[0])
    print("Last day:", weather_records[-1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    Display a results table using print() and f-strings, with columns aligned.

    **The table must include:**

    - Date
    - High temperature (°F)
    - Low temperature (°F)
    - Chance of rain (%)
    - Maximum wind speed (mph)
    - Whether the day passes every rule

    **Choosing the best day:**

    - If several days pass, choose the lowest chance of rain.
    - If rain probability is tied, choose the lower wind.
    - If no days pass, choose the day that breaks the fewest rules.
    - If those days are tied, choose the earlier day.
    - A value equal to a weather limit passes.

    Print one clear answer sentence naming the selected location, recommended date, and reason.

    The answer sentence must be generated by Python using an f-string, so it updates when the inputs or forecast change.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    Independently verify at least one result in this notebook.

    A Python verification cell must show both results and demonstrate that they agree.

    **My verification:**

    [Explain which result you checked.]

    **Result from the main program:**

    [Record the first result.]

    **Result from the independent check:**

    [Record the second result.]

    **Do they agree?**

    [Explain what you found.]
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    Choose one piece of AI-generated code that you reviewed.

    **What did the agent suggest?**

    [Write your answer.]

    **What did I change, or how did I verify it?**

    [Write your answer.]

    **How do I know the code works correctly?**

    [Write your answer.]

    **Which cell or GitHub commit demonstrates this?**

    [Identify the cell or commit.]

    If the AI-generated code was correct the first time, explain how you tested and verified it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Reading It Back

    ### Function 1

    **Function name:** [Name]

    **What goes into the function?**

    [Explain the inputs.]

    **What comes out of the function?**

    [Explain the output.]

    **One line I needed to understand:**

    [Identify and explain the line in your own words.]

    ### Function 2

    **Function name:** [Name]

    **What goes into the function?**

    [Explain the inputs.]

    **What comes out of the function?**

    [Explain the output.]

    **One line I needed to understand:**

    [Identify and explain the line in your own words.]

    ### My Prediction

    Choose one change to the tool, such as changing the town or a weather limit.

    **Input I plan to change:**

    [Write your answer.]

    **What I predict will happen:**

    [Write your prediction before making the change.]

    **STOP: Commit and push with the exact message:**

    `mp2: prediction`

    Only after committing and pushing should I change the input and run the notebook again.

    ### What Actually Happened

    [Describe the results after changing the input.]

    **Did the results match my prediction?**

    [Explain why or why not.]
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Going Further

    Attempt at least one task beyond the main assignment.

    **Ideas for Option C:**

    - Compare two or three towns.
    - Compare the forecast against a second weather API.
    - Score each day out of 10 instead of using pass/fail.
    - Allow users to change the weather rules without editing Python code.

    **What I attempted:**

    [Describe the additional task.]

    **How I attempted it:**

    [Explain what you did.]

    **What I found:**

    [Describe the outcome, including any difficulties.]

    **Where can my work be found?**

    [Identify the relevant notebook cell.]

    The attempt counts even if it does not succeed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Time Spent

    Approximate number of hours spent working on this project outside class:

    [Enter one number.]

    This section is not graded.
    """)
    return


if __name__ == "__main__":
    app.run()
