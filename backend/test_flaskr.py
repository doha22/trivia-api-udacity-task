import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app 
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:root@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        return True
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_success(self):
      response = self.client().get('/categories')
      data = json.loads(response.data)

      self.assertEqual(response.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['categories'])
      self.assertTrue(len(data['categories']))


    def test_get_questions_in_category_for_success(self):
        category_id = 1
        response = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], category_id)


    def test_get_questions_in_category_with_error(self):
        category_id = 100
        response = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

   #get questions
    def test_get_questions_for_success(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertTrue(data['total_questions'])
      
   # create new question

    def test_create_new_question_for_success(self):
      
        questions_before = Question.query.all()
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)

        questions_after = Question.query.all()
        question = Question.query.filter_by(id=data['created']).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(questions_after) - len(questions_before) == 1)
        self.assertIsNotNone(question)

    # fail in create question
    def test_question_creation_with_error(self):
        questions_before = Question.query.all()
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)

        questions_after = Question.query.all()
        self.assertEqual(response.status_code, 422)
        self.assertTrue(len(questions_after) == len(questions_before))

  
    #search question
    def test_search_questions(self):
        response = self.client().post('/questions',json={'searchTerm': 'how'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_search_questions_with_error(self):
        response = self.client().post('/questions',json={'searchTerm': 'abc'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')


    #
    
     

       

       


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()