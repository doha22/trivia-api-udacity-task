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
        # get all categories
        all_categories = Category.query.all()
       
       # convert to dictionary to be compatable with frontend 
        dic = {}
        for category in all_categories:
            dic[category.id] = category.type

        # return data to view
        return jsonify({
            'success': True,
            'categories': dic
        })
         


# will do post for categories cause categories doesn't exist 
# will insert categories from postman

  @app.route('/new_category', methods=['POST'])
  def new_category():

    body = request.get_json()
    if not body:
      abort(400)
    
    category = Category(
    
    type= body.get('type'),
        )
    category.insert()
    

    selection = Category.query.order_by(Category.id).all()


    return jsonify({
        "success": True ,
        "message":"inserted "
        # "category":selection
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

   # get all questions
    all_questions  = Question.query.all()
    # call paginate fn to limit questions per page
    current_questions  = paginate_questions(request, all_questions)
     
   
      #get the gategories     
    categories_all= Category.query.all()
    # convert to dictionary to be compatable with front-end instead of using list
    cat_dic = {}
    for category in categories_all:
        cat_dic[category.id] = category.type
   



    return jsonify({
        "success": True ,
        "questions" :current_questions ,
        "total_questions": len(all_questions ),
        "categories":cat_dic
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
    question = Question.query.get(question_id)

    #check first if question exist , if no question , get error, else delete it
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
    
    if 'searchTerm' in body.keys():
        return question_search(request, body['searchTerm'])

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

    print(body.get('searchTerm'))
    if (body.get('searchTerm')):
      search_term  = body.get('searchTerm')

      selection  = Question.query.filter(Question.question.ilike(f'%{search_term }%')).all()
    
    # not found
      if (len(selection) == 0):
          abort(404)
          
      paginated = paginate_questions(request, selection)

      print(paginated)

      return jsonify({
            'success': True,
            'questions': paginated,
            'total_questions': len(Question.query.all())
        })


      

    else:
    # no search term inserted
      abort(404)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def category_question(id):
    #get all questions related to category_id
    
    #to get category name 
    category = Category.query.get(id)
    print(category)
    cat= category.type


   # if no category 
    if category is None:
      abort(400)
    
    # do casting for category_id
    print(str(category.id))
    str_id = str(category.id)
   
   # get all questions with the category id = <int:id>
    selected_questions = Question.query.filter_by(category=str_id).all()
    print(selected_questions[0])
    # THEN call function paginate to limit the questions per page 
    paginated = paginate_questions(request, selected_questions)


    return jsonify({
        'success': True,
        'questions': paginated,
        'total_questions': len(selected_questions),
        'current_category': cat
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
    if not body:
        abort(400)
    if (body.get('previous_questions') is None or body.get('quiz_category') is None):
        abort(400)
    previous_questions = body.get('previous_questions')
    category = body.get('quiz_category')

   # if there are previous questions 
    if len(previous_questions) !=0 :
        abort(400)
    str_id = str(category['id'])
    # check there are questions in category
    if str_id == 0:
        # if  category id is 0 
        selection = Question.query.order_by(func.random())
    else:
        # load a random object of questions from the specified category
        selection = Question.query.filter(
            Question.category == str_id).order_by(func.random())
    if not selection.all():
        #no question available with this category type
        abort(404)
         
    else:
        # if category found , then get random question
        question = selection.filter(Question.id.notin_(previous_questions)).first()
   
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

    