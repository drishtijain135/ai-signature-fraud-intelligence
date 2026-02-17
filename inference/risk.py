def calculate_risk(similarity):
    """
    Converts similarity score into financial fraud intelligence metrics.
    """

    # Convert similarity into fraud probability
    fraud_probability = 1 - float(similarity)

    # Risk Score (0–100)
    risk_score = fraud_probability * 100

    # Behavioral Deviation Index (scaled indicator)
    behavioral_deviation_index = fraud_probability * 10

    # Risk Level Classification
    if risk_score >= 75:
        risk_level = "High Risk"
    elif risk_score >= 40:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    return {
        "risk_score": round(risk_score, 2),
        "fraud_probability": round(fraud_probability, 2),
        "behavioral_deviation_index": round(behavioral_deviation_index, 2),
        "risk_level": risk_level
    }

