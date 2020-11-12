import os
from flask import Flask, request, abort, jsonify ,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func
from models import setup_db, Question, Category

from config import paginate_questions


QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/*": {"origin": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
    return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories= Category.query.all()
    categories = [category.format() for category in categories]
    return jsonify({
        "success": True ,
        "categories":categories
      })
         


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():

    questions = Question.query.all()
    paginated_questions = paginate_questions(request, questions)

      #get the gategories     
    categories= Category.query.all()
    categories = [category.format() for category in categories]

    return jsonify({
        "success": True ,
        "questions" :paginated_questions ,
        "total_questions": len(questions),
        "categories":categories
      })

      




  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
  # using one_or_none() if there is no question_id
    question = Question.query.filter(Question.id == question_id).one_or_none()
    if question is None:
      abort(404)
    #else delete
    question.delete()

    return jsonify({
        "success": True ,
        "question deleted" :question_id 
        
      })

    






  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()
    if not body:
      abort(400)
    
    if 'search_term' in body.keys():
        return search_questions(request, body['search_term'])

    for key in ['question', 'answer', 'difficulty', 'category']:
        if key not in body.keys() or body[key] == None or body[key] == '':
            return abort(422)
  
    question = Question(
    question=body.get('question'),
    answer=body.get('answer'),
    difficulty= body.get('difficulty'),
    category= body.get('category'),
        )
    question.insert()
    

    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    
    return jsonify({
        "success": True ,
        'created': question.id,
        'question_created': question.question,
        'questions': current_questions,
        
      })
   





  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def question_search():
    body = request.get_json()
    if not body:
      abort(400)

    if body.get('search_term'):
      search_term = body.get('search_term')

      selection  = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    
      if (len(selection) == 0):
          abort(404)
      paginated = paginate_questions(request, selection)

      return jsonify({
            'success': True,
            'questions': paginated,
            'total_questions': len(Question.query.all())
        })


      

    else:
    # no search term inserted
      abort(400)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def category_question(id):
    category = Category.query.filter(id == id).one_or_none()

    if category is None:
      abort(404)

    selection = Question.query.filter_by(category=category.id).all()
    paginated = paginate_questions(request, selection)


    return jsonify({
        'success': True,
        'questions': paginated,
        'total_questions': len(Question.query.all()),
        'current_category': category.type
    })



  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    body = request.get_json()

    previous_questions = []
    #to get the previois question
    previous = body.get('previous_questions') # from frontend

    category = body.get('quiz_category')     # from frontend

    if ((category is None) or (previous is None)):
        abort(400)
    
    if (category['id'] == 0):
        selection = Question.query.order_by(func.random())
       
    else:
        selection = Question.query.filter(Question.category == category_id).order_by(func.random())

    if not selection.all():
              # no question
      abort(404)

    else:
        # random question
        question = selection.filter(Question.id.notin_( previous_questions)).first()
    if question is None:
        # all questions were played
        return jsonify({
            'success': True
        })
    # Found a question that wasn't played before
    return jsonify({
        'success': True,
        'question': question.format()
    })
  




  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
            "success": False,
            "error": 404,
            "message": 'NOT_FOUND'
        }), 404

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal error'
    }), 500






  
  return app

    