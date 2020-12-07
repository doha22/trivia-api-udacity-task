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

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

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


## Endpoints 

#####  GET '/categories'
```
   Sample
   curl http://127.0.0.1:5000/categories

    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
    {
          "categories": {
              "1": "Science", 
              "2": "Art", 
              "3": "Geography", 
              "4": "History", 
              "5": "Entertainment", 
              "6": "Sports"
          }, 
          "success": true
      }

```
#####  POST 'questions/search'
```
   Sample
   curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "what"}'

    - will search of question by passing search term .
    - input :
      {
 	"searchTerm":"what"
 	
        }
    - output will be :
    {
    "questions": [
        {
            "answer": "search on google",
            "category": "1",
            "difficulty": 3,
            "id": 3,
            "question": "what means by inverse engineering"
        },
        {
            "answer": "don't have any idea",
            "category": "6",
            "difficulty": 2,
            "id": 4,
            "question": "what is the result of last match between ahly and zamalek"
        },
        {
            "answer": "see course of udicity ",
            "category": "4",
            "difficulty": 2,
            "id": 8,
            "question": "what do you now about GIT?"
        }
    ],
    "success": true,
    "total_questions": 12
}     
    

```


#####  POST '/new_category'
```
   Sample
   curl http://127.0.0.1:5000/new_category -X POST -H "Content-Type: application/json" -d '{"type": "music"}'

    - insert new category  
    - implement in backend only 
     
    - output be :
    {
    "message": "inserted ",
    "success": true
        }      
    

```

#####  GET /questions
    Sample
    curl http://127.0.0.1:5000/questions
      - return all questions
      - return only 10 question per page
      - output will be :
      {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "see course of udicity ",
            "category": "1",
            "difficulty": 1,
            "id": 1,
            "question": "how to post new article using js"
        },
        {
            "answer": "see on printrest",
            "category": "1",
            "difficulty": 2,
            "id": 2,
            "question": "how to draw cat"
        },
        {
            "answer": "search on google",
            "category": "1",
            "difficulty": 3,
            "id": 3,
            "question": "what means by inverse engineering"
        },
        {
            "answer": "don't have any idea",
            "category": "6",
            "difficulty": 2,
            "id": 4,
            "question": "what is the result of last match between ahly and zamalek"
        },
        {
            "answer": "you can see on printrest",
            "category": "2",
            "difficulty": 2,
            "id": 5,
            "question": "how to draw mouse?"
        },
        {
            "answer": "see many ideas on printrest",
            "category": "5",
            "difficulty": 2,
            "id": 6,
            "question": "how can make surprise box"
        }
      }





##### DELETE /question/Question_id

    Sample
    curl http://127.0.0.1:5000/questions/1 -X DELETE
      - delete question by question id 
      - return question id 
      
      {
      "deleted": 1, 
      "success": true
     }

##### POST /questions
     
     Sample
     curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d'{ "question": "how to learn js", "answer": "you can find tutorial on w3schools", "difficulty": 1, "category": "1" } '
      - submit form of question by fill (question , answer , diffculty , category)
      - return question id 
      
      {
      "created": {
        "answer": "you can find tutorial on w3schools", 
        "category": 1, 
        "difficulty": 1, 
        "id": 2, 
        "question": "how to learn js"
      }, 
      "success": true
    }
    
 
    
   ##### GET /categories/<int:id>/questions

   
    Sample
    curl -X GET http://127.0.0.1:5000/questions
      - return questions related to category_id
      - output:
     {
    "current_category": "Science",
    "questions": [
        {
            "answer": "see course of udicity ",
            "category": "1",
            "difficulty": 1,
            "id": 1,
            "question": "how to post new article using js"
        },
        {
            "answer": "see on printrest",
            "category": "1",
            "difficulty": 2,
            "id": 2,
            "question": "how to draw cat"
        },
        {
            "answer": "search on google",
            "category": "1",
            "difficulty": 3,
            "id": 3,
            "question": "what means by inverse engineering"
        }
    ],
    "success": true,
    "total_questions": 3
}
    
  ##### POST /quizzes

     Sample
      curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Science","id":1},"previous_questions":[20]}'
      - return one random question and success value
      
      
      {
      "question": {
        "answer": "you can find tutorial on w3schools", 
        "category": 1, 
        "difficulty": 1, 
        "id": 2, 
        "question": "how to learn js"
      }, 
      "success": true
    }





## Testing
To run the tests, run
    
    create db by using terminal :
        dropdb trivia_test
        createdb trivia_test
        psql trivia_test < trivia.psql
    or create db from pgadmin4  directly named trivia_test
    then from pgadmin4 restore trivia.psql 
    python test_flaskr.py
