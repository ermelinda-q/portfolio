# Importing the libraries and functions from functions_sql.py file.
import calendar
from functions_sql import query_sql_data, exists_in_table, insert_actor

############################################################
########  Menu Choice 1 - View Directors & Films   #########
############################################################

# Function to get user input, calls query_sql_data function
# and displays results.
def view_directors_and_films():
    name = input("\nEnter director Name: ").strip()
    results = query_sql_data("directors_films",name)
    print(f"Film Details For: ", name)
    print("-" * 30)
    if results:
        for row in results:
            print(row['directorname']," | ", row['filmname'], " | ", row['studioname'])
        print("\n")
    else:
        print("No directors found of that name\n")


############################################################
###### Menu Choice 2 - View Actors by Month of Birth #######
############################################################

# Function to get user input, call query_sql_data function
# and displays results.
def view_actors_by_month():
    print("")
    while True:
        user_input = input("Enter Month: ").strip()
        # Validating numbers
        if user_input.isdigit():
            month = int(user_input)
            if 1 <= month <= 12:
                break
            else:
                continue
        # Validating any other user input
        elif len(user_input) == 3:
            month_abbrs = [m[:3].lower() for m in calendar.month_name if m]
            if user_input.lower() in month_abbrs:
                month = month_abbrs.index(user_input.lower()) + 1
                break
            else:
                continue
        else:
            continue
    # Calling get_actors_by_month function and displaying results
    actors = query_sql_data("actors_by_month", month)
    for actor in actors:
        print(f"{actor['actorName']} | {actor['actorDOB']} | {actor['actorGender']}")
    print("")

            
############################################################
##########     Menu Choice 3 - Add New Actor     ###########
############################################################

# Function to get user input, actor details, validates user input than if all 
# good calls insert_actor function and adds actor to database(actor table).
def add_actor():
    print("\nAdd New Actor")
    print("-" * 16)
    
    actor_id = input("Actor ID: ")
    name = input("Name: ")
    dob = input("DOB: ")
    gender = input("Gender: ")
    country_id = input("Country ID: ")

    # Check if actor ID already exists
    if exists_in_table("actor", "ActorID", actor_id):
        print(f"*** ERROR *** Actor ID: {actor_id} already exists\n")
        return

    # Check if the country ID exists
    if not exists_in_table("country", "CountryID", country_id):
        print(f"*** ERROR *** Country ID: {country_id} does not exist\n")
        return

    # Insert the actor if all good
    result = insert_actor(actor_id, name, dob, gender, country_id)
    
    # print whatever message returns from result
    print(result)
