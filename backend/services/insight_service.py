def generate_insights(data):
    insights = []

    lab_values = data.get("lab_test_values", [])

    low_params = []
    high_params = []

    for item in lab_values:
        if item.get("status") == "Low":
            low_params.append(item["name"])
        elif item.get("status") == "High":
            high_params.append(item["name"])

    if low_params:
        insights.append(f"Some parameters are lower than normal: {', '.join(low_params[:5])}")

    if high_params:
        insights.append(f"Some parameters are higher than normal: {', '.join(high_params[:5])}")

    blood_markers = ["Hemoglobin", "RBC", "HCT", "MCV", "MCH"]
    low_blood = [p for p in blood_markers if p in low_params]

    if len(low_blood) >= 2:
        insights.append("Multiple blood-related parameters are low, which may indicate anemia or related conditions.")

    inflammation_markers = [
        "High sensitivity CRP",
        "Erythrocyte Sedimentation Rate"
    ]
    high_inflammation = [p for p in inflammation_markers if p in high_params]

    if high_inflammation:
        insights.append("Inflammation markers are elevated, which may indicate inflammation or infection.")

    return insights
