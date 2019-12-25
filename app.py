import os
from flask import Flask, jsonify
from models import setup_db, db, Blog
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__) 
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = 'true'
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!!!!!"
        return greeting

    @app.route('/blogs')
    def show_blogs():
        result = db.session.query(Blog).all()
        blogs = [blog.format() for blog in result]
        data = {
            'success': True,
            'blogs': blogs, 
        } 
        return jsonify(data)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()