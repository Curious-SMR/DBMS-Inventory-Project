# Store Inventory Manager

#### Description:
The Store Inventory Manager is a web-based application designed to help store owners manage their product inventory efficiently. Built using Flask and SQLite, this application allows users to add, edit, and delete products from the inventory, as well as view detailed product information. Additionally, it includes a user authentication system to ensure secure access to the inventory data.

## Features:
1. **User Authentication**: Users can register, log in, and log out securely.
2. **Product Management**: Add, edit, and delete products from the inventory.
3. **Dashboard**: View a summary of the inventory, including the total number of products and the total value of all products.
4. **Responsive Design**: The application is designed to work well on both desktop and mobile devices.

## Project Files:
### 1. `app.py`
This is the main application file. It contains all the route definitions and the core logic of the application, including:
- **User Authentication Routes**: For logging in, logging out, and registering users.
- **Product Management Routes**: For adding, editing, and deleting products.
- **Dashboard Route**: For displaying the user dashboard with inventory statistics.

### 2. `inventory.db`
This is the SQLite database file that stores all the data for the application, including user information and product details.

### 3. `templates/`
This folder contains all the HTML templates used in the application. The key files include:
- **layout.html**: The base template that includes the common structure and CSS for all pages.
- **index.html**: The main page that displays the list of products.
- **register.html**: The registration page for new users.
- **login.html**: The login page for existing users.
- **manage.html**: The page for adding and editing products.
- **user_dashboard.html**: The user dashboard that provides summary information about the inventory.

### 4. `static/`
This folder contains all the static files, including CSS and JavaScript files. The key file is:
- styles.css: The CSS file that styles the application.

## Design Choices:
### Database Choice:
I chose SQLite for this project due to its simplicity and ease of setup. SQLite is lightweight and doesn't require a separate server, making it perfect for small to medium-sized applications like this one.

### Framework:
Flask was chosen as the web framework for its minimalistic and flexible nature. Flask allows for rapid development and is highly customizable, making it an ideal choice for this project.

### User Authentication:
The user authentication system was implemented to ensure that only authorized users can access and modify the inventory. The concept of hashing of passwords is utilized so as to keep the database cryptic. This adds a layer of security to the application, protecting sensitive inventory data.

### Responsive Design:
To make the application accessible on both desktop and mobile devices, I implemented a responsive design using CSS. This ensures that users can manage their inventory on the go, providing greater flexibility and convenience.

## Future Improvements:
While the current version of the Store Inventory Manager is fully functional, there are several areas for potential improvement:
1. Enhanced Security: Implementing more robust security measures.
2. User Roles: Adding different user roles (e.g., admin, manager) with varying levels of access to the application.
3. Product Categories: Allowing users to categorize products for better organization.
4. Search Functionality: Implementing a search feature to quickly find products in the inventory.

## Conclusion:
The Store Inventory Manager is a robust and user-friendly application that provides all the essential features needed to manage a store's inventory effectively. By leveraging Flask and SQLite, I was able to create a lightweight and efficient solution that can be easily expanded and customized in the future. I'm proud of the work I've done on this project and look forward to adding more features and improvements.
