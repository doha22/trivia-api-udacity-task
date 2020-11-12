from flask import request, abort

#constant variable
QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    if page < 1:
        return abort(422)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    formatted_questions = questions[start:end]

    return formatted_questions
