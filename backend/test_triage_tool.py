
from app.ai.tools.triage_tool import (
    apply_triage_safety_rules
)

print("\nCASE 1")
print(
    apply_triage_safety_rules(
        "hair loss",
        "Low"
    )
)

print("\nCASE 2")
print(
    apply_triage_safety_rules(
        "chest pain",
        "Low"
    )
)

print("\nCASE 3")
print(
    apply_triage_safety_rules(
        "patient is unconscious",
        "Medium"
    )
)

print("\nCASE 4")
print(
    apply_triage_safety_rules(
        "shortness of breath",
        "High"
    )
)

print("\nCASE 5")
print(
    apply_triage_safety_rules(
        "anaphylaxis",
        "Low"
    )
)