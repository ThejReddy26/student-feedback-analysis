from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from models.feedback_model import get_courses, get_questions, save_feedback

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("/feedback", methods=["GET", "POST"])
def feedback():
    config = current_app.config
    courses = get_courses(config)
    questions = get_questions(config)

    if request.method == "POST":
        try:
            course_id = int(request.form.get("course_id", ""))
            valid_courses = {c["course_id"] for c in courses}
            if course_id not in valid_courses:
                raise ValueError("Please select a valid course.")

            answers = []
            for question in questions:
                raw = request.form.get(f"rating_{question['question_id']}", "")
                rating = int(raw)
                if rating < 1 or rating > 5:
                    raise ValueError("Every rating must be between 1 and 5.")
                answers.append((question["question_id"], rating))

            if not answers:
                raise ValueError("No active feedback questions are available.")

            comment = request.form.get("comment", "").strip()
            if len(comment) > 1000:
                raise ValueError("Comment must be 1000 characters or fewer.")

            save_feedback(config, course_id, answers, comment)
            flash("Thank you! Your anonymous feedback was submitted.", "success")
            return redirect(url_for("index"))
        except (ValueError, TypeError):
            flash("Please select a course and provide a rating from 1 to 5 for every question.", "danger")

    return render_template("feedback.html", courses=courses, questions=questions)
