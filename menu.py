"""

After successful authentication, the user can access the menu.
The menu displays options for boat, customer, and reservations operations.
The user selects an option from the menu to perform CRUD operations.
Each selected option prompts the user to choose from another list for specific operations.

"""

import create_table as ct
import datetime

dbname = "BoatRentalsDB.sqlite"


class Menu:

    def main(self):
        print("Welcome to Boat Rentals, Please enter your credentials")
        login = False
        while not login:
            username = input("Enter username: ")
            password = input("Enter password: ")
            login = ct.Admin().authenticate(username, password)

            while login:
                user_input = int(input("1. Boat\n2. Customer\n3. Reservation\n4. Exit\n"))
                if user_input == 1:
                    boat_rentals = ct.BoatInfo(dbname)
                    boat_option = ""

                    while boat_option != 5:
                        boat_option = int(input("Select from the options below:\n1. Add Boat\n"
                                                "2. View Boat\n3. Update Boat\n4. Delete Boat\n5. Exit\n"))
                        if boat_option == 1:
                            boat_model = input("Please enter boat model: ")
                            boat_size = int(input("Please enter boat size: "))
                            occupancy = int(input("Please enter occupancy: "))
                            price = int(input("Please enter price: "))
                            boat_rentals.add_boat(boat_model, boat_size, occupancy, price, "Available")
                        elif boat_option == 2:
                            view_boat = int(input("1. View one boat\t\t2. View all the boats\t\t3. Exit\n"))
                            if view_boat == 1:
                                boat_id = int(input("Enter the boat id to view: "))
                                print(boat_rentals.fetch_boat(boat_id))
                            elif view_boat == 2:
                                print(boat_rentals.list_all_boats())
                            else:
                                break
                        elif boat_option == 3:
                            boat_id = int(input("Enter the boat id to update: "))
                            boat_model = input("Enter the boat model to update: ")
                            boat_size = input("Enter the boat size to update: ")
                            occupancy = int(input("Please enter occupancy: "))
                            price = int(input("Please enter price: "))
                            boat_rentals.update_boat(boat_id, boat_model, boat_size, occupancy, price, "Available")
                        elif boat_option == 4:
                            boat_id = int(input("Enter the boat id to delete: "))
                            boat_rentals.delete_boat(boat_id)
                        else:
                            if boat_option != 5:
                                print("Invalid Selection, please try again\n")
                            else:
                                break

                elif user_input == 2:
                    cl_customer = ct.Customer()

                    customer_option = ""

                    while customer_option != 5:
                        customer_option = int(input("Select from the options below:\n"
                                                    "1. Add Customer\n2. View Customer\n3. Update Customer"
                                                    "\n4. Delete Customer\n5. Exit\n"))

                        if customer_option == 1:
                            customer_name = input("Enter customer name: ")
                            customer_phone = input("Enter the contact number: ")

                            cl_customer.add_customer(customer_name, customer_phone)
                        elif customer_option == 2:
                            view_customer = int(input("1. View one Customer\t\t2. View all the Customers\n"))
                            if view_customer == 1:
                                customer_id = int(input("Enter the customer id to view: "))
                                cl_customer.fetch_customer(customer_id)
                            else:
                                print(cl_customer.list_all_customers())
                        elif customer_option == 3:
                            customer_id = int(input("Enter the customer id you want to update: "))
                            customer_name = input("Enter customer name: ")
                            customer_phone = input("Enter the contact number: ")
                            cl_customer.update_customer(customer_id, customer_name, customer_phone)
                            cl_customer.fetch_customer(customer_id)
                        elif customer_option == 4:
                            customer_id = int(input("Enter the customer id you want to delete: "))
                            cl_customer.delete_customer(customer_id)
                        else:
                            if customer_option != 5:
                                print("Invalid Selection, please try again\n")
                            else:
                                break

                elif user_input == 3:
                    reservation = ct.Reservations()

                    reservation_option = ""

                    while reservation_option != 5:
                        reservation_option = int(input("Select from the options below:"
                                                       "\n1. Add Reservation\n2. View Reservation"
                                                       "\n3. Update Reservation\n4. Delete Reservation\n5. Exit\n"))

                        if reservation_option == 1:
                            boat_id = int(input("Enter the boat ID: "))
                            customer_id = int(input("Enter the customer ID: "))
                            duration = input("Enter the duration (in hrs): ")

                            # Get the current date and time
                            current_datetime = datetime.datetime.now()
                            # print(current_datetime)

                            # Extract the date and time components into separate variables
                            current_date = str(current_datetime.date())
                            current_time = str(current_datetime.time())

                            # print(current_date + "\t\t" + current_time)

                            reservation.add_reservation(boat_id, customer_id, current_date, duration, current_time)
                        elif reservation_option == 2:
                            view_reservation = int(input("1. View one Reservation\t\t2. View all the reservations\n"))
                            if view_reservation == 1:
                                reservation_id = int(input("Enter the reservation id to view: "))
                                reservation.fetch_reservation(reservation_id)
                            else:
                                reservation.list_all_reservations()
                        elif reservation_option == 3:
                            reservation_id = int(input("Enter the reservation id to update: "))
                            boat_id = int(input("Enter the boat ID: "))
                            customer_id = int(input("Enter the customer ID: "))
                            duration = input("Enter the duration (in hrs): ")

                            # Get the current date and time
                            current_datetime = datetime.datetime.now()

                            # Extract the date and time components into separate variables
                            current_date = str(current_datetime.date())
                            current_time = str(current_datetime.time())

                            reservation.update_reservation(
                                reservation_id, boat_id, customer_id, current_date, duration, current_time
                            )
                        elif reservation_option == 4:
                            reservation_id = int(input("Enter the reservation id to delete: "))
                            reservation.delete_reservation(reservation_id)
                        else:
                            if reservation_option != 5:
                                print("Invalid Selection, please try again\n")
                            else:
                                break
                else:
                    if user_input != 4:
                        print("Invalid Selection, please try again\n")
                    else:
                        break


menu = Menu()
menu.main()
