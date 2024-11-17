from tabulate import tabulate, SEPARATING_LINE
import sys
import requests
import random
import os
import inflect
import textwrap
import shutil


BASE = []
ALLBASE = []


#To create a country and store data about it
class Country:
    def __init__(self, name, population, area, region, timezones):
        self._name = name
        self._population = population
        self._area = area
        self._region = region
        self._timezones = timezones

    @property
    def name(self):
        return self._name

    @property
    def population(self):
        return self._population

    @property
    def area(self):
        return self._area

    @property
    def region(self):
        return self._region

    @property
    def timezone(self):
        return self._timezones


#To start the program
def main():
    menu()


#Main menu for selecting actions
def menu():
    clear()
    #Action selection table
    headers = ["COUNTRY GUESSER"]
    table = [
        ["START             1"],
        SEPARATING_LINE,
        ["HELP              2"],
        ["ABOUT             3"],
        ["QUIT              4"]]
    print(tabulate(table, headers, tablefmt="simple"))

    #Controls the selection in the table
    try:
        i = choose(1, 4)
    except EOFError:
        end()
    match i:
        case 1:
            clear()
            get_group()
            game()
        case 2:
            clear()
            help()
        case 3:
            clear()
            about()
        case 4:
            clear()
            end()


#Collects the appropriate data to call the add() function
def get_level(lvl: int):

    #Subjectively assigned continents to the level of difficulty
    e = ["Europe", "Americas"]
    m = ["Asia"]
    h = ["Africa", "Oceania", "Antarctic"]

    ALLBASE.extend(add(e) + add(m) + add(h))

    #Sends a command to add a given group of countries to the game database
    match lvl:
        case 1:
            BASE.extend(add(e))
        case 2:
            BASE.extend(add(m))
        case 3:
            BASE.extend(add(h))
        case 12:
            BASE.extend(add(e) + add(m))
        case 13:
            BASE.extend(add(e) + add(h))
        case 23:
            BASE.extend(add(m) + add(h))
        case 123:
            BASE.extend(add(e) + add(m) + add(h))
        case _:
            raise ValueError("Function got wrong value")


#Collects the appropriate data to call the get_level() function
def get_group():
    #Counts the number of appearances of countries from a given region
    european = american = asian = african = oceanian = antarctican = 0
    countries = download("https://restcountries.com/v3.1/all")
    for country in countries:
        match country.get("region"):
            case "Europe":
                european += 1
            case "Americas":
                american += 1
            case "Asia":
                asian += 1
            case "Africa":
                african += 1
            case "Oceania":
                oceanian += 1
            case "Antarctic":
                antarctican += 1

    #Table for selecting the level of difficulty
    headers = ["index", "difficulty level", "number of countries"]
    table = [
        ["1", "easy", european + american],
        ["2", "medium", asian],
        ["3", "hard", african + oceanian + antarctican]
    ]
    print(tabulate(table, headers, tablefmt="pretty"))
    print(tabulate([["4", "press to go back"]], tablefmt="pretty"))

    #Controls the selection in the table
    while True:
        values = []
        try:
            values.extend(input("Select the group (or groups) you want to play from: ").split())
        except EOFError:
            menu()
        match len(values):
            case 1:
                if "1" in values or "2" in values or "3" in values:
                    get_level(int(values[0]))
                elif values[0] == "4":
                    menu()
                else:
                    print("Inappropriate option")
            case 2:
                if "1" in values and "2" in values:
                    get_level(12)
                elif "1" in values and "3" in values:
                    get_level(13)
                elif "2" in values and "3" in values:
                    get_level(23)
                else:
                    raise ValueError("Inappropriate option")
            case 3:
                if "1" in values and "2" in values and "3" in values:
                    get_level(123)
            case _:
                print("You can choose a maximum of 3 options")

        #Interrupts the loop if data has been correctly added to the database
        if BASE:
            clear()
            break


#Downloads data from given API link in JSON format
def download(url: str):
    response = requests.get(url)
    r = response.json()
    return r

#Returns a list of countries matching the criteria
def add(reg: list):
    country_data = []

    #Gets country list
    countries = download("https://restcountries.com/v3.1/all")

    #Checks all countries and adds those whose region matches the appropriately selected option (difficulty level)
    for country in countries:
        region = country.get("region")
        if region in reg:
            data = {
                "name": country["name"]["common"],
                "population": country.get("population"),
                "area": country.get("area"),
                "region": region,
                "timezones": country.get("timezones")
            }
            country_data.append(data)

    return country_data


