def calculate_risk(similarity):
    fraud_probability = 1 - similarity
    risk_score = fraud_probability * 100

    if risk_score < 40:
        level = "Low Risk"
    elif risk_score < 70:
        level = "Medium Risk"
    else:
        level = "High Risk"

    return {
        "risk_score": round(risk_score, 2),
        "fraud_probability": round(fraud_probability, 2),
        "risk_level": level
    }
