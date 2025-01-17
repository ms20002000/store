# Store Backend Project

This repository contains the backend code for the Store project, a web application built using Django and PostgreSQL, with Docker for containerization and Nginx for serving static files.

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Static Files](#static-files)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Store backend provides a robust and scalable API for managing products, orders, discounts, and user accounts. It is designed to be deployed in a containerized environment using Docker, ensuring easy scalability and maintainability.

## Technologies Used

- **Django**: A high-level Python web framework for rapid development and clean design.
- **PostgreSQL**: An advanced, open-source relational database.
- **Docker**: Containerization for consistent development and deployment environments.
- **Nginx**: A high-performance web server for serving static files and reverse proxying.

## Setup and Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/store-backend.git
    cd store-backend
    ```

2. **Install dependencies**:
    Make sure you have Docker and Docker Compose installed on your machine.

3. **Set up environment variables**:
    Create a `.env` file in the project root and define the necessary environment variables (see [Environment Variables](#environment-variables)).

4. **Build and start the Docker containers**:
    ```bash
    docker compose up --build
    ```

## Running the Project

To start the project, run the following command:
```bash
docker compose up
