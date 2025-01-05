#Group 6
#TP079880 TP081807, TP080934
def shipping_management_main():
    print("Welcome to the Shipping Management System")
    while True:
        print("\nFeatures Menu")
        print("1. User Main")
        print("2. Admin Main")
        print("3. Driver Main")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            user_main()
        elif choice == "2":
            admin_menu()
        elif choice == "3":
            driver_main()
        elif choice == "4":
            print("Thank you for using the Shipping Management System!")
            break
        else:
            print("Invalid choice. Please try again.")

def get_next_order_number(username):
    """Get the user's next order number"""
    user_order_file = f"{username}_order_history.txt"
    try:
        with open(user_order_file, "r") as file:
            orders = file.readlines()
            if not orders:
                return 1  # Return 1 if there is no order
            last_order = orders[-1].strip()
            order_number_part = last_order.split("Order number: ")
            if len(order_number_part) > 1:
                last_order_number = int(order_number_part[-1].strip())
                return last_order_number + 1
            else:
                return 1
    except FileNotFoundError:
        return 1


def make_order(username):
    """user-ordered"""
    # Select cargo size
    size = int(input('Choose the consignment size:\n1. small parcel\n2. bulk order\n3. special cargo\nPlease enter the number(1-3): '))
    size = {1: "small parcel", 2: "bulk order", 3: "special cargo"}.get(size, None)
    if not size:
        print('Invalid choice. Please try again.')
        return make_order(username)

    # Enter the weight and select the means of transportation
    weight = int(input('Enter the weight of parcel (kg): '))
    if weight <= 10:
        vehicle = "Motorcycle"
    elif 10 < weight <= 50:
        vehicle = "Van"
    elif 50 < weight <= 100:
        vehicle = "Truck"
    else:
        print('Invalid weight. Please try again.')
        return make_order(username)

    # Select Package Type
    package = int(input('Choose the package you want:\n1. Normal package\n2. Special package\n*Special package including liquid and glass.\nPlease enter the number (1/2): '))
    package = {1: "Normal package", 2: "Special package"}.get(package, None)
    if not package:
        print('Invalid choice. Please try again.')
        return make_order(username)

    # Enter Address
    while True:
        address = input("Please enter the address:\n")
        if len(address.split()) < 100:
            break
        else:
            print("Your address is too long. Please limit it to 100 words.")

    # Select Payment Method
    order_payment = int(input('Choose the payment method:\n1. credit/debit card\n2. UPI\n3. Mobile wallet\n4. Cash\n5. Other\nPlease enter the number (1-5): '))
    if 1 <= order_payment <= 5:
        order_payment = "Done payment"
    else:
        print('Invalid choice. Please try again.')
        return make_order(username)

    # Enter order time
    order_time = input("Please enter the order time (YYYY-MM-DD HH:MM): ")

    # Get order number and generate order information
    order_number = get_next_order_number(username)
    order = f"{order_payment} | {size}, {vehicle}, {package}, {address}, {order_time}. Order number: {order_number}"

    # Write order information to user files
    user_order_file = f"{username}_order_history.txt"
    with open(user_order_file, "a") as file:
        file.write(f"{order}\n")

    print(f"{order_payment}\nOrder checking: {size}, {vehicle}, {package}, {address}, Order time: {order_time}. This is order number {order_number}")
    user_menu(username)


def check_order(username):
    """View Order with Delivery Status"""
    user_order_file = f"{username}_order_history.txt"
    driver_deliveries_file = "driver_deliveries.txt"

    # Read user orders
    try:
        with open(user_order_file, "r") as file:
            orders = file.readlines()
    except FileNotFoundError:
        print("No orders found.")
        return

    if not orders:
        print("No orders found.")
        return

    # Read driver deliveries
    delivery_status = {}
    try:
        with open(driver_deliveries_file, "r") as file:
            for line in file:
                parts = line.strip().split(", ")
                order_info = {}
                for part in parts:
                    if ": " in part:
                        key, value = part.split(": ", 1)
                        order_info[key.strip()] = value.strip()
                user = order_info.get("User", "")
                status = order_info.get("Status", "Unknown")
                delivery_status[user] = status
    except FileNotFoundError:
        print("Delivery status file not found. Delivery status will not be shown.")

    # Display orders with delivery status
    print("\nYour Order History:")
    print(f"{'Order Number':<15} {'Payment Status':<15} {'Consignment Size':<20} {'Vehicle Type':<15} {'Package Type':<20} {'Address':<65} {'Order Time':<20} {'Delivery Status':<15}")
    print("=" * 195)

    for order in orders:
        parts = order.strip().split(" | ")
        if len(parts) < 2:
            print(f"Invalid order format: {order.strip()}, skipping this entry.")
            continue

        payment_status = parts[0]
        details = parts[1].split(", ")
        if len(details) < 5:
            print(f"Insufficient details in order: {order.strip()}, skipping this entry.")
            continue

        consignment_size = details[0]
        vehicle_type = details[1]
        package_type = details[2]
        address = ",".join(details[3:-1])
        order_time = details[4].split(". Order number:")[0]
        order_number = details[-1].split(": ")[-1]
        delivery_status_text = delivery_status.get(username, "Unknown")

        print(f"{order_number:<15} {payment_status:<15} {consignment_size:<20} {vehicle_type:<15} {package_type:<20} {address:<65} {order_time:<20} {delivery_status_text:<15}")

    user_menu(username)
  

