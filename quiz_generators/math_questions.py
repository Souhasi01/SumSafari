# quiz_generators/math_questions.py
from fractions import Fraction
import random

# Addition, Subtraction, Multiplication, Division
def addition_subtraction_multiplication_division():
    a, b = random.randint(1, 5000), random.randint(1, 5000)
    c, d = random.randint(2500, 5000), random.randint(1, 2500)
    e, f = random.randint(1, 5000), random.randint(1, 200)
    g, h = random.randint(1, 8000), random.randint(1, 30)
    
    return [
        {"question": f"{a} + {b} =", "answer": str(a + b), "solution": "Add the two numbers"},
        {"question": f"{c} - {d} =", "answer": str(c - d), "solution": "Subtract the two numbers"},
        {"question": f"{e} * {f} =", "answer": str(e * f), "solution": "Multiply the two numbers"},
        {"question": f"{g} / {h} =", "answer": str(g // h), "solution": "Divide the two numbers (integer division)"},
        {"question": f" After selling {a} mangoes, a fruit seller has {b} left. How many mangoes did he have at first?", "answer": str(a + b), "solution": "Add the sold and remaining mangoes"},
        {"question": f" A shop had {c} books. It sold {d} books. How many books are left?", "answer": str(c - d), "solution": "Subtract the sold books from the total books"},
        {"question": f" If one packet contains {e} biscuits, how many biscuits are there in {f} such packets?", "answer": str(e * f), "solution": "Multiply the number of biscuits per packet by the number of packets"},
        {"question": f" A car travels {g} km in {h} hours. What is its speed in km/h?", "answer": str(g // h), "solution": "Divide distance by time"},
        {"question": f" What is {b} more than {a}?", "answer": str(a + b), "solution": "Add the two numbers"},
        {"question": f" What is {d} less than {c}?", "answer": str(c - d), "solution": "Subtract the second number from the first"}
    ]

# Fractions & Decimals
def fractions_decimals():
     # generate random numerators and denominators
    num1, denom1 = random.randint(1, 9), random.randint(1, 9)
    num2, denom2 = random.randint(1, 9), random.randint(1, 9)

    frac1 = Fraction(num1, denom1)
    frac2 = Fraction(num2, denom2)

    x, y = round(random.uniform(0.1, 1), 2), round(random.uniform(0.1, 1), 2)
    return [
        {"question": f"{x} + {y} =", "answer": str(round(x + y, 2)), "solution": "Add the two decimals"},
        {"question": f"{x + y} - {x} =", "answer": str(y), "solution": "Subtract the first decimal from the sum"},
        {"question": f"{frac1} + {frac2} =", 
         "answer": str(frac1 + frac2), 
         "solution": f"Add the fractions: {frac1} + {frac2} = {frac1 + frac2}"},
        {"question": f"{frac2} - {frac1} =", 
         "answer": str(frac2 - frac1), 
         "solution": f"Subtract the first fraction from the second: {frac2} - {frac1} = {frac2 - frac1}"},
        {"question": f"{frac1} * {frac2} =", 
         "answer": str(frac1 * frac2), 
         "solution": f"Multiply the fractions: {frac1} * {frac2} = {frac1 * frac2}"},
        {"question": f"{frac2} / {frac1} =",
         "answer": str(frac2 / frac1), 
         "solution": f"Divide the fractions: {frac2} / {frac1} = {frac2 / frac1}"},
        {"question": f" Convert {x} to a fraction.", "answer": str(Fraction(x).limit_denominator()), "solution": "Convert decimal to fraction"},
        {"question": f" Convert {frac1} to a decimal.", "answer": str(round(float(frac1), 2)), "solution": "Convert fraction to decimal"},
        {"question": f" What is {x} increased by 25%?", "answer": str(round(x * 1.25, 2)), "solution": "Multiply by 1.25 to increase by 25%"},
        {"question": f" What is {y} decreased by 10%?", "answer": str(round(y * 0.9, 2)), "solution": "Multiply by 0.9 to decrease by 10%"}
    ]

# Length, Perimeter, Area
def length_perimeter_area():
    l, w, b, h = random.randint(1, 100), random.randint(1, 90), random.randint(1, 10), random.randint(1, 10)
    x,y,z = random.randint(1, 100), random.randint(1, 50), random.randint(1, 60)
    a = random.randint(1000, 6000)
    return [
        {"question": f"Perimeter of rectangle {l}x{w}?", "answer": str(2*(l + w)), "solution": "2*(length + width)"},
        {"question": f" A triangle has a perimeter of {x} cm. Two of its sides are of lengths {y} cm and {z} cm respectively. Find the length of the third side.", "answer": str(x - y - z), "solution": "Subtract the known sides from the perimeter"},
        {"question": f". Convert {y} m = _____ cm ", "answer": str(y * 100), "solution": "Multiply meters by 100 to get centimeters"},
        {"question": f"Convert {a} m into kilometres.", "answer": str(a / 1000), "solution": "Divide meters by 1000 to get kilometers"},
        {"question": f"Area of triangle base {b} height {h}?", "answer": str(0.5 * b * h), "solution": "0.5 * base * height"},
        {"question": f"Area of rectangle {l}x{w}?", "answer": str(l * w), "solution": "length * width"},
        {"question": f" A rectangular garden is {l} m long and {w} m wide. What is its area?", "answer": str(l * w), "solution": "length * width"},
        {"question": f" A triangle has a base of {b} cm and a height of {h} cm. What is its area?", "answer": str(0.5 * b * h), "solution": "0.5 * base * height"},
        {"question": f" Convert {z} cm = _____ m ", "answer": str(z / 100), "solution": "Divide centimeters by 100 to get meters"},
        {"question": f"Convert {a} cm into metres.", "answer": str(a / 100), "solution": "Divide centimeters by 100 to get meters"}
    ]

# Patterns, Sequences, Powers
def patterns_sequences_powers():
    start = random.randint(1, 5)
    return [
        {"question": f"Next in sequence: {start}, {start*2}, {start*4}, ?", "answer": str(start*8), "solution": "Multiply by 2 each step"},
        {"question": f"What is {start}^3?", "answer": str(start**3), "solution": f"{start} multiplied by itself 3 times"},
        {"question": f"2, 4, 6, 8, 10, …", "answer": str(12), "solution": f"even numbers increasing by 2"},
        {"question": f"3, 6, 9, 12, 15, …", "answer": str(18), "solution": f"multiples of 3 increasing by 3"},
        {"question": f"1, 3, 5, 7, 9, …", "answer": str(11), "solution": f"odd numbers increasing by 2"},
        {"question": f"What is {start}^4?", "answer": str(start**4), "solution": f"{start} multiplied by itself 4 times"},
        {"question": f"5, 10, 15, 20, 25, …", "answer": str(30), "solution": f"multiples of 5 increasing by 5"},
        {"question": f"10, 20, 30, 40, 50, …", "answer": str(60), "solution": f"multiples of 10 increasing by 10"},
        {"question": f"What is {start}^2?", "answer": str(start**2), "solution": f"{start} multiplied by itself"},
        {"question": f"Next in sequence: {start}, {start+3}, {start+6}, ?", "answer": str(start+9), "solution": "Add 3 each step"}
    ]

# Volume, Speed
def volume_speed():
    side = random.randint(1, 10)
    distance, time, speed = random.randint(20, 100), random.randint(1, 10), random.randint(1, 10)
    return [
        {"question": f"Volume of cube side {side}?", "answer": str(side**3), "solution": "side^3"},
        {"question": f"Find the volume of a cuboid {side+3} cm long, {side+2} cm wide and {side} cm high.", "answer": str(side * (side + 2) * (side + 3)), "solution": "length * width * height"},
        {"question": f" The volume of a plastic container, {side} cm high and {side+3} cm long, is {side * (side + 2) * (side + 3)} cm3. Find its width.", "answer": str(side * (side + 2) * (side + 3) // ((side + 3) * side)), "solution": "Volume / (length * height)"},
        {"question": f"Speed = distance / time. If {distance}km in {time}h?", "answer": str(distance // time), "solution": f"{distance}/{time}"},
        {"question": f"  Emily roller skates at an average speed of {speed} km/h.How far can she travel in {time} hours?", "answer": str(speed * time), "solution": "speed * time"},
        {"question": f" A car travels {distance} km in {time} hours. What is its speed in km/h?", "answer": str(distance // time), "solution": "distance / time"},
        {"question": f" If a cyclist travels at a speed of {speed} km/h, how far will they travel in {time} hours?", "answer": str(speed * time), "solution": "speed * time"},
        {"question": f" Volume of cube side {side+2}?", "answer": str((side + 2)**3), "solution": "(side + 2)^3"},
        {"question": f" Find the volume of a cuboid {side+4} cm long, {side+3} cm wide and {side+2} cm high.", "answer": str((side + 4) * (side + 3) * (side + 2)), "solution": "length * width * height"},
        {"question": f" Speed = distance / time. If {distance+20}km in {time+2}h?", "answer": str((distance + 20) // (time + 2)), "solution": f"{distance + 20}/{time + 2}"}
    ]

# Percentages & Averages
def percentages_averages():
    total_marks, obtained_marks = random.randint(200, 500), random.randint(100, 200)
    num1, num2, num3 = random.randint(10, 50), random.randint(10, 50), random.randint(10, 50)
    num4 = random.randint(120, 200)
    num1, denom1 = random.randint(1, 9), random.randint(1, 9)
    frac1 = Fraction(num1, denom1)
    return [
        {"question": f" What is {obtained_marks} as a percentage of {total_marks}?", "answer": str(round((obtained_marks / total_marks) * 100, 2)), "solution": "(obtained / total) * 100"},
        {"question": f" Find the average of {num1}, {num2}, and {num3}.", "answer": str(round((num1 + num2 + num3) / 3, 2)), "solution": "(num1 + num2 + num3) / 3"},
        {"question": f" A student scored {num1}, {num2}, and {num3} in three subjects. What is his average score?", "answer": str(round((num1 + num2 + num3) / 3, 2)), "solution": "(score1 + score2 + score3) / 3"},
        {"question": f" If a shirt costs Rs {num1} and is sold at a discount of {num2}%, what is the discount amount?", "answer": str(round((num2 / 100) * num1, 2)), "solution": "(discount% / 100) * cost"},
        {"question": f" A shop offers a discount of {num2}% on a jacket that costs Rs {num1}. What is the price after discount?", "answer": str(round(num1 - (num2 / 100) * num1, 2)), "solution": "cost - discount amount"},
        {"question": f" What is {num2}% of {num1}?", "answer": str(round((num2 / 100) * num1, 2)), "solution": "(percentage / 100) * total"},
        {"question": f" Robin eats {frac1} of a cake. What percentage of the cake does he eat?", "answer": str(round(float(frac1) * 100, 2)), "solution": "Convert fraction to decimal and multiply by 100"},
        {"question": f" A student scored {obtained_marks} out of {total_marks}. What is his percentage score?", "answer": str(round((obtained_marks / total_marks) * 100, 2)), "solution": "(obtained / total) * 100"},
        {"question": f" Meera spends an average of Rs {num1} per day during a school week. What is the total amount of money she spends during the week?", "answer": str(round((num1 + num2 + num3 + num4) / 4, 2)), "solution": "(num1 + num2 + num3 + num4) / 4"},
        {"question": f" The average mass of 5 boxes is {num4}. Two boxes have masses {num1} and {num2}. What is the average mass of the remaining 3 boxes?", "answer": str(round((num4 * 5 - num1 - num2) / 3, 2)), "solution": "(average_mass * total_boxes - known_masses) / remaining_boxes"}
        
    ]   

# Ratio & Proportion
def ratio_proportion():
    a, b, c = random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)
    return [
        {"question": f" Simplify the ratio {a*b}:{a*c}.", "answer": f"{b}:{c}", "solution": "Divide both terms by a"},
        {"question": f" If the ratio of boys to girls in a class is {a}:{b} and there are {a+b} students, how many boys are there?", "answer": str(a), "solution": f"Boys = (a / (a + b)) * total_students"},
        {"question": f" If 3 pens cost Rs {a*5}, how much do 7 pens cost?", "answer": str((a*5 // 3) * 7), "solution": "Find cost per pen and multiply by 7"},
        {"question": f" A recipe requires a ratio of flour to sugar of {a}:{b}. If you have {a*2} cups of flour, how much sugar do you need?", "answer": str(b*2), "solution": "Maintain the ratio to find sugar amount"},
        {"question": f" If 5 apples cost Rs {a*10}, how much do 8 apples cost?", "answer": str((a*10 // 5) * 8), "solution": "Find cost per apple and multiply by 8"},
        {"question": f" Simplify the ratio {a*c}:{b*c}.", "answer": f"{a}:{b}", "solution": "Divide both terms by c"},
        {"question": f" If the ratio of cats to dogs in a pet shop is {a}:{b} and there are {a+b} animals, how many dogs are there?", "answer": str(b), "solution": f"Dogs = (b / (a + b)) * total_animals"},
        {"question": f" A recipe requires a ratio of salt to water of {a}:{b}. If you have {b*3} cups of water, how much salt do you need?", "answer": str(a*3), "solution": "Maintain the ratio to find salt amount"},
        {"question": f" If 4 oranges cost Rs {a*8}, how much do 10 oranges cost?", "answer": str((a*8 // 4) * 10), "solution": "Find cost per orange and multiply by 10"},
        {"question": f" If 6 bananas cost Rs {a*12}, how much do 9 bananas cost?", "answer": str((a*12 // 6) * 9), "solution": "Find cost per banana and multiply by 9"}
    ]

# Capacity & Mass
def capacity_mass():
    num1, num2, num3, num4 = random.randint(6, 10), random.randint(1, 100), random.randint(1, 5), random.randint(1, 100)
    num5 = random.randint(1000, 5000)
    return [
        {"question": f"{num5}g = ? kg", "answer": str(num5 // 1000), "solution": "Divide grams by 1000 to get kilograms"},
        {"question": f"{num5}ml = ? l", "answer": str(num5 // 1000), "solution": "Divide milliliters by 1000 to get liters"},
        {"question": f"{num5}cm = ? m", "answer": str(num5 // 100), "solution": "Divide centimeters by 100 to get meters"},
        {"question": f"{num5}mm = ? cm", "answer": str(num5 // 10), "solution": "Divide millimeters by 10 to get centimeters"},
        {"question": f"{num5}mm = ? m", "answer": str(num5 // 1000), "solution": "Divide millimeters by 1000 to get meters"},
        {"question": f"How much oil is left in a barrel containing {num1} L {num2} cl if {num3} L and {num4} cl is taken out from it?", "answer": f"{num1 - num3} L {num2 - num4} cl", "solution": "Subtract the taken out amount from the total"},
        {"question": f"A tank contains {num1} litres and {num2} millilitres of water. If {num3} litres and {num4} millilitres are removed, how much water is left in the tank?", "answer": f"{num1 - num3} litres and {num2 - num4} millilitres", "solution": "Subtract the removed amount from the total"},
        {"question": f"A box filled with fruits has a total mass of {num1} kg {num2} g. If the box itself weighs {num3} kg {num4} g, what is the mass of the fruits?", "answer": f"{num1 - num3} kg {num2 - num4} g", "solution": "Subtract the box weight from the total mass"},
        {"question": f"5000g = ? kg", "answer": "5", "solution": "Divide grams by 1000 to get kilograms"},
        {"question": f"A packet of flour has a mass of {num1} kg {num2} g. What is the total mass of 9 such packets?", "answer": f"{(num1 * 9) + ((num2 * 9) // 1000)} kg {(num2 * 9) % 1000} g", "solution": "Multiply the mass of one packet by 9" }
    ]

# Money & Time
def money_time():
    num1, num2 = random.randint(1, 10), random.randint(1, 10)
    return [
        {"question": f"{num1} hour = ? minutes", "answer": str(num1 * 60), "solution": "Multiply hours by 60 to get minutes"},
        {"question": f"{num1} day = ? hours", "answer": str(num1 * 24), "solution": "Multiply days by 24 to get hours"},
        {"question": f"{num1} week = ? days", "answer": str(num1 * 7), "solution": "Multiply weeks by 7 to get days"},
        {"question": f"{num1} month = ? days", "answer": str(num1 * 30), "solution": "Assume a month has 30 days"},
        {"question": f"{num1} year = ? months", "answer": str(num1 * 12), "solution": "Multiply years by 12 to get months"},
        {"question": f" If a toy costs Rs {num2 * 250} and is sold for Rs {num2 * 300}, what is the profit?", "answer": str(num2 * 50), "solution": f"Selling price - Cost price"},
        {"question": f" A book costs Rs {num2 * 150}. If there is a discount of 10%, what is the discounted price?", "answer": str(num2 * 150 - (num2 * 150 * 0.1)), "solution": "Cost price - (Discount% of Cost price)"},
        {"question": f" If you save Rs {num2 * 200} every month, how much will you save in a year?", "answer": str(num2 * 200 * 12), "solution": "Monthly savings * 12"},
        {"question": f" A watch costs Rs {num2 * 1200}. If it is sold for Rs {num2 * 1000}, what is the loss?", "answer": str(num2 * 1200 - num2 * 1000), "solution": "Cost price - Selling price"},
        {"question": f" If you have Rs {num2 * 500} and spend Rs {num2 * 150}, how much money is left?", "answer": str(num2 * 500 - num2 * 150), "solution": "Total money - Spent money"}
    ]

TOPIC_GENERATORS = {
    1: addition_subtraction_multiplication_division,
    2: fractions_decimals,
    3: length_perimeter_area,
    4: patterns_sequences_powers,
    5: volume_speed,
    6: percentages_averages,
    7: ratio_proportion,
    8: capacity_mass,
    9: money_time,
}

def generate_quiz(topic_code=None, n=10):
    import random

    if topic_code is None:
        generators = TOPIC_GENERATORS.values()
    else:
        generators = [TOPIC_GENERATORS.get(topic_code)]

    questions = []
    for gen in generators:
        if gen:
            questions.extend(gen())

    random.shuffle(questions)
    return questions[:n]
