# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# API Documentation

## RESTful and very simple

All calls are made with either `GET`, `POST`, or `DELETE` HTTP methods.

CORS is only relaxed on `/api/` URL endpoints to limit scope.

## Error codes and Endpoint conventions

All responses are returned in JSON format, a `"success"` key, which will return either `True` or `False`.

When error codes are returned (`400`, `404`, `422`, and `500`), they will return in a format like the following 404 example:

```bash
{
    "success": False,
    "error": 404,
    "message": "Not found"
}
```

## API Objects

The Trivia API is made up of two types, Categories and Questions.

- Categories
  - Categories for Trivia questions can be one of 6 possible values: Science, Art, Geography, History, Entertainment, and Sports
- Questions
  - Trivia questions contain the question itself, the category it belongs to, the difficulty and an answer

## GET '/api/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs

##### EXAMPLE `curl http://localhost:5000/api/categories`

```bash
{
    "categories": {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    },
    "success": true
}
```

## GET '/api/questions'

- Gets a list of all the trivia questions across all categories
- Paginates response to limit to 10 results per page
- Append URL parameter `?page=<num>` to return a different page (defaults to page 1)
- Request Arguments: None
- Returns: All categories, a list of questions with key value pairs, success status, and total number of questions in database

##### EXAMPLE `curl http://localhost:5000/api/questions?page=2`

```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Six",
      "category": "6",
      "difficulty": 4,
      "id": 22,
      "question": "When Michael Jordan played for the Chicago Bulls, how many NBA Championships did he win?"
    },
    ... TRUNCATED FOR BREVITY ...
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 1,
      "id": 24,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "total_questions": 39
}
```

## DELETE '/api/questions/<question_id>'

- Deletes a question by id
- Request Arguments: question id
- Returns: Success status and id of deleted question if successful

##### EXAMPLE `curl -X DELETE http://localhost:5000/api/questions/6`

```bash
{
    'deleted': 6,
    'success': true
}
```

## POST '/api/questions'

- This endpoint performs two functions
  - Creates a new question via a form
  - Searches questions by search term form

### Creating a new question

- Request Arguments: question data via `application/json` type
- Returns: Success status and id of newly created question if successful

##### EXAMPLE `curl -X POST http://localhost:5000/api/questions -H "Content-Type: application/json" -d '{"question": " What is the symbol for potassium?", "answer": "K", "category": "1", "difficulty": 1}'`

```bash
{
    "success": true,
    "added": 24
}
```

### Searching questions via search term form

- Request Arguments: search term data via `application/json` type
- Returns: Success status and a list of questions and their data that met the search results

##### EXAMPLE `curl -X POST http://localhost:5000/api/questions -H "Content-Type: application/json" -d '{"searchTerm": "symbol"}'`

```bash
{
  "questions": [
    {
      "answer": "K",
      "category": "1",
      "difficulty": 1,
      "id": 24,
      "question": " What is the symbol for potassium?"
    }
  ],
  "success": true
}
```

## GET '/api/categories/<category_id>/questions'

- Gets all the questions based on a particular category
- Request Arguments: category_id
- Returns: Success status and list of questions for that category, plus a total question count of the non-paginated results

##### EXAMPLE `curl http://localhost:5000/api/categories/3/questions`

```bash
{
  "categories": {
    "id": 5,
    "type": "Entertainment"
  },
  "current_category": 5,
  "questions": [
    {
      "answer": "7",
      "category": "5",
      "difficulty": 2,
      "id": 12,
      "question": "How many films did Sean Connery play James Bond in?"
    },
    {
      "answer": "1997",
      "category": "5",
      "difficulty": 3,
      "id": 13,
      "question": "In what year was the first episode of South Park aired?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

## POST '/api/quizzes'

- Enables the playing of a Trivia game
  - Returns a random question for a given category that has not been asked already
  - Can return questions randomly chosen from a particular category, or across all of them
- Request Arguments: quiz category and a list of previously asked questions , encoded in `application/json` format
- Returns: success status and if successful, a random question. If there are no more questions to return in that category, the API just returns success but with no question key/value pair, which tells the frontend the quiz is over.

##### EXAMPLE of getting a question from all categories (category 0), and none have been asked yet `curl -X POST http://localhost:5000/api/quizzes -H "Content-Type: application/json" -d '{previous_questions: [], quiz_category: {type: "click", id: 0}}'`

```bash
{
  "question": {
    "answer": "1877",
    "category": "6",
    "difficulty": 3,
    "id": 11,
    "question": " In what year was the first ever Wimbledon Championship held?"
  },
  "success": true
}
```

##### EXAMPLE of getting a question from the History category (category 4), and there are no more questions left in that category `curl -X POST http://localhost:5000/api/quizzes -H "Content-Type: application/json" -d '{previous_questions: [5, 9, 23, 12], quiz_category: {type: "History", id: "4"}}'`

```bash
{
  "success": true
}
```