def cancel_order(username):
    """Cancel Order Function"""
    user_order_file = f"{username}_order_history.txt"
    try:
        with open(user_order_file, "r") as file:
            orders = file.readlines()
    except FileNotFoundError:
        print("No orders to cancel.")
        user_menu(username)
        return

    if not orders:
        print("No orders to cancel.")
        user_menu(username)
        return

    print("Your Order History:")
    for idx, order in enumerate(orders, start=1):
        print(f"{idx}. {order.strip()}")

    try:
        order_to_cancel = int(input("Enter the order number you want to cancel: "))
        order_found = False

        for order in orders:
            if f"Order number: {order_to_cancel}" in order:
                orders.remove(order)
                order_found = True
                break

        if order_found:
            with open(user_order_file, "w") as file:
                file.writelines(orders)
            print(f"Order number {order_to_cancel} canceled successfully.")
        else:
            print("Invalid order number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

    user_menu(username)


def re_order(username):
    make_order(username)

def review(username):
    file_name = "reviews.txt"

    while True:
        # Get a valid rating from the user
        while True:
            try:
                rating = int(input("Please rate from 1 to 5 stars: "))
                if 1 <= rating <= 5:
                    print(f"Thank you for your rating of {rating} stars!")
                    break
                else:
                    print("Please enter a valid option between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")

        # Get a comment from the user
        while True:
            command = input("Please share your comments about our service (or type 'exit' to quit): ").strip()

            if command.lower() == 'exit':
                print("Exiting the review section.")
                return

            words = command.split()

            if len(words) > 100:
                print("Your comment is too long. Please limit it to 100 words.")
            else:
                print("Thanks for your comment!")
                break

        # Save the rating and comment to the file
        with open(file_name, "a") as file:
            file.write(f"Username: {username}\n")
            file.write(f"Rating: {rating}\n")
            file.write(f"Comment: {command}\n")
            file.write("---\n")

        # Ask if the user wants to submit another review
        another_review = input("Would you like to submit another review? (yes/no): ").strip().lower()
        if another_review == 'no':
            print("Exiting the review section.")
            break
        elif another_review != 'yes':
            print("Invalid option. Exiting the review section.")
            break


def user_menu(username):
    while True:
        menu = int(input(f"Welcome {username}! Order management:\n"
                         "1-Make Orders\n"
                         "2-Check Orders\n"
                         "3-Cancel Orders\n"
                         "4-Reorder\n"
                         "5-Rating and Review\n"
                         "6-Exit\n"
                         "Please enter the number: "))
        if menu == 1:
            make_order(username)
        elif menu == 2:
            check_order(username)
        elif menu == 3:
            cancel_order(username)
        elif menu == 4:
            re_order(username)
        elif menu == 5:
            review(username)
        elif menu == 6:
            print("Thank you")
            user_main()
        else:
            print("Please Choose A Valid Option.")

def sign_up():
    """User Registration"""
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    try:
        with open("users.txt", "r") as file:
            users = file.readlines()
            for user in users:
                existing_username, _ = user.strip().split(',')
                if existing_username == username:
                    print("Username already signed up. Try a different one.")
                    return user_main()
    except FileNotFoundError:
        pass

    with open("users.txt", "a") as file:
        file.write(f"{username},{password}\n")
    print("Sign-up successful.")
    user_menu(username)


def log_in():
    """user login"""
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        with open("users.txt", "r") as file:
            users = file.readlines()
            for user in users:
                existing_username, existing_password = user.strip().split(',')
                if existing_username == username and existing_password == password:
                    print("Login successful!")
                    user_menu(username)
                    return
            print("Invalid username or password.")
            user_main()
    except FileNotFoundError:
        print("No users found. Please sign up first.")
        user_main()

def user_main():
    while True:
        choice = input("Choose an option:\n1. Log in\n2. Sign up\n3. Exit\nEnter your choice (1/2/3): ")
        if choice == '1':
            log_in()
        elif choice == '2':
            sign_up()
        elif choice == '3':
            print("Goodbye!")
            shipping_management_main()
        else:
            print("Invalid choice. Please try again.")

def get_valid_float(prompt):
    """Get valid floating point input"""
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Invalid input, please enter a number.")


# Initialization of the graph (representing distances between different locations)
def load_graph_from_file(file_name):
    """Loads graph data from a specified file."""
    graph = {}
    try:
        with open(file_name, 'r') as file:
            for line in file:
                if line.strip():  # Ignore empty lines
                    start, end, distance = line.strip().split(',')
                    distance = float(distance)
                    if start not in graph:
                        graph[start] = {}
                    graph[start][end] = distance
    except FileNotFoundError:
        print(f"File '{file_name}' not found. Starting with an empty graph.")
    return graph

# Load the graph from the file
graph = load_graph_from_file("routes.txt")

# Simple Dijkstra algorithm（No any library）
def read_routes_from_txt(file_name):
    """Reads route information from a .txt file."""
    routes = {}
    try:
        with open(file_name, 'r') as file:
            for line in file:
                if line.strip():  # Ignore empty lines
                    parts = line.strip().split(',')
                    if len(parts) == 3:  # Ensure there are exactly 3 parts
                        start, end, distance = parts
                        if start not in routes:
                            routes[start] = {}
                        routes[start][end] = float(distance)
                    else:
                        print(f"Skipping invalid line: {line.strip()}")
    except FileNotFoundError:
        print(f"File '{file_name}' not found. Starting with an empty route list.")
    return routes

def write_route_to_txt(file_name, start, end, distance):
    """Appends a new route to the .txt file."""
    with open(file_name, 'a') as file:
        file.write(f"{start},{end},{distance}\n")

def add_route(file_name):
    """Adds a new route to the text file."""
    print("\n--- Add Route Information ---")
    start = input("Enter starting location: ").strip()
    end = input("Enter destination: ").strip()
    try:
        distance = float(input("Enter distance (in km): ").strip())
    except ValueError:
        print("Invalid distance. Please enter a numeric value.")
        return

    write_route_to_txt(file_name, start, end, distance)
    print(f"Route added: {start} -> {end} ({distance} km)")

def view_routes(file_name):
    """Displays all routes stored in the text file."""
    print("\n--- All Routes ---")
    routes = read_routes_from_txt(file_name)
    if not routes:
        print("No routes available.")
        return

    for start, destinations in routes.items():
        for end, distance in destinations.items():
            print(f"Start: {start}, End: {end}, Distance: {distance} km")

def dijkstra(graph, start, end):
    """Calculating the shortest path using Dijkstra's algorithm"""
    distances = {}
    for node in graph:
        distances[node] = float('inf')
    distances[start] = 0

    previous_nodes = {}
    for node in graph:
        previous_nodes[node] = None

    unvisited = set(graph.keys())

    while unvisited:
        current_node = None

        # Find the node with the smallest distance among the unvisited nodes
        for node in unvisited:
            if current_node is None or distances[node] < distances[current_node]:
                current_node = node

        if current_node is None or distances[current_node] == float('inf'):
            break

        unvisited.remove(current_node)

        # Update the distance of neighboring nodes
        for neighbor, weight in graph[current_node].items():
            new_distance = distances[current_node] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node

    # Backtracking paths
    path = []
    current = end
    while current:
        path.insert(0, current)
        current = previous_nodes[current]

    if distances[end] == float('inf'):
        return float('inf'), []
    return distances[end], path


def route_and_fuel_management(file_name):
    """Manages routes and calculates costs."""
    print("\n--- Route and Fuel Management ---")
    routes = read_routes_from_txt(file_name)

    if not routes:
        print("No routes available. Please add routes first.")
        return

    start = input("Enter the start location: ").strip()
    end = input("Enter the destination location: ").strip()

    # Check if both start and end locations are in the graph
    if start not in routes or end not in routes:
        print("Invalid locations entered. Please try again.")
        return

    # Proceed with Dijkstra's algorithm if locations are valid
    distance, path = dijkstra(routes, start, end)
    if distance == float('inf'):
        print(f"No route found from {start} to {end}.")
    else:
        print(f"Shortest distance: {distance} km")
        print(f"Path: {' -> '.join(path)}")

# Admin menu
FILE_NAME = "routes.txt"

def get_vehicle_prices():
    """Return vehicle prices per kilometer."""
    return {
        "Motorcycle": 2.0,  # Price per km for normal goods
        "Van": 5.0,
        "Truck": 8.0
    }

def get_fuel_price():
    """Return the current fuel price."""
    return 2.15  # Price per liter of fuel

def get_special_goods_info():
    """Return special goods surcharge percentage and valid types."""
    return 1.2, ["normal", "fragile", "hazardous", "perishable"]

def choose_vehicle_by_weight(weight):
    """Choose the appropriate vehicle based on the weight of the cargo."""
    vehicle_prices = get_vehicle_prices()
    if weight <= 10:
        return "Motorcycle", vehicle_prices["Motorcycle"]
    elif 10 < weight <= 100:
        return "Van", vehicle_prices["Van"]
    else:
        return "Truck", vehicle_prices["Truck"]

def calculate_fuel_cost(distance, vehicle_type):
    """Calculate fuel used and cost based on distance and vehicle type."""
    fuel_efficiency_mapping = {
        "Motorcycle": 35,
        "Van": 15,
        "Truck": 8
    }
    fuel_efficiency = fuel_efficiency_mapping.get(vehicle_type, 0)
    if fuel_efficiency == 0:
        raise ValueError("Invalid vehicle type for fuel efficiency calculation.")
    
    fuel_price = get_fuel_price()  # Retrieve current fuel price
    fuel_used = distance / fuel_efficiency
    fuel_cost = fuel_used * fuel_price
    return fuel_used, fuel_cost

def calculate_transport_cost(distance, price_per_km):
    """Calculate transport cost based on distance and price per kilometer."""
    return distance * price_per_km

def validate_cargo_type(cargo_type):
    """Validate the cargo type input."""
    _, special_goods_types = get_special_goods_info()
    if cargo_type not in special_goods_types:
        raise ValueError("Invalid cargo type. Please enter one of the following: " + ", ".join(special_goods_types))

# Route and Cost Calculation
def route_and_cost_calculation():
    """Prompt user for route details and calculate costs."""
    print("\n--- Route and Cost Calculation ---")
    start = input("Enter the start location: ").strip()
    end = input("Enter the destination location: ").strip()
    
    # Validate distance input
    try:
        distance = get_valid_float("Please enter the distance in kilometers: ")
    except ValueError:
        print("Invalid distance. Please enter a numeric value.")
        return

    # Validate weight input
    try:
        weight = get_valid_float("Please enter the weight of the shipment in kilograms: ")
    except ValueError:
        print("Invalid weight. Please enter a numeric value.")
        return

    # Validate cargo type input
    cargo_type = input("Enter the type of cargo (normal, fragile, hazardous, perishable): ").strip().lower()
    try:
        validate_cargo_type(cargo_type)
    except ValueError as e:
        print(e)
        return

    # Choose vehicle
    vehicle_type, price_per_km = choose_vehicle_by_weight(weight)

    # Apply special goods surcharge
    surcharge_percentage, special_goods_types = get_special_goods_info()
    if cargo_type in special_goods_types and cargo_type != "normal":
        price_per_km *= surcharge_percentage

    # Calculate fuel and transport costs
    fuel_used, fuel_cost = calculate_fuel_cost(distance, vehicle_type)
    transport_cost = calculate_transport_cost(distance, price_per_km)

    # Output results
    print(f"\nRoute: {start} -> {end}")
    print(f"Distance: {distance} km")
    print(f"Vehicle: {vehicle_type}")
    print(f"Fuel Used: {fuel_used:.2f} liters")
    print(f"Fuel Cost: RM{fuel_cost:.2f}")
    print(f"Transport Cost: RM{transport_cost:.2f}")

vehicles = {}

def load_vehicles_from_file(vehicle_file):
    """Load vehicles from a text file."""
    vehicles = {}
    try:
        with open(vehicle_file, 'r') as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) != 4:
                        print(f"Skipping line due to incorrect format: {line.strip()}")
                        continue
                    vehicle_id, vehicle_type, performance_rating, inspection_due = parts
                    vehicles[vehicle_id] = {
                        "type": vehicle_type,
                        "performance_rating": float(performance_rating),
                        "maintenance_history": [],
                        "inspection_due": inspection_due.lower() == 'true'
                    }
    except FileNotFoundError:
        print(f"File '{vehicle_file}' not found. Starting with an empty fleet.")
    return vehicles

