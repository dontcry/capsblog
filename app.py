import json
from flask import Flask, jsonify, request, abort
from models import setup_db, db, Blog
from flask_cors import CORS

def parse_body(body_data):
    json_data = json.loads(body_data)
    return json_data

def create_app(test_config=None):

    app = Flask(__name__) 
    setup_db(app) 
    CORS(app, resource={r'/api/*': {'origins': '*'}})
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def get_greeting():
        excited = 'true'
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!!!!!"
        return greeting

    @app.route('/api/blogs')
    def show_blogs():
        result = db.session.query(Blog).all()
        blogs = [blog.format() for blog in result]
        data = {
            'success': True,
            'blogs': blogs, 
        } 
        return jsonify(data) 

    @app.route('/api/blogs', methods=['POST'])
    def create_blog():
        request_body = parse_body(request.get_data())
        try:
            blog = Blog(title=request_body['title']) 
            db.session.add(blog) 
            db.session.commit() 
            data = {
                'success': True,
                'blog': blog.format(), 
            } 
            return jsonify(data) 
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    return app
app = create_app()

if __name__ == '__main__':
    app.run()