
# Barnes

## Project Overview

Many individuals and small business owners struggle to manage their finances effectively due to the complexity of tracking income, expenses, assets, savings goals, and debts. The challenge is often compounded when personal and business finances are intertwined, leading to a lack of clarity and control over financial health.

There is a need for an intuitive and comprehensive budget tracking solution that can provide clear visibility into both personal and business financial activities, helping users make informed decisions, achieve savings goals, and manage debts efficiently.

**Barnes** is a comprehensive budget tracker application designed to help individuals and small business owners effectively manage their finances. The application provides separate dashboards for personal and business finances, enabling users to track income, expenses, assets, savings goals, and debts. With features like reporting, analytics, and predictive planning, Barnes aims to simplify financial management and promote financial health.

## Features

### 1. User Management
- **User Registration and Login**: Secure registration and login with authentication using email or phone number.
- **Profile Management**: Users can manage and update their profiles.
- **Referral System**: Users can refer others to the platform using a unique referral code.

### 2. Income and Expense Tracking
- **Income Logging**: Users can log and categorize their income, with support for recurring income entries.
- **Expense Logging**: Users can track and categorize their expenses, with options for budget limits for different categories.

### 3. Debt Management
- **Debt Tracking**: Users can manage their debts, including tracking repayment schedules and categorizing different types of debts.

### 4. Asset Management
- **Asset Tracking**: Users can log and monitor their assets and investments, with the ability to categorize and update them.

### 5. Savings Goals
- **Savings Goals Setup**: Users can set, track, and monitor savings goals, specifying target amounts and deadlines.
- **Progress Tracking**: Visual progress indicators for each savings goal.

### 6. Financial Reports
- **Comprehensive Reporting**: Users can generate detailed financial reports based on their income, expenses, debts, and assets.
- **Predictive Planning**: Insights and recommendations based on historical financial data.

### 7. Business and Personal Finance Dashboards
- **Separate Dashboards**: Different dashboards for personal and business finances to ensure clear visibility and management of both.
- **Customizable Categories**: Users can create custom categories for both personal and business finances.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Deployment](#deployment)
- [Contributors](#contributors)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before running the Barnes application, ensure you have the following installed:

- Python 3.8+
- Flask
- SQLAlchemy
- A database system (e.g., PostgreSQL, MySQL, or SQLite for development)
- Virtual Environment (optional but recommended)

## Configuration

The `config.py` file contains all the configuration settings for the application, including database URIs, secret keys, and other environment-specific variables.

## Database Setup

1. Install the necessary database system (e.g., PostgreSQL).

2. Configure your database connection in the `config.py` file.

3. Run the following command to initialize the database:

    ```bash
    python init_db.py
    ```

## Deployment

To deploy Barnes to a production environment:

1. **Set Up Your Server**: Provision a server (e.g., on AWS, DigitalOcean).

2. **Install Dependencies**: Install Python, Flask, and other dependencies on the server.

3. **Configure Environment Variables**: Set up your environment variables for the production environment.

4. **Database Migration**: Run database migrations to ensure the production database schema is up to date.

5. **Start the Application**: Use a production-grade WSGI server like Gunicorn to serve your Flask app.

    ```bash
    gunicorn app:app
    ```

## Contributors

- [Tulley](https://github.com/two23three)
- [Kuria](https://github.com/iankuria668)
- [Mwachi](https://github.com/MwachiOfficial)
- [Bill](https://github.com/Bjoseph23)
- [Andy](https://github.com/Muny1re1)
- [George](https://github.com/migeroreloaded)
- [Mariya](https://github.com/mariyaschrome)
- [Sharon](https://github.com/B-Sharon)

## Contributing

We welcome contributions to Barnes! To contribute:

1. Fork the repository.

2. Create a new branch with a descriptive name.

3. Make your changes, ensuring the code follows our style guidelines.

4. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. You’re free to use, modify, and distribute the software under the terms of the license.
