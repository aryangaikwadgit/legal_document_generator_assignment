EXTRACTION_PROMPT = """
You are an information extraction system for legal documents.

Extract the case information required by the provided schema.

Rules:
1. Extract only information explicitly present in the document.
2. Do not invent, assume, or infer facts.
3. Preserve names, dates, numbers, legal terms, and factual meaning.
4. Preserve respondent numbers and names exactly.
5. Extract the actual material associated with each exhibit.
6. Do not use instructions such as "to be annexed" as exhibit descriptions.
7. Treat each parent-level reply point as one reply_points item.
8. Combine bullets belonging to the same reply point.
9. Preserve the original order and substantive information.
10. Do not include information from unrelated content.
11. Return only the structured output.

{format_instructions}

DOCUMENT:

{document_text}
"""


TEMPLATE_ANALYSIS_PROMPT = """
You are a legal document template analysis system.

Analyze the supplied reference documents and identify the reusable
structure and presentation rules for an Affidavit in Reply.

Use the format document for:
- required sections
- fixed conventions
- numbering rules
- document requirements

Use the sample document for:
- section order
- alignment
- spacing
- headings
- party presentation
- numbering
- prayer
- jurat
- verification
- advocate block

Do not copy case-specific facts from the sample.

For each section provide:
- name
- order
- placeholder
- instruction
- numbering where applicable
- alignment where applicable
- formatting where applicable

Identify the complete structure from beginning to end.

Return only the structured output.

FORMAT DOCUMENT:

{format_document}

SAMPLE DOCUMENT:

{sample_document}

{format_instructions}
"""


GENERATION_PROMPT = """
You are a legal document drafting system.

Generate an Affidavit in Reply using only:

1. STRUCTURED CASE INFORMATION — what the document should say
2. LEARNED DOCUMENT STRUCTURE — how it should be presented

Rules:
1. Use case-specific information only from STRUCTURED CASE INFORMATION.
2. Follow the learned structure and section order.
3. Do not copy case-specific facts from the sample.
4. Do not invent facts, reliefs, parties, dates, or exhibits.
5. Keep the document concise and close to the supplied case information.
6. Return only the structured output.

Use these section types:

- heading
- cause_title
- affidavit_title
- deponent
- numbered_paragraph
- prayer_heading
- prayer_intro
- prayer_item
- jurat
- verification
- advocate

CONTENT:

Use the case information to fill the learned template.

Do not treat example text in the learned structure as additional case content.
Use example wording only as a style and drafting guide.

HEADING:

Use the supplied forum, jurisdiction, case type, case number and year.

Return all of these as ONE "heading" section.

Do not create separate sections with type "jurisdiction" or "case_number".

Do not duplicate words already present in a supplied value.

CAUSE TITLE:

Use the supplied petitioner and all supplied respondents in their original
numbering.

Place VERSUS where required by the learned structure.

Use actual supplied party names. Do not copy parties from the sample.

AFFIDAVIT TITLE:

Use the supplied answering respondent number.

DEPONENT:

Use the supplied deponent name, designation, address and respondent number.

Follow the learned structure, but do not add missing personal details.

BODY:

Create exactly one numbered paragraph for each supplied reply point.

Use the reply point as the substantive content and rewrite it only as
needed to match the style of the learned template.

Do not append the template's example paragraphs to the reply points.

After all reply points, add the closing paragraph required by the learned
structure.

Therefore:

number of body paragraphs =
number of reply points + required closing paragraph.

Keep the body focused on the supplied reply points.

Do not add new allegations, facts, arguments, or explanations.

PRAYER:

Create:
1. one prayer_heading
2. one prayer_intro when required by the learned structure
3. exactly one prayer_item for each supplied prayer point

Do not invent additional prayer points.

Use the lettering convention learned from the template.

JURAT:

Use the supplied place and date.

Follow the learned jurat wording and structure.

Keep Before Me and DEPONENT in their appropriate positions.

VERIFICATION:

Use the supplied deponent, place, date and verification information.

The paragraph range must match the actual number of generated numbered
body paragraphs.

Do not copy the sample's paragraph range.

ADVOCATE:

Use the supplied advocate firm and answering respondent.

Follow the learned advocate structure.

FORMATTING:

Follow the formatting rules learned from the reference documents.

Do not add formatting that is not supported by the learned structure.

MISSING INFORMATION:

If a required case-specific value is not supplied, use:

[NOT PROVIDED]

Do not guess.

FINAL RULE:

The case information determines WHAT is written.

The learned document structure determines HOW it is written.

Do not mix these two responsibilities.

LEARNED DOCUMENT STRUCTURE:

{document_structure}

STRUCTURED CASE INFORMATION:

{mapped_content}

{format_instructions}
"""
