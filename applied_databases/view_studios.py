from db_connections import connection_sql
studios = None  

############################################################
########        Menu Choice 6 - View Studios       #########
############################################################
# This functions used the appdbproj(MySQL database), run query 
# and return studios from studio table ordered by studio id.
def view_studios():
    global studios
    conn = connection_sql()
    if studios is None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT studioID, studioName FROM studio ORDER BY studioID")
            studios = cursor.fetchall()
        except Exception as e:
            print("Error fetching studios:", e)
            return

    print("\nStudioID   |  StudioName")
    for studio in studios:
        print(studio[0], "  |  ", studio[1])
    print("")