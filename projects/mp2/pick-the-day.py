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
    return (
        highest_high_f,
        lowest_high_f,
        max_rain_chance,
        max_wind_mph,
        place,
        state,
    )


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
    return (weather_records,)


@app.cell
def _(
    highest_high_f,
    lowest_high_f,
    max_rain_chance,
    max_wind_mph,
    weather_records,
):
    def check_weather(day, limits):
        broken_rules = 0

        if day["high_f"] < limits["lowest_high_f"]:
            broken_rules += 1

        if day["high_f"] > limits["highest_high_f"]:
            broken_rules += 1

        if day["rain_chance"] > limits["max_rain_chance"]:
            broken_rules += 1

        if day["wind_mph"] > limits["max_wind_mph"]:
            broken_rules += 1

        passes = broken_rules == 0

        return passes, broken_rules


    weather_limits = {
        "lowest_high_f": lowest_high_f,
        "highest_high_f": highest_high_f,
        "max_rain_chance": max_rain_chance,
        "max_wind_mph": max_wind_mph
    }

    print(check_weather(weather_records[0], weather_limits))
    return check_weather, weather_limits


@app.cell
def _(check_weather, weather_limits, weather_records):
    def find_best_day(records, limits):
        good_days = []

        for _day in records:
            passes, broken_rules = check_weather(_day, limits)

            if passes:
                good_days.append(_day)

        if len(good_days) > 0:
            best_day = good_days[0]

            for _day in good_days:
                if _day["rain_chance"] < best_day["rain_chance"]:
                    best_day = _day

                elif _day["rain_chance"] == best_day["rain_chance"]:
                    if _day["wind_mph"] < best_day["wind_mph"]:
                        best_day = _day

        else:
            best_day = records[0]
            best_broken = check_weather(best_day, limits)[1]

            for _day in records:
                passes, broken_rules = check_weather(_day, limits)

                if broken_rules < best_broken:
                    best_day = _day
                    best_broken = broken_rules

        return best_day


    recommended_day = find_best_day(weather_records, weather_limits)

    print(recommended_day)
    return (recommended_day,)


@app.cell
def _(check_weather, weather_limits, weather_records):
    for _day in weather_records:
        _passes, _broken = check_weather(_day, weather_limits)
        print(_day["date"], _passes, _day["rain_chance"], _day["wind_mph"])
    return


@app.cell
def _(weather_records):
    import json
    import os

    os.makedirs("projects/mp2/data", exist_ok=True)

    with open("projects/mp2/data/weather_records.json", "w") as _file:
        json.dump(weather_records, _file, indent=4)

    print("Saved", len(weather_records), "weather records.")
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


@app.cell
def _(check_weather, weather_limits, weather_records):
    print(f"{'Date':<12}{'High (F)':>11}{'Low (F)':>11}{'Rain (%)':>11}{'Wind (mph)':>12}{'Pass?':>10}")
    print("-" * 67)

    for _day in weather_records:
        _passes, _broken = check_weather(_day, weather_limits)

        if _passes:
            _status = "Yes"
        else:
            _status = "No"

        print(f"{_day['date']:<12}{_day['high_f']:>11.1f}{_day['low_f']:>11.1f}{_day['rain_chance']:>11}{_day['wind_mph']:>12.1f}{_status:>10}")
    return


@app.cell
def _(check_weather, place, recommended_day, state, weather_limits):
    _best_passes, _best_broken = check_weather(recommended_day, weather_limits)

    if _best_passes:
        print(f"The best day for an outdoor event in {place}, {state} is {recommended_day['date']}, with a high temperature of {recommended_day['high_f']}°F, a {recommended_day['rain_chance']}% chance of rain, and wind speeds of {recommended_day['wind_mph']} mph. It meets all weather requirements and has the best combination of rain probability and wind speed among qualifying days.")
    else:
        print(f"No day meets all weather requirements in {place}, {state}. The best alternative is {recommended_day['date']}, with a high temperature of {recommended_day['high_f']}°F, a {recommended_day['rain_chance']}% chance of rain, and wind speeds of {recommended_day['wind_mph']} mph. It breaks {_best_broken} weather rule(s), the fewest among the seven days.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    Independently verify at least one result in this notebook.

    A Python verification cell must show both results and demonstrate that they agree.

    **My verification:**

    I independently checked whether my recommended day, which is October 19, 2026, satisfied all four limits that were set up. I used a separate if statement to count the broken rules without calling my original function.

    **Result from the main program:**

    0 broken rules.

    **Result from the independent check:**

    0 broken rules.

    **Do they agree?**

    Yes, both methods returned with 0 broken rules. This confirmed my assumption on top and made sure they adhered to my limits.
    """)
    return


@app.cell
def _(
    check_weather,
    highest_high_f,
    lowest_high_f,
    max_rain_chance,
    max_wind_mph,
    recommended_day,
    weather_limits,
):
    # Result from the main function
    main_broken = check_weather(recommended_day, weather_limits)[1]

    # Independent calculation
    independent_broken = 0

    if recommended_day["high_f"] < lowest_high_f:
        independent_broken += 1

    if recommended_day["high_f"] > highest_high_f:
        independent_broken += 1

    if recommended_day["rain_chance"] > max_rain_chance:
        independent_broken += 1

    if recommended_day["wind_mph"] > max_wind_mph:
        independent_broken += 1

    # Compare both results
    print("Main function - broken rules:", main_broken)
    print("Independent check - broken rules:", independent_broken)
    print("Do they agree?", main_broken == independent_broken)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    Choose one piece of AI-generated code that you reviewed.

    **What did the agent suggest?**

    The AI helped create the check_weather() function, which checks if a day meets my limit requirements and counts how many limits the day break.

    **What did I change, or how did I verify it?**

    I tested my fiction using the weather data provided by Open-Meteo. For Oct 16, the function returned false and 1 broken limit. The results matched the measurement.

    **How do I know the code works correctly?**

    In section 6, I independently checked the recommendation code. I used separate if-statements, my original functions returned 0 limits broken, and my independent check returned the name. Python confirmed that both results agreed by displaying True.

    **Which cell or GitHub commit demonstrates this?**

    The check_weather() function in Section 4 and the independent verification cell in Section 6 demonstrate how I tested the AI-generated code.
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
