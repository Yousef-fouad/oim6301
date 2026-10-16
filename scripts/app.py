
import bmi

# Step 1: Create a list of 8 people
# Heights are in centimeters, weights in kilograms

people = [
    {"name": "Alex", "height": 1.75, "weight": 70},
    {"name": "Maya", "height": 1.60, "weight": 50},
    {"name": "Sam", "height": 1.80, "weight": 95},
    {"name": "Lina", "height": 1.65, "weight": 46},
    {"name": "Omar", "height": 1.70, "weight": 102},
    {"name": "Nora", "height": 1.72, "weight": 75},
    {"name": "Ethan", "height": 1.85, "weight": 80},
    {"name": "Chloe", "height": 1.58, "weight": 78}
]

# Step 2: Print each person
for person in people:
    print(person)
    print(person["height"])


# Step 3: Print name and BMI category
for person in people:
    value = bmi.compute_bmi(person["height"], person["weight"])
    category = bmi.classify_bmi(value)

    print(f"{person['name']}: {value:.2f}, {category}")


# Step 4: Count BMI categories
counts = {
    "Underweight": 0,
    "Normal": 0,
    "Overweight": 0,
    "Obese": 0
}

highest_bmi = 0
highest_person = ""

for person in people:
    value = bmi.compute_bmi(person["height"], person["weight"])
    category = bmi.classify_bmi(value)

    counts[category] = counts[category] + 1

    if value > highest_bmi:
        highest_bmi = value
        highest_person = person["name"]

print("Category counts:", counts)
print("Highest BMI:", highest_person, round(highest_bmi, 2))

# Check the total
print("Total counted:", sum(counts.values()))
print("Number of people:", len(people))
