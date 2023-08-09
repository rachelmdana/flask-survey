from flask import Flask, render_template, request, redirect, flash
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "queenmillie2020"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route('/', methods=['GET', 'POST'])
def show_home():
    if request.method == 'POST':
        return redirect('/question/0')

    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions
    return render_template('home.html', title=survey_title, instructions=survey_instructions)


@app.route('/questions/<int:question_idx>', methods=["GET", "POST"])
def survey_questions(question_idx):
    # Check if the requested question index is within the valid range
    if question_idx < len(satisfaction_survey.questions):
        # Check if the requested question index matches the user's progress
        if question_idx != len(responses):
            # Flash a message about invalid question access and redirect
            flash("You're trying to access an invalid question.")
            return redirect(f"/questions/{len(responses)}")

        # Handle POST request (user submits answer)
        if request.method == "POST":
            selected_choice = request.form.get('choice')
            responses.append(selected_choice)

            next_question_idx = question_idx + 1

            # Check if there's another question to display
            if next_question_idx < len(satisfaction_survey.questions):
                return redirect(f"/questions/{next_question_idx}")
            else:
                return redirect("/completion")

        # Handle GET request (displaying the question)
        question = satisfaction_survey.questions[question_idx]
        return render_template('question.html', question=question, question_idx=question_idx)

    else:
        # Flash a message about invalid question access and redirect to the completion page
        flash("You're trying to access an invalid question.")
        return redirect("/completion")


@app.route('/completion')
def survey_complete():
    return render_template('completion.html')
