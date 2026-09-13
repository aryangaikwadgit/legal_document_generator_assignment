import re
import unicodedata
from html import escape

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


class PDFBuilder:

    def __init__(self):
        self.page_width, self.page_height = A4
        self.left_margin = 1 * inch
        self.right_margin = 1 * inch
        self.usable_width = (
            self.page_width
            - self.left_margin
            - self.right_margin
        )

        self.normal_style = ParagraphStyle(
            "Normal",
            fontName="Times-Roman",
            fontSize=12,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=4,
        )

        self.center_style = ParagraphStyle(
            "Center",
            parent=self.normal_style,
            alignment=TA_CENTER,
        )

        self.justify_style = ParagraphStyle(
            "Justify",
            parent=self.normal_style,
            alignment=TA_JUSTIFY,
        )

        self.jurat_style = ParagraphStyle(
            "Jurat",
            parent=self.normal_style,
            alignment=TA_LEFT,
            spaceAfter=2,
        )

        self.bold_center_style = ParagraphStyle(
            "BoldCenter",
            parent=self.center_style,
            fontName="Times-Bold",
        )

        self.bold_right_style = ParagraphStyle(
            "BoldRight",
            parent=self.normal_style,
            fontName="Times-Bold",
            alignment=TA_RIGHT,
        )

    def sanitize(self, text):
        replacements = {
            "\u25cf": "",
            "\u2022": "",
            "\u2011": "-",
            "\u2013": "-",
            "\u2014": "-",
            "\u2018": "'",
            "\u2019": "'",
            "\u201c": '"',
            "\u201d": '"',
        }

        for bad, good in replacements.items():
            text = text.replace(bad, good)

        return unicodedata.normalize("NFKC", text).strip()

    def text(self, value):
        return escape(
            self.sanitize(value)
        ).replace("\n", "<br/>")

    def party_table(self, text):
        rows = []
        versus_rows = []

        left_width = self.usable_width * 0.74
        right_width = self.usable_width - left_width

        for line in text.splitlines():
            line = self.sanitize(line)

            if not line:
                continue

            if line.upper() == "VERSUS":
                versus_rows.append(len(rows))
                rows.append([
                    Paragraph(
                        "<b>VERSUS</b>",
                        self.bold_center_style,
                    ),
                    "",
                ])
                continue

            match = re.match(
                r"^(.*?)(\s+\.\.\.\s*.+)$",
                line,
            )

            if match:
                left_text = match.group(1).strip()
                right_text = match.group(2).strip()
            else:
                left_text = line
                right_text = ""

            rows.append([
                Paragraph(
                    self.text(left_text),
                    self.normal_style,
                ),
                Paragraph(
                    self.text(right_text),
                    ParagraphStyle(
                        "PartyRight",
                        parent=self.normal_style,
                        alignment=TA_RIGHT,
                    ),
                ),
            ])

        table = Table(
            rows,
            colWidths=[left_width, right_width],
        )

        style = [
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]

        for row in versus_rows:
            style.extend([
                ("SPAN", (0, row), (1, row)),
                ("ALIGN", (0, row), (1, row), "CENTER"),
                ("TOPPADDING", (0, row), (1, row), 6),
                ("BOTTOMPADDING", (0, row), (1, row), 6),
            ])

        table.setStyle(TableStyle(style))

        return table

    def attestation_table(self):
        table = Table(
            [
                [
                    Paragraph(
                        "Before Me",
                        self.normal_style,
                    ),
                    Paragraph(
                        "<b>DEPONENT</b>",
                        self.bold_right_style,
                    ),
                ]
            ],
            colWidths=[
                self.usable_width * 0.5,
                self.usable_width * 0.5,
            ],
        )

        table.setStyle(
            TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ])
        )

        return table

    def add_section(self, story, section):

        if section.type == "heading":
            for line in section.content.splitlines():
                if line.strip():
                    story.append(
                        Paragraph(
                            self.text(line),
                            self.bold_center_style,
                        )
                    )
                    story.append(Spacer(1, 2))

        elif section.type == "cause_title":
            story.append(self.party_table(section.content))
            story.append(Spacer(1, 6))

        elif section.type == "affidavit_title":
            story.append(
                Paragraph(
                    self.text(section.content),
                    self.bold_center_style,
                )
            )
            story.append(Spacer(1, 8))

        elif section.type == "deponent":
            story.append(
                Paragraph(
                    self.text(section.content),
                    self.normal_style,
                )
            )
            story.append(Spacer(1, 5))

        elif section.type == "numbered_paragraph":
            story.append(
                Paragraph(
                    f"<b>{section.number}.</b> "
                    f"{self.text(section.content)}",
                    self.justify_style,
                )
            )
            story.append(Spacer(1, 4))

        elif section.type == "prayer_heading":
            story.append(PageBreak())
            story.append(Spacer(1, 10))
            story.append(
                Paragraph(
                    self.text(section.content),
                    self.bold_center_style,
                )
            )
            story.append(Spacer(1, 5))

        elif section.type == "prayer_intro":
            story.append(
                Paragraph(
                    self.text(section.content),
                    self.normal_style,
                )
            )
            story.append(Spacer(1, 4))

        elif section.type == "prayer_item":
            label = section.label or "a"
            content = self.sanitize(section.content)

            if content.startswith(f"({label})"):
                content = content[len(label) + 2:].strip()

            story.append(
                Paragraph(
                    f"<b>({label})</b> {self.text(content)}",
                    self.normal_style,
                )
            )
            story.append(Spacer(1, 3))

        elif section.type == "jurat":
            lines = [
                self.sanitize(line)
                for line in section.content.splitlines()
                if line.strip()
                and line.strip().upper()
                not in ["DEPONENT", "BEFORE ME"]
            ]

            for line in lines:
                story.append(
                    Paragraph(
                        self.text(line),
                        self.jurat_style,
                    )
                )
                story.append(Spacer(1, 3))

            story.append(self.attestation_table())
            story.append(Spacer(1, 8))

        elif section.type == "verification":
            lines = [
                self.sanitize(line)
                for line in section.content.splitlines()
                if line.strip()
                and line.strip().upper()
                not in ["VERIFICATION", "DEPONENT"]
            ]

            story.append(
                Paragraph(
                    "VERIFICATION",
                    self.bold_center_style,
                )
            )
            story.append(Spacer(1, 5))

            for line in lines:
                story.append(
                    Paragraph(
                        self.text(line),
                        self.normal_style,
                    )
                )
                story.append(Spacer(1, 3))

            story.append(
                Paragraph(
                    "<b>DEPONENT</b>",
                    self.bold_right_style,
                )
            )
            story.append(Spacer(1, 6))

        elif section.type == "advocate":
            for line in section.content.splitlines():
                if line.strip():
                    story.append(
                        Paragraph(
                            self.text(line),
                            self.normal_style,
                        )
                    )

    def build(self, generated_document, output_path):
        document = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=self.left_margin,
            rightMargin=self.right_margin,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )   

        story = []

        for section in generated_document.sections:
            self.add_section(story, section)

        document.build(story)