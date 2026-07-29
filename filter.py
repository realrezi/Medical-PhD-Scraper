import re


def matches_medical_phd(title, description=""):
    """
    Validates if a position is for a PhD related to medicine, medical sciences, 
    or related clinical/biomedical fields.
    """
    text_corpus = f"{title} {description}".lower()

    # Patterns to identify PhD or Doctorate degrees
    phd_terms = [
        r"\b(phd|doctorate|ph\.d\.)\b"
    ]

    # Patterns to identify medical, biomedical, or health-related fields
    medical_terms = [
        r"\b(medicine|medical|biomedical|health|clinical|pharmaceutical|therapeutic|oncology|cardiology|neuroscience|genetics|immunology|pathology|radiology|anesthesiology|surgery|internal\s+medicine|pediatrics|psychiatry|public\s+health)\b",
        r"medicine\s+sciences?",
        r"medical\s+research",
        r"biomedical\s+research",
        r"clinical\s+research",
        r"health\s+sciences",
        r"life\s+sciences",  # Often includes medical research
        r"molecular\s+medicine",
        r"experimental\s+medicine",
        r"translational\s+medicine",
    ]

    has_phd_term = False
    for pattern in phd_terms:
        if re.search(pattern, text_corpus):
            has_phd_term = True
            break

    has_medical_term = False
    for pattern in medical_terms:
        if re.search(pattern, text_corpus):
            has_medical_term = True
            break

    # A match is found if both a PhD term and a medical term are present
    return has_phd_term and has_medical_term