def load_maintenance_history(maintenance_file, vehicles):
    """Load maintenance history from a text file."""
    try:
        with open(maintenance_file, 'r') as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) < 3:
                        print(f"Skipping line due to incorrect format: {line.strip()}")
                        continue
                    vehicle_id, date, description = parts
                    if vehicle_id in vehicles:
                        vehicles[vehicle_id]["maintenance_history"].append((date, description))
    except FileNotFoundError:
        print(f"File '{maintenance_file}' not found. No maintenance history loaded.")

def save_vehicles_to_file(vehicle_file, vehicles):
    """Save vehicles to a text file."""
    with open(vehicle_file, 'w') as file:
        for vehicle_id, details in vehicles.items():
            inspection_due = 'true' if details["inspection_due"] else 'false'
            file.write(f"{vehicle_id},{details['type']},{details['performance_rating']},{inspection_due}\n")

def add_vehicle(vehicle_id, vehicle_type, performance_rating, vehicles, vehicle_file):
    """Add a new vehicle to the fleet."""
    if vehicle_id in vehicles:
        print("Vehicle ID already exists.")
    else:
        vehicles[vehicle_id] = {
            "type": vehicle_type,
            "performance_rating": performance_rating,
            "maintenance_history": [],
            "inspection_due": False
        }
        print(f"Vehicle {vehicle_id} added successfully.")
        save_vehicles_to_file(vehicle_file, vehicles)
        
