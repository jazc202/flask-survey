import surveys as surveys
import flask as fl
import jinja2 as ji
from flask_debugtoolbar import DebugToolbarExtension

# the toolbar is only enabled in debug mode:

app = fl.Flask(__name__)

app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'secret'

toolbar = DebugToolbarExtension(app)


responses = []
q = 0

# Next, let’s handle our first request. When the user goes to the root route, render a page that shows the user the title of the survey, the instructions, and a button to start the survey. The button should serve as a link that directs the user to /questions/0 (the next step will define that route).



@app.route('/')
def root():
    return fl.render_template('home.html', surveys=surveys.surveys, q=q)


@app.post('/begin')
def begin():
    fl.session['current_survey'] = fl.request.form.get('surveys')
    fl.session['responses'] = []

    return fl.redirect(fl.url_for('questions', q=0))


@app.route('/questions/<int:q>')
def questions(q):
    if q != len(fl.session['responses']):
        fl.flash('stop it')
        return fl.redirect(fl.url_for('questions', q=len(fl.session['responses'])))

    if len(fl.session['responses']) == len(surveys.surveys[fl.session['current_survey']].questions):
        fl.flash('stop it')
        return fl.redirect(fl.url_for('thanks'))
    question = surveys.surveys[fl.session['current_survey']].questions[int(q)]
    return fl.render_template('questions.html', q=q, question=question.question, answers=question.choices, allow_txt=question.allow_text)

# responses [
# {question: q, choice: c, comment: com}
# ]

@app.post('/answer/<int:q>')
def answer(q):
    choice = fl.request.form.get('choices')
    question = surveys.surveys[fl.session['current_survey']].questions[int(q)].question
    comment = fl.request.form.get('comment')

    answer = {'question': question, 'choice': choice, 'comment': comment}
    q += 1
    responses = fl.session['responses']
    responses.append(answer)
    fl.session['responses'] = responses
    
    if q >= len(surveys.surveys[fl.session['current_survey']].questions):
        response = fl.make_response(fl.redirect(fl.url_for('thanks')))
        response.set_cookie('finished_survey', fl.session['current_survey'])
        return response
        # return fl.redirect(fl.url_for('thanks'))

    else:
        return fl.redirect(fl.url_for('questions', q=q))


@app.route('/thanks')
def thanks():
    return fl.render_template('thanks.html', answers=fl.session['responses'])
