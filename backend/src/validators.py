import re
import unicodedata

from docx import Document


class AffidavitValidator:

    def __init__(self, document_path):
        self.document_path = document_path

    def normalize(self, text):
        text = unicodedata.normalize("NFKC", text)
        return (
            text.replace("‘", "'")
            .replace("’", "'")
            .replace("“", '"')
            .replace("”", '"')
            .replace("–", "-")
            .replace("—", "-")
            .replace("\xa0", " ")
        )

    def extract_blocks(self):
        document = Document(self.document_path)
        blocks = []

        for element in document.element.body.iterchildren():
            tag = element.tag.split("}")[-1]

            if tag == "p":
                text = "".join(
                    node.text or ""
                    for node in element.iter()
                    if node.tag.endswith("}t")
                ).strip()

                if text:
                    blocks.append(text)

            elif tag == "tbl":
                for row in element.iterchildren():
                    cells = []

                    for cell in row.iterchildren():
                        if cell.tag.endswith("}tc"):
                            text = "".join(
                                node.text or ""
                                for node in cell.iter()
                                if node.tag.endswith("}t")
                            ).strip()

                            if text:
                                cells.append(text)

                    if cells:
                        blocks.append(" ".join(cells))

        return blocks

    def text(self, blocks):
        return self.normalize("\n".join(blocks))

    def check_required_sections(self, blocks, case_information):
        text = self.text(blocks)

        required = [
            case_information.forum,
            case_information.jurisdiction_type,
            f"{case_information.case_type} NO. {case_information.case_number} OF {case_information.year}",
            f"AFFIDAVIT IN REPLY ON BEHALF OF RESPONDENT NO. {case_information.answering_respondent_number}",
            "PRAYER",
            "VERIFICATION",
            "BEFORE ME",
            case_information.advocate_firm,
        ]

        return {
            "check": "required_sections",
            "passed": all(
                self.normalize(item).lower() in text.lower() for item in required
            ),
        }

    def check_entities(self, blocks, case_information):
        text = self.text(blocks)

        entities = [
            case_information.petitioner,
            case_information.deponent.name,
            case_information.deponent.designation,
            case_information.deponent.address,
            case_information.case_number,
            str(case_information.year),
            case_information.place,
            case_information.advocate_firm,
        ]

        entities += [respondent.name for respondent in case_information.respondents]

        return {
            "check": "entity_accuracy",
            "passed": all(
                self.normalize(item).lower() in text.lower() for item in entities
            ),
        }

    def check_paragraphs(self, blocks, case_information):
        prayer_index = next(
            (i for i, block in enumerate(blocks) if block.strip().upper() == "PRAYER"),
            len(blocks),
        )

        numbers = []

        for block in blocks[:prayer_index]:
            match = re.match(r"^(\d+)\.\s+", block)

            if match:
                number = int(match.group(1))

                if number == len(numbers) + 1:
                    numbers.append(number)

        expected = list(range(1, len(case_information.reply_points) + 2))

        return {
            "check": "paragraph_numbering",
            "passed": numbers == expected,
            "expected": expected,
            "found": numbers,
        }

    def check_verification(self, blocks, case_information):
        text = self.text(blocks)
        expected = len(case_information.reply_points) + 1

        match = re.search(
            r"paragraphs\s+1\s+to\s+(\d+)",
            text,
            re.IGNORECASE,
        )

        found = int(match.group(1)) if match else None

        return {
            "check": "verification_range",
            "passed": found == expected,
            "expected": expected,
            "found": found,
        }

    def check_exhibits(self, blocks, case_information):
        text = self.text(blocks)
        results = []

        for exhibit in case_information.exhibits:
            label = re.search(r"[A-Z]", exhibit.label.upper())

            if not label:
                continue

            letter = label.group(0)

            found = (
                re.search(
                    rf"EXHIBIT\s*-\s*['\"]?{letter}['\"]?",
                    text,
                    re.IGNORECASE,
                )
                is not None
            )

            results.append(found)

        return {
            "check": "exhibit_references",
            "passed": all(results) if results else True,
        }

    def check_prayer(self, blocks):
        text = self.text(blocks)

        return {
            "check": "prayer_format",
            "passed": bool(
                re.search(
                    r"\([a-z]\)\s+",
                    text,
                    re.IGNORECASE,
                )
            ),
        }

    def check_order(self, blocks, case_information):
        text = self.text(blocks)

        sections = [
            case_information.forum,
            case_information.jurisdiction_type,
            f"{case_information.case_type} NO. {case_information.case_number} OF {case_information.year}",
            "VERSUS",
            "AFFIDAVIT IN REPLY",
            "PRAYER",
            "BEFORE ME",
            "VERIFICATION",
            case_information.advocate_firm,
        ]

        positions = []

        for section in sections:
            position = text.lower().find(self.normalize(section).lower())
            positions.append(position)

        return {
            "check": "section_order",
            "passed": (
                all(position >= 0 for position in positions)
                and positions == sorted(positions)
            ),
        }

    def check_consistency(self, blocks, case_information):
        text = self.text(blocks)

        respondent = (
            f"RESPONDENT NO. " f"{case_information.answering_respondent_number}"
        )

        return {
            "check": "consistency",
            "passed": (
                respondent.lower() in text.lower()
                and case_information.deponent.name.lower() in text.lower()
                and case_information.place.lower() in text.lower()
                and self.check_verification(
                    blocks,
                    case_information,
                )["passed"]
            ),
        }

    def check_hallucination(self, blocks, case_information):
        text = self.text(blocks)

        unsupported = [
            r"age\s+\d+",
            r"occupation\s*:",
            r"registered\s+office",
            r"having\s+its\s+office",
        ]

        found = [
            pattern
            for pattern in unsupported
            if re.search(pattern, text, re.IGNORECASE)
        ]

        return {
            "check": "hallucination",
            "passed": not found,
            "found": found,
        }

    def validate(self, case_information):
        blocks = self.extract_blocks()

        results = [
            self.check_required_sections(
                blocks,
                case_information,
            ),
            self.check_entities(
                blocks,
                case_information,
            ),
            self.check_paragraphs(
                blocks,
                case_information,
            ),
            self.check_verification(
                blocks,
                case_information,
            ),
            self.check_exhibits(
                blocks,
                case_information,
            ),
            self.check_prayer(blocks),
            self.check_order(
                blocks,
                case_information,
            ),
            self.check_consistency(
                blocks,
                case_information,
            ),
            self.check_hallucination(
                blocks,
                case_information,
            ),
        ]

        passed = sum(result["passed"] for result in results)

        total = len(results)

        return {
            "checks": results,
            "passed_checks": passed,
            "total_checks": total,
            "validation_score": (round(passed / total, 4) if total else 0),
        }