#Shows the program's operating instructions
def help():
    tekst = (
        "Main Menu\n"
        "Enter one of the 4 available digits and press Enter. "
        "If the input does not match any of the displayed options, the program will prompt you to try again."
        "Press Ctrl-D to close the program.\n"
        " 1 - START:"
        "Begins the game and takes you to the level selection menu.\n"
        " 2 - HELP:"
        "Displays program instructions. "
        "To exit the help screen, press 'q' and confirm with Enter.\n"
        " 3 - ABOUT:"
        "Shows basic information about the program. "
        "To exit the about screen, press 'q' and confirm with Enter.\n"
        " 4 - QUIT:"
        "Exits the program.\n\n"
        "Level Selection Menu\n"
        "Enter one, two, or three of the available digits. "
        "If selecting more than one, separate them with spaces.\n"
        " 1 - EASY:"
        "Contains countries from Europe and the Americas.\n"
        " 2 - MEDIUM:"
        "Contains countries from Asia.\n"
        " 3 - HARD:"
        "Contains countries from Africa, Oceania, and Antarctica.\n"
        "After selecting your desired level(s), the game will begin.\n"
        "Press Ctrl-D to return to the Main Menu.\n\n"
        "Game\n"
        "A prompt for guessing the country will appear. "
        "You must enter the common name of the country in English and press Enter. "
        "Press Ctrl-D to end the game and return to the Level Selection Menu. "
        "A table with 5 columns will be displayed, containing statistics for the selected country:\n"
        "Name:"
        "Displays the name of the country.\n"
        "Population:"
        "Shows the population count.\n"
        "Area:"
        "Displays the surface area.\n"
        "Region:"
        "Indicates the continent.\n"
        "Timezones:"
        "Shows the timezone(s) or the number of timezones, if the country has more than one.\n"
        "After a correct guess, the number of attempts will be shown. "
        "Press 'c' and confirm with Enter to return to the Main Menu."
        )
    print(view_on_terminal(tekst))

    #Allows leaving the page
    print("\n\nPress 'q' and then enter to exit ", end="")
    if key("q"):
        menu()

#Shows information about the program
def about():
    tekst = (
        'The "Country Guesser" program is an interactive game where the player must guess the country randomly selected by the computer. There are three difficulty levels, each featuring specific sets of countries. Players can choose one or more difficulty levels, which will mix countries from the selected categories.\n'
        "The game begins with the player guessing a random country. After each guess, the program provides feedback, highlighting the differences in various statistics between the guessed country and the one chosen by the computer. Using this information, the player can make more accurate guesses in subsequent rounds.\n"
        "The game continues until the player correctly identifies the drawn country. Once the correct guess is made, the total number of attempts is displayed.\n"
        "The program was written as a final project for CS50P, Author: Konrad Mateja"
        "Good luck in the game!!!"
        )
    print(view_on_terminal(tekst))

    #Allows leaving the page
    print("\n\nPress 'q' and then enter to exit ", end="")
    if key("q"):
        clear()
        menu()


#Returns text adjusted to the size of the terminal window
def view_on_terminal(txt: str):
    sections = txt.split("\n")
    return "\n\n".join([textwrap.fill(section, width = shutil.get_terminal_size().columns, drop_whitespace = True) for section in sections]).rstrip()


#Checks whether a given button has been pressed
def key(k: str):
    try:
        while True:
            if input() == k:
                break
    except EOFError:
            pass
    finally:
            return True

#Asks for a variable until it is in a given range and then returns it
def choose(start: int, end: int):
    while True:
        i = input("Select option: ")
        if i.isnumeric():
            if start <= int(i) <= end:
                return int(i)


#Prints the differences in the parameters of the country drawn and guessed until the answer is correct
def game():
    global BASE
    global ALLBASE
    i = ""
    attempt = 0
    l = [["NAME", "POPULATON", "AREA", "REGION", "TIMEZONES"]]
    p = inflect.engine()

    #Draws a country from the database participating in the game and creates an object of class Country() based on it
    drawn = random.choice(BASE)
    answear = Country(drawn["name"], drawn["population"], drawn["area"], drawn["region"], drawn["timezones"])

    while i.title() != answear.name:
        try:
            i = input("Take a guess: ")
        except EOFError:
            BASE = []
            l = [["NAME", "POPULATON", "AREA", "REGION", "TIMEZONES"]]
            i = ""
            attempt = 0
            clear()
            get_group()

        #Creates an object based on the Country() class if the user's guess is correct
        if in_base(i)[0]:
            c = in_base(i)[1]
            guess = Country(c["name"], c["population"], c["area"], c["region"], c["timezones"])

            attempt += 1
            l.append(compare(guess, answear))

            clear()
            print(f"Number of attempts: {attempt}\n", tabulate(l, headers="firstrow"), sep="")

    print(f"Congratulations, you guessed the country correctly on your {p.number_to_words(p.ordinal(attempt))} attempt!!!\n"
          "Press 'c' to continue", end=" ")
    if key("c"):
        BASE = []
        ALLBASE = []
        clear()
        menu()


