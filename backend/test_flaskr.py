import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from settings import TEST_DB_NAME, DB_USER, DB_PASSWORD


from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME        
        database_user = DB_USER
        database_password = DB_PASSWORD
        self.database_path = "postgresql://{}:{}@{}/{}".format(database_user, database_password,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalQuestions'], 10)
        self.assertEqual(response.status_code, 400)

     
   
    def test_delete_questions(self):
        response = self.client().delete('/questions/50')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted question'], 'Question deleted successfully')

        self.assertEqual(data['success'], False)

    
    def test_post_questions(self):
        response = self.client().post('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_search_questions(self):
        response = self.client().post('/questions/search')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(data['success'], True)
    
    def test_search_categories(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200) 

        self.assertEqual(data['success'], True)

    
    def test_play_quiz(self):
        response = self.client().post('/quizzes')
        data =json.loads(response.data)
        self.assertEqual(response.status_code, 200) 

        self.assertEqual(data['success'], True)
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()