def log_vehicle_maintenance(vehicle_id, date, description, mileage, inspection_due, vehicles, maintenance_file, vehicle_file):
    """Log maintenance for a specific vehicle and set inspection alert."""
    if vehicle_id in vehicles:
        maintenance_record = (date, f"{description}. Mileage: {mileage} kilometers.")
        vehicles[vehicle_id]["maintenance_history"].append(maintenance_record)
        vehicles[vehicle_id]["inspection_due"] = inspection_due
        print(f"Maintenance logged for vehicle {vehicle_id}. Inspection due status set to {'Yes' if inspection_due else 'No'}.")
        save_maintenance_history(maintenance_file, vehicles)
        save_vehicles_to_file(vehicle_file, vehicles)
    else:
        print("Vehicle ID not found.")
        
def save_maintenance_history(maintenance_file, vehicles):
    """Save maintenance history to a text file."""
    with open(maintenance_file, 'w') as file:
        for vehicle_id, details in vehicles.items():
            for date, description in details["maintenance_history"]:
                file.write(f"{vehicle_id},{date},{description}\n")

def view_all_vehicles(vehicles):
    """View all vehicles in the fleet."""
    if not vehicles:
        print("No vehicles in the fleet.")
    else:
        for vehicle_id, details in vehicles.items():
            print(f"Vehicle ID: {vehicle_id}, Type: {details['type']}, Performance Rating: {details['performance_rating']}, Inspection Due: {'Yes' if details['inspection_due'] else 'No'}")
            print("-" * 30)

