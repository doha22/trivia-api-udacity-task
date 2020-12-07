import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import math
from sqlalchemy import func
from starter.backend.flaskr.__init__ import create_app
from starter.backend.models import *


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}:root@{}/{}".format('localhost:5432', self.database_name)
        self.database_name = "trivia_test"
        self.database_user = "postgres"
        self.database_path = "postgres://{}:root@{}/{}".format(
            self.database_user, 'localhost:5432', self.database_name)

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



    def test_get_questions_in_category_for_success(self):
        category_id = 1
        response = self.client().get('/categories/1/questions'.format(category_id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 'Science')


    def test_get_questions_in_category_with_error(self):

        response = self.client().get('/categories/b/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'NOT_FOUND')

   ######test pagination

    def test_get_paginated_questions(self):

        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertGreater(len(data['questions']), 0)
        self.assertGreater(data['total_questions'], 0)
        self.assertEqual(type(data['total_questions']), int)

    def test_422_request_valid_page(self):
        # total_questions = len(Question.query.all())
        response = self.client().get(
            '/questions?page=0')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')



   ##### create new question

    def test_create_new_question_for_success(self):

        questions_before = Question.query.all()
        response = self.client().post('/questions', json={
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 3,
            'category': 1
        })

        data = json.loads(response.data)
        # get number of questions after post
        questions_after = Question.query.all()
        question = Question.query.filter_by(id=data['created']).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(questions_after) - len(questions_before) == 1)
        self.assertIsNotNone(question)

    ####### fail in create question

    def test_question_creation_with_error(self):
        questions_before = Question.query.all()
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)

        questions_after = Question.query.all()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(questions_after) == len(questions_before))
    #

    #######search question
    #
    def test_search_questions(self):
        response = self.client().post('/questions/search',json={'searchTerm': 'which'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)



    def test_search_questions_with_error(self):

        response = self.client().post('/questions/search',
                                      json={'searchTerm': 'abcdefghijk'})


        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'NOT_FOUND')


    # test delete question
    #first create question then delete the question by question_id
    def test_delete_question(self):
        self.new_question={
            'question': 'create new question',
            'answer': 'test answer',
            'difficulty': 1,
            'category': 1
        }

        question = Question(question=self.new_question['question'], answer=self.new_question['answer'],
                            category=self.new_question['category'], difficulty=self.new_question['difficulty'])
        question.insert()
        question_id = question.id

        response = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


     #test the quiz play

    def test_play_quiz(self):
        questions = Question.query.order_by(func.random()).limit(2).all()
        # previous_questions = [question.id for question in questions]

        response = self.client().post('/quizzes', json={
            'previous_questions':[],
            # 'quiz_category': {'id': 1}
            'quiz_category': {'type': 'Science', 'id': 1}
        })


        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_failed_play_quiz(self):
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()