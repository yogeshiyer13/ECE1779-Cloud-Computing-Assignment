# ECE1779-Introduction-to-Cloud-Computing
Projects completed under this course:

Assignment - It deals with creation of gallery page and detecting the text from the images.

The app has been deployed using EC2 (Server based) from AWS. To run the static app you can simply do the following:

- Instructions:
1. Set database;
MySQL code for creating a table: run:

mysql -u username -p password <A1.sql (for example)

In the config.py file, you need to set up your own database first!

Set the config file In the config.py file, you need to set up your own database first!

2. Run the flask:

Run the flask: virtual env to run the flask by using python3:

For Mac OS:

- python3 -m venv venv
- source ./venv/bin/activate

For Windows OS:

- python3 -m venv venv
- ./venv/bin/activate

setup the env for flask:

For Mac OS:

- EXPORT FLASK_APP=main.py
- EXPORT FLASK_ENV=development flask run

For Windows user:

- SET FLASK_APP=main.py

- SET FLASK_ENV=development

flask run

For more info refer this document
[Github](https://github.com/) 
