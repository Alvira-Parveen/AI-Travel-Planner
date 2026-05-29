from fpdf import FPDF


def clean_text(text):

    if text is None:
        return ""

    text = str(text)

    replacements = {
        "₹": "Rs.",
        "→": "->",
        "✅": "",
        "✈️": "",
        "📍": "",
        "🏙️": "",
        "🧳": "",
        "📅": "",
        "💰": "",
        "🧠": "",
        "🌤️": "",
        "📄": "",
        "❤️": "",
        "⭐": "",
        "🌄": "",
        "🍽️": "",
        "🏨": "",
        "🚕": "",
        "🎒": "",
        "🎯": "",
        "•": "-",
        "—": "-",
        "–": "-"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Keep only latin-1 compatible chars
    text = text.encode("latin-1", "replace").decode("latin-1")

    return text


def create_pdf(travel_content):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", size=12)

    cleaned_content = clean_text(travel_content)

    lines = cleaned_content.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            pdf.ln(3)
            continue

        try:
            pdf.multi_cell(
                0,
                8,
                line
            )

        except Exception:
            continue

    pdf.output("AI_Travel_Plan.pdf")
