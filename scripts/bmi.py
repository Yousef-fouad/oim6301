
# Classify BMI
def classify_bmi(bmi):
    if bmi >= 30:
        category = "Obese"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 18.5:
        category = "Normal"
    else:
        category = "Underweight"

    return category


# Calculate BMI
def compute_bmi(height, weight):
    height = height / 100
    bmi = weight / (height ** 2)
    return bmi


# Main function
def main():
    height = float(input("Enter your height in centimeters: "))
    weight = float(input("Enter your weight in kilograms: "))

    bmi = compute_bmi(height, weight)
    category = classify_bmi(bmi)

    print(f"Your BMI is {bmi:.2f}, {category}")


main()


