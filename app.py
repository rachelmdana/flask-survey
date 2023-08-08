from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "queenmillie2020"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/', methods=['GET', 'POST'])
def show_home():
    if request.method == 'POST':
        session['responses'] = []
        return redirect('/questions/0')

    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions
    return render_template('home.html', title=survey_title, instructions=survey_instructions)


@app.route('/question/<int:question_idx>', methods=["GET", "POST"])
def survey_questions(question_idx):
    responses = session.get('responses', [])

    if question_idx < len(satisfaction_survey.questions):
        if question_idx != len(responses):
            flash("You're trying to access an invalid question.")
            return redirect(f"/question/{len(responses)}")

        if request.method == "POST":
            selected_choice = request.form.get('choice')
            responses.append(selected_choice)
            session['responses'] = responses

            next_question_idx = question_idx + 1

            if next_question_idx < len(satisfaction_survey.questions):
                return redirect(f"/question/{next_question_idx}")
            else:
                return redirect("/completion")

        question = satisfaction_survey.questions[question_idx]
        return render_template('question.html', question=question, question_idx=question_idx)

    else:
        flash("You're trying to access an invalid question.")
        return redirect("/completion")


@app.route('/completion')
def survey_complete():
    return render_template('completion.html')
