import surveys as surveys
import flask as fl
import jinja2 as ji
from flask_debugtoolbar import DebugToolbarExtension

# the toolbar is only enabled in debug mode:

app = fl.Flask(__name__)

app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = '<replace with a secret key>'

toolbar = DebugToolbarExtension(app)


responses = []
q = 0

# Next, let’s handle our first request. When the user goes to the root route, render a page that shows the user the title of the survey, the instructions, and a button to start the survey. The button should serve as a link that directs the user to /questions/0 (the next step will define that route).

@app.route('/')
def root():
    return fl.render_template('home.html', title=surveys.satisfaction_survey.title, instructions=surveys.satisfaction_survey.instructions, q=q)


@app.route('/questions/<int:q>')
def questions(q):
    if q != len(responses):
        fl.flash('stop it')
        return fl.redirect(fl.url_for('questions', q=len(responses)))
    
    if len(responses) == len(surveys.satisfaction_survey.questions):
        fl.flash('stop it')
        return fl.redirect(fl.url_for('thanks'))
    question = surveys.satisfaction_survey.questions[int(q)]
    return fl.render_template('questions.html', q=q, question=question.question, answers=question.choices)

@app.post('/answer/<int:q>')
def answer(q):
    answered = fl.request.form.get('choices')
    q += 1
    responses.append(answered)

    if q >= len(surveys.satisfaction_survey.questions):
        return fl.redirect(fl.url_for('thanks'))
    
    else:
        return fl.redirect(fl.url_for('questions', q=q))

@app.route('/thanks')
def thanks():
    return fl.render_template('thanks.html', answers = responses)
