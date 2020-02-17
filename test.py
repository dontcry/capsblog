import json
import unittest
from models import setup_db, Actor, Movie, db
from flask_sqlalchemy import SQLAlchemy 
from app import create_app


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "UDACasting"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        self.new_movie = {'title': "Fireworks"}
        self.new_actor = {
            'name': "lihaoran",
            'age': 40
        }

        self.update_actor = {
            'id': 1, 
            'name': "Maya Angelou",
            'age': 41
        }
        self.restore_actor = {
            'id': 1, 
            'name': "Maya Angelou",
            'age': 1
        }
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
 
    def test_get_all_movies(self):
        res = self.client().get('/api/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_create_new_movie(self):
        count_before_creation = Movie.query.count()
        res = self.client().post('/api/movies', json=self.new_movie)
        data = json.loads(res.data)
        count_after_creation = Movie.query.count()
        self.assertEqual(count_before_creation, count_after_creation - 1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        count_before_creation = Movie.query.count()
        movie = Movie.query.order_by(db.desc(Movie.id)).first()
        res = self.client().delete('/api/movies/' + str(movie.id))
        data = json.loads(res.data)
        count_after_creation = Movie.query.count()
        self.assertEqual(count_before_creation, count_after_creation + 1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
