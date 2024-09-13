# Lunch Place Decision Service Documentation

## Overview

The Lunch Place Decision Service is an internal tool designed for companies to facilitate their employees in choosing a lunch place based on daily menus uploaded by restaurants.

## Features

### Authentication
- **Restaurants** receive a unique API Key upon registration, allowing them to upload their daily menus.
- **Employees** authenticate using JWT tokens to vote on menus.
- **Company Admin** has the authority to register both Restaurants and Employees into the system.

### Restaurant Registration
- Company Admin can create a restaurant profile in the system, which generates an API Key for the restaurant.

### Menu Upload
- Restaurants can upload their menu for each day using their API Key for authentication.

### Employee Registration
- Company Admin can register employees, enabling them to vote on the daily menus.

### Voting on Menus
- **Old API Version:** Allows employees to vote for one menu.
- **New API Version:** Enables employees to vote for their top three menus, assigning points from 1 to 3 for their top choices.

### Voting Logic
- Votes via the old API version create or update a vote record with the top points for the day.
- Votes via the new API version create or update a vote record with points for the top three choices for the day.

### Results Retrieval
- Anybody can view the current day's voting results, showing the most popular menus.
### API Documentation (Swagger)
  Open a web browser and go to `http://localhost:8000/swagger-ui/` (adjust the port if necessary). You should see the Swagger UI loaded with your API documentation based on the `schema.yml` file.
### Versioning Strategy

#### Custom Header Versioning

- **Header Name:** `X-API-VERSION`
- **Purpose:** Allows clients to specify the desired version of the API for each request, ensuring compatibility and access to specific features available in that version.
- **Format:** The version value should be in the format `major.minor` (e.g., `1.0`), where:
  - `major` represents significant changes and potentially breaking changes.
  - `minor` represents backward-compatible improvements and additions.

#### Version Specification

If `X-API-VERSION` header in their requests, to indicate which version of the API they wish to use, is `None` or invalid, the default version of API would be selected.


## Getting Started

### Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework

### Installation

1. Clone the repository and navigate into it.
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

### Linting and Typing Checks

To ensure code quality, readability, and type correctness, we employ a series of linting and typing checks. These checks are encapsulated in a script named `lint.sh`, which should be run before committing changes to the repository.

#### Using `lint.sh`

The `lint.sh` script automates the process of linting and typing checks. It runs the following tools:

- **Flake8:** Checks for coding style issues.
- **AutoPEP8:** Automatically formats Python code to conform to the PEP 8 style guide.
- **isort:** Sorts imports alphabetically, and automatically separated into sections.
- **Mypy:** Performs static type checking.

#### Running the Script

To run the script, navigate to your project's root directory in the terminal and execute:

```bash
./lint.sh
```

Ensure the script has executable permissions. If not, grant them with:

```bash
chmod +x lint.sh
```

### Testing with Pytest

Our project uses `pytest` for running unit and integration tests, as well as a comprehensive suite of all tests. This ensures that new changes do not break existing functionality and that the application behaves as expected.

#### Running Tests

- **Unit Tests:** Focus on testing individual components in isolation.
  ```bash
  pytest -m "unit"
  ```
- **Integration Tests:** Test the integration between different components or systems.
  ```bash
  pytest -m "integration"
  ```
- **All Tests:** To run the entire test suite without filtering.
  ```bash
  pytest
  ```

#### Best Practices

- **Run Frequently:** Execute `lint.sh` and the relevant `pytest` commands frequently during development. This helps catch and fix issues early, improving the overall quality of the codebase.
- **Pre-commit Hooks:** Consider setting up pre-commit hooks that automatically run `lint.sh` and `pytest -m "unit"` to ensure that commits meet the quality standards.
- **Continuous Integration (CI):** Integrate these tools into your CI pipeline to automatically check every push or pull request. This ensures that all contributions are vetted for quality before merging.

### Updating API Document Swagger
#### Step 1: Generate the Initial OpenAPI Schema
1. **Generate the Schema**

   Run the following command in your terminal to generate the initial `schema.yml` file:

   ```bash
   python manage.py generateschema > schema.yml
   ```

   This command will create a `schema.yml` file in your project root directory containing the OpenAPI schema for your project.

#### Step 2: Edit the Schema on Swagger Editor

You might want to customize or correct the automatically generated schema to better match your API's functionality or to add additional information that DRF's schema generation might not include.