def view_maintenance_history():
    """View maintenance history for all vehicles."""
    try:
        with open('maintenance_history.txt', 'r') as file:
            maintenance_records = file.readlines()
        
        if not maintenance_records:
            print("No maintenance history available.")
            return

        print("\n--- Maintenance History ---")
        for record in maintenance_records:
            parts = record.strip().split(',')
            if len(parts) < 3:
                print(f"Skipping invalid record: {record.strip()}")
                continue
            
            vehicle_id = parts[0].strip()
            date = parts[1].strip()
            description = parts[2].strip()
            print(f"Vehicle ID: {vehicle_id}, Date: {date}, Description: {description}")

    except FileNotFoundError:
        print("No maintenance history file found.")

def view_single_vehicle_maintenance_history(vehicle_id, vehicles):
    """View maintenance history for a single vehicle."""
    if vehicle_id in vehicles:
        print(f"\n--- Maintenance History for Vehicle ID: {vehicle_id} ---")
        if vehicles[vehicle_id]["maintenance_history"]:
            for date, description in vehicles[vehicle_id]["maintenance_history"]:
                print(f" - Date: {date}, Description: {description}")
        else:
            print("No maintenance history available for this vehicle.")
    else:
        print("Vehicle ID not found.")

file_name = "vehicles.txt"  
load_vehicles_from_file(file_name)

# Load routes from a file
def load_graph_from_file(file_name):
    """Loads graph data from a specified file."""
    graph = {}
    try:
        with open(file_name, 'r') as file:
            for line in file:
                if line.strip():  # Ignore empty lines
                    start, end, distance = line.strip().split(',')
                    distance = float(distance)
                    if start not in graph:
                        graph[start] = {}
                    graph[start][end] = distance
    except FileNotFoundError:
        print(f"File '{file_name}' not found. Starting with an empty graph.")
    return graph

# Load the graph from the file
graph = load_graph_from_file("routes.txt")

def check_user_orders(user_file):
    """View orders for a specific user."""
    try:
        with open(user_file, "r") as file:
            orders = file.readlines()
    except FileNotFoundError:
        print("No orders found.")
        return

    if not orders:
        print("No orders found.")
        return

    print("\nUser Order History:")
    print(f"{'Order Number':<15} {'Payment Status':<15} {'Consignment Size':<20} {'Vehicle Type':<15} {'Package Type':<20} {'Address':<65} {'Order Time':<20}")
    print("=" * 170)

    for order in orders:
        parts = order.strip().split(" | ")
        if len(parts) < 2:
            print(f"Invalid order format: {order.strip()}, skipping this entry.")
            continue

        payment_status = parts[0]
        details = parts[1].split(", ")

        if len(details) < 5:
            print(f"Insufficient details in order: {order.strip()}, skipping this entry.")
            continue

        consignment_size = details[0]
        vehicle_type = details[1]
        package_type = details[2]
        address = ",".join(details[3:-1])
        order_time = details[4].split(". Order number:")[0]
        order_number = details[-1].split(": ")[-1]

        print(f"{order_number:<15} {payment_status:<15} {consignment_size:<20} {vehicle_type:<15} {package_type:<20} {address:<65} {order_time:<20}")
    admin_menu()

    
def view_driver_deliveries():
    print("\n--- Driver Deliveries Overview ---")
    try:
        with open('driver_deliveries.txt', 'r') as file:
            for line in file:
                if line.strip():  # Check if the line is not empty
                    # Initialize variables
                    driver_id = None
                    status = None
                    pickup_time = None
                    delivery_time = None
                    
                    # Split the line by commas
                    parts = line.strip().split(',')
                    
                    # Loop through parts to find Driver ID, Status, Pickup Time, and Expected Delivery Time
                    for part in parts:
                        part = part.strip()  # Remove leading/trailing whitespace
                        if 'Driver ID:' in part:
                            driver_id = part.split(':')[1].strip()  # Get the value after 'Driver ID:'
                        elif 'Status:' in part:
                            status = part.split(':')[1].strip()  # Get the value after 'Status:'
                        elif 'Pickup Time:' in part:
                            pickup_time = part.split(':')[1].strip()  # Get the value after 'Pickup Time:'
                        elif 'Expected Delivery Time:' in part:
                            delivery_time = part.split(':')[1].strip()  # Get the value after 'Expected Delivery Time:'
                    
                    # Check if all required fields were found
                    if driver_id is not None and status is not None and pickup_time is not None and delivery_time is not None:
                        print(f"Driver ID: {driver_id}, Status: {status}, Pickup Time: {pickup_time}, Expected Delivery Time: {delivery_time}")
                    else:
                        print(f"Skipping line due to missing information: {line.strip()}")
    except FileNotFoundError:
        print("No delivery status file found.")

