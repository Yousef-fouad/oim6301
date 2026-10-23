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
    - Maximum rain probability: 5%
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

    max_rain_chance = 5
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

    # Number of days: 7
    # First day: {'date': '2026-10-22', 'high_f': 65.7, 'low_f': 44.2, 'rain_chance': 0, 'wind_mph': 13.7}
    # Last day: {'date': '2026-10-28', 'high_f': 54.7, 'low_f': 39.5, 'rain_chance': 1, 'wind_mph': 5.5}
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

    # (True, 0)

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

    # {'date': '2026-10-25', 'high_f': 65.5, 'low_f': 43.8, 'rain_chance': 0, 'wind_mph': 5.1}

    return (recommended_day,)


@app.cell
def _(check_weather, weather_limits, weather_records):
    for _day in weather_records:
        _passes, _broken = check_weather(_day, weather_limits)
        print(_day["date"], _passes, _day["rain_chance"], _day["wind_mph"])

    #     2026-10-22 True 0 13.7
    # 2026-10-23 False 0 12.4
    # 2026-10-24 True 0 5.2
    # 2026-10-25 True 0 5.1
    # 2026-10-26 True 0 7.2
    # 2026-10-27 True 0 9.1
    # # 2026-10-28 False 1 5.5
    return


@app.cell
def _(weather_records):
    import json
    import os

    os.makedirs("projects/mp2/data", exist_ok=True)

    with open("projects/mp2/data/weather_records.json", "w") as _file:
        json.dump(weather_records, _file, indent=4)

    print("Saved", len(weather_records), "weather records.")
    return json, os


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

    # Date           High (F)    Low (F)   Rain (%)  Wind (mph)     Pass?
    # -------------------------------------------------------------------
    # 2026-10-22         65.7       44.2          0        13.7       Yes
    # 2026-10-23         54.6       37.7          0        12.4        No
    # 2026-10-24         58.4       34.0          0         5.2       Yes
    # 2026-10-25         65.5       43.8          0         5.1       Yes
    # 2026-10-26         69.8       45.6          0         7.2       Yes
    # 2026-10-27         56.4       44.0          0         9.1       Yes
    # 2026-10-28         54.7       39.5          1         5.5        No

    return


