user_height = input("please enter your height(unit: m): ")

user_weight = input("please enter your weight(unit: kg): ")

user_BMI = float(user_weight) / (float(user_height) ** 2)
#BMI = weight / (height ** 2)

print(f"Your BMI is {user_BMI}")

'''
slim: user_BMI < 18.5
normal: 18.5 <= user_BMI < 24
fat: 24 <= user_BMI < 30
very fat: user_BMI >30
'''

if user_BMI < 18.5:
    print("You are pretty slim.")
elif 18.5 <= user_BMI < 24:
    print("You are within normal range.")
elif 24 <= user_BMI < 30:
    print("You are fat.")
else:
    print("Go to gym buddy.")