#Checks whether a given country is in the database where the game is run and returns a list containing True and the name of this country or False
def in_base(guess: str):
    for country in ALLBASE:
        if country["name"] == guess.title():
            return [True, country]
    return [False]

#The function compares 2 objects of the same class
def compare(obj1: Country, obj2: Country):
    t = []

    #Saves data about the object
    obj1_stats = obj1.__dict__
    obj2_stats = obj2.__dict__

    #Writes hints based on the differences between the guessed and drawn country
    for stat in obj1_stats:
        if stat == "_name":
            if obj1_stats[stat] == obj2_stats.get(stat):
                t.append(correct(obj1_stats[stat]))
            else:
                t.append(incorrect(obj1_stats[stat]))
        elif (stat == "_population" or stat == "_area") and (isinstance(obj1_stats[stat], float) or isinstance(obj1_stats[stat], int)):
            if obj1_stats[stat] > obj2_stats.get(stat):
                t.append(incorrect("Less"))
            elif obj1_stats[stat] < obj2_stats.get(stat):
                t.append(incorrect("More"))
            else:
                t.append(correct(str(obj2_stats.get(stat))))
        elif isinstance(obj1_stats[stat], list) and obj1_stats[stat][0].startswith("UTC"):
            if len(obj1_stats[stat]) == 1 and len(obj2_stats.get(stat)) == 1 and obj1_stats[stat][0] != "UTC" and obj2_stats.get(stat)[0] != "UTC":
                hour1, minutes1 = obj1_stats[stat][0].replace("UTC", "").replace("+", "").split(":")
                hour2, minutes2 = obj2_stats.get(stat)[0].replace("UTC", "").replace("+", "").split(":")
                if int(hour1) > int(hour2):
                    t.append(incorrect("Earlier"))
                elif int(hour1) < int(hour2):
                    t.append(incorrect("Later"))
                else:
                    if int(hour1) < 0:
                        if int(minutes1) > int(minutes2):
                            t.append(incorrect("Later"))
                        elif int(minutes1) < int(minutes2):
                            t.append(incorrect("Earlier"))
                        else:
                            t.append(correct(obj2_stats.get(stat)[0]))
                    elif int(hour1) > 0:
                        if int(minutes1) > int(minutes2):
                            t.append(incorrect("Earlier"))
                        elif int(minutes1) < int(minutes2):
                            t.append(incorrect("Later"))
                        else:
                            t.append(correct(obj2_stats.get(stat)[0]))
            else:
                if len(obj1_stats[stat]) > len(obj2_stats.get(stat)):
                    t.append(incorrect("Less"))
                elif len(obj1_stats[stat]) < len(obj2_stats.get(stat)):
                    t.append(incorrect("More"))
                elif obj1_stats[stat][0] == obj2_stats.get(stat)[0] and obj1_stats[stat][0] == "UTC":
                    t.append(correct("None"))
                else:
                    t.append(correct(str(len(obj2_stats.get(stat)))))
        else:
            if obj1_stats[stat] == obj2_stats.get(stat):
                t.append(correct(obj2_stats.get(stat)))
            else:
                t.append(incorrect("Other"))

    return t


#Clears the terminal screen
def clear():
    #Works for Windows
    if os.name == "nt":
        os.system("cls")
    #Works for Linux/MacOS
    else:
        os.system("clear")


#Colors the given string green using ANSI codes
def correct(s: str):
    return "\033[32m" + s + "\033[0m"


#Colors the given string red using ANSI codes
def incorrect(s: str):
    return "\033[31m" + s + "\033[0m"


#Ends the program and thanks the user for playing
def end():
    clear()
    sys.exit("Thank you for playing!")


#Runs the main() function only when the program is started directly
if __name__ == "__main__":
    main()