# Admin menu
def admin_menu():
    VEHICLE_FILE_NAME = "vehicles.txt"
    vehicles = load_vehicles_from_file(VEHICLE_FILE_NAME)
    ROUTE_FILE_NAME = "routes.txt"
    MAINTENANCE_HISTORY_FILE_NAME = "maintenance_history.txt"
    
    # Load vehicles from file at the start of the admin menu
    load_vehicles_from_file(VEHICLE_FILE_NAME)
    load_maintenance_history(MAINTENANCE_HISTORY_FILE_NAME, vehicles)

    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Vehicle")
        print("2. Log Vehicle Maintenance")
        print("3. View All Vehicle")
        print("4. View Maintenance History")
        print("5. View Single Vehicle Maintenance History")
        print("6. Add Route Information")
        print("7. View All Routes")
        print("8. Route and Fuel Management")
        print("9. Route and Cost Calculation")
        print("10. Check User Order History")
        print("11. View Driver Deliveries")
        print("12. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            vehicle_id = input("Enter Vehicle ID: ")
            vehicle_type = input("Enter Vehicle Type: ")
            performance_rating = float(input("Enter Performance Rating: "))
            add_vehicle(vehicle_id, vehicle_type, performance_rating, vehicles, VEHICLE_FILE_NAME)
            
        elif choice == '2':
            vehicle_id = input("Enter Vehicle ID: ")
            date = input("Enter Maintenance Date (YYYY-MM-DD): ")
            description = input("Enter Maintenance Description: ")
            mileage = float(input("Enter Mileage: "))
            inspection_due = input("Is inspection due? (yes/no): ").lower() == 'yes'
            log_vehicle_maintenance(vehicle_id, date, description, mileage, inspection_due, vehicles, MAINTENANCE_HISTORY_FILE_NAME, VEHICLE_FILE_NAME)
            
        elif choice == '3':
            view_all_vehicles(vehicles)
            
        elif choice == '4':
            view_maintenance_history()
            
        elif choice == '5':
            vehicle_id = input("Enter Vehicle ID to view maintenance history: ")
            view_single_vehicle_maintenance_history(vehicle_id, vehicles)
            
        elif choice == '6':
            add_route(ROUTE_FILE_NAME)
            
        elif choice == '7':
            view_routes(ROUTE_FILE_NAME)
            
        elif choice == '8':
            route_and_fuel_management(ROUTE_FILE_NAME)
            
        elif choice == '9':
            route_and_cost_calculation()
            
        elif choice == '10':
            username = input("Enter the username of the user whose orders you want to check: ")
            user_file = f"{username}_order_history.txt"  # Construct the user order file name
            check_user_orders(user_file)  # Pass the user file to the function
            
        elif choice == '11':
            view_driver_deliveries()
            
        elif choice == '12':
            # Save vehicles to file before exiting
            save_vehicles_to_file(VEHICLE_FILE_NAME, vehicles)
            save_maintenance_history(MAINTENANCE_HISTORY_FILE_NAME, vehicles)
            print("\nExiting Admin Menu. Goodbye!")
            shipping_management_main()
        else:
            print("\nInvalid choice. Please try again.")

# Driver Management System

drivers = {}

# Function to read data from a file
def read_file(file_name):
    data = []
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    row = []
                    in_quotes = False
                    current_field = []
                    for char in line.strip():
                        if char == '"':  # Toggle in_quotes when encountering a quote
                            in_quotes = not in_quotes
                        elif char == ',' and not in_quotes:  # If a comma is outside quotes, split field
                            row.append(''.join(current_field).strip())
                            current_field = []
                        else:  # Add character to the current field
                            current_field.append(char)
                    row.append(''.join(current_field).strip())  # Append the last field
                    data.append(row)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")  # Handle file not found error
    return data

# Function to write data to a file
def write_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        for entry in data:
            escaped_entry = []
            for field in entry:
                if ',' in field or '"' in field:  # Escape fields containing commas or quotes
                    field = '"' + field.replace('"', '""') + '"'  # Double quotes inside the field
                escaped_entry.append(field)
            file.write(','.join(escaped_entry) + '\n')

# Function to append a single row to a file
def append_file(file_name, new_entry):
    with open(file_name, 'a', encoding='utf-8') as file:
        escaped_entry = []
        for field in new_entry:
            if ',' in field or '"' in field:  # Escape fields containing commas or quotes
                field = '"' + field.replace('"', '""') + '"'  # Double quotes inside the field
            escaped_entry.append(field)
        file.write(','.join(escaped_entry) + '\n')

# Main driver management system menu
def driver_main():
    print("Welcome to the Driver Management System")

    while True:
        print("\nMain Menu")
        print("1. Driver Login")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            driver_id = driver_login()  # Handle driver login
            if driver_id:
                driver_menu(driver_id)  # Show driver menu if login is successful
        elif choice == '2':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Driver login menu
def driver_login():
    while True:
        print("\nDriver Login")
        print("1. Login")
        print("2. Create New Profile")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            profiles = read_file('drivers.txt')  # Read profiles from file
            driver_id = input("Enter your Driver ID: ")

            for profile in profiles:
                if profile[0] == driver_id:  # Check if driver ID exists
                    print(f"Welcome, {profile[1]}!")
                    return driver_id
            print("Invalid Driver ID. Please try again.")
        elif choice == '2':
            add_new_profile()  # Create a new driver profile
        elif choice == '3':
            print("Exiting login system.")
            return None
        else:
            print("Invalid choice. Please try again.")

# Driver menu after login
def driver_menu(driver_id):
    while True:
        print("\nDriver Main Menu")
        print("1. Profile Management")
        print("2. Delivery Management")
        print("3. Route Management")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            profile_menu(driver_id)  # Manage driver profile
        elif choice == '2':
            delivery_menu(driver_id)  # Manage deliveries
        elif choice == '3':
            route_menu(driver_id)  # Manage routes
        elif choice == '4':
            print("Exiting Driver Menu.")
            break
        else:
            print("Invalid choice. Please try again.")

# Profile management menu
def profile_menu(driver_id):
    while True:
        print("\nProfile Management Menu")
        print("1. View Profile")
        print("2. Update Profile")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            view_profile(driver_id)  # View driver profile
        elif choice == '2':
            update_profile(driver_id)  # Update driver profile
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

# Function to view user orders
def view_user_orders(username):
    user_order_file = f"{username}_order_history.txt"
    print(f"Looking for file: {user_order_file}")
    try:
        with open(user_order_file, "r") as file:
            orders = file.readlines()
    except FileNotFoundError:
        print("No orders found.")
        return

    if not orders:
        print("No orders found.")
        return

    print("\nUser Order History:")
    print(
        f"{'Order Number':<15} {'Payment Status':<15} {'Consignment Size':<20} {'Vehicle Type':<15} {'Package Type':<20} {'Address':<65} {'Order Time':<20}")
    print("=" * 170)

    for order in orders:
        parts = order.strip().split(" | ")
        if len(parts) < 2:
            print(f"Invalid order format: {order.strip()}, skipping this entry.")
            continue

        payment_status = parts[0]
        details = parts[1].split(", ")

        if len(details) < 5:
            print(f"Insufficient details in order: {order.strip()}, skipping this entry.")
            continue

        consignment_size = details[0]
        vehicle_type = details[1]
        package_type = details[2]
        address = ",".join(details[3:-1])
        order_time = details[4].split(". Order number:")[0]
        order_number = details[-1].split(": ")[-1]

        print(
            f"{order_number:<15} {payment_status:<15} {consignment_size:<20} {vehicle_type:<15} {package_type:<20} {address:<65} {order_time:<20}")

# Function to manage deliveries
def manage_delivery(driver_id, username):
    """Manage order dispatch and update delivery details for a user."""
    # Construct the filename for the user's order history
    user_order_file = f"{username}_order_history.txt"

    # Read the user's order history file
    try:
        with open(user_order_file, "r") as file:
            orders = file.readlines()
    except FileNotFoundError:
        print("No order history found for this user.")
        return

    # Check if the orders file is empty
    if not orders:
        print("No orders found.")
        return

    # Header for order details
    print("\nConsignment/Shipment Details:")
    print(
        f"{'Order Number':<15} {'Payment Status':<15} {'Consignment Size':<20} {'Vehicle Type':<15} {'Package Type':<20} {'Address':<65} {'Order Time':<20}")
    print("=" * 170)

    # Process each order in the order history
    for order in orders:
        parts = order.strip().split(" | ")  # Split the order details into parts
        if len(parts) < 2:
            print(f"Invalid order format: {order.strip()}, skipping this entry.")
            continue

        payment_status = parts[0]
        details = parts[1].split(", ")  # Split the details

        # Ensure all required details are present
        if len(details) < 5:
            print(f"Insufficient details in order: {order.strip()}, skipping this entry.")
            continue

        # Extract individual details
        consignment_size = details[0]
        vehicle_type = details[1]
        package_type = details[2]
        address = ",".join(details[3:-1])
        order_time = details[4]
        order_number = details[-1].split(": ")[-1]  # Extract the order number

        # Print the formatted order details
        print(
            f"{order_number:<15} {payment_status:<15} {consignment_size:<20} {vehicle_type:<15} {package_type:<20} {address:<65} {order_time:<20}")

    # Get pickup and delivery times
    pickup_time = input("\nEnter pickup time (YYYY-MM-DD HH:MM): ").strip()
    delivery_time = input("Enter expected delivery time (YYYY-MM-DD HH:MM): ").strip()

    # Validate and get the delivery status
    while True:
        delivery_status = input("Enter delivery status (in transit/completed): ").strip().lower()
        if delivery_status in ["in transit", "completed"]:
            break
        print("Invalid status. Please enter 'in transit' or 'completed'.")

    # Append the updated delivery details to the file
    with open('driver_deliveries.txt', 'a') as file:
        file.write(
            f"Driver ID: {driver_id}, User: {username}, Pickup Time: {pickup_time}, Expected Delivery Time: {delivery_time}, Status: {delivery_status}\n"
        )

    print(f"\nDelivery details for driver {driver_id} updated successfully.")

# Function for delivery menu
def delivery_menu(driver_id):
    """Display the delivery management menu for drivers."""
    while True:
        # Print menu options for delivery management
        print("\nDelivery Management Menu")
        print("1. Update and View Delivery Status")
        print("2. View User Orders")
        print("3. Back to Main Menu")

        # Get user choice from the menu
        choice = input("Enter your choice: ")

        # Call the appropriate function based on the choice
        if choice == '1':
            # Prompt for username to update delivery status
            username = input("Enter the username of the user whose delivery status you want to update: ")
            manage_delivery(driver_id, username)
        elif choice == '2':
            # Prompt for username to view user orders
            username = input("Enter the username of the user whose orders you want to view: ")
            view_user_orders(username)
        elif choice == '3':
            break  # Exit the menu
        else:
            # Handle invalid menu input
            print("Invalid choice. Please try again.")

# Function for view pre-planned best route or calculate menu
def view_or_calculate_route(driver_id):
    """Choose between viewing a pre-planned route or calculating the shortest route."""
    # Present route options to the driver
    print("Choose an option:")
    print("1. View Pre-Planned Best Route")
    print("2. Calculate Shortest Route")

    # Get user choice for route management
    choice = input("Enter your choice: ")
    if choice == '1':
        # Display pre-planned route
        view_best_route()
    elif choice == '2':
        # Prompt for start and end locations to calculate the route
        start = input("Enter the start location: ").strip()
        end = input("Enter the destination location: ").strip()
        calculate_shortest_route(start, end)
    else:
        # Handle invalid input for route options
        print("Invalid choice. Please try again.")

# Function to calculate shortest route
def calculate_shortest_route(start, end):
    """Calculate and display the shortest route between two locations."""
    # Call Dijkstra's algorithm to find the shortest route
    distance, path = dijkstra(graph, start, end)
    if distance == float('inf'):
        # No route found scenario
        print(f"No route found from {start} to {end}.")
    else:
        # Display the shortest route and distance
        print(f"Shortest distance from {start} to {end}: {distance} km")
        print(f"Path: {' -> '.join(path)}")

# Function for route menu
def route_menu(driver_id):
    """Display the route management menu for drivers."""
    while True:
        # Print menu options for route management
        print("\nRoute Management Menu")
        print("1. View Or Calculate the Best Route")
        print("2. Back to Main Menu")

        # Get user choice from the route menu
        choice = input("Enter your choice: ")

        # Call the appropriate function based on the choice
        if choice == '1':
            # Manage route options
            view_or_calculate_route(driver_id)
        elif choice == '2':
            break  # Exit the menu
        else:
            # Handle invalid input for route menu
            print("Invalid choice. Please try again.")

# Function to view driver profile information
def view_profile(driver_id):
    """Display the profile details of a driver."""
    # Load driver profiles from the file
    profiles = read_file('drivers.txt')

    # Search for the driver profile in the data
    for profile in profiles:
        if profile[0] == driver_id:
            # Print driver profile details
            print("\nDriver Profile:")
            print(f"Name: {profile[1]}")
            print(f"Contact: {profile[2]}")
            print(f"Address: {profile[3]}")
            print(f"Availability: {profile[4]}")
            print(f"License: {profile[5]}")
            print(f"Health Report: {profile[6]}")
            return
    # Handle case where profile is not found
    print("Profile not found.")

# Function to update driver profile info
def update_profile(driver_id):
    """Update specific fields in a driver's profile."""
    profiles = read_file('drivers.txt')  # Load profiles from file

    for i, profile in enumerate(profiles):
        if profile[0] == driver_id:
            # Display current profile details
            print("\nCurrent Profile Details:")
            fields = ["Name", "Contact", "Address", "Availability", "License", "Health Report"]
            for idx, field in enumerate(fields, 1):
                value = profile[idx]
                print(f"{idx}. {field}: {value}")

            # Prompt user for the field to update
            field_to_update = input("Enter the number of the field you want to update: ")
            if field_to_update in ['1', '2', '3', '4', '5', '6']:
                # Update the selected field with the new value
                new_value = input("Enter the new value: ")
                profile[int(field_to_update)] = new_value
                profiles[i] = profile
                write_file('drivers.txt', profiles)  # Save updated profiles back to file
                print("Profile updated successfully.")
                return
            else:
                # Handle invalid field selection
                print("Invalid choice. Returning to menu.")
                return
    # Handle case where profile is not found
    print("Profile not found.")

# Function to add new profile
def add_new_profile():
    """Add a new driver's profile to the system."""
    profiles = read_file('drivers.txt')  # Load existing profiles from file
    print("\nEnter New Profile Details:")

    # Get and validate new driver ID
    driver_id = input("Driver ID: ")
    if any(profile[0] == driver_id for profile in profiles):
        print("Driver ID already exists. Cannot add duplicate profile.")
        return

    # Collect new profile information
    name = input("Name: ")
    contact = input("Contact: ")
    address = input("Address (full address): ")
    availability = input("Availability (Yes/No): ")
    license_status = input("License: ")
    health_report = input("Health Report: ")

    # Create and save new profile
    new_profile = [driver_id, name, contact, address, availability, license_status, health_report]
    append_file('drivers.txt', new_profile)
    print("New profile added successfully.")

# Function view pre-planned best route
def view_best_route():
    """Show the Pre-Planned route."""
    # Display predefined best routes
    print("\n---Pre-Planned Best Routes---")
    print("1. Route 1: Johor - Kuala Lumpur - Butterworth - Kedah -  Perlis")
    print("2. Route 2: Johor - Kuala Lumpur - Terengganu - Kelantan")
    

# Start the admin menu
shipping_management_main()