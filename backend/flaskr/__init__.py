import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.orm import load_only
from sqlalchemy.sql.elements import Null

from sqlalchemy.sql.functions import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    @TODO: Set up CORS.
    '''
    CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTION')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        try:
            formatted_categories = [cat.format() for cat in categories]
            if len(formatted_categories) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'categories': formatted_categories
            })
        except:
            abort(400)

    '''

    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        current_page = request.args.get('page', 1, type=int)
        questions = Question.query.paginate(per_page=QUESTIONS_PER_PAGE,
                                            page=current_page)
        if questions.total == 0:
            abort(404)

        formatted_questions = [qes.format() for qes in questions.items]

        categories = Category.query.all()
        formatted_categories = [cat.format() for cat in categories]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions': len(Question.query.all()),
            'categories': formatted_categories,
            'currentCategory': None
        })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    TEST:click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter(Question.id == id).one_or_none()

        if (question is None):
            abort(404)
        else:
            question.delete()
        return jsonify({
            'success': True,
            'deletedId': id
        })

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will
    appear at the end of the last page
    of the questions list in the "List" tab.
    '''

    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        if not body:
            abort(400)

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        if(new_question is None or
           new_answer is None or
           new_difficulty is None or
           new_category is None):
            abort(400)

        try:
            question = Question(question=new_question,
                                answer=new_answer,
                                category=new_category,
                                difficulty=new_difficulty)
            question.insert()
            return jsonify({
                'success': True
            })
        except:
            abort(422)

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])   # edit the front-end
    def search_questions():
        body = request.get_json()

        if not body:
            abort(400)

        searchTerm = body.get('searchTerm', None)

        if (searchTerm is None):
            abort(400)

        current_page = request.args.get('page', 1, type=int)
        questions = Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).paginate(per_page=QUESTIONS_PER_PAGE, page=current_page)  # noqa: E501
        formatted_questions = [qes.format() for qes in questions.items]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions': len(Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).all()),  # noqa: E501
            'currentCategory': None
        })

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_catgeroyQuestions(id):
        current_page = request.args.get('page', 1, type=int)

        category = Category.query.filter(Category.id == id).one_or_none()
        if category is None:
            abort(404)

        questions = Question.query.filter(Question.category == id).paginate(per_page=QUESTIONS_PER_PAGE, page=current_page)  # noqa: E501
        formatted_questions = [qes.format() for qes in questions.items]
        current_cat = Category.query.filter(Category.id == id).one_or_none()

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions': len(questions.items),
            'currentCategory': current_cat.type
        })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()
        if body is None:
            abort(422)
        previous_q = body.get('previous_questions', None)
        category = body.get('quiz_category', None)
        category_id = category.get('id')

        if (previous_q is None or category is None):
            abort(400)

        if category_id == 0 or (category is Null):
            query = Question.query.order_by(func.random()).filter(Question.id.notin_(previous_q))  # noqa: E501
        else:
            query = Question.query.filter(Question.category == category_id).order_by(func.random()).filter(Question.id.notin_(previous_q))  # noqa: E501

        if not query.all():
            return jsonify({
                'success': True
            })

        question = query.first()

        if not (question.format().get('question')):
            while (not (question.format().get('question'))):
                question = query.first()

        if len(previous_q) == 5:   # going by my instructor note that the quiz is five questions only  # noqa: E501
            return jsonify({
                'success': True
            })

        return jsonify({
            'success': True,
            'question': question.format()
        })

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(422)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
