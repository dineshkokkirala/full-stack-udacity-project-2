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
        self.database_path = "postgres://{}/{}".format(
            'postgres:Dinesh1@@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_play_quiz_4(self):
        """Tests out the quiz playing functionality"""
        res = self.client().post('/api/quizzes',
                                 json={"previous_questions": [13], "quiz_category": {"type": "Geography"}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_play_quiz_3(self):
        """Tests out the quiz playing functionality"""
        res = self.client().post('/api/quizzes',
                                 json={"previous_questions": [13, 14, 15], "quiz_category": {"type": "Geography", "id": "3"}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertFalse('question' in data)

    def test_play_quiz_2(self):
        """Tests out the quiz playing functionality"""
        res = self.client().post('/api/quizzes',
                                 json={"previous_questions": [13, 14], "quiz_category": {"type": "Geography", "id": "3"}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['id'], 15)

    def test_play_quiz_1(self):
        """Tests out the quiz playing functionality"""
        res = self.client().post('/api/quizzes',
                                 json={"previous_questions": [], "quiz_category": {"type": "Geography", "id": "3"}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])
        self.assertEqual(data['question']['category'], 3)

    def test_get_categories(self):
        """Gets the /api/categories endpoint and checks valid results"""
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)

    def test_get_all_questions(self):
        """Gets all questions, including paginations (every 10 questions).  This endpoint should 
        return a list of questions, number of total questions, current category, categories."""
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['questions'][0]['id'], 5)

    def test_question_search(self):
        """Search for a term in a question"""
        res = self.client().post('/api/questions',
                                 json={"searchTerm": "  PeaNUT  "})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['questions'][0]['id'], 12)

    def test_get_questions_of_category(self):
        """Test GET request of questions only by a certain category"""
        res = self.client().get('/api/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 3)

        res = self.client().get('/api/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_post_empty_question(self):
        """POST a new question without a question or answer, should fail 400"""
        empty_question = {
            "question": "          ",
            "answer": "           ",
            "category": "6",
            "difficulty": 1
        }
        res = self.client().post('/api/questions', json=empty_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_invalid_delete_question(self):
        """Try to delete a question that doesn't exist, should get a 404 error"""
        res = self.client().delete(f'/api/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)

    def test_pagination(self):
        """Tests the pagination by getting page 2 and looking for known features"""
        res = self.client().get('/api/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 9)
        self.assertEqual(data['questions'][0]['id'], 15)

    def test_page_doesnt_exist(self):
        """Make sure we get a 404 error on a page which we know doesn't exist"""
        res = self.client().get('/api/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)


if __name__ == "__main__":
    unittest.main()
