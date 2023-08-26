"""

This file handles CRUD operations for:
1. Admin User
2. Boat Information
3. Customer Details
4. Reservations

It also includes reading from a CSV file and saving into the database.

The boat info table includes the boat availability for the reservation.

"""

import db_base as db
import csv

# Using a global variable for the database name to avoid redundancy.

dbname = "BoatRentalsDB.sqlite"


# Creating the Tables for the database - 'BoatRentalsDB'
class Reset_DB(db.DBbase):

    def __init__(self):
        super().__init__(dbname)

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Admin;
                DROP TABLE IF EXISTS BoatInfo;
                DROP TABLE IF EXISTS Customer;
                DROP TABLE IF EXISTS Reservation;

                CREATE TABLE Admin (
                    admin_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    username Text,
                    password Text
                );
                    
                CREATE TABLE BoatInfo(
                     boat_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                     boat_model TEXT,
                     boat_size INTEGER,
                     occupancy INTEGER,
                     price INTEGER,
                     status TEXT
                 );

                CREATE TABLE Customer(
                    customer_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    customer_name TEXT NOT NULL,
                    customer_phone TEXT NOT NULL
                );

                CREATE TABLE Reservation(
                    reservation_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                    boat_id INTEGER NOT NULL,
                    customer_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    duration TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    FOREIGN KEY (boat_id) REFERENCES Boat(boat_id),
                    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
                );
            """
            self.execute_script(sql)
        except Exception as e:
            print("An error occurred.", e)


# CRUD operations for the Admin User
class Admin(db.DBbase):
    def __init__(self):
        super().__init__(dbname)

    def add_user(self, username=None, password=None):
        try:
            super().get_cursor.execute(
                """Insert into Admin (username,password) values (?,?);""",
                (username, password))
            super().get_connection.commit()
            print(f"Add {username} successfully.")

        except Exception as e:
            print("An error as occurred while adding admin", e)

    def update_user(self, admin_id, username=None, password=None):
        try:
            if username is not None and username != "":
                super().get_cursor.execute("""update Admin set username = ? WHERE admin_id = ?;""",
                                           (username, admin_id,))

            if password is not None and password != "":
                super().get_cursor.execute("""update Admin set password = ? WHERE admin_id = ?;""",
                                           (password, admin_id,))
            super().get_connection.commit()
            print("Admin record Updated successfully!")

        except Exception as e:
            print("An error as occurred while updating admin details", e)

    def delete_user(self, admin_id):

        try:
            super().get_cursor.execute("""DELETE FROM Admin WHERE admin_id = ?;""", (admin_id,))
            super().get_connection.commit()
            print("Admin details deleted successfully !")

        except Exception as e:
            print("An error as occurred while deleting admin", e)

    def fetch_user(self, admin_id=None):
        try:
            if admin_id is not None:
                return super().get_cursor.execute("""SELECT * FROM Admin WHERE admin_id = ? ;""",
                                                  (admin_id,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM Admin;""").fetchall()
        except Exception as e:
            print("An error occurred : {}".format(e))

    def authenticate(self, username, password):
        try:
            admin_details = super().get_cursor.execute("""SELECT * FROM Admin WHERE username = ? and password = ? ;""",
                                                       (username, password,)).fetchone()
            if admin_details is None:
                print("Invalid credentials. Please Try Again!")
            else:
                print(f"Welcome! {username}")
                return True
        except Exception as e:
            print("An error occurred : {}".format(e))


