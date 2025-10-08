# ai_utils.py

def granite_generate_response(prompt: str) -> str:
    if "group a exam" in prompt.lower():
        return ("To apply for Group A Civil Services Exam (like UPSC), "
                "visit the UPSC official website (https://www.upsc.gov.in). "
                "Register on the portal, fill the application form, "
                "upload required documents, pay the fee, and download the admit card.")
    elif "civil service" in prompt.lower():
        return ("Civil Services exams (IAS, IPS, IFS, etc.) are conducted by UPSC. "
                "Eligibility: Any graduation degree, Age 21–32 years (varies by category).")
    else:
        return "I’m still learning! Please ask about Group A or Civil Services."


def analyze_sentiment(feedback: str) -> str:
    feedback = feedback.lower()
    if any(word in feedback for word in ["good", "great", "excellent", "helpful"]):
        return "Positive 😀"
    elif any(word in feedback for word in ["bad", "poor", "slow", "useless"]):
        return "Negative 😞"
    else:
        return "Neutral 😐"


def process_concern(concern: str) -> str:
    """
    Dummy concern processing.
    Later you can store this in a DB or send to officials.
    """
    concern = concern.lower()
    if "road" in concern:
        return "Concern noted: Road issue reported. Public works department will review."
    elif "water" in concern:
        return "Concern noted: Water supply issue reported. Municipal department will review."
    elif "electricity" in concern or "light" in concern:
        return "Concern noted: Electricity/lighting issue reported. Electricity board will review."
    else:
        return "Your concern has been recorded. The respective department will review it."
