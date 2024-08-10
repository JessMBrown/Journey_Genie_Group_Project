from Joana_OpenTripMapAPI import OpenTripMapApi
from pprint import pprint
from collections import deque


def knows_destination():
    chosen_country = input("Please, enter the name of the country: ")  # modify to make it a fixed list of countries
    #  Make a list of cities to chose from
    #  Ask specificities about the hotel they are looking for
    #  call hotels function to get list of hotels
    #  call activities function to make suggestions find_activities(city)
    #  call email function


def tailored_trip():
    # take user input on what type of holiday he would like
    # create code to get countries and get user to choose one
    # call find cities to display list of cities
    # call hotels function to display hotels
    # call activities function to display activities
    # call email function to get email sent
    pass

def take_me_anywhere():
    #  create code to random to call find country
    # ask is user wants another try
    # call cities
    # call hotels
    # call activities
    # call email
    pass

def find_cities(country): # or should it be find countries and cities??
    pass
def find_hotels(city):
    pass
def find_activities(city):
    pass
def get_email():
    pass

def get_input(prompt):
    while True:
        user_input = input(prompt).lower()
        if user_input in ['y', 'n']:
            return user_input
        print("Sorry, that's not a possible option. Please enter 'Y' or 'N'.")

def main():
    # Welcoming user and getting some basic details
    print("Hello! Welcome to Journey Genie! Let's start prepping your next holiday!")
    start_date = input("First, please enter the start date for your holiday (YYYY-MM-DD): ")
    end_date = input("Now, please enter the end date for your holiday (YYYY-MM-DD): ")
    num_adults = input('How many adults will you be? ')
    num_children = input("How many children? ")
    knows_where = get_input("Do you know which country you'd like to go to? Y/N ")

    if knows_where == 'y':
        knows_destination()
    elif knows_where == 'n':
        wants_random = get_input("No worries! We're here to help! Would you like us to make a random guess of a nice holiday place for you? Y/N ")
        if wants_random == 'y':
            take_me_anywhere()
        elif wants_random == 'n':
            print("Ok! Let's tailor a nice holiday for you!")
            tailored_trip()


if __name__ == "__main__":
    main()
