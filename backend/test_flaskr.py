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
        self.database_path = "postgresql://postgres:123@localhost:5432/" + self.database_name 
        setup_db(self.app, self.database_path)

        self.Q = {
         'id':40,
         'question': 'who is the CEO of Udacity',
         'answer': 'Gabriel Dalporto',
         'category': 4,
         'difficulty': 2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
       
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
       
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['currentCategory'], None)

    def test_404_sent_requesting_beyond_valid_page(self):
       
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_question(self):
    
        res = self.client().post('/questions', json=self.Q)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_add_question_with_incomplete_info(self):

        Q = {
         'id':40,
         'question': 'who is the CEO of Udacity',
         'difficulty': 2
        }
    
        res = self.client().post('/questions', json=Q)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)    

    def test_delete_question(self):
        q = Question(question=self.Q['question'], answer=self.Q['answer'],
            category=self.Q['category'], difficulty=self.Q['difficulty'])
        q.insert()

        res = self.client().delete('/questions/'+str(q.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_if_question_does_not_exist(self):
        
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_search_questions(self):
       
        res = self.client().post('/questions/search',json={'searchTerm': 'Clay'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['currentCategory'], None)

    def test_search_questions_with_unavaliable_search_term(self):
        
        res = self.client().post('/questions/search',json={'searchTerm': 'qwerty'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['totalQuestions'], 0)

        
    def test_get_catgeroyQuestions(self):
        
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_if_category_has_no_questions(self):
        
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_quizzes(self):
        info={
            'previous_questions': [5, 9],
            'quiz_category': {
                'id': '4',
                'type': 'History'
            }
        }

        res = self.client().post('/quizzes', json=info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    def test_quizzes_with_invalid_category(self):
        info= {
            'previous_questions': [],
            'quiz_category': {
                'id': '100',
                'type': 'Randoms'
            }
        }
        res = self.client().post('/quizzes', json=info)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True) 
        # when success is the only attribute in the json body means the quiz has stopped
    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()