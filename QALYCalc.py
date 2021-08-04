import math
import matplotlib.pyplot as plt
import os

# Fields 

yMax  = 100

# Functions

def life_func(year, life_expectancy, quality_percent):
    quality_percent = quality_percent / 100
    max_quality_threshold = 1
    decline_proportion = 5/7

    if (year / life_expectancy) < decline_proportion:
        return max_quality_threshold * quality_percent
    elif year <= life_expectancy:
        b = max_quality_threshold
        a = life_expectancy * (1 - decline_proportion)
        h = decline_proportion * life_expectancy
        y = b * math.sqrt(a**2 - h**2 + 2 * h * year - year **2) / a
        return y * quality_percent
    else:
        return 0

def QALY_analysis(n_helped, pct_helped, pct_now, le_now, le_helped, year_helped, iteration):
    year_min = year_helped
    year_max = max([le_helped, le_now]) + 1
    iterations = 500
    d_year = (year_max - year_min) / iterations

    quality_sum = 0
    X = []
    top = []
    bottom = []

    current_year = 0
    while current_year < year_helped:
        X.append(current_year)
        top.append(life_func(current_year, le_now, pct_now) * 100 * n_helped)
        bottom.append(life_func(current_year, le_now, pct_now)* 100 * n_helped) 
        current_year += d_year

    for i in range(iterations):
        year = year_min + i * d_year
        X.append(year)
        t = life_func(year, le_helped, pct_helped) * n_helped
        b = life_func(year, le_now, pct_now) * n_helped
        top.append(t * 100)
        bottom.append(b * 100)
        quality_change = t - b
        area = d_year * quality_change
        quality_sum += area
    
    plt.figure(iteration)
    plt.plot(X, top, label="Quality of life with Altruistic Act")
    plt.plot(X, bottom, label="Quality of life without Altruistic Act")
    color_str = 'green'
    if quality_sum <= 0:
        color_str = 'red'
    fill_label = "Change in quality of life: %f QUALY's" % (quality_sum * n_helped)
    plt.fill_between(X, top, bottom, color=color_str, label=fill_label, alpha=0.5)

    format_graph(iteration)
    return quality_sum

def format_graph(iteration):
    font = {
        'fontname' :  'Times New Roman'
    }
    plt.grid(color='gray', linestyle='-', linewidth= .5)
    plt.title("Quality of life per Person vs. Time Graph Comparison\nSituation #%d" % iteration, font)
    plt.xlabel("Age (years)", font)
    plt.ylabel("Total Quality of Life (Cumulative %) ", font)
    plt.legend()
    plt.ylim([0, yMax])
    plt.xlim([0, 100])

def show_results(qualys):
    print_title()

    for i in range(len(qualys)):
        print("******************************")
        print("Situation #%s Efficacy: %f QUALYs" % (str(i + 1), qualys[i]))
        print("******************************\n")
    
def print_title():
    print("******************************")
    print("Ethical QALY Altruism Simulator")
    print("Developed by Atticus Rex 2021")
    print("******************************")
    print("\n")

    
def clear_shell():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    running = True
    
    print_title()
    
    

    while running:
        iterations = int(input("How many ethical situations are being compared?\nYour Answer: "))
        n_people = []

        for i in range(iterations):
            clear_shell()
            print_title()
            n_people.append(int(input("\nHow many people are being helped in Situation %d?\nYour Answer: " % (i + 1))))

        global yMax
        yMax = 100 * max(n_people) * 1.05

        qualys = []

        clear_shell()

        for i in range(iterations):
            print_title()

            print("******************************")
            print("Situation #%s" % str(i + 1))
            print("******************************")
            pct_now = float(input("\nWhat is their quality of life percentage currently?\nYour Answer: "))
            pct_helped = float(input("\nWhat would their quality of life\npercentage be after being helped?\nYour Answer: "))
            le_now = float(input("\nWhat is these population's current life expectancy?\nYour Answer: "))
            le_helped = float(input("\nWhat is their life expectancy after being helped?\nYour Answer: "))
            year_helped = float(input("\nHow old are they when they get helped?\nYour Answer: "))

            result = n_people[i] * QALY_analysis(n_people[i], pct_helped, pct_now, le_now, le_helped, year_helped, i + 1)
            qualys.append(result)
            clear_shell()
        
        
        show_results(qualys)



        plt.show()
        
        decision = input("Would you like to test another scenario (y/n): ")
        clear_shell()
        print_title()
        if decision == ("n"):
            running = False



# Main

main()
    