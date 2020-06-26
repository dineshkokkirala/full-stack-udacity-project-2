import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# Pagination
def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection[start:end]]
    return questions


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,OPTIONS,DELETE,PATCH')
        return response
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/api/categories')
    def get_categories():
        try:
            categories = Category.query.all()
            caty_dict = {cat.id: cat.type for cat in categories}
            return jsonify({
                "success": True,
                "categories": caty_dict
            })

        except Exception as e:
            print(e)
            abort(500)

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.



  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.


  '''
    @app.route('/api/questions')
    def get_questions():
        questions = Question.query.all()
        total_questions = len(questions)
        ques_list = paginate(request, questions)
        categories = Category.query.all()
        cat_dict = {cat.id: cat.type for cat in categories}

        if len(ques_list) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': ques_list,
            'categories': cat_dict,
            'total_questions': total_questions,
            'current_category': None
        })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  '''
    @app.route('/api/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        question = Question.query.get(q_id)

        if not question:
            abort(404)
        else:
            try:
                question.delete()
                return jsonify({
                    'success': True,
                    'deleted': q_id
                })
            except Exception:
                abort(422)

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  '''
    @app.route('/api/questions', methods=['POST'])
    def add_question():
        form_data = request.json

        if "searchTerm" in form_data:
            searchTerm = form_data['searchTerm'].strip()

            questions = Question.query.filter(Question.question.ilike(
                f'%{searchTerm}%')).all()

            ques_list = [q.format() for q in questions]

            return jsonify({
                "success": True,
                "questions": ques_list
            })

        else:

            if (form_data['question'].strip() == "") or (form_data['answer'].strip() == ""):
                abort(400)

            try:
                new_question = Question(question=form_data['question'].strip(), answer=form_data['answer'].strip(),
                                        category=form_data['category'], difficulty=form_data['difficulty'])
                new_question.insert()
            except Exception:
                abort(422)

            return jsonify({
                "success": True,
                "added": new_question.id
            })

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  '''
    @app.route('/api/categories/<int:cat_id>/questions')
    def get_category_questions(cat_id):
        questions = Question.query.filter_by(category=str(cat_id)).all()

        q_list = paginate(request, questions)

        if len(q_list) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': q_list,
            'total_questions': len(questions),
            'categories': Category.query.get(cat_id).format(),
            'current_category': cat_id
        })

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  '''
    @app.route('/api/quizzes', methods=['POST'])
    def play_quiz():

        request_data = request.json
        try:
            request_cat = request_data['quiz_category']['id']
        except Exception:
            abort(400)

        if request_cat == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(
                category=str(request_cat)).all()

            questions = [q.format() for q in questions]

        try:
            prev_qs = request_data['previous_questions']
        except Exception:
            abort(400)

        pruned_qs = []
        for q in questions:
            if q['id'] not in prev_qs:
                pruned_qs.append(q)

        if len(pruned_qs) == 0:
            return jsonify({
                'success': True
            })

        question = random.choice(pruned_qs)

        return jsonify({
            'success': True,
            'question': question
        })

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        })

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        })

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        })

    return app


if __name__ == '__main__':
    app.run()
