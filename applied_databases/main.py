# Import functions needed.
from view_add_sql import view_directors_and_films, view_actors_by_month, add_actor
from add_actor_marriage import add_actor_marriage
from view_studios import view_studios
from submenu import *
from find_actor_spouse import find_actor_partner
from procedure import create_run_procedure

def main():
    print("\nMoviesDB\n---------\n")
    display_menu()

    while True:
        choice = input("Choice: ").strip().lower()

        if choice == "1":
            view_directors_and_films()
        elif choice == "2":
            view_actors_by_month()
        elif choice == "3":
            add_actor()
        elif choice == "4":
            find_actor_partner()  # Requires Neo4j
        elif choice == "5":
            add_actor_marriage()   # Requires Neo4j
        elif choice == "6":
            view_studios()
        elif choice == "7":
            create_run_procedure()
        elif choice == "8":
            generate_reports_menu()
        elif choice == "x":
            break
        else:
            print("")

        display_menu()


def display_menu():
    print("MENU")
    print("=" * 4)
    print("1 - View Directors & Films")
    print("2 - View Actors by Month of Birth")
    print("3 - Add New Actor")
    print("4 - View Married Actors")
    print("5 - Add Actor Marriage")
    print("6 - View Studios")
    print("7 - Create/Run Procedure")
    print("8 - Generate Reports")
    print("x - Exit application")



if __name__ == "__main__":
    main()
