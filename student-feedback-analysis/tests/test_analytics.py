from analysis.analytics import build_summary

def test_build_summary_calculates_average_and_counts():
    rows = [
        {"course_name": "Python", "question_text": "Clarity", "rating": 4, "submitted_at": None},
        {"course_name": "Python", "question_text": "Clarity", "rating": 2, "submitted_at": None},
        {"course_name": "Math", "question_text": "Clarity", "rating": 5, "submitted_at": None},
    ]
    result = build_summary(rows)
    assert result["total_responses"] == 3
    assert result["overall_average"] == 3.67
    assert len(result["courses"]) == 2

def test_empty_summary():
    result = build_summary([])
    assert result["total_responses"] == 0
    assert result["overall_average"] is None
