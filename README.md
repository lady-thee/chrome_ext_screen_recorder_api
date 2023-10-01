# Screen Recording Chrome Extension API

## Table of Contents

- [Introduction](#introduction)
- [Purpose](#purpose)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Welcome to the Screen Recording Chrome Extension API project. This API is designed to capture video chunks from a screen recorder extension, combine and save them, and provide a web interface for viewing the recorded video along with an AI generated transcript.

## Purpose

The primary purpose of this project is to provide a backend API for managing and rendering screen recordings captured by a Chrome extension. It allows users to store and view their recorded content seamlessly.

## Technologies Used

The following technologies and libraries were used in this project:

- Django
- Django Rest Framework
- Gunicorn
- Pydantic
- Pydantic Settings
- Django Cors Headers
- Pillow /Psycopg2-binary (PotsgreSQL)
- Dj-Database-URL
- OpenAI Whisper
- Torch

## Installation

To get started with this project, follow these steps:

1. Clone the repository:

   
   ```git clone <repository_url>```

2. Install dependencies:
     
     ```pip install -r requirements.txt```

3. Configure your database settings, API keys, and other environment variables as needed.

4. Run migrations:

     ```python manage.py migrate```


5. Start the development server:

     ```python manage.py runserver```

6. Access the API at [http://localhost:8000/api/upload_video] in your web browser.



# Usage
To use this API, refer to the API documentation or follow the guidelines in the project's documentation.



# A Problem?
Raise an issue!