# CRUD operations for Boat Information
class BoatInfo(db.DBbase):
    def __init__(self, row):
        super().__init__(dbname)

        self.boat_id = row[0]
        self.boat_model = row[1]
        self.boat_size = row[2]
        self.occupancy = row[3]
        self.price = row[4]
        self.status = row[5]

    def add_boat(self, boat_model, boat_size, occupancy, price, status):
        try:
            super().get_cursor.execute(
                "INSERT INTO BoatInfo (boat_model, boat_size, occupancy,price,status) values (?,?,?,?,?);",
                (boat_model, boat_size, occupancy, price, status))
            super().get_connection.commit()
            print(f"Add {boat_model} successfully.")
        except Exception as e:
            print("An error occurred on boat details creation!!.", e)

    def update_boat(self, boat_id, boat_model, boat_size=None, occupancy=None, price=None, status=None):
        try:
            super().get_cursor.execute(
                """
                UPDATE BoatInfo SET boat_model = ?,boat_size = ?,price = ? , status = ?, occupancy = ?
                        WHERE boat_id = ?;
                """,
                (boat_model, boat_size, price, status, occupancy, boat_id,))
            super().get_connection.commit()
            print("Updation is Successfully performed!")
        except Exception as e:
            print("An error occurred while updating Boat details :", e)

    def delete_boat(self, boat_id):
        try:
            super().get_cursor.execute("DELETE FROM BoatInfo WHERE boat_id = ?;", (boat_id,))
            super().get_connection.commit()
            print("Boat details deleted  successfully !")
        except Exception as e:
            print("An error occurred while deleting boat details !!.", e)

    def fetch_boat(self, boat_id=None):
        try:
            if boat_id:
                boat_data = super().get_cursor.execute("SELECT * FROM BoatInfo WHERE boat_id = ? ;",
                                                       (boat_id,)).fetchone()
                boat_id, boat_model, boat_size, occupancy, price, status = boat_data
                print(f"Boat ID: {boat_id}")
                print(f"Boat Model: {boat_model}")
                print(f"Boat Size: {boat_size}")
                print(f"Occupancy: {occupancy}")
                print(f"Price: {price}")
                print(f"Status: {status}")
            else:
                print(f"No information found for Boat ID: {boat_id}")
        except Exception as e:
            print("An error occurred : {}".format(e))

    def list_all_boats(self):
        try:
            sql = """SELECT * FROM BoatInfo"""
            super().get_cursor.execute(sql)
            all_boats = super().get_cursor.fetchall()

            if all_boats:
                for boat_data in all_boats:
                    boat_id, boat_model, boat_size, price, status, occupancy = boat_data
                    print(f"Boat ID: {boat_id}")
                    print(f"Boat Model: {boat_model}")
                    print(f"Boat Size: {boat_size}")
                    print(f"Price: {price}")
                    print(f"Status: {status}")
                    print(f"Occupancy: {occupancy}")
                    print("---------------------\n")
            else:
                print("No information found.")
        except Exception as e:
            print("An error has occurred while fetching customers.", e)


# CRUD operations for Customers who will be reserving the boats
class Customer(db.DBbase):
    def __init__(self):
        super().__init__(dbname)

    def add_customer(self, customer_name, customer_phone):
        try:
            sql = """INSERT INTO Customer (customer_name, customer_phone) VALUES (?, ?)"""
            super().get_cursor.execute(sql, (customer_name, customer_phone))
            super().get_connection.commit()
            print("Customer added successfully.")
        except Exception as e:
            print("An error has occurred while adding the customer.", e)

    def update_customer(self, customer_id, customer_name, customer_phone):
        try:
            sql = """UPDATE Customer SET customer_name=?, customer_phone=? WHERE customer_id=?"""
            super().get_cursor.execute(sql, (customer_name, customer_phone, customer_id))
            super().get_connection.commit()
            print("Customer updated successfully.")
        except Exception as e:
            print("An error has occurred while updating the customer.", e)

    def delete_customer(self, customer_id):
        try:
            sql = """DELETE FROM Customer WHERE customer_id=?"""
            super().get_cursor.execute(sql, (customer_id,))
            super().get_connection.commit()
            print("Customer deleted successfully.")
        except Exception as e:
            print("An error has occurred while deleting the customer.", e)

    def fetch_customer(self, customer_id):
        try:
            customer_data = super().get_cursor.execute("""SELECT * FROM Customer WHERE customer_id=?""",
                                                       (customer_id,)).fetchone()

            if customer_data:
                customer_id, customer_name, customer_phone = customer_data
                print(f"Customer ID: {customer_id}")
                print(f"Customer Name: {customer_name}")
                print(f"Customer Phone: {customer_phone}")
            else:
                print(f"No information found for Customer ID: {customer_id}")
        except Exception as e:
            print("An error has occurred while fetching the customer.", e)

    def list_all_customers(self):
        try:
            sql = """SELECT * FROM Customer"""
            super().get_cursor.execute(sql)
            all_customers = super().get_cursor.fetchall()

            if all_customers:
                print("All Customers:")
                for customer_data in all_customers:
                    customer_id, customer_name, customer_phone = customer_data
                    print(f"Customer ID: {customer_id}")
                    print(f"Customer Name: {customer_name}")
                    print(f"Customer Phone: {customer_phone}")
                    print("---------------------\n")
            else:
                print("No customers found.")
        except Exception as e:
            print("An error has occurred while fetching customers.", e)


