import sys
import json
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, jsonify, request, abort
from user import get_access_token, get_users, get_user_info
from models import setup_db, db, Actor, Movie, Cast
from flask_cors import CORS
from auth import AuthError, requires_auth

access_token = ''

def get_auth0_access_token():
    global access_token 
    access_token = get_access_token() 

apsched = BackgroundScheduler()
apsched.add_job(get_auth0_access_token, 'interval', seconds=1000)
apsched.start()


def parse_body(body_data):
    json_data = json.loads(body_data)
    return json_data

def create_app(test_config=None):
    app = Flask(__name__) 
 
    setup_db(app) 
    CORS(app, resource={r'/api/*': {'origins': 'http://127.0.0.1:8080/'}})
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response
 
    @app.route('/api/userinfo')
    def getUserInfo(): 
        print('getUserInfo')
        userinfo = get_user_info()
        if userinfo:  
            data = {
                'success': True, 
                'userinfo':userinfo
            }  
            return jsonify(data) 
        else: 
           abort(401)

    
 
    @app.route('/api/actors') 
    @requires_auth('read:actors')
    def actors():
        result = Actor.query.order_by('id').all()
        actors = [actor.format() for actor in result]
        return jsonify({'success': True, 'actors': actors})

    @app.route('/api/actors/<int:actor_id>', methods=['GET']) 
    @requires_auth('read:actors')
    def get_actor(actor_id): 
        try:
            actor = Actor.query.order_by('id').filter(
                Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404) 
            return jsonify({
                'actor': actor.format(),
                'success': True})
        finally:
            db.session.close()

    @app.route('/api/actors', methods=['POST']) 
    @requires_auth('create:actor')
    def create_actor():
        request_body = parse_body(request.get_data()) 
        req_name = request_body['name'] 
        actor = Actor(name=req_name) 
        Actor.insert(actor) 
        result = Actor.query.order_by('id').all()
        actors = [actor.format() for actor in result]
        return jsonify({'success': True, 'actors': actors}) 

    @app.route('/api/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actor') 
    def update_actor(actor_id):
        request_body = parse_body(request.get_data())
        try:
            actor = db.session.query(Actor).filter(
                Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404) 
            if 'name' in request_body:
                actor.name = request_body['name'] 
            if 'age' in request_body:
                actor.age = request_body['age']
            if 'gender' in request_body:
                actor.gender = request_body['gender']            
            if 'photo' in request_body:
                actor.photo = request_body['photo']                
            actor.update()
            result = Actor.query.order_by('id').all()
            actors = [actor.format() for actor in result]
            return jsonify({'success': True, 'actors': actors})
        except Exception:
            print(sys.exc_info())
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/api/actors/<int:actor_id>', methods=['DELETE']) 
    @requires_auth('delete:actor')
    def delete_actor(actor_id):
        try:
            actor = db.session.query(Actor).filter(
                Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            actor.delete()
            result = Actor.query.order_by('id').all()
            actors = [actor.format() for actor in result]
            return jsonify({'success': True, 'actors': actors})
        except Exception:
            print(sys.exc_info())
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    @app.route('/api/movies')
    @requires_auth('read:movies')
    def movies():
        result = Movie.query.order_by('id').all()
        movies = [movie.format() for movie in result]
        return jsonify({'success': True, 'movies': movies})

    @app.route('/api/movies/<int:movie_id>', methods=['GET']) 
    @requires_auth('read:movies')
    def get_movie(movie_id): 
        try:
            movie = Movie.query.order_by('id').filter(
                Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404) 
            return jsonify({
                'movie': movie.format(),
                'success': True})
        finally:
            db.session.close()

    @app.route('/api/movies', methods=['POST']) 
    @requires_auth('create:movie')
    def create_movie():
        request_body = parse_body(request.get_data()) 
        req_title = request_body['title'] 
        movie = Movie(title=req_title)  
        if 'release_date' in request_body:
            movie.release_date = request_body['release_date']
        if 'poster' in request_body:
            movie.poster = request_body['poster']   
        Movie.insert(movie) 
        result = Movie.query.order_by('id').all()
        movies = [movie.format() for movie in result]
        return jsonify({'success': True, 'movies': movies}) 

    @app.route('/api/movies/<int:movie_id>', methods=['PATCH']) 
    @requires_auth('update:movie')
    def update_movie(movie_id):
        request_body = parse_body(request.get_data())
        try:
            movie = db.session.query(Movie).filter(
                Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404) 
            if 'title' in request_body:
                movie.title = request_body['title'] 
            if 'release_date' in request_body:
                movie.release_date = request_body['release_date']
            if 'poster' in request_body:
                movie.poster = request_body['poster']                
            movie.update()
            result = Movie.query.order_by('id').all()
            movies = [movie.format() for movie in result]
            return jsonify({'success': True, 'movies': movies})
        except Exception:
            print(sys.exc_info())
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/api/movies/<int:movie_id>', methods=['DELETE']) 
    @requires_auth('delete:movie')
    def delete_movie(movie_id):
        try:
            movie = db.session.query(Movie).filter(
                Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()
            result = Movie.query.order_by('id').all()
            movies = [movie.format() for movie in result]
            return jsonify({'success': True, 'movies': movies})
        except Exception:
            print(sys.exc_info())
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    return app

app = create_app()

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not found'
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(400)
def badrequest(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400

@app.errorhandler(AuthError)
def AuthErrorHandle(error):
    err = error.to_dict()
    return jsonify({
        "success": False,
        "error": err['status_code'],
        "message": err['message'],
    }), err['status_code']
if __name__ == '__main__':
    app.run()