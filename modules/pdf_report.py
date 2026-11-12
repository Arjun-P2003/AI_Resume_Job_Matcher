
from io import BytesIO
from xml.sax.saxutils import escape
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)

from modules.improvement_suggestions import generate_suggestions


# ==================================================
# COLOUR THEME
# ==================================================

NAVY = HexColor("#17365D")
BLUE = HexColor("#2563EB")
LIGHT_BLUE = HexColor("#EFF6FF")
GREEN = HexColor("#166534")
LIGHT_GREEN = HexColor("#DCFCE7")
ORANGE = HexColor("#92400E")
LIGHT_ORANGE = HexColor("#FEF3C7")
GREY = HexColor("#64748B")
LIGHT_GREY = HexColor("#F4F7FB")
DARK = HexColor("#1E293B")


def generate_pdf_report(
    resume_filename,
    job_description,
    similarity_score,
    results
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=42,
        leftMargin=42,
        topMargin=65,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    # ==================================================
    # TEXT STYLES
    # ==================================================

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=26,
        textColor=colors.white,
        alignment=TA_LEFT,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=9,
        textColor=HexColor("#DBEAFE"),
        leading=13
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=NAVY,
        spaceBefore=13,
        spaceAfter=7
    )

    normal_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=14,
        textColor=DARK,
        spaceAfter=4
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=normal_style,
        fontSize=8,
        leading=11,
        textColor=GREY
    )

    badge_style = ParagraphStyle(
        "BadgeText",
        parent=normal_style,
        fontSize=8,
        leading=11,
        alignment=TA_CENTER
    )

    suggestion_title_style = ParagraphStyle(
        "SuggestionTitle",
        parent=normal_style,
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=NAVY,
        spaceAfter=4
    )

    suggestion_body_style = ParagraphStyle(
        "SuggestionBody",
        parent=normal_style,
        leftIndent=8,
        fontSize=8.5,
        leading=13
    )

    story = []

    # ==================================================
    # HEADER
    # ==================================================

    header_content = [
        [
            Paragraph(
                "AI Resume &amp; Job Match Report",
                title_style
            )
        ],
        [
            Paragraph(
                "Professional Resume Analysis &amp; Job Compatibility Report",
                subtitle_style
            )
        ]
    ]

    header_table = Table(
        header_content,
        colWidths=[7.05 * inch]
    )

    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 18),
        ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ("TOPPADDING", (0, 0), (-1, 0), 18),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ("TOPPADDING", (0, 1), (-1, 1), 3),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 16)
    ]))

    story.append(header_table)
    story.append(Spacer(1, 15))

    # ==================================================
    # REPORT DATE AND FILE
    # ==================================================

    details_data = [
        [
            Paragraph(
                f"<b>Resume:</b> {escape(str(resume_filename))}",
                normal_style
            ),
            Paragraph(
                f"<b>Report Date:</b> "
                f"{datetime.now().strftime('%d %b %Y')}",
                normal_style
            )
        ]
    ]

    details_table = Table(
        details_data,
        colWidths=[4.2 * inch, 2.85 * inch]
    )

    details_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#D5DEEA")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10)
    ]))

    story.append(details_table)

    # ==================================================
    # MATCHING SCORE CARDS
    # ==================================================

    story.append(
        Paragraph("Matching Overview", heading_style)
    )

    score_cards = [
        [
            Paragraph(
                f'<font color="#2563EB"><b>{similarity_score}%</b></font><br/>'
                '<font size="8">AI Text Similarity</font>',
                badge_style
            ),
            Paragraph(
                f'<font color="#166534"><b>{results["match_percentage"]}%</b></font><br/>'
                '<font size="8">Skill Match</font>',
                badge_style
            ),
            Paragraph(
                f'<font color="#166534"><b>{len(results["matched_skills"])}</b></font><br/>'
                '<font size="8">Matched Skills</font>',
                badge_style
            ),
            Paragraph(
                f'<font color="#92400E"><b>{len(results["missing_skills"])}</b></font><br/>'
                '<font size="8">Missing Skills</font>',
                badge_style
            )
        ]
    ]

    score_table = Table(
        score_cards,
        colWidths=[1.76 * inch] * 4
    )

    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), LIGHT_BLUE),
        ("BACKGROUND", (1, 0), (1, 0), LIGHT_GREEN),
        ("BACKGROUND", (2, 0), (2, 0), LIGHT_GREEN),
        ("BACKGROUND", (3, 0), (3, 0), LIGHT_ORANGE),
        ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#D5DEEA")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 13),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 13)
    ]))

    story.append(score_table)

    # ==================================================
    # SKILL SECTIONS
    # ==================================================

    def add_skill_section(title, skills, background, text_color):

        story.append(
            Paragraph(title, heading_style)
        )

        if not skills:
            story.append(
                Paragraph("None detected.", normal_style)
            )
            return

        badge_cells = []

        for skill in skills:

            safe_skill = escape(str(skill))

            badge_cells.append(
                Paragraph(
                    f'<font color="{text_color.hexval()}">'
                    f'<b>{safe_skill}</b></font>',
                    badge_style
                )
            )

        rows = []

        for index in range(0, len(badge_cells), 3):

            row = badge_cells[index:index + 3]

            while len(row) < 3:
                row.append("")

            rows.append(row)

        badge_table = Table(
            rows,
            colWidths=[2.35 * inch] * 3
        )

        badge_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), background),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.white),
            ("INNERGRID", (0, 0), (-1, -1), 3, colors.white),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
        ]))

        story.append(badge_table)

    add_skill_section(
        "Matched Skills",
        results["matched_skills"],
        LIGHT_GREEN,
        GREEN
    )

    add_skill_section(
        "Missing Skills",
        results["missing_skills"],
        LIGHT_ORANGE,
        ORANGE
    )

    add_skill_section(
        "Additional Resume Skills",
        results["extra_skills"],
        LIGHT_BLUE,
        BLUE
    )

    # ==================================================
    # IMPROVEMENT SUGGESTIONS
    # ==================================================

    suggestions = generate_suggestions(results)

    if suggestions:

        first_suggestion = suggestions[0]

        # Keep the heading and first suggestion together
        first_suggestion_content = [
            Paragraph(
                "AI Resume Improvement Suggestions",
                heading_style
            ),
            Spacer(1, 3),
            Paragraph(
                f"1. {escape(first_suggestion['title'])}",
                suggestion_title_style
            ),
            Paragraph(
                escape(first_suggestion["description"]),
                suggestion_body_style
            )
        ]

        for action in first_suggestion["actions"]:

            first_suggestion_content.append(
                Paragraph(
                    f"&bull; {escape(action)}",
                    suggestion_body_style
                )
            )

        first_suggestion_table = Table(
            [[first_suggestion_content]],
            colWidths=[7.05 * inch]
        )

        first_suggestion_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
            ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#D5DEEA")),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9)
        ]))

        story.append(first_suggestion_table)
        story.append(Spacer(1, 8))

        # Remaining suggestion cards
        for index, suggestion in enumerate(suggestions[1:], start=2):

            suggestion_content = []

            suggestion_content.append(
                Paragraph(
                    f"{index}. {escape(suggestion['title'])}",
                    suggestion_title_style
                )
            )

            suggestion_content.append(
                Paragraph(
                    escape(suggestion["description"]),
                    suggestion_body_style
                )
            )

            for action in suggestion["actions"]:

                suggestion_content.append(
                    Paragraph(
                        f"&bull; {escape(action)}",
                        suggestion_body_style
                    )
                )

            suggestion_table = Table(
                [[suggestion_content]],
                colWidths=[7.05 * inch]
            )

            suggestion_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
                ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#D5DEEA")),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9)
            ]))

            story.append(
                KeepTogether([
                    suggestion_table,
                    Spacer(1, 8)
                ])
            )

    # ==================================================
    # JOB DESCRIPTION
    # ==================================================

    story.append(
        Paragraph("Job Description", heading_style)
    )

    safe_description = escape(
        job_description
    ).replace("\n", "<br/>")

    story.append(
        Paragraph(
            safe_description,
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # ==================================================
    # DISCLAIMER
    # ==================================================

    story.append(
        HRFlowable(
            width="100%",
            color=HexColor("#D5DEEA")
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "<b>Important Note:</b> AI Text Similarity measures "
            "document similarity. Skill Match measures recognized "
            "job skill coverage. Neither score represents hiring "
            "probability. Improvement suggestions are "
            "rule-based recommendations.",
            small_style
        )
    )

    # ==================================================
    # PAGE FOOTER
    # ==================================================

    def add_page_footer(canvas, doc):

        canvas.saveState()

        page_width, page_height = A4

        canvas.setStrokeColor(HexColor("#D5DEEA"))
        canvas.setLineWidth(0.5)

        canvas.line(
            42,
            38,
            page_width - 42,
            38
        )

        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GREY)

        canvas.drawString(
            42,
            25,
            "AI Resume & Job Matcher"
        )

        canvas.drawRightString(
            page_width - 42,
            25,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    # ==================================================
    # BUILD PDF
    # ==================================================

    document.build(
        story,
        onFirstPage=add_page_footer,
        onLaterPages=add_page_footer
    )

    buffer.seek(0)

    return buffer.getvalue()
