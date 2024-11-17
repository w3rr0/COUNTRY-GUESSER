from project import download, add, in_base, compare, correct, incorrect, get_level, Country
import pytest
import requests

def test_download():
    #Working API
    assert download("https://pokeapi.co/api/v2/pokemon/pikachu") == requests.get("https://pokeapi.co/api/v2/pokemon/pikachu").json()
    assert download("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd") == requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd").json()
    assert download("https://api.spacexdata.com/v4/launches/latest") == requests.get("https://api.spacexdata.com/v4/launches/latest").json()
    assert download("https://api.thedogapi.com/v1/breeds") == requests.get("https://api.thedogapi.com/v1/breeds").json()


def test_add():
    #Known region
    assert add("Antarctic") == [{'name': 'South Georgia', 'population': 30, 'area': 3903.0, 'region': 'Antarctic', 'timezones': ['UTC-02:00']}, {'name': 'Antarctica', 'population': 1000, 'area': 14000000.0, 'region': 'Antarctic', 'timezones': ['UTC-03:00', 'UTC+03:00', 'UTC+05:00', 'UTC+06:00', 'UTC+07:00', 'UTC+08:00', 'UTC+10:00', 'UTC+12:00']}, {'name': 'Bouvet Island', 'population': 0, 'area': 49.0, 'region': 'Antarctic', 'timezones': ['UTC+01:00']}, {'name': 'French Southern and Antarctic Lands', 'population': 400, 'area': 7747.0, 'region': 'Antarctic', 'timezones': ['UTC+05:00']}, {'name': 'Heard Island and McDonald Islands', 'population': 0, 'area': 412.0, 'region': 'Antarctic', 'timezones': ['UTC+05:00']}]
    #Unknown region
    assert add("region") == []
    #Not a string
    with pytest.raises(TypeError):
        add(123)


def test_in_base():
    #Adds countries to the database for testing purposes
    get_level(1)
    #In base
    assert in_base("Poland") == [True, {'name': 'Poland', 'population': 37950802, 'area': 312679.0, 'region': 'Europe', 'timezones': ['UTC+01:00']}]
    assert in_base("mexico") == [True, {'name': 'Mexico', 'population': 128932753, 'area': 1964375.0, 'region': 'Americas', 'timezones': ['UTC-08:00', 'UTC-07:00', 'UTC-06:00']}]
    #Not in base
    assert in_base("Country") == [False]
    assert in_base("Cat") == [False]


def test_compare():
    #Mixed correct and incorrect
    first = Country("name1", 1000, 300.0, "Americas", ["UTC-02:00"])
    second = Country("name2", 100, 300.0, "Europe", ["UTC-02:00"])
    assert compare(first, second) == ["\033[31mname1\033[0m", "\033[31mLess\033[0m", "\033[32m300.0\033[0m", "\033[31mOther\033[0m", "\033[32mUTC-02:00\033[0m"]
    #All incorrect
    first = Country("name1", 1, 20.1, "Asia", ["UTC-01:00"])
    second = Country("name2", 2, 20.0, "Oceania", ["UTC+01:15"])
    assert compare(first, second) == ["\033[31mname1\033[0m", "\033[31mMore\033[0m", "\033[31mLess\033[0m", "\033[31mOther\033[0m", "\033[31mLater\033[0m"]
    #All correct
    first = Country("name", 100, 50.5, "Africa", ["UTC-01:00", "UTC-02:00"])
    second = Country("name", 100, 50.5, "Africa", ["UTC+02:00", "UTC+03:00"])
    assert compare(first, second) == ["\033[32mname\033[0m", "\033[32m100\033[0m", "\033[32m50.5\033[0m", "\033[32mAfrica\033[0m", "\033[32m2\033[0m"]


def test_correct():
    #Correct input
    assert correct("hello") == "\033[32mhello\033[0m"
    assert correct("test") == "\033[32mtest\033[0m"
    assert correct("CS50P") == "\033[32mCS50P\033[0m"
    #Not a string
    with pytest.raises(TypeError):
        correct(1)


def test_incorrect():
    #Correct input
    assert incorrect("cat") == "\033[31mcat\033[0m"
    assert incorrect("dog") == "\033[31mdog\033[0m"
    assert incorrect("CS50P") == "\033[31mCS50P\033[0m"
    #Not string
    with pytest.raises(TypeError):
        incorrect(50)
