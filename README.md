# COUNTRY GUESSER

### Test Your Geography Knowledge (and Luck)!

#### This program was developed as a final project for [CS50P](https://cs50.harvard.edu/python/) and as a way to further develop my own skills. The game involves guessing a randomly chosen country based on hints from previous attempts.

---

### Video Demo: <https://youtu.be/RPnLgQUoFxM>

---

## Before you start the program

Ensure you have Python installed, then install these packages:
- tabulate
- requests
- inflect

you can type in bash:

    pip install tabulate requests inflect


## Instructions
> The program starts from the MAIN MENU.

### MAIN MENU
#### Allows you to access one of the core features of the program:

1. START
   - Begins the game and moves to the **LEVEL MENU**.
2. HELP
   - Displays instructions on how to use the program.
3. ABOUT
   - Shows general information about the program.
4. QUIT
   - Exits the program.

---

### LEVEL MENU
#### Allows you to select the country group for the game.

1. easy
   - Europe and Americas
2. medium
   - Asia
3. hard
   - Africa, Oceania, and Antarctica
4. press to go back
   - Returns to the previous menu.

If you want to select more than one option, separate them with spaces.

---

### Gameplay
#### Time to Guess!
   - The first attempt must be made blindly.
   - If the country is not in the database, you’ll need to try again.
   - After each guess, a table will show the differences between the guessed country and the computer-chosen country.

---

### The Table
#### Includes 5 categories:
- name
   - Name of the country
- population
   - Population
- area
   - Area size
- region
   - Continent
- timezones
   - Time zone (if only one exists) or the number of time zones (if multiple)

######

   - Each attempt will be added to the bottom of the table, keeping previous guesses visible to help with further guessing.
   - The number of attempts is tracked and displayed after each guess.
   - The game continues until you correctly guess the selected country.

---

### End of Game

   - After a correct guess, the number of attempts will be displayed.
   - To return to the main menu, press ‘c’ and confirm with enter.

---

## Program Structure
#### Each function explained step-by-step.

> Country

The class initializes with constants:
- _name
- _population
- _area
- _region
- _timezones

These constants store country information. Properties return specific data.

> main

Calls the **menu** function when the program starts, which is its sole purpose.

> menu

Starts with **clear**, creates a table with [tabulate](https://pypi.org/project/tabulate/), and calls **choose** to handle the four options.
Depending on the option chosen, it calls other functions:
1. **get_group** and **game**
2. **help**
3. **about**
4. **end** (alternatively, use ctrl-d).

All actions are preceded by **clear**.

> get_level

Accepts an argument:
- lvl (int)

Variables are associated with difficulty levels, each containing specific continents:
- e (easy)
   - Europe
   - Americas (both)
- m (medium)
   - Asia
- h (hard)
   - Africa
   - Oceania
   - Antarctic

At this stage, the **ALLBASE** global variable is populated with all countries (from all regions).

Note: This step is delayed to avoid potential database changes mid-program, keeping countries in **ALLBASE** and **BASE** consistent.

Based on **lvl**, adds the selected group of countries to **BASE**.

> get_group

Fetches all countries from the database via the [REST Countries API](https://restcountries.com).

Counts each region's countries and creates a table with [tabulate](https://pypi.org/project/tabulate/), displaying level options and their country counts.

The program takes user input for the level selection, allowing multi-option selections (e.g., combining easy and hard), though option ‘4’ cannot be combined:
1. easy
2. medium
3. hard
4. press to go back

Options 1-3 call **get_level** with the appropriate parameter, while option 4 or ctrl-d goes back to the main menu (**menu**).

The loop continues until **BASE** is properly populated.

> download

Accepts an argument:
- url (str)

Fetches API data from the **url** argument and returns it in JSON format.

> add

Accepts an argument:
- reg (list)

Creates a list from all countries fetched from the [REST Countries API](https://restcountries.com) whose regions are in **reg**:
- name (common country name)
- population
- area
- region
- timezones

Returns the generated list.

> help

Displays program navigation help using the **view_on_terminal** function.

Pressing ‘q’ and confirming with enter or ctrl-d returns to the previous window (**menu**).

> about

Displays general information about the program using **view_on_terminal**.

Pressing ‘q’ and confirming with enter or ctrl-d returns to the previous window (**menu**).

> view_on_terminal

Accepts an argument:
- txt (str)

Splits the **txt** argument into paragraphs by "\n", then joins them with a line space between each, adjusting to the terminal display size.

Returns the formatted text.

> key

Accepts an argument:
- k (str)

Returns true if the key **k** or ctrl-d is pressed.

> choose

Accepts arguments:
- start (int)
- end (int)

Prompts the user to select an option and returns it if within **start** and **end**; otherwise, it repeats the sequence.

> game

Randomly selects a country from **BASE** and creates a **Country** object.

Prompts the user to enter a guess; if ctrl-d is pressed, **clear** is used, and it returns to the previous menu (**get_group**). If the guessed country is in **ALLBASE**, a table created with [tabulate](https://pypi.org/project/tabulate/) will display the differences between guessed and target country using **compare**.

If the guess is correct, **clear** is called, and the number of attempts is shown. Pressing ‘c’ and enter or ctrl-d returns to **menu**, and **BASE** and **ALLBASE** are cleared.

> in_base

Accepts an argument:
- guess (str)

Checks if the country from **guess** is in **ALLBASE**. If not, returns a list with **False** at index 0. If it exists, returns a list with **True** at index 0 and a dictionary with:
- name
- population
- area
- region
- timezones

> compare

Accepts arguments:
- obj1 (Country instance)
- obj2 (Country instance)

Compares each attribute and adds differences:
- More/Less for population, area, timezone count
- Other for region
- Earlier/Later for timezone

Differences are shown in red via **incorrect**, while matches are green via **correct**.

Returns the list.

> clear

Checks the OS and calls the appropriate terminal clearing command.

> correct

Accepts an argument:
- s (str)

Returns **s** in green.

> incorrect

Accepts an argument:
- s (str)

Returns **s** in red.

> end

Clears the terminal with **clear** and exits, thanking the user.

---

The final line in the code runs **main** if the program is executed directly.
