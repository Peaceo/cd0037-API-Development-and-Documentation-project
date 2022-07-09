import os
import unittest
import json
from urllib import response
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
        response = self.client().get('/questions?page=1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["totalQuestions"])
        
    def test_get_questions_failure(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], "Not found")
         
    def test_delete_questions(self):
        response = self.client().delete('/questions/57')
        data = json.loads(response.data)
        questions = Question.query.filter(Question.id == 57).one_or_none()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(questions, None)

    def test_delete_questions_failure(self):
        response = self.client().delete('/questions/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], "Unprocessable")

    def test_post_questions(self):
        response = self.client().post('/questions/json', json = {
            "question": "who is the founded of udacity", 
            "answer":   "Sebastian Thrun",
            "difficulty": 1,
            "category":"sciences"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_questions_failure(self):
        response = self.client().post('/questionsjson', json = {
            "question": "who is the founded of udacity", 
            "answer":   "Sebastian Thrun",
            "difficulty": 1,
            "category":"sciences"})
  
    def test_search_questions(self):
        response = self.client().post('/questions/<string:search_term>', json = {"search": "who"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_questions_failure(self):
        response = self.client().post("/questions/<string:search_term>", json={"search": "sponge"})
    
    def test_get_categories(self):
        response = self.client().get("/categories")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["categories"])

    def test_get_categories_failure(self):
        response = self.client().get("/ategories")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
    
    def test_get_by_categories(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["TotalQuestions"])

    def test_get_by_categories_failure(self):
        response = self.client().get("/categories/1000/questions")
        data = json.loads(response.data)
       
    def test_play_quiz(self):
        response = self.client().post("/quizzes/json",json={"previous_questions": [4, 6], "quiz_category": "ALL"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    
    def test_play_failure(self):
        response = self.client().post("/quizzes/json", json={"previous_questions": [1], "quiz_category": "food"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()