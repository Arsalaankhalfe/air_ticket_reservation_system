import mysql.connector

db = mysql.connector.connect(
    user='root',
    password='Arsalaan@2020',
    host='localhost',
    database="booking_system"
)

cursor = db.cursor()

def register_customer():
    try:
        name = input("Enter full name: ")
        email = input("Enter email ID: ")
        gender = input("Enter gender (male/female/other): ")
        journey_date = input("Enter journey date (YYYY-MM-DD): ")

        cursor.execute("""
            INSERT INTO passenger (name, email, gender, journey_date)
            VALUES (%s, %s, %s, %s)
        """, (name, email, gender, journey_date))

        db.commit()
        print("Customer registered successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def view_class_types():
    cursor.execute("SELECT * FROM ticket_class")
    for row in cursor.fetchall():
        print(f"Class ID: {row[0]}, Name: {row[1]}, Price per passenger: ₹{row[2]}")

def calculate_ticket_price():
    view_class_types()
    try:
        class_id = int(input("Enter the class ID: "))
        passengers = int(input("Enter number of passengers: "))
        cursor.execute("SELECT price FROM classtype WHERE classid = %s", (class_id,))
        price = cursor.fetchone()

        if price:
            print(f"Total ticket cost for {passengers} passenger(s): ₹{price[0] * passengers}")
        else:
            print("Invalid class ID.")
    except ValueError:
        print("Please enter valid numbers.")

def view_food_menu():
    cursor.execute("SELECT * FROM food")
    for row in cursor.fetchall():
        print(f"Food ID: {row[0]}, Item: {row[1]}, Price: ₹{row[2]}")

def order_food():
    total_cost = 0
    view_food_menu()

    while input("\nWould you like to order food? (y/n): ").lower() == 'y':
        try:
            food_id = int(input("Enter Food ID: "))
            qty = int(input("Enter quantity: "))
            cursor.execute("SELECT price FROM food WHERE food_id = %s", (food_id,))
            price = cursor.fetchone()

            if price:
                total_cost += price[0] * qty
                print(f"Added ₹{price[0] * qty} to bill.")
            else:
                print("Invalid Food ID.")
        except ValueError:
            print("Please enter valid numbers.")

    print(f"Total food bill: ₹{total_cost}")

def calculate_luggage_bill():
    cursor.execute("SELECT * FROM luggage")
    for row in cursor.fetchall():
        print(f"Max Weight: {row[1]}kg, Rate: ₹{row[2]} per kg")

    try:
        weight = int(input("Enter luggage weight in kg: "))
        cursor.execute("SELECT rate FROM luggage WHERE weight = %s", (weight,))
        rate = cursor.fetchone()

        if rate:
            print(f"Total luggage charge: ₹{weight * rate[0]}")
        else:
            print("Invalid luggage weight.")
    except ValueError:
        print("Please enter a valid number.")

def calculate_total():
    calculate_ticket_price()
    order_food()
    calculate_luggage_bill()

def menu():
    while True:
        print("""
        ==== Air Ticket Booking Menu ====
        1. Register a new customer
        2. View travel class types
        3. Calculate ticket price
        4. View food menu
        5. Order food
        6. Calculate luggage charges
        7. Calculate total cost
        8. Cancel ticket
        9. Exit system
        """)

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            register_customer()
        elif choice == '2':
            view_class_types()
        elif choice == '3':
            calculate_ticket_price()
        elif choice == '4':
            view_food_menu()
        elif choice == '5':
            order_food()
        elif choice == '6':
            calculate_luggage_bill()
        elif choice == '7':
            calculate_total()
        elif choice == '8':
            print("Ticket cancelled successfully.")
        elif choice == '9':
            print("Thanks for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

menu()
db.close()