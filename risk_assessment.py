def assess_risk(
    fever,
    pain_level,
    breathing_issue,
    medication_taken
):

    if (
        fever == "Yes"
        and pain_level == "Severe"
    ):
        return "High"

    if breathing_issue == "Yes":
        return "High"

    if medication_taken == "No":
        return "Medium"

    if pain_level == "Moderate":
        return "Medium"

    return "Low"