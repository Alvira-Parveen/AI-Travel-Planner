from fpdf import FPDF


def clean_text(text):

    if text is None:
        return ""

    # ensure we are working with a string
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
        "📄": ""
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove any remaining characters that cannot be encoded in latin-1
    filtered = ''.join(ch for ch in text if ord(ch) < 256)

    return filtered


def create_pdf(travel_content):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", size=12)

    # Clean unsupported characters
    cleaned_content = clean_text(travel_content)

    lines = cleaned_content.split("\n")

    for line in lines:

        pdf.multi_cell(0, 10, line)

    pdf.output("AI_Travel_Plan.pdf")