@app.cell
def _(check_weather, place, recommended_day, state, weather_limits):
    _best_passes, _best_broken = check_weather(recommended_day, weather_limits)

    if _best_passes:
        print(f"The best day for an outdoor event in {place}, {state} is {recommended_day['date']}, with a high temperature of {recommended_day['high_f']}°F, a {recommended_day['rain_chance']}% chance of rain, and wind speeds of {recommended_day['wind_mph']} mph. It meets all weather requirements and has the best combination of rain probability and wind speed among qualifying days.")
    else:
        print(f"No day meets all weather requirements in {place}, {state}. The best alternative is {recommended_day['date']}, with a high temperature of {recommended_day['high_f']}°F, a {recommended_day['rain_chance']}% chance of rain, and wind speeds of {recommended_day['wind_mph']} mph. It breaks {_best_broken} weather rule(s), the fewest among the seven days.")

        # The best day for an outdoor event in Wellesley, Massachusetts is 2026-10-25, with a high temperature of 65.5°F, a 0% chance of rain, and wind speeds of 5.1 mph. It meets all weather requirements and has the best combination of rain probability and wind speed among qualifying days.

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    Independently verify at least one result in this notebook.

    A Python verification cell must show both results and demonstrate that they agree.

    **My verification:**

    **On October 22, 2026, my program recommended October 25 for an outdoor event in Wellesley, Massachusetts.**

    I independently checked the recommended day using separate if statements to count how many weather requirements it broke, without calling my original function.

    **Result from the main program:**

    0 broken rules.

    **Result from the independent check:**

    0 broken rules.

    **Do they agree?**

    Yes, both methods returned 0 broken rules, and Python displayed True. This confirms that my recommended day, October 25, met all four weather requirements and that my function correctly identifies the number of broken rules.
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

    # Main function - broken rules: 0
    # Independent check - broken rules: 0
    # Do they agree? True
    return independent_broken, main_broken


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    Choose one piece of AI-generated code that you reviewed.

    **What did the agent suggest?**

    The AI helped create the check_weather() function, which checks if a day meets my limit requirements and counts how many limits the day break.

    **What did I change, or how did I verify it?**

    I tested my fuction using the weather data provided by Open-Meteo. For Oct 25, the function returned True and 0 broken limit. The results matched the measurement.

    **How do I know the code works correctly?**

    In Section 6, I independently verified my `check_weather()` function using separate `if` statements. In my latest test, both calculations returned 0 broken rules, and Python displayed `True`. In my earlier October 16 test, the function correctly identified 1 broken rule. These results show that my function works correctly even when the live weather forecast changes.

    **Which cell or GitHub commit demonstrates this?**

    The check_weather() function in Section 4 and the independent verification cell in Section 6 demonstrate how I tested the AI-generated code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Reading It Back

    ### Function 1 — get_forecast(place, state)

    **Inputs:**

    The town name and state.

    **Output:**

    A list containing seven daily weather records, including each day's date, high temperature, low temperature, chance of rain, and maximum wind speed.

    **One line I needed to understand:**

    `for _i in range(len(daily["time"])):`

    This line goes through the dates returned by the API. The variable _i identifies the position of each day, allowing the function to collect the corresponding weather measurements from the different lists.

    ### Function 2 — find_best_day(records, limits)

    **Inputs:**

    A list of weather records and a dictionary containing the weather limits.

    **Output:**

    The record for the best day to hold the outdoor event.

    **One line I needed to understand:**

    `best_broken = check_weather(best_day, limits)[1]`

    The `check_weather()` function returns two values: whether the day passes and the number of rules it breaks. The 1 selects the second value, which tells us how many rules that day breaks.

    ### My Prediction

    **Input I plan to change:**

    I will change the maximum rain chance from 30% to 5% in my Inputs section.

    **What I predict will happen:**

    I expect fewer days to qualify because I am making the rain requirement stricter. Based on my current weather data, I predict that none of the seven days will meet all four requirements.

    I also expect the recommended date to change from October 19 to October 16, 2026. This is because October 16 breaks only one rule and is the earliest date among the days tied for the fewest broken rules.

    I expect the table to show no passing days, and the final recommendation sentence to explain why the alternative day was selected.

    **What actaully Happened**

    After changing the maximum rain chance from 30% to 5%, I ran my program again. My results showed that none of the seven days passed all four weather requirements.

    The recommended day changed from October 19 to October 16, 2026. October 16 had a high temperature of 67.0°F, a 79% chance of rain, and wind speeds of 12.0 mph. It broke one weather rule and was the earliest date among the days tied for the fewest broken rules.

    Did the Results Match My Prediction?

    Yes, my prediction was correct. Lowering the rain limit made the requirements stricter, resulting in no qualifying days. The program selected October 16 as the best alternative, following the rules I programmed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Going Further

    Attempt at least one task beyond the main assignment.


    ### What I Attempted

    I decided to go beyond the pass/fail system by creating a weather scoring system that rates each day out of 10.

    ### How I Attempted It

    I used my existing check_weather() function to count how many weather requirements each day breaks. Every day starts with 10 points, and I subtract 2 points for each broken rule.

    ### What I Found


    This scoring system makes it easier to compare the weather conditions across the seven days. However, I still need to consider rain probability and wind speed to choose the best day when multiple days receive the same score.

    ### Where My Work Is Located

    The Python cell directly under Section 9 — Going Further.
    """)
    return


@app.cell
def _(check_weather, weather_limits, weather_records):
    print("Weather Scores")
    print("-----------------------")

    for _day in weather_records:
        _broken = check_weather(_day, weather_limits)[1]
        _score = 10 - (_broken * 2)

        print(f"{_day['date']}: {_score}/10")
    return


@app.cell
def _(
    check_weather,
    independent_broken,
    json,
    main_broken,
    os,
    place,
    recommended_day,
    state,
    weather_limits,
    weather_records,
):
    os.makedirs("projects/mp2/evidence", exist_ok=True)

    with open("projects/mp2/evidence/weather_records_2026-10-22.json", "w") as _file:
        json.dump(weather_records, _file, indent=4)

    verification_results = {
        "recommended_day": recommended_day,
        "main_function_broken_rules": main_broken,
        "independent_check_broken_rules": independent_broken,
        "agree": main_broken == independent_broken
    }

    with open("projects/mp2/evidence/section6_verification.json", "w") as _file:
        json.dump(verification_results, _file, indent=4)

    going_further_scores = {}
    for _day in weather_records:
        _broken = check_weather(_day, weather_limits)[1]
        going_further_scores[_day["date"]] = 10 - (_broken * 2)

    with open("projects/mp2/evidence/section9_scores.json", "w") as _file:
        json.dump(going_further_scores, _file, indent=4)

    with open("projects/mp2/evidence/program_outputs_2026-10-22.txt", "w") as _file:
        _file.write(f"{'Date':<12}{'High (F)':>11}{'Low (F)':>11}{'Rain (%)':>11}{'Wind (mph)':>12}{'Pass?':>10}\n")
        _file.write("-" * 67 + "\n")
        for _day in weather_records:
            _passes, _broken = check_weather(_day, weather_limits)
            _status = "Yes" if _passes else "No"
            _file.write(f"{_day['date']:<12}{_day['high_f']:>11.1f}{_day['low_f']:>11.1f}{_day['rain_chance']:>11}{_day['wind_mph']:>12.1f}{_status:>10}\n")
        _file.write("\n")
        _file.write(f"The best day for an outdoor event in {place}, {state} is {recommended_day['date']}, with a high temperature of {recommended_day['high_f']}\u00b0F, a {recommended_day['rain_chance']}% chance of rain, and wind speeds of {recommended_day['wind_mph']} mph. It meets all weather requirements and has the best combination of rain probability and wind speed among qualifying days.\n")

    print("Saved evidence files to projects/mp2/evidence/")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Time Spent

    Approximate number of hours spent working on this project outside class:

    [ 8 hours]

    This section is not graded.
    """)
    return


if __name__ == "__main__":
    app.run()
