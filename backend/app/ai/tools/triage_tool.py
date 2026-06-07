def apply_triage_safety_rules(
    symptoms: str,
    ai_urgency: str
):

    symptoms_lower = symptoms.lower()

    emergency_patterns = {

        "Cardiac": [
            "heart attack",
            "cardiac arrest",
            "crushing chest pain",
            "severe chest pain"
        ],

        "Respiratory": [
            "cannot breathe",
            "not breathing",
            "respiratory distress",
            "severe breathing difficulty"
        ],

        "Neurological": [
            "unconscious",
            "loss of consciousness",
            "sudden paralysis",
            "sudden weakness",
            "sudden numbness",
            "facial drooping"
        ],

        "Stroke": [
            "slurred speech",
            "unable to speak",
            "one sided weakness",
            "one sided numbness"
        ],

        "Trauma": [
            "major trauma",
            "severe bleeding",
            "gunshot",
            "stab wound"
        ],

        "Allergic": [
            "anaphylaxis",
            "throat swelling"
        ],

        "Pediatric Critical": [
            "blue lips",
            "not responding"
        ]
    }

    high_risk_patterns = {

        "Cardiac": [
            "chest pain",
            "palpitations",
            "irregular heartbeat",
            "chest tightness"
        ],

        "Respiratory": [
            "shortness of breath",
            "breathing difficulty",
            "persistent cough",
            "coughing blood"
        ],

        "Neurological": [
            "stroke",
            "seizure",
            "confusion",
            "paralysis",
            "slurred speech",
            "numbness",
            "weakness",
            "blurred vision",
            "loss of vision",
            "migraine with numbness",
            "dizziness"
        ],

        "Trauma": [
            "fracture",
            "head injury",
            "deep wound",
            "fall injury"
        ],

        "Infectious": [
            "high fever",
            "sepsis",
            "blood infection",
            "persistent fever"
        ],

        "Gastrointestinal": [
            "vomiting blood",
            "blood in stool",
            "severe abdominal pain",
            "black stool"
        ],

        "Renal": [
            "blood in urine",
            "unable to urinate"
        ],

        "Diabetic": [
            "low sugar",
            "high sugar",
            "diabetic emergency"
        ],

        "Psychiatric": [
            "suicidal thoughts",
            "self harm",
            "hallucinations"
        ],

        "Emergency General": [
            "collapse",
            "fainting",
            "severe pain"
        ]
    }

    # STEP 1 — Emergency Override

    for category, keywords in emergency_patterns.items():

        for keyword in keywords:

            if keyword in symptoms_lower:

                return {

                    "original_ai_urgency": ai_urgency,

                    "urgency_level": "Emergency",

                    "override_applied": True,

                    "trigger_category": category,

                    "trigger_keyword": keyword,

                    "reason":
                    f"Critical {category.lower()} symptom detected."
                }

    # STEP 2 — High Risk Override

    for category, keywords in high_risk_patterns.items():

        for keyword in keywords:

            if keyword in symptoms_lower:

                if ai_urgency.lower() in [
                    "low",
                    "medium"
                ]:

                    return {

                        "original_ai_urgency": ai_urgency,

                        "urgency_level": "High",

                        "override_applied": True,

                        "trigger_category": category,

                        "trigger_keyword": keyword,

                        "reason":
                        f"High-risk {category.lower()} symptom detected."
                    }

    # STEP 3 — Age-Based Safety Upgrade

    if ai_urgency.lower() == "low":

        elderly_keywords = [
            "chest pain",
            "shortness of breath",
            "weakness",
            "confusion",
            "dizziness"
        ]

        for keyword in elderly_keywords:

            if keyword in symptoms_lower:

                return {

                    "original_ai_urgency": ai_urgency,

                    "urgency_level": "Medium",

                    "override_applied": True,

                    "trigger_category": "Age Safety",

                    "trigger_keyword": keyword,

                    "reason":
                    "Potentially serious symptom detected."
                }

    # STEP 4 — No Override

    return {

        "original_ai_urgency": ai_urgency,

        "urgency_level": ai_urgency,

        "override_applied": False,

        "trigger_category": None,

        "trigger_keyword": None,

        "reason":
        "No safety override required."
    }