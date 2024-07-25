# Project Overview

This project is a custom Streamlit application that incorporates various features, including authentication, custom pages, and integration with AWS services like Secrets Manager for secure credential management. The project is organized into a clear directory structure for easy navigation and maintainability.

## Directory Structure

The project directory is structured as follows:

```
framework/
├── authpages/
│   ├── login.py
│   ├── logout.py
│   ├── manage.py
│   ├── profile.py
│   ├── register.py
├── configs/
│   ├── config.yaml
│   ├── routes.yaml
├── custpages/
│   ├── company.py
│   ├── example.py
├── images/
│   ├── ice.png
├── screencasts/
│   ├── streamlit-app-2024-07-19-15-07-28.webm
├── styles/
│   ├── examples/
│   │   ├── [example CSS files]
│   ├── default.css
├── utils/
│   ├── cookie_handler.py
│   ├── custom_logger.py
│   ├── database.py
│   ├── route_loader.py
│   ├── s3.py
│   ├── styles.py
│   ├── validation.py
├── .gitignore
├── app.log
├── app.py
├── README.md
```

### Directory Descriptions

- **authpages/**: Contains the authentication-related pages, including login, logout, profile management, and user registration.

- **configs/**: Houses configuration files such as `config.yaml` for app-wide settings and `routes.yaml` for defining the application's routes.

- **custpages/**: Custom application pages for specific business logic or content.

- **images/**: Stores image assets used in the application, such as logos.

- **screencasts/**: Contains screencast recordings or other media files.

- **styles/**: CSS stylesheets for customizing the appearance of the Streamlit application. The `examples/` folder includes example styles.

- **utils/**: Utility scripts for various functions, including:
  - `cookie_handler.py`: Manages cookies for user sessions.
  - `custom_logger.py`: Custom logging setup.
  - `database.py`: Handles database connections and operations.
  - `route_loader.py`: Manages routing and navigation.
  - `s3.py`: AWS S3 integration utilities.
  - `styles.py`: Handles loading of styles and configuration settings.
  - `validation.py`: Validation utilities for form inputs and other data.

- **.gitignore**: Specifies files and directories to be ignored by Git version control.

- **app.log**: Log file for the application.

- **app.py**: Main entry point for the Streamlit application. Initializes the app, sets up logging, loads styles, and handles routing.

## Usage

To run the application, execute the `app.py` script using Streamlit. Ensure that your environment is set up with the necessary dependencies listed in `requirements.txt`.

```bash
streamlit run app.py
```

## Configuration

The application uses YAML files for configuration. Key configurations include:

- `config.yaml`: Contains settings like page titles, layout options, and theme styles.
- `routes.yaml`: Defines the navigation routes, roles, and permissions.

## Security Considerations

- **Secrets Management**: For secure handling of credentials and sensitive data, the application integrates with AWS Secrets Manager. The use of IAM roles ensures that secrets are only accessible to authorized services and users.

---

This structure provides a comprehensive overview and description of the project components and how they are organized. You can modify the details as needed to fit the specific nuances of your project.