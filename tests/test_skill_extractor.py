from src.skill_extractor import extract_skills, compare_skills


def test_extract_skills():
    text = "Experience with Python, SQL, and Docker."

    result = extract_skills(text)

    assert "Python" in result
    assert "SQL" in result
    assert "Docker" in result


def test_case_insensitive():
    text = "Experience with PYTHON and sql."

    result = extract_skills(text)

    assert "Python" in result
    assert "SQL" in result


def test_compare_skills():
    resume_skills = ["Python", "SQL", "Git"]
    job_skills = ["Python", "SQL", "Docker"]

    matching, missing, coverage = compare_skills(
        resume_skills,
        job_skills
    )

    assert matching == ["Python", "SQL"]
    assert missing == ["Docker"]
    assert round(coverage, 1) == 66.7


def test_no_skills():
    result = extract_skills(
        "Excellent communication and teamwork."
    )

    assert result == []


def test_empty_job_skills():
    matching, missing, coverage = compare_skills(
        ["Python", "SQL"],
        []
    )

    assert matching == []
    assert missing == []
    assert coverage == 0

def test_skill_aliases():
    text = (
        "Experience with JS, ML, Postgres, "
        "RESTful APIs, and sklearn."
    )

    result = extract_skills(text)

    assert "JavaScript" in result
    assert "Machine Learning" in result
    assert "PostgreSQL" in result
    assert "REST API" in result
    assert "Scikit-learn" in result

def test_negated_skills():
    text = "I have no experience with AWS."

    result = extract_skills(text)

    assert "AWS" not in result

def test_aspirational_skills():
    text = "I am interested in learning Docker."

    result = extract_skills(text)

    assert "Docker" not in result