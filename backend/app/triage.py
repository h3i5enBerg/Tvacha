from __future__ import annotations

from app.schemas import CareGuidance, ConditionPrediction, SymptomInput, TriageResult

PRELIMINARY_DISCLAIMER = (
    "This result is an AI-assisted preliminary dermatological screening tool and "
    "does not constitute a medical diagnosis. Always consult a qualified "
    "dermatologist or registered AYUSH/medical practitioner for clinical evaluation."
)

_AYUSH_CONDITION_GUIDANCE: dict[str, list[str]] = {
    "eczema": [
        "Gentle cleansing with lukewarm Neem (Azadirachta indica) leaf decoction or mild non-soap cleanser, followed by patting dry.",
        "Apply pure Aloe vera (Kumari) gel or plain coconut/sesame oil on intact, non-oozing dry skin to support barrier hydration.",
    ],
    "fungal": [
        "Keep skin folds clean and thoroughly dry; wash affected garments separately and dry in direct sunlight.",
        "Traditional Neem (Azadirachta indica) or Haridra (Curcuma longa) wash may support hygiene on intact skin; avoid occlusive oils or steroid creams.",
    ],
    "psoriasis": [
        "Maintain regular skin hydration using bland emollients or traditional coconut/wrightia (777) oil preparations on intact plaques.",
        "Avoid harsh scrubbing of scales and manage stress/sleep triggers alongside clinician-guided care.",
    ],
    "contact dermatitis": [
        "Rinse the exposed area gently with cool water and identify/remove the suspected irritant or allergen.",
        "Apply soothing Aloe vera (Kumari) gel on intact skin; avoid applying unverified herbal pastes over blistered areas.",
    ],
    "acne": [
        "Wash gently twice daily with a mild cleanser; avoid squeezing or picking lesions to prevent secondary infection.",
        "Diluted Haridra (Curcuma longa) or Neem-based gentle wash may help surface hygiene on intact skin.",
    ],
    "nevus": [
        "Protect the pigmented spot from excessive UV exposure using shade, protective clothing, and broad-spectrum sunscreen.",
        "Do not apply caustic herbal pastes, home acids, or abrasive scrubs to moles or pigmented lesions.",
    ],
}

_DEFAULT_AYUSH_CARE = [
    "Maintain gentle skin hygiene with lukewarm water and mild, fragrance-free cleansing.",
    "Avoid self-applying unstandardized herbal pastes or over-the-counter steroid creams without professional advice.",
]


def evaluate_triage(
    symptoms: SymptomInput,
    top_predictions: list[ConditionPrediction],
) -> TriageResult:
    """Evaluate clinical urgency from symptom red flags and top model predictions."""
    high_flags: list[str] = []
    moderate_flags: list[str] = []

    if symptoms.bleeding:
        high_flags.append("Active bleeding reported")
    if symptoms.fever:
        high_flags.append("Systemic fever reported")
    if symptoms.rapid_spread:
        high_flags.append("Rapidly spreading lesion")

    if top_predictions:
        top_pred = top_predictions[0]
        if "Suspicious Lesion" in top_pred.condition_name and top_pred.confidence > 0.45:
            high_flags.append(
                f"Suspicious lesion pattern detected ({top_pred.confidence:.0%} confidence)"
            )

    if symptoms.pain:
        moderate_flags.append("Localized pain reported")
    if symptoms.duration_days > 14:
        moderate_flags.append(f"Persistent duration ({symptoms.duration_days} days)")
    elif symptoms.itching and symptoms.duration_days > 7:
        moderate_flags.append(f"Persistent itching ({symptoms.duration_days} days)")

    all_flags = high_flags + moderate_flags

    if high_flags:
        return TriageResult(
            urgency_level="high",
            urgency_reason=(
                "High-priority clinical review recommended due to red-flag findings: "
                + "; ".join(high_flags)
                + "."
            ),
            red_flags_triggered=all_flags,
        )

    if moderate_flags:
        return TriageResult(
            urgency_level="moderate",
            urgency_reason=(
                "Prompt outpatient evaluation advised due to: "
                + "; ".join(moderate_flags)
                + "."
            ),
            red_flags_triggered=all_flags,
        )

    return TriageResult(
        urgency_level="low",
        urgency_reason=(
            "No immediate red-flag symptoms reported. Monitor the lesion and "
            "schedule a routine checkup if it changes or fails to improve."
        ),
        red_flags_triggered=[],
    )


def _select_ayush_care(top_condition: str, urgency_level: str) -> list[str]:
    """Return condition-appropriate AYUSH supportive care with safety contraindications."""
    lower = top_condition.lower()
    if urgency_level == "high" or "suspicious" in lower:
        return [
            "Contraindication: Do NOT apply herbal pastes, oils, Neem/Haridra poultices, or Jatyadi formulations to open, bleeding, or suspicious lesions prior to clinical examination.",
            "Keep the area clean, dry, and loosely covered with a sterile dressing if oozing until evaluated by a doctor.",
        ]

    for key, steps in _AYUSH_CONDITION_GUIDANCE.items():
        if key in lower:
            return [
                *steps,
                "Contraindication: Discontinue any topical preparation immediately if stinging, oozing, or bleeding develops.",
            ]

    return _DEFAULT_AYUSH_CARE


def build_care_guidance(top_condition: str, urgency_level: str) -> CareGuidance:
    """Build preliminary general hygiene, AYUSH supportive care, and doctor referral guidance."""
    if urgency_level == "high":
        general_steps = [
            "Avoid scratching, squeezing, or applying unprescribed creams or home remedies to the lesion.",
            "Keep the area clean and gently protected; avoid friction from tight clothing.",
            "Monitor temperature and photograph the lesion if safe, to show changes to your clinician.",
        ]
        when_to_see_doctor = (
            "Seek urgent medical or dermatological evaluation within 24 hours "
            "(or immediately if fever worsens, bleeding continues, or swelling spreads rapidly)."
        )
    elif urgency_level == "moderate":
        general_steps = [
            "Keep the affected skin clean and dry; use mild, fragrance-free cleansers.",
            "Avoid scratching, harsh soaps, and known irritants or tight synthetic fabrics.",
            "Track any changes in size, border, color, or pain over the next few days.",
        ]
        when_to_see_doctor = (
            "Schedule an outpatient appointment with a dermatologist or AYUSH skin clinic "
            "within 3–7 days, or sooner if symptoms worsen."
        )
    else:
        general_steps = [
            "Maintain gentle daily hygiene and avoid scratching or picking at the skin.",
            "Avoid harsh detergents, fragranced lotions, and prolonged moisture in skin folds.",
            "Re-scan the area in 7 days to monitor whether the lesion is resolving.",
        ]
        when_to_see_doctor = (
            "Consult a doctor if the lesion persists beyond 2 weeks, begins to bleed, "
            "becomes painful, or spreads."
        )

    return CareGuidance(
        general_steps=general_steps,
        ayush_supportive_care=_select_ayush_care(top_condition, urgency_level),
        when_to_see_doctor=when_to_see_doctor,
        disclaimer=PRELIMINARY_DISCLAIMER,
    )