1. **Open the Swagger Editor**

   Visit [Swagger Editor](https://editor.swagger.io/) in your web browser.

2. **Import Your Schema**

   In the Swagger Editor, you can either paste the content of your `schema.yml` directly into the editor or use the "File" menu to import the `schema.yml` file.

3. **Edit and Validate Your Schema**

   Once your schema is loaded into the editor, you can make any necessary adjustments. Swagger Editor provides real-time validation and feedback on your schema, which can help you identify and fix issues.

4. **Export the Updated Schema**

   After you've made your changes, use the "File" > "Save as YAML" option in Swagger Editor to download the updated schema. Save this file as `schema.yml` again.

#### Step 3: Move the Updated Schema to Your Static Files Directory

To serve the updated `schema.yml` through your Django application, you should place it in a static files directory. Assuming your project has an app named `lunch_service`, 

**Move the Schema File**

   Move your updated `schema.yml` file to the `lunch_service/static/` directory.

#### Step 4: **Visit the Swagger UI Page**
   Open a web browser and go to `http://localhost:8000/swagger-ui/` (adjust the port if necessary). You should see the Swagger UI loaded with your API documentation based on the `schema.yml` file.


## Enhancing API Quality with Future Features

Elevating the quality, usability, and security of your API involves incorporating advanced features that cater to the evolving needs of users and the system itself. Here are essential enhancements to consider for future development:

- **Introduction of `vote_points` in the `Menu` Model**
  - **Objective**: To streamline the process of selecting a menu for lunch by minimizing the need for aggregation queries in the Vote Model. Incorporating a `vote_points` field directly within the `Menu` model can significantly enhance response times and overall performance.
- **Using [Django REST Framework API Key](https://djangorestframework-simple-apikey.readthedocs.io/en/latest/).** 
  - **Objective**: Right now, for simplicity, Implemented API Key authentication in IsRestaurant permission declaration. But for complex usage, we can use [Django REST Framework API Key](https://djangorestframework-simple-apikey.readthedocs.io/en/latest/).

- **Creation of an `Item` Model Linked to `Menu`**
  - **Objective**: To lay the groundwork for extended functionality and scalability. By establishing an `Item` model with a ForeignKey connection to the `Menu` model, the system can offer more detailed and structured data management. Initially, for simplicity, a TextField attribute is used to list items.

- **Provide setting configuration per environment like production, staging, testing**
  - **Objective**: To lay the groundwork for extended functionality and scalability. By establishing an `Item` model with a ForeignKey connection to the `Menu` model, the system can offer more detailed and structured data management. Initially, for simplicity, a TextField attribute is used to list items.


- **Rate Limiting and Throttling**
  - **Objective**: These measures are crucial for safeguarding your API against overutilization and potential abuse. By setting a cap on the number of requests a user can make within a specific period (rate limiting) and controlling the request rate (throttling), you can ensure equitable access for all users while preventing service disruptions or slowdowns due to excessive traffic.

- **Pagination**
  - **Objective**: This feature enhances both the performance and user experience of your API by partitioning large datasets into smaller, more manageable segments. Pagination facilitates more efficient data retrieval and processing for clients, significantly reducing server load and streamlining data handling.

## Docker Setup for [Your Project Name]

## Prerequisites

- Docker: Ensure you have Docker installed on your system. If not, follow the installation instructions for [Docker](https://docs.docker.com/get-docker/).
- Docker Compose: Ensure Docker Compose is installed. It usually comes with Docker for Windows and Docker for Mac, but you might need to install it separately on Linux. See the [Docker Compose installation guide](https://docs.docker.com/compose/install/).

## Project Setup

1. **Clone the Repository**

   Start by cloning the project repository to your local machine.

   ```bash
   git clone [repository URL]
   cd [project directory]
   ```

2. **Environment Configuration**

   Copy the sample environment configuration file and adjust the variables according to your local environment.

   ```bash
   cp .env.example .env
   ```
  
   Be sure to replace values like database credentials, secret keys, and any other necessary configurations. If you are going to run using docker, you should set the `POSTGRES_HOST` as the database service name `db`

3. **Build the Docker Containers**

   Use Docker Compose to build the application and database containers.

   ```bash
   docker-compose up --build
   ```

   This command builds the images for your services (as defined in `docker-compose.yml`) and starts the containers. The first build might take some time as it needs to fetch the base images and install dependencies.

4. **Database Migrations**

   After the containers are up and running, you need to apply database migrations to set up the initial database schema.

   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a Company Admin (Optional)**

   To access the admin panel, you'll need to create a superuser account.

   ```bash
   docker-compose exec web python manage.py create_company_admin
   ```

6. **Accessing the Application**

   Once everything is set up, you can access the application by navigating to `http://localhost:8000` in your web browser. Adjust the port according to your `docker-compose.yml` configuration if necessary.

## Development Commands

Here are some common commands you'll use during development:

- **Starting the Containers**: `docker-compose up` (add `-d` for detached mode)
- **Stopping the Containers**: `docker-compose down`
- **Viewing Container Logs**: `docker-compose logs` (add `-f` to follow the log output)
- **Running Management Commands**: `docker-compose exec web python manage.py [command]`