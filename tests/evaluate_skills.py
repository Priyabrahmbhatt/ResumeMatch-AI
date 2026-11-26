from src.skill_extractor import extract_skills

evaluation_data = [
    {
        "text": "I have experience with Python, SQL, and Docker.",
        "expected": ["Python", "SQL", "Docker"],
    },
    {
        "text": "Built web applications using JS and React.",
        "expected": ["JavaScript", "React"],
    },
    {
        "text": "Developed ML models using sklearn and Pandas.",
        "expected": ["Machine Learning", "Scikit-learn", "Pandas"],
    },
    {
        "text": "Worked with Postgres, Git, and Linux.",
        "expected": ["PostgreSQL", "Git", "Linux"],
    },
    {
        "text": "Excellent communication and leadership skills.",
        "expected": [],
    },
        {
        "text": "I have no experience with AWS.",
        "expected": [],
    },
    {
        "text": "Interested in learning Docker and Kubernetes.",
        "expected": [],
    },
    {
        "text": "Developed machine learning models using Python.",
        "expected": ["Machine Learning", "Python"],
    },
]


def evaluate():
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for example in evaluation_data:
        predicted = set(extract_skills(example["text"]))
        expected = set(example["expected"])

        true_positives += len(predicted & expected)
        false_positives += len(predicted - expected)
        false_negatives += len(expected - predicted)

        print("\nText:", example["text"])
        print("Expected:", sorted(expected))
        print("Predicted:", sorted(predicted))

    precision = (
        true_positives / (true_positives + false_positives)
        if true_positives + false_positives > 0
        else 0
    )

    recall = (
        true_positives / (true_positives + false_negatives)
        if true_positives + false_negatives > 0
        else 0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall > 0
        else 0
    )

    print("\n--- Evaluation Results ---")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    print(f"F1-score: {f1:.2%}")


if __name__ == "__main__":
    evaluate()