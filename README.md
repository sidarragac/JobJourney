<h1 align="center">
    <img src="https://github.com/user-attachments/assets/c74bdfd7-bf04-4935-a0ea-38eade4f9475" alt="logo" height="50px" align="center"/><br>
    JobJourney
</h1>

**Welcome to JobJourney. Let's walk through this guide for a fast introduction to our project.**
# Table of contents
- [Table of contents](#table-of-contents)
- [About](#about)
  - [About JobJourney](#about-jobjourney)
- [How to install](#how-to-install)
- [License](#license)

# About
JobJourney is a web application developed by [Santiago Idárraga](https://github.com/sidarragac), [Mateo García](https://github.com/mgarciac10) and [Juan José Botero](https://github.com/JuanJoseBotero) as the project for the "Integrator Project I" taguth by professor Paola Vallejo.

## About JobJourney
JobJourney is for those who dont have an idea of how to start their professional career or how to continue it to reach their dream job. Our scope is to guide individuals in their professional development by providing personalized, structured career roadmaps build with AI.


# How to install
To keep a copy of our project, you can follow the next steps:
1. (Optional) Fork the repository.
2. Clone the repository.
  ```bash
    git clone https://github.com/sidarragac/JobJourney.git
  ```
  * Make sure you are in the folder:
  ```bash
    cd ./JobJourney
  ```
3. Create a Python virtual environment.
  ```bash
    python -m venv venv
  ```
4. Activate the virtual environment.
  ```bash
    ./venv/scripts/activate
  ``` 
5. Install the required libraries, using the ``` requirements.txt ``` file.
  ```bash
    pip install -r requirements.txt
  ```
6. Get your OpenAI API KEY[^1], and save it on a ``` .env ``` file located on the project root folder, with the following structure: ``` OPENAI_API_KEY = <YOUR OPENAI API KEY> ```.
  * Up to this point, your folder should look like this:
  ```bash
    JobJourney
    ├───accounts                    
    ├───admin
    ├───analytics
    ├───roadMap
    ├───venv
    ├───.env
    ├───.gitignore
    ├───manage.py
    ├───README.md
    └───requirements.txt
  ```
7. Make the database migrations.
  ```bash
    python manage.py migrate
  ```
  * This step will create ```db.sqlite3``` file. This is the database with all the required tables and relationships.
8. Run the development server.
  ```bash
    python manage.py runserver
  ```

# License
Copyright 2024, Santiago Idárraga, Juan José Botero, Mateo García. All rights reserved JobJourney.

[^1]: To know more about the OpenAI API, please visit the [OpenAI website](https://openai.com/api/). Please be aware that a $5 fee is required to get access to one key.