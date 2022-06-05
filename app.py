from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start_survey():
    """Shows the survey start screen"""
    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions

    return render_template('survey_start.html', title = survey_title, instructions = survey_instructions)

@app.route('/questions/<num>')
def question_page(num):
    """Shows the question screen, if the user changes the url to an invalid question, or tries to skip questions, the page will automatically redirect to the next unanswered question."""
    next_question = int(num) + 1
    length = len(satisfaction_survey.questions)
    answers = len(session['responses'])
    
    try:
        current_question = satisfaction_survey.questions[int(num)].question
        choices = satisfaction_survey.questions[int(num)].choices
    except IndexError:
            flash("Invalid question!")
            return redirect(f'/questions/{answers}')

    if answers != int(num):
        flash("Invalid question!")
        return redirect(f'/questions/{answers}')
    else:
        return render_template('questions.html', current_question=current_question, next=next_question, choices = choices, length = length, answers = answers)
        
@app.route('/initial-session')
def set_initial_session():
    """Sets the initial session for the browser"""
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/handle-form-session')
def handle_session():
    """Return the next question and save answers to session"""
    responses = session['responses']
    responses.append(request.args['answer'])
    session['responses'] = responses
        
    length = len(session['responses'])
    survey_question_amt = len(satisfaction_survey.questions)
    print(length)
    print(session['responses'])

    if length == survey_question_amt:
        return redirect('/end')
    else:
        return redirect(f'/questions/{length}')

@app.route('/end')
def end():
    """End page for the survey"""
    return render_template('end.html')
    