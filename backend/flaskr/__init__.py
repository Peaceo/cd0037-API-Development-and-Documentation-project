import os
from pickle import APPEND
from unicodedata import category
from webbrowser import get
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
from models import setup_db, Question, Category, db
from importlib import reload





QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__) 
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000/"}})
    # CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    '''   @app.after_request
    def after_request(response):
        
        response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept, Observe, Authorization, Cache-Control')
        response.headers.add('Access-Control-Allow-Origin',"http://localhost:3000")
        response.headers.add('Access-Control-Allow-Methods', 'GET, HEAD, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Allow', 'GET,PUT,POST,DELETE,PATCH,UPDATE')

        return response '''
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin',"http://localhost:3000")

        response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        
        response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        response.headers.add('Access-Control-Allow-Credentials', 'true')

        return response

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def all_categories():
        categories = Category.query.all()
        formatted_categories = {}
        for category in categories:
            formatted_categories[f'{category.id}'] = category.type
        data = {
            "categories": formatted_categories
        }
        return jsonify(data)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def question():
        # db query
        questions = Question.query.all()
        categories = Category.query.all()
        length = len(questions)
        formatted_questions = paginate_questions(request, questions)

        if len(formatted_questions) == 0:
            abort(404)
        try:        
            formatted_questions = [question.format() for question in questions]
            formatted_categories = {}
            for category in categories:
                formatted_categories[f'{category.id}'] = category.type
                
            
            return jsonify({
                
                'questions': formatted_questions,
                'totalQuestions':length,
                'categories': formatted_categories,
                'currentCategory': category.type,
                'success': True            
            })
        except:
            abort(404)

        
        ''' 
            for question in questions:
                data = {
                'questions':{
                    'achieve':'achievement',
                    'id':question.id,
                    'question': question.question,
                    'answer': question.answer,
                    'difficulty': str(question.difficulty),
                    'category': str(question.category)
                }
            }
        return jsonify(data)


        })'''

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            # unique_question = Question.query.filter_by(id=question_id).first()
            unique_question = Question.query.filter(Question.id == question_id).one_or_none()

            if unique_question is None:
                abort(404)
            
            unique_question.delete()    
            # selection = Question.query.order_by(Question.id).all()
            # current_question = paginate_questions(request, selection)

            return jsonify({
            'success': True,
            'deleted question': question_id, 
            })
        except:
            abort(422)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods = ['POST'])
    def post_new_question():        
        body = request.get_json()
        try:
            question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty_score = body.get('difficulty', None)

            question = Question(question=question, answer=new_answer, category=new_category, difficulty=new_difficulty_score)
            question.insert()
            db.session.close()

            return jsonify({
                    "success": True,
                    "created": question.id,   
                })

        except:
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/<string:search_term>', methods=['POST'])
    # @cross_origin(origins='*')
    def search_questions(search_term):
        # search = request.form.get('search_term')
        try:
            search_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            data = paginate_questions(request, search_questions)
            count = len(search_questions)
            # data = []
            # for search in search_questions:
            #     data.append({
            #         "id":search.id,
            #         "question":search.question,
            #         "answer":search.answer,
            #         "category":search.category,
            #         "new_difficulty":search.difficulty,
            #     }) 

            response = jsonify({
                    
                    "success":True,
                    "count":count,
                    "data":data

                })
            # response.headers.add("Access-Control-Allow-Origin", "*")
            # response.header("Access-Control-Allow-Origin", "*");
            # response.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
            return response
        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<string:category_id>/questions', methods=['GET'])
    def get_questions_by_categories(category_id):
        try:
            # categories_questions = Question.query.filter(Question.category.ilike(f'{category_id}')).order_by(Question.id).all()
            categories_questions = Question.query.filter(Question.category == category_id).all()
            # questions = questions.query.filter(questions.name.ilike('%' + request.form['search_term'] + '%')).all()
            current_question = paginate_questions(request, categories_questions)
            print(current_question)

            if current_question == None:
                abort(404)


            return jsonify({                
                "questions":current_question,
                "TotalQuestions":len(current_question),
                "currentCategory":"Science"
                
            })
        except:
            abort(404)  
    


    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get("previous_questions")
        quiz_category = body.get("quiz_category")
        questions = Question.query.all()

        play_question = []

        for item in questions:
            if len(previous_questions) == 0 and item.category != int(
                quiz_category["id"]
            ):
                play_question.append(item.format())
            else:
                for item_ in previous_questions:
                    if item_ != item.id and item.category != int(quiz_category["id"]):
                        play_question.append(item.format())

        return jsonify({"question": random.choice(play_question)})

        

            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """   
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422  

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400, 
            "message": "bad request"
            }), 400


    
    
    
    ''' @app.route('/')
    def hello():
        return "Hello World"
    return app 
''' 
    return app

