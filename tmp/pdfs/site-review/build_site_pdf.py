from io import BytesIO
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path("/Users/erikaduraku/Documents/ILGMUN")
SCREENSHOTS = ROOT / "tmp/pdfs/site-review/screenshots"
OUTPUT = ROOT / "output/pdf/ILG-MUN-IV-Website-Review.pdf"

SECTIONS = [
    ("Home", "home.png"),
    ("About ILG MUN", "about.png"),
    ("Committees", "committees.png"),
    ("UNHRC", "unhrc.png"),
    ("ECOSOC", "ecosoc.png"),
    ("UNODC", "unodc.png"),
    ("United Nations Security Council", "security-council.png"),
    ("Resources", "resources.png"),
    ("ILG Team", "team.png"),
    ("Contact", "contact.png"),
]

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 24
HEADER_H = 40
IMAGE_W = PAGE_W - 2 * MARGIN


def draw_title_page(pdf: canvas.Canvas) -> None:
    pdf.setFillColor(HexColor("#10283F"))
    pdf.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#0F8F87"))
    pdf.circle(PAGE_W - 92, PAGE_H - 78, 92, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#673451"))
    pdf.circle(68, 62, 58, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setFont("Helvetica-Bold", 34)
    pdf.drawString(62, PAGE_H - 156, "ILG MUN IV")
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(62, PAGE_H - 190, "Complete Website Visual Review")
    pdf.setFillColor(HexColor("#F5EEDD"))
    pdf.setFont("Helvetica", 12)
    pdf.drawString(62, PAGE_H - 222, "Desktop captures of every public website section")
    pdf.drawString(62, PAGE_H - 242, "Prepared for design feedback - 2 August 2026")
    pdf.showPage()


def draw_section(pdf: canvas.Canvas, title: str, image_path: Path) -> None:
    with Image.open(image_path) as source:
        image = source.convert("RGB")
        width, height = image.size
        rendered_height = IMAGE_W * height / width
        section_height = rendered_height + HEADER_H + 2 * MARGIN
        pdf.setPageSize((PAGE_W, section_height))

        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=92, optimize=True)
        buffer.seek(0)

        pdf.setFillColor(HexColor("#F7F3EB"))
        pdf.rect(0, 0, PAGE_W, section_height, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#10283F"))
        pdf.rect(0, section_height - HEADER_H - MARGIN / 2, PAGE_W, HEADER_H + MARGIN / 2, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(MARGIN, section_height - 29, title)
        pdf.drawImage(ImageReader(buffer), MARGIN, MARGIN, width=IMAGE_W, height=rendered_height, preserveAspectRatio=True)
        pdf.showPage()


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=landscape(A4), pageCompression=1)
    pdf.setTitle("ILG MUN IV - Complete Website Visual Review")
    pdf.setAuthor("ILG Model United Nations")
    draw_title_page(pdf)
    for title, filename in SECTIONS:
        draw_section(pdf, title, SCREENSHOTS / filename)
    pdf.save()


if __name__ == "__main__":
    main()
