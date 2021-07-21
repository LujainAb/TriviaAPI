# Full Stack Trivia API Final Project


## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch.
The application includes:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


All backend code follows PEP8 style guidlines 


## API Reference
you can find the API Refrence and all the endpoints doucumation within the following URL: 
https://documenter.getpostman.com/view/16709336/TzsWuqgm

## General idea of the application
### Homepage:
![homepage](https://user-images.githubusercontent.com/51900114/126504825-085c66a6-34f4-4050-9695-a9e23a92ba1b.png)

### View the questions answers: 
![view answer](https://user-images.githubusercontent.com/51900114/126504988-ccaeb41c-c419-4a5c-b091-b6d6075ce546.png)

### Add a questions:
![addq](https://user-images.githubusercontent.com/51900114/126505023-939c1642-2a7f-48a3-a50c-c745b3f2e2e7.png)

### Quiz's catgeories:
![quiz1](https://user-images.githubusercontent.com/51900114/126505126-28596f52-ba8b-4523-a0ae-b376aeb30a00.png)

### Quiz Question:
![quiz](https://user-images.githubusercontent.com/51900114/126505230-82be6233-9d4d-491d-b101-ef5f1098761f.png)



## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on `http://127.0.0.1:3000/`. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend
The [./backend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/backend/README.md) directory contains a partially completed Flask and SQLAlchemy server.  `__init__.py` is to define endpoints and can reference models.py for DB and SQLAlchemy setup.


### Frontend

The [./frontend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. 


>View the [README within ./frontend for more details.](./frontend/README.md)


## Deployment N/A

## Authors
Backend both by Udacity team and i, Lujain Almutairi. and the frontend is enhanced by my amazing instructor @iMishaDev from Udacity Misk.

## Acknowledgements 
Thanks to the awesome team at Udacity for this amazing opportunaity to work on this app! 


