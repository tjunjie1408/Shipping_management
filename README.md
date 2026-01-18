Shipping Management System (Group 6)
This is a console-based (CLI) logistics and shipping management system developed in Python. The system simulates real-world logistics operations and integrates three main modules: User, Admin, and Driver. It covers core functionalities such as order processing, vehicle scheduling, route planning (Dijkstra's Algorithm), and shipment tracking.

👥 Project Members (Group 6)
TP079880

TP081807

TP080934

🚀 Project Introduction
This project uses File I/O for persistent data storage, eliminating the need for additional database configurations. The system is designed with comprehensive role-based access control, where users can access specific functional menus after logging in with different roles.

Key Highlights
Multi-Role System: Independent operation interfaces for Users, Admins, and Drivers.

Intelligent Route Planning: Built-in Dijkstra algorithm to calculate the shortest path and transport costs between two locations.

Data Persistence: All orders, users, vehicles, and maintenance records are saved in .txt files.

Complete Order Lifecycle: Management of the entire process from ordering, payment, and delivery updates to receipt and reviews.

🛠️ Features
1. User Module
Sign Up & Login: Secure account creation and authentication.

Make Order:

Customize consignment size (small parcel/bulk order/special cargo).

Automatic vehicle recommendation based on weight (Motorcycle/Van/Truck).

Select package type (Normal/Special) and payment method.

Order Management:

Check Order: View order history details and current delivery status.

Cancel Order: Cancel orders that are in a valid state.

Review System: Rate services (1-5 stars) and leave comments.

2. Admin Module
Vehicle Management:

Add new vehicles and set performance ratings.

Log vehicle maintenance history and set inspection alerts.

Route & Cost Management:

Add Route: Input new nodes and distances.

Route Calculation: Input start and end points to automatically calculate the shortest distance, fuel usage, and estimated transport cost.

System Monitoring:

Check order history for any user.

View delivery task status for all drivers.

Generate comprehensive reports.

3. Driver Module
Profile Management:

View and update driver profile details (Contact, License, Health Report, etc.).

Delivery Management:

Update the status of assigned orders (In Transit/Completed).

Record pickup time and expected delivery time.

Route Assistance:

View pre-planned best routes.

Use the built-in calculator to find the shortest driving path.

📂 File Structure
Plaintext
.
├── Group 6.py                  # Main project entry file (Full Version)
├── shipping_management.py      # Main project entry file (Backup/Iterative Version)
├── routes.txt                  # Stores route nodes and distance data
├── vehicles.txt                # Stores vehicle information and status
├── drivers.txt                 # Stores driver profiles
├── users.txt                   # Stores user login credentials
├── [username]_order_history.txt # Dynamically generated order history for specific users
├── driver_deliveries.txt       # Records of driver delivery tasks
├── maintenance_history.txt     # Vehicle maintenance and service records
├── reviews.txt                 # User review data
└── Assignment Project/         # Modular development directory (Layered .py files)
    ├── main.py
    ├── admin_module.py
    ├── driver_module.py
    ├── user_module.py
    └── utils.py
💻 Quick Start
Requirements
Python 3.x

Steps to Run
Clone or Download the Repository.

Ensure Data Files Exist:

Some missing .txt files will be created automatically upon the first run, but it is recommended to keep routes.txt to ensure the pathfinding algorithm has base data.

Start the Program: Run the following command in your terminal to start the main program:

Bash
python "Group 6.py"
Or:

Bash
python shipping_management.py
Operation Guide:

Follow the on-screen prompts and enter numbers to select the corresponding role and function.

When testing the route algorithm, ensure the location names entered match those stored in routes.txt.

📝 Algorithm Explanation (Dijkstra)
The project implements Dijkstra's Algorithm within the route_and_fuel_management and calculate_shortest_route functions. This algorithm reads the node graph from routes.txt, calculates the shortest path weight (distance) from a start point to a destination, and uses this to estimate fuel consumption and shipping costs.
