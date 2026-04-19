def generate_risk(structured_data):
    lab_values = structured_data.get("lab_test_values", [])

    abnormal = [i for i in lab_values if i.get("status") in ["Low", "High"]]
    total = len(lab_values)

    if total == 0:
        return "Unknown"

    abnormal_count = len(abnormal)
    abnormal_ratio = abnormal_count / total

    # 🔹 Cap abnormal influence
    capped_count = min(abnormal_count, 8)

    # 🔹 Base score
    score = (capped_count * 1.0) + (abnormal_ratio * 4)

    # 🔹 Adjust for clustering (generic, no hardcoding)
    name_groups = [i["name"].split()[0] for i in abnormal]
    cluster_bonus = len(name_groups) - len(set(name_groups))

    score += cluster_bonus

    # 🔹 Final classification
    if score >= 12:
        return "High"
    elif score >= 6:
        return "Moderate"
    elif abnormal_count >= 1:
        return "Mild"
    else:
        return "Low"