# CRUD operations for reservation of the boats for a particular customer
class Reservations(db.DBbase):

    def __init__(self):
        super().__init__(dbname)

    def add_reservation(self, boat_id, customer_id, date, duration, start_time):
        try:
            if self.is_available(boat_id):
                sql = """
                    INSERT INTO Reservation (boat_id, customer_id, date, duration, start_time)
                    VALUES (?, ?, ?, ?, ?)
                """
                super().get_cursor.execute(sql, (boat_id, customer_id, date, duration, start_time))
                super().get_connection.commit()

                super().get_cursor.execute("UPDATE BoatInfo SET status = 'Unavailable' WHERE boat_id = ?;", (boat_id,))
                super().get_connection.commit()
                print("Reservation added successfully.")
            else:
                print("Boat not available at the specified time.")
        except Exception as e:
            print("An error has occurred.", e)

    def update_reservation(self, reservation_id, boat_id, customer_id, date, duration, start_time):
        try:
            # print(type(reservation_id))
            # print(type(boat_id))
            # print(type(customer_id))
            # print(type(date))
            # print(type(duration))
            # print(type(start_time))
            # Convert 'duration' to an integer if it's not already.
            duration = int(duration)

            sql = """
                    UPDATE Reservation
                    SET boat_id=?, customer_id=?, date=?, duration=?, start_time=?
                    WHERE reservation_id=?
                """
            super().get_cursor.execute(sql, (boat_id, customer_id, date, duration, start_time, reservation_id))
            super().get_connection.commit()

            super().get_cursor.execute("UPDATE BoatInfo SET status = 'Unavailable' WHERE boat_id = ?;", (boat_id,))
            super().get_connection.commit()
            print("Reservation updated successfully.")

        except Exception as e:
            print("An error has occurred.", e)

    def delete_reservation(self, reservation_id):
        try:
            sql = """DELETE FROM Reservation WHERE reservation_id=?"""

            boat_id_tuple = super().get_cursor.execute("""SELECT boat_id FROM Reservation WHERE reservation_id=?;""",
                                                       (reservation_id,)).fetchone()

            # Extract the boat_id from the tuple
            if boat_id_tuple:
                boat_id = boat_id_tuple[0]
                # print(boat_id)

                super().get_cursor.execute("UPDATE BoatInfo SET status = 'Available' WHERE boat_id = ?;", (boat_id,))
                super().get_connection.commit()

                super().get_cursor.execute(sql, (reservation_id,))
                super().get_connection.commit()

                print("Reservation deleted successfully.")
            else:
                print("Reservation not found.")
        except Exception as e:
            print("An error has occurred while deleting the reservation.", e)

    def fetch_reservation(self, reservation_id):
        try:
            # sql = """
            #     SELECT reservation_id, boat_id, customer_id, date, duration, start_time
            #     FROM Reservation
            #     WHERE reservation_id=?;
            # """
            reservation_data = super().get_cursor.execute("""SELECT * FROM Reservation WHERE reservation_id=?;""",
                                                          (reservation_id,)).fetchone()

            if reservation_data:
                reservation_id, boat_id, customer_id, date, duration, start_time = reservation_data
                print(f"Reservation ID: {reservation_id}")
                print(f"Boat ID: {boat_id}")
                print(f"Customer ID: {customer_id}")
                print(f"Date: {date}")
                print(f"Duration: {duration}")
                print(f"Start Time: {start_time}")
            else:
                print(f"No Reservations found for reservation id:{reservation_id}")
        except Exception as e:
            print("An error has occurred while fetching the reservation.", e)

    def list_all_reservations(self):
        try:
            sql = "SELECT * FROM Reservation"
            super().get_cursor.execute(sql)
            all_reservations = super().get_cursor.fetchall()

            if all_reservations:
                print("All Reservations:")
                for reservation_data in all_reservations:
                    reservation_id, boat_id, customer_id, date, duration, start_time = reservation_data
                    print(f"Reservation ID: {reservation_id}")
                    print(f"Boat ID: {boat_id}")
                    print(f"Customer ID: {customer_id}")
                    print(f"Date: {date}")
                    print(f"Duration: {duration}")
                    print(f"Start Time: {start_time}")
                    print("---------------------\n")
            else:
                print("No reservations found.")
        except Exception as e:
            print("An error has occurred while fetching reservations.", e)

    def is_available(self, boat_id):
        try:
            sql = """SELECT status FROM BoatInfo WHERE boat_id = ?"""
            params = (boat_id, )

            # if reservation_id:
            #     sql += " AND reservation_id <> ?"
            #     params += (reservation_id,)

            status_tuple = super().get_cursor.execute(sql, params).fetchone()  # Removed the parentheses here
            is_conflicting = False

            if status_tuple:
                status = status_tuple[0]

                if status == 'Available':
                    is_conflicting = True

            # print(is_conflicting)

            return is_conflicting
        except Exception as e:
            print("An error occurred while checking availability.", e)
            return False


