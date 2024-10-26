# Rule-Based System with AST Evaluation and Rule Combination

This project is a rule-based system built with Django, which allows users to create, combine, and evaluate logical rules using Abstract Syntax Trees (ASTs). The project supports rule storage in a database, offers a web interface for viewing and managing rules, and allows combined rule creation. It is ideal for applications requiring dynamic rule evaluation, such as workflow automation or decision support systems.

## Table of Contents
- Features
- Project Structure
- Installation
- Usage
- Design Choices
- Dependencies

## Features
- **Rule Creation:** Users can create rules with logical operators (AND, OR, >, <, =) and store them in the database.
- **Rule Combination:** Multiple rules can be combined, stored, and evaluated as a single rule.
- **AST-Based Evaluation:** Rules are converted to an Abstract Syntax Tree for efficient evaluation.
- **User Interface:** A web interface allows users to create, view, combine, and evaluate rules.
- **Data Storage:** Rules and combined rules are stored in the database for persistence.
- **JSON and Session Support:** Rule data is stored in sessions to handle redirection, and JSON is used to store and retrieve rules.

## Project Structure

project-root/
│
├── rule_app/                       # Main Django app
│   ├── migrations/                 # Django migrations
│   ├── templates/rule_app/         # HTML templates
│   │   ├── index.html              # Home page template
│   │   ├── display_rule.html       # Template for viewing rules
│   │   ├── combined_display_rule.html  # Template for viewing combined rules
│   ├── views.py                    # Contains all Django views
│   ├── models.py                   # Rule model definition
│   ├── urls.py                     # URL routes for the application
│   ├── rule_engine.py              # Core logic for rule parsing and evaluation
│   └── admin.py                    # Admin interface configuration
│
├── project_name/                   # Main Django project
│   ├── settings.py                 # Django project settings
│   ├── urls.py                     # Project URL configuration
│   └── wsgi.py                     # WSGI configuration for deployment
│
├── manage.py                       # Django management script
└── README.md                       # Project documentation (this file)

## Installation
- **Prerequisites**
  - Python 3.7 or higher
  - Django 3.2 or higher
  - Git (optional, if you want to clone the repository)
 
- **Instructions**
  - **Clone the Repository**
    - git clone https://github.com/VasuGadde0203/Rule_Engine_Project.git
    - cd Rule_Engine_Project
  - **Create and Activate Virtual Environment**
    - python3 -m venv env
    - source env/bin/activate
  - **Install Dependencies**
    - pip install -r requirements.txt
  - **Apply Migrations**
    - python manage.py makemigrations
    - python manage.py migrate
  - **Run the Server**
    - python manage.py runserver
  - **Access the Application**
    - Open your browser and go to http://127.0.0.1:8000 to view the application.

## Usage
- **Home Page:** Access the main interface.
- **Create Rule:** Use the form to input rules as logical expressions, which are parsed into AST and stored in the database.
- **Combine Rules:** Select and combine existing rules, generating a combined AST, which is stored and can be evaluated as a single rule.
- **View and Evaluate Rules:** View stored rules or combined rules and evaluate them against input data.

## Design Choices
- **Abstract Syntax Tree (AST) for Rule Parsing**
The AST was chosen for parsing and evaluating rules because it allows for flexible, modular representation of logical expressions. By decomposing rules into operators and operands, we enable both individual rule evaluation and combined rule formation. The tree structure also allows efficient traversal and evaluation of complex rules with nested logic.

- **Rule Storage in Database**
Rules are stored in a Django model to persist data and allow easy management through the Django admin interface. Combined rules are stored in a dedicated JSON field to capture nested expressions, providing a versatile storage solution compatible with Django’s ORM.

- **Session-Based Redirection**
For redirecting data between views (e.g., rule creation to display view), session storage is utilized, ensuring temporary persistence across requests without requiring the database.

## Dependencies
- **Django:** Web framework for handling server-side logic.
- **Python Libraries:** json, ast (standard library modules used in rule parsing and evaluation).