# Saving the Boat Information from a CSV file into the table 'BoatInfo'
class ReadCSV(db.DBbase):
    def __init__(self):
        super().__init__(dbname)
        self._boat_list = []

    def read_csv(self, file_name):

        try:
            with open(file_name, "r") as record:
                csv_reader = csv.reader(record)
                next(record)
                for row in csv_reader:
                    cust = BoatInfo(row)
                    self._boat_list.append(cust)

        except Exception as e:
            print(e)

    def save_to_database(self):
        print("Records to save: ", len(self._boat_list))
        save = input("Continue? ").lower()
        if save == "y":
            for item in self._boat_list:
                # boat_id,boat_model,boat_size,occupancy,price,status
                try:
                    super().get_cursor.execute(
                        """
                            Insert into BoatInfo 
                            (boat_id, boat_model, boat_size, occupancy,price,status) values (?,?,?,?,?,?);
                        """,
                        (item.boat_id, item.boat_model, item.boat_size, item.occupancy, item.price, item.status,))
                    super().get_connection.commit()
                    print("items list", item.boat_id, item.boat_model, item.boat_size, item.occupancy, item.price,
                          item.status)
                except Exception as e:
                    print(e)
        else:
            print("csv export aborted.")

# Calling all the functions necessary to perform before the menu is accessed.

# createTable = Reset_DB()
# createTable.reset_database()

# saveData = Admin()
# saveData.add_user("Yaswanth", "Yash123")
# saveData.add_user("Meghana", "Mega123")
# saveData.add_user("Manavi", "Man123")

# fetchDataCSV = ReadCSV(dbname)
# fetchDataCSV.read_csv("BoatDetails.csv")
# fetchDataCSV.save_to_database()
