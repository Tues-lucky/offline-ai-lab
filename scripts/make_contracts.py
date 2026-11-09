"""Generate fictitious Hong Kong-style test contracts plus an answer key."""
import sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, KeepTogether)

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
ss = getSampleStyleSheet()
TITLE = ParagraphStyle("t", parent=ss["Title"], fontSize=16, spaceAfter=4)
SUB = ParagraphStyle("s", parent=ss["Normal"], alignment=TA_CENTER, fontSize=9.5,
                     textColor=colors.HexColor("#555555"), spaceAfter=14)
H = ParagraphStyle("h", parent=ss["Heading3"], fontSize=11, spaceBefore=10, spaceAfter=4)
P = ParagraphStyle("p", parent=ss["Normal"], fontSize=10, leading=14, alignment=TA_JUSTIFY,
                   spaceAfter=5)
PI = ParagraphStyle("pi", parent=P, leftIndent=8 * mm, firstLineIndent=-8 * mm)
CELL = ParagraphStyle("c", parent=ss["Normal"], fontSize=8.8, leading=11.5)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold")
FOOT = "FICTITIOUS SAMPLE DOCUMENT - FOR AI TESTING ONLY - NOT LEGAL ADVICE"


def footer(c, doc):
    c.saveState()
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawString(20 * mm, 12 * mm, FOOT)
    c.drawRightString(190 * mm, 12 * mm, f"Page {doc.page}")
    c.restoreState()


def build(fname, title, subtitle, parties, recitals, clauses, schedules, signatories):
    doc = SimpleDocTemplate(f"{OUT}/{fname}", pagesize=A4, leftMargin=20 * mm,
                            rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=22 * mm,
                            title=title, author="Fictitious sample")
    s = [Paragraph(title, TITLE), Paragraph(subtitle, SUB)]
    s.append(Paragraph("<b>THIS AGREEMENT</b> is made on the date stated above BETWEEN:", P))
    for i, p in enumerate(parties, 1):
        s.append(Paragraph(f"({i})&nbsp;&nbsp;{p}", PI))
    if recitals:
        s.append(Paragraph("<b>WHEREAS:</b>", P))
        for i, r in enumerate(recitals):
            s.append(Paragraph(f"({chr(65 + i)})&nbsp;&nbsp;{r}", PI))
    s.append(Paragraph("<b>IT IS AGREED</b> as follows:", P))
    for n, (head, subs) in enumerate(clauses, 1):
        s.append(Paragraph(f"{n}.&nbsp;&nbsp;{head.upper()}", H))
        for m, text in enumerate(subs, 1):
            label = f"{n}.{m}" if len(subs) > 1 else f"{n}.1"
            s.append(Paragraph(f"{label}&nbsp;&nbsp;{text}", PI))
    s.append(Spacer(1, 10))
    s.append(Paragraph("<b>IN WITNESS WHEREOF</b> the parties have executed this Agreement "
                       "on the date first written above.", P))
    rows = [[Paragraph(f"<b>SIGNED</b> by {a}<br/>for and on behalf of<br/>{b}<br/><br/>"
                       "______________________________", CELL) for a, b in signatories]]
    t = Table(rows, colWidths=[85 * mm] * len(signatories))
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s += [Spacer(1, 6), t]
    for stitle, items in schedules:
        s.append(PageBreak())
        s.append(Paragraph(stitle, ParagraphStyle("st", parent=H, fontSize=12,
                                                  alignment=TA_CENTER, spaceAfter=10)))
        if os.environ.get("FLAT"):
            short = stitle.split(" - ")[0].title()
            for k, v in items:
                s.append(Paragraph(f"{short} | <b>{k}</b>: {v}", P))
            continue
        data = [[Paragraph(f"<b>{k}</b>", CELL), Paragraph(v, CELL)] for k, v in items]
        tb = Table(data, colWidths=[55 * mm, 115 * mm])
        tb.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F2F2F2")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        s.append(tb)
    doc.build(s, onFirstPage=footer, onLaterPages=footer)


LUMEN = ("<b>LUMEN ANALYTICS (HK) LIMITED</b>, a company incorporated in Hong Kong whose "
         "registered office is at Room 1801, 18th Floor, Kestrel Centre, 28 Mariner Street, "
         "Quarry Bay, Hong Kong")

# ---------------------------------------------------------------- 1. LEASE
build(
    "01_Office_Tenancy_Agreement_Kestrel_Centre.pdf",
    "TENANCY AGREEMENT (OFFICE PREMISES)",
    "Dated 1 November 2026 &nbsp;|&nbsp; Room 1801, Kestrel Centre, Quarry Bay",
    ["<b>HARBOURVIEW PROPERTIES LIMITED</b>, a company incorporated in Hong Kong whose "
     "registered office is at 30th Floor, Harbourview Tower, 1 Pier Road, Central, Hong Kong "
     "(the <b>\"Landlord\"</b>); and",
     LUMEN.replace("Room 1801, 18th Floor, Kestrel Centre, 28 Mariner Street, Quarry Bay",
                   "Unit 502, 5th Floor, Tidewater Building, 9 Lantern Street, Sheung Wan")
     + " (the <b>\"Tenant\"</b>)."],
    ["The Landlord is the registered owner of the Premises.",
     "The Landlord has agreed to let and the Tenant has agreed to take the Premises on the "
     "terms of this Agreement."],
    [
        ("Definitions and Interpretation", [
            "<b>\"Building\"</b> means Kestrel Centre, 28 Mariner Street, Quarry Bay, Hong Kong.",
            "<b>\"Premises\"</b> means Room 1801 on the 18th Floor of the Building, as more "
            "particularly described in Schedule 1.",
            "<b>\"Term\"</b> means the term of years set out in Clause 2.1.",
            "<b>\"Handover Date\"</b> means 15 December 2026.",
            "<b>\"Rent\"</b>, <b>\"Management Fee\"</b> and <b>\"Deposit\"</b> mean the amounts "
            "set out in Schedule 2.",
            "Clause headings are for convenience only and shall not affect interpretation. "
            "Words importing the singular include the plural and vice versa.",
        ]),
        ("Term and Handover", [
            "The Landlord lets and the Tenant takes the Premises for a term of three (3) years "
            "commencing on 1 January 2027 and expiring on 31 December 2029 (both days inclusive).",
            "The Landlord shall deliver vacant possession of the Premises to the Tenant on the "
            "Handover Date for the purpose of fitting-out. No Rent shall be payable during the "
            "period from the Handover Date to the day before the commencement of the Term, but "
            "the Tenant shall pay the Management Fee and all utility charges for that period.",
        ]),
        ("Rent and Other Payments", [
            "The Tenant shall pay the Rent monthly in advance on the first day of each calendar "
            "month without any deduction or set-off.",
            "The Tenant shall be entitled to the rent-free period (if any) specified in "
            "Schedule 2, during which the Rent (but not the Management Fee) shall not be payable.",
            "If any Rent, Management Fee or other sum payable under this Agreement remains unpaid "
            "seven (7) days after its due date, the Tenant shall pay interest on that sum at the "
            "rate of two per cent (2%) per month from the due date until the date of payment.",
            "The Tenant shall pay the Management Fee monthly in advance together with the Rent. "
            "The Management Fee may be revised by the Landlord or the manager of the Building "
            "from time to time at their absolute discretion, and the Tenant shall pay the revised "
            "Management Fee from the date specified in the Landlord's written notice.",
        ]),
        ("Deposit", [
            "On signing this Agreement the Tenant shall pay the Deposit to the Landlord as "
            "security for the due performance of the Tenant's obligations.",
            "The Landlord may deduct from the Deposit any arrears of Rent or other sums due, and "
            "any costs incurred by reason of the Tenant's breach. The Tenant shall restore the "
            "Deposit to its full amount within seven (7) days of written demand.",
            "Subject to Clause 4.2, the Deposit shall be refunded to the Tenant without interest "
            "within thirty (30) days after the later of the expiry or earlier termination of this "
            "Agreement and the delivery of vacant possession. If this Agreement is terminated by "
            "reason of the Tenant's breach, the Deposit shall be forfeited to the Landlord without "
            "prejudice to the Landlord's other rights.",
        ]),
        ("Tenant's Obligations", [
            "The Tenant shall use the Premises as an office only and for no other purpose.",
            "The Tenant shall not assign, sublet or part with possession of the Premises or any "
            "part thereof without the prior written consent of the Landlord, which the Landlord "
            "may withhold in its absolute discretion.",
            "The Tenant shall keep the interior of the Premises, including all fixtures, fittings "
            "and any air-conditioning units exclusively serving the Premises, in good and "
            "tenantable repair and condition (fair wear and tear excepted).",
            "On the expiry or earlier termination of this Agreement, the Tenant shall, at its own "
            "cost and if so required by the Landlord, reinstate the Premises to bare-shell "
            "condition, including the removal of any fixtures and fittings installed by any "
            "previous occupier of the Premises, whether or not installed by the Tenant.",
            "The Tenant shall insure its own contents and maintain public liability insurance of "
            "not less than HK$10,000,000 for any one occurrence.",
        ]),
        ("Landlord's Obligations and Exclusions", [
            "The Tenant paying the Rent and performing its obligations shall peaceably hold and "
            "enjoy the Premises without interruption by the Landlord.",
            "The Landlord shall keep the main structure, roof and exterior walls of the Building "
            "in proper repair, provided that the Landlord has received written notice of any "
            "defect and has had a reasonable time to remedy it.",
            "The Landlord shall not be liable to the Tenant for any loss or damage arising from "
            "any defect in or failure of the lifts, air-conditioning, electricity, water supply "
            "or other services of the Building, or from typhoon, rainstorm, fire or other cause "
            "beyond the Landlord's control, and the Rent shall not abate or cease to be payable "
            "in any such event.",
        ]),
        ("Early Termination", [
            "The Tenant may terminate this Agreement by giving to the Landlord not less than "
            "three (3) months' prior written notice, but not before the end of the first eighteen "
            "(18) months of the Term.",
            "Notwithstanding anything in this Agreement, the Landlord may terminate this "
            "Agreement at any time by giving to the Tenant not less than six (6) months' prior "
            "written notice if the Landlord resolves to redevelop or substantially refurbish the "
            "Building. The Tenant shall not be entitled to any compensation for such termination.",
            "If any Rent is unpaid for fourteen (14) days after its due date (whether formally "
            "demanded or not), or if the Tenant commits any other material breach of this "
            "Agreement, the Landlord may re-enter the Premises, whereupon this Agreement shall "
            "terminate without prejudice to the Landlord's accrued rights.",
        ]),
        ("Option to Renew", [
            "Provided there is no subsisting breach, the Tenant may renew this Agreement for a "
            "further term of two (2) years by giving written notice to the Landlord not less "
            "than six (6) months before the expiry of the Term. The rent for the renewed term "
            "shall be the prevailing open market rent as determined by the Landlord.",
        ]),
        ("Stamp Duty and Costs", [
            "The stamp duty payable on this Agreement and its counterpart shall be borne "
            "entirely by the Tenant.",
            "Each party shall bear its own legal costs in connection with the preparation and "
            "execution of this Agreement.",
        ]),
        ("Notices", [
            "Any notice under this Agreement shall be in writing and delivered by hand or sent "
            "by registered post to the address of the recipient stated in this Agreement (or "
            "such other address as notified in writing). A notice sent by registered post shall "
            "be deemed received two (2) business days after posting.",
        ]),
        ("Governing Law and Jurisdiction", [
            "This Agreement shall be governed by and construed in accordance with the laws of the "
            "Hong Kong Special Administrative Region, and the parties submit to the non-exclusive "
            "jurisdiction of the courts of Hong Kong.",
        ]),
    ],
    [
        ("SCHEDULE 1 - THE PREMISES", [
            ("Premises", "Room 1801, 18th Floor, Kestrel Centre, 28 Mariner Street, Quarry Bay, "
                         "Hong Kong"),
            ("Saleable area", "Approximately 1,250 square feet"),
            ("Car parking", "None included"),
            ("Existing fixtures", "Ceiling, lighting, carpet and two glass partitioned rooms "
                                  "installed by the previous occupier"),
        ]),
        ("SCHEDULE 2 - FINANCIAL TERMS", [
            ("Rent", "HK$68,000 per calendar month, exclusive of Management Fee, Government "
                     "rates and Government rent"),
            ("Management Fee", "HK$6,250 per calendar month (HK$5.00 per square foot of "
                               "saleable area), subject to Clause 3.4"),
            ("Government rates and rent", "Payable by the Tenant quarterly as assessed"),
            ("Handover Date", "1 December 2026"),
            ("Rent-free period", "1 January 2027 to 28 February 2027 (both days inclusive). "
                                 "Rent shall first become payable on 1 March 2027."),
            ("Deposit", "HK$222,750, being three (3) months' Rent and Management Fee"),
            ("Permitted use", "Office for the business of data analytics consultancy"),
        ]),
    ],
    [("its authorised signatory", "Harbourview Properties Limited"),
     ("its authorised signatory", "Lumen Analytics (HK) Limited")],
)

# ---------------------------------------------------------- 2. EMPLOYMENT
build(
    "02_Employment_Agreement_Senior_Data_Analyst.pdf",
    "EMPLOYMENT AGREEMENT",
    "Dated 10 November 2026 &nbsp;|&nbsp; Position: Senior Data Analyst",
    [LUMEN + " (the <b>\"Company\"</b>); and",
     "<b>MS WONG KA YAN</b>, holder of a fictitious identity reference SAMPLE-0001, residing in "
     "Hong Kong (the <b>\"Employee\"</b>)."],
    [],
    [
        ("Appointment and Commencement", [
            "The Company shall employ the Employee as Senior Data Analyst with effect from "
            "1 December 2026 (the <b>\"Commencement Date\"</b>).",
            "The Employee shall report to the Head of Analytics or such other person as the "
            "Company may designate from time to time.",
        ]),
        ("Probation", [
            "The first three (3) months of employment shall be a probationary period. During the "
            "probationary period either party may terminate the employment by giving not less "
            "than seven (7) days' written notice or payment in lieu of notice.",
        ]),
        ("Duties", [
            "The Employee shall perform such duties consistent with her position as the Company "
            "may assign, and shall devote her whole working time and attention to the business "
            "of the Company.",
            "The Employee shall not, without the prior written consent of the Company, engage in "
            "any other business or employment during the period of her employment.",
        ]),
        ("Working Hours and Place of Work", [
            "Normal working hours are 9:00 a.m. to 6:00 p.m., Monday to Friday, with a one-hour "
            "lunch break. The Employee may be required to work additional hours without further "
            "remuneration as reasonably necessary for the proper performance of her duties.",
            "The Employee's place of work shall be the Company's office in Hong Kong.",
        ]),
        ("Remuneration", [
            "The Company shall pay the Employee a monthly salary of HK$52,000, payable in arrears "
            "on the last working day of each month.",
            "The Employee may be eligible for a discretionary bonus as described in the Schedule. "
            "Any bonus is at the absolute discretion of the Company and shall not be payable if, "
            "on the payment date, the Employee is serving notice or is no longer employed.",
            "The Company and the Employee shall make contributions to a Mandatory Provident Fund "
            "scheme in accordance with applicable law.",
        ]),
        ("Annual Leave and Holidays", [
            "The Employee shall be entitled to fifteen (15) working days of paid annual leave in "
            "each calendar year (pro-rated for any part year), in addition to general holidays.",
            "Unused annual leave may be carried forward to the following year up to a maximum of "
            "five (5) days, and any days in excess shall lapse.",
        ]),
        ("Sickness", [
            "The Employee shall be entitled to sickness allowance in accordance with the "
            "Employment Ordinance (Cap. 57). The Employee shall provide a medical certificate for "
            "any absence due to sickness of more than one (1) day.",
        ]),
        ("Confidentiality", [
            "The Employee shall not, during or after her employment, disclose to any person or "
            "use for any purpose other than the Company's business any confidential information "
            "relating to the Company, its clients or its business.",
        ]),
        ("Intellectual Property", [
            "All intellectual property rights in any work, software, models, reports or data "
            "created by the Employee in the course of her employment shall vest in and belong to "
            "the Company absolutely.",
        ]),
        ("Termination", [
            "After the probationary period, either party may terminate the employment by giving "
            "the other not less than two (2) months' written notice or payment in lieu of notice.",
            "The Company may terminate the employment without notice or payment in lieu in the "
            "circumstances permitted under section 9 of the Employment Ordinance (Cap. 57).",
            "The Company may require the Employee not to attend work during all or part of any "
            "notice period (garden leave), during which the Employee shall continue to receive "
            "her salary.",
        ]),
        ("Non-Competition", [
            "For a period of twelve (12) months after the date on which the employment ends "
            "(the <b>\"Termination Date\"</b>), the Employee shall not, within Hong Kong, directly "
            "or indirectly be engaged, concerned or interested in any business which competes "
            "with the data analytics business of the Company in which the Employee was involved "
            "during the twelve (12) months before the Termination Date.",
            "The restricted period in Clause 11.1 shall be reduced by any period of garden leave "
            "served under Clause 10.3.",
        ]),
        ("Non-Solicitation", [
            "For a period of twelve (12) months after the Termination Date, the Employee shall not "
            "solicit or entice away any client of the Company with whom she dealt during the "
            "twelve (12) months before the Termination Date, or any employee of the Company.",
        ]),
        ("Return of Property", [
            "On the Termination Date, the Employee shall return to the Company all property, "
            "documents, devices and data belonging to the Company, and shall not retain any copy.",
        ]),
        ("Governing Law and Jurisdiction", [
            "This Agreement shall be governed by the laws of Hong Kong, and the parties submit to "
            "the exclusive jurisdiction of the courts of Hong Kong.",
        ]),
    ],
    [("SCHEDULE - BENEFITS AND SPECIAL TERMS", [
        ("Medical insurance", "Group outpatient and inpatient cover from the Commencement Date"),
        ("Discretionary bonus", "Target up to one (1) month's salary, assessed annually in March "
                                "by reference to individual and company performance"),
        ("Professional training", "Up to HK$8,000 per year for approved courses, repayable in "
                                  "full if the Employee resigns within 12 months of the course"),
        ("Special term - non-competition",
         "Notwithstanding Clause 11.1, if the Company terminates the employment other than "
         "under Clause 10.2, the restricted period in Clause 11.1 shall be six (6) months "
         "instead of twelve (12) months."),
    ])],
    [("its Director", "Lumen Analytics (HK) Limited"), ("the Employee", "herself")],
)

# --------------------------------------------------------------- 3. NDA A
build(
    "03_Mutual_NDA_Pearlstone_Capital.pdf",
    "MUTUAL NON-DISCLOSURE AGREEMENT",
    "Dated 3 October 2026 &nbsp;|&nbsp; Lumen Analytics / Pearlstone Capital",
    [LUMEN + " (<b>\"Lumen\"</b>); and",
     "<b>PEARLSTONE CAPITAL PARTNERS LIMITED</b>, a company incorporated in Hong Kong whose "
     "registered office is at 12th Floor, Granite House, 45 Ledger Road, Admiralty, Hong Kong "
     "(<b>\"Pearlstone\"</b>)."],
    ["The parties wish to exchange information for the purpose of evaluating a possible "
     "engagement under which Lumen would provide data analytics services to Pearlstone (the "
     "<b>\"Purpose\"</b>)."],
    [
        ("Definitions", [
            "<b>\"Confidential Information\"</b> means all information, in any form, disclosed by "
            "one party (the <b>\"Discloser\"</b>) to the other (the <b>\"Recipient\"</b>) in "
            "connection with the Purpose, including business plans, client data, financial "
            "information, models and source code, whether or not marked as confidential.",
            "<b>\"Representatives\"</b> means a party's directors, employees and professional "
            "advisers who need to know the Confidential Information for the Purpose.",
        ]),
        ("Obligations of Confidentiality", [
            "The Recipient shall keep the Discloser's Confidential Information strictly "
            "confidential and shall use it only for the Purpose.",
            "The Recipient may disclose Confidential Information to its Representatives, provided "
            "that it informs them of its confidential nature and remains responsible for any "
            "breach by them.",
            "The Recipient shall apply to the Discloser's Confidential Information no lower "
            "standard of care than it applies to its own confidential information, and in any "
            "event no less than a reasonable standard of care.",
        ]),
        ("Exceptions", [
            "The obligations in Clause 2 shall not apply to information which (a) is or becomes "
            "public other than through breach of this Agreement; (b) was lawfully known to the "
            "Recipient before disclosure; (c) is independently developed by the Recipient; or "
            "(d) is required to be disclosed by law, regulation or order of a competent court or "
            "regulator, provided that the Recipient gives prompt notice to the Discloser where "
            "lawful to do so.",
        ]),
        ("Return and Destruction", [
            "On written request, the Recipient shall promptly return or destroy all Confidential "
            "Information of the Discloser, save for copies retained in automatic electronic "
            "back-up systems or as required by law, which shall remain subject to this Agreement.",
        ]),
        ("Term and Duration of Obligations", [
            "This Agreement shall continue for two (2) years from its date, unless terminated "
            "earlier by either party on thirty (30) days' written notice.",
            "The obligations of confidentiality in this Agreement shall survive termination and "
            "shall continue for a period of three (3) years from the date of each disclosure of "
            "Confidential Information.",
        ]),
        ("No Obligation and No Licence", [
            "Nothing in this Agreement obliges either party to enter into any further agreement. "
            "No licence or other right in any Confidential Information is granted except as "
            "expressly stated.",
        ]),
        ("Remedies", [
            "Each party acknowledges that damages alone may not be an adequate remedy for breach "
            "of this Agreement, and the Discloser shall be entitled to seek injunctive relief in "
            "addition to any other remedy.",
        ]),
        ("General", [
            "This Agreement constitutes the entire agreement between the parties relating to its "
            "subject matter. Any variation must be in writing and signed by both parties.",
            "Neither party may assign this Agreement without the prior written consent of the "
            "other.",
        ]),
        ("Governing Law and Jurisdiction", [
            "This Agreement shall be governed by and construed in accordance with the laws of "
            "Hong Kong, and the parties submit to the non-exclusive jurisdiction of the courts of "
            "Hong Kong.",
        ]),
    ],
    [],
    [("its Director", "Lumen Analytics (HK) Limited"),
     ("its Director", "Pearlstone Capital Partners Limited")],
)

# --------------------------------------------------------------- 4. NDA B
build(
    "04_NDA_Northgate_Robotics_English_Law.pdf",
    "CONFIDENTIALITY AGREEMENT",
    "Dated 15 September 2026 &nbsp;|&nbsp; Northgate Robotics / Lumen Analytics",
    ["<b>NORTHGATE ROBOTICS LTD</b>, a company incorporated in England and Wales whose "
     "registered office is at 7 Foundry Yard, Manchester, United Kingdom "
     "(the <b>\"Disclosing Party\"</b>); and",
     LUMEN + " (the <b>\"Receiving Party\"</b>)."],
    ["The Disclosing Party intends to disclose certain information to the Receiving Party for "
     "the purpose of the Receiving Party assessing the feasibility of developing a fleet "
     "analytics dashboard for the Disclosing Party's autonomous warehouse robots (the "
     "<b>\"Project\"</b>)."],
    [
        ("Definitions", [
            "<b>\"Confidential Information\"</b> means all technical, commercial and other "
            "information disclosed by or on behalf of the Disclosing Party in connection with "
            "the Project, including sensor data, navigation algorithms, customer lists and "
            "pricing, whether disclosed orally, in writing or electronically.",
            "<b>\"Trade Secrets\"</b> means any Confidential Information which the Disclosing Party "
            "identifies in writing as a trade secret at the time of disclosure.",
            "<b>\"Effective Date\"</b> means the date of this Agreement.",
        ]),
        ("Undertakings of the Receiving Party", [
            "The Receiving Party shall hold the Confidential Information in confidence and shall "
            "not disclose it to any third party without the prior written consent of the "
            "Disclosing Party.",
            "The Receiving Party shall use the Confidential Information solely for the Project.",
            "The Receiving Party shall not reverse engineer, decompile or analyse the composition "
            "of any software, data or hardware provided by the Disclosing Party, except to the "
            "extent strictly necessary for the Project.",
            "The Receiving Party shall store all Confidential Information on systems located in "
            "Hong Kong or the United Kingdom only, and shall not upload Confidential Information "
            "to any third-party artificial intelligence service.",
        ]),
        ("Permitted Disclosure", [
            "The Receiving Party may disclose Confidential Information to those of its employees "
            "who need to know it for the Project and who are bound by written obligations of "
            "confidentiality no less strict than those in this Agreement.",
            "The Receiving Party may disclose Confidential Information to the extent required by "
            "law or by any governmental or regulatory authority, provided that it gives the "
            "Disclosing Party as much notice as is lawfully possible.",
        ]),
        ("Duration", [
            "The obligations in this Agreement shall continue for five (5) years from the "
            "Effective Date.",
            "Notwithstanding Clause 4.1, the obligations in respect of Trade Secrets shall "
            "continue for so long as the relevant information remains a trade secret.",
        ]),
        ("Return of Information", [
            "Within ten (10) business days of the Disclosing Party's written request, or upon "
            "completion of the Project, the Receiving Party shall return or securely destroy all "
            "Confidential Information and certify such destruction in writing.",
        ]),
        ("Warranties and Liability", [
            "The Confidential Information is provided \"as is\". The Disclosing Party gives no "
            "warranty as to its accuracy or completeness.",
            "The Receiving Party shall indemnify the Disclosing Party against all losses, costs "
            "and expenses arising from any breach of this Agreement by the Receiving Party or its "
            "employees.",
        ]),
        ("General", [
            "This Agreement may only be varied in writing signed by both parties.",
            "A person who is not a party to this Agreement shall have no right under the "
            "Contracts (Rights of Third Parties) Act 1999 to enforce any of its terms.",
        ]),
        ("Governing Law and Jurisdiction", [
            "This Agreement and any dispute or claim arising out of or in connection with it "
            "shall be governed by and construed in accordance with the laws of England and Wales.",
            "The courts of England shall have exclusive jurisdiction to settle any dispute or "
            "claim arising out of or in connection with this Agreement.",
        ]),
    ],
    [],
    [("its Managing Director", "Northgate Robotics Ltd"),
     ("its Director", "Lumen Analytics (HK) Limited")],
)

# --------------------------------------------------------- 5. CONSULTANCY
build(
    "05_Consultancy_Agreement_Meridian_Advisory.pdf",
    "CONSULTANCY SERVICES AGREEMENT",
    "Dated 20 October 2026 &nbsp;|&nbsp; Lumen Analytics / Meridian Advisory",
    [LUMEN + " (the <b>\"Client\"</b>); and",
     "<b>MERIDIAN ADVISORY PTE. LTD.</b>, a company incorporated in Singapore whose registered "
     "office is at 80 Quayside Avenue, #12-03, Singapore (the <b>\"Consultant\"</b>)."],
    ["The Client wishes to engage the Consultant to provide regulatory and data governance "
     "advisory services, and the Consultant has agreed to do so on the terms of this "
     "Agreement."],
    [
        ("Engagement and Services", [
            "The Client engages the Consultant to provide the services described in the Schedule "
            "(the <b>\"Services\"</b>), and the Consultant shall provide the Services with "
            "reasonable skill, care and diligence.",
            "The Consultant shall act as an independent contractor. Nothing in this Agreement "
            "creates any relationship of employment, partnership or agency.",
        ]),
        ("Term", [
            "This Agreement shall commence on 1 November 2026 and continue for twelve (12) "
            "months, unless terminated earlier in accordance with Clause 7.",
        ]),
        ("Fees and Payment", [
            "In consideration of the Services, the Client shall pay the Consultant a fixed fee of "
            "HK$45,000 per calendar month, exclusive of any applicable taxes.",
            "The Consultant shall invoice the Client monthly in arrears. The Client shall pay each "
            "undisputed invoice within thirty (30) days of receipt.",
            "If the Client fails to pay any undisputed amount by its due date, the Client shall "
            "pay interest on the overdue amount at the rate of one point five per cent (1.5%) per "
            "month, accruing daily from the due date until payment in full.",
            "The Client shall reimburse reasonable out-of-pocket expenses approved by the Client "
            "in writing in advance, against receipts.",
        ]),
        ("Client Obligations", [
            "The Client shall provide the Consultant with such information and access to "
            "personnel as the Consultant reasonably requires to perform the Services.",
        ]),
        ("Confidentiality and Data Protection", [
            "Each party shall keep confidential all information of the other party obtained "
            "under this Agreement, during the Term and for two (2) years thereafter.",
            "The Consultant shall comply with the Personal Data (Privacy) Ordinance (Cap. 486) in "
            "respect of any personal data received from the Client.",
        ]),
        ("Limitation of Liability", [
            "The Consultant's total aggregate liability arising out of or in connection with this "
            "Agreement shall not exceed the total fees paid by the Client in the six (6) months "
            "preceding the event giving rise to the claim.",
            "Neither party shall be liable for any indirect or consequential loss, or loss of "
            "profit, however arising.",
        ]),
        ("Termination", [
            "Either party may terminate this Agreement for convenience by giving the other not "
            "less than thirty (30) days' written notice.",
            "Either party may terminate this Agreement immediately by written notice if the "
            "other party commits a material breach which is not remedied within fourteen (14) "
            "days of written notice requiring it to be remedied.",
            "On termination, the Client shall pay all fees accrued up to the date of termination.",
        ]),
        ("Governing Law", [
            "This Agreement shall be governed by and construed in accordance with the laws of "
            "Singapore.",
        ]),
        ("Dispute Resolution", [
            "Any dispute arising out of or in connection with this Agreement shall be referred "
            "to and finally resolved by arbitration administered by the Hong Kong International "
            "Arbitration Centre (HKIAC) under the HKIAC Administered Arbitration Rules in force "
            "when the notice of arbitration is submitted.",
            "The seat of arbitration shall be Hong Kong. The tribunal shall consist of one "
            "arbitrator, and the language of the arbitration shall be English.",
        ]),
    ],
    [("SCHEDULE - THE SERVICES", [
        ("Scope", "Advice on data governance policies, privacy impact assessments for AI "
                  "analytics projects, and regulatory horizon scanning for Hong Kong and "
                  "Singapore"),
        ("Time commitment", "Up to six (6) consultant days per calendar month; additional days "
                            "charged at HK$9,000 per day with prior written approval"),
        ("Key personnel", "Lead consultant: Mr Daniel Lim (fictitious). Replacement requires "
                          "the Client's prior written approval"),
        ("Deliverables", "Monthly written advisory memo; one data governance policy pack by "
                         "31 January 2027"),
    ])],
    [("its Director", "Lumen Analytics (HK) Limited"), ("its Director", "Meridian Advisory Pte. Ltd.")],
)

# -------------------------------------------------------------- ANSWER KEY
doc = SimpleDocTemplate(f"{OUT}/00_ANSWER_KEY_do_not_upload.pdf", pagesize=A4,
                        leftMargin=15 * mm, rightMargin=15 * mm, topMargin=18 * mm,
                        bottomMargin=20 * mm, title="Answer key - Set B")
story = [Paragraph("ANSWER KEY - RAG TEST SET B", TITLE),
         Paragraph("Do NOT upload this file to the Knowledge base. Scoring: 2 = correct with "
                   "correct citation, 1 = partly correct or missing/wrong citation, 0 = wrong "
                   "or fabricated.", SUB)]

docs = [["#", "File", "Governing law", "Trap built in"],
        ["01", "Office Tenancy Agreement", "Hong Kong",
         "Handover Date conflict (Cl. 1.4 vs Sch. 2); ambiguous break clause (Cl. 7.1); "
         "rent-free period only in Schedule 2"],
        ["02", "Employment Agreement", "Hong Kong",
         "Non-compete 12 months (Cl. 11.1) but 6 months in Schedule if Company terminates; "
         "reduced by garden leave (Cl. 11.2)"],
        ["03", "Mutual NDA - Pearlstone", "Hong Kong",
         "No payment / interest terms at all; 3 years from EACH disclosure"],
        ["04", "NDA - Northgate Robotics", "England and Wales",
         "5 years from Effective Date, trade secrets indefinitely; bans uploading to third-party AI"],
        ["05", "Consultancy - Meridian", "Singapore",
         "Governing law Singapore BUT arbitration seated in Hong Kong (HKIAC); has 1.5% late "
         "interest that can be wrongly attributed to an NDA"]]


def tbl(data, widths):
    rows = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(data)]
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


story += [Paragraph("Document overview", H), tbl(docs, [10 * mm, 42 * mm, 30 * mm, 98 * mm])]

qa = [["Q", "Question (and which file to select)", "Expected answer", "Fail if..."],
      ["8", "List the parties, effective date, term and governing law of this agreement in a "
            "table. [01 Lease]",
       "Harbourview Properties Limited (Landlord); Lumen Analytics (HK) Limited (Tenant). Dated "
       "1 Nov 2026. Term 3 years, 1 Jan 2027 - 31 Dec 2029 (Cl. 2.1). Hong Kong law, "
       "non-exclusive HK courts (Cl. 11).",
       "Gives Tenant's address as Kestrel Centre (that is the Premises, Tenant's office is "
       "Tidewater Building); invents a date"],
      ["9", "What does the termination clause say? Quote the clause number. [01 Lease]",
       "Cl. 7: 7.1 tenant break - 3 months' notice, not before end of first 18 months; 7.2 "
       "landlord may terminate on 6 months' notice for redevelopment, no compensation; 7.3 "
       "re-entry if rent unpaid 14 days or material breach.",
       "Misses 7.2 or 7.3; wrong clause numbers"],
      ["10", "What is the late payment interest rate under this NDA? [03 NDA Pearlstone]",
       "\"Not found in the provided documents.\" NDA A has no payment or interest terms.",
       "Answers 2% (from Lease Cl. 3.3) or 1.5% (from Consultancy Cl. 3.3)"],
      ["11", "Compare the confidentiality period in the Pearlstone NDA and the Northgate NDA. "
             "Which is longer? [03 + 04]",
       "Pearlstone: 3 years from the date of EACH disclosure (Cl. 5.2). Northgate: 5 years from "
       "Effective Date (Cl. 4.1), trade secrets for as long as they remain secret (Cl. 4.2). "
       "Northgate is generally longer; best answers note that a late Pearlstone disclosure can "
       "run past 5 years from signing (e.g. disclosure in Sep 2028 runs to Sep 2031).",
       "Says 2 years for Pearlstone (that is the agreement term, Cl. 5.1); misses trade-secret "
       "carve-out"],
      ["12", "Which of the uploaded agreements are governed by a law other than Hong Kong law? "
             "[all files]",
       "Two: 04 Northgate NDA (England and Wales, Cl. 8.1) and 05 Meridian Consultancy "
       "(Singapore, Cl. 8.1). Note: 05 has HKIAC arbitration seated in Hong Kong (Cl. 9) but "
       "governing law is still Singapore.",
       "Finds only one; lists 05 as Hong Kong law because of the arbitration seat; includes "
       "an HK-law document"],
      ["13", "From the tenant's perspective, which three clauses in this lease are most "
             "unfavourable, and why? [01 Lease]",
       "Any 3 of: 7.2 landlord redevelopment break, no compensation; 5.4 reinstatement to bare "
       "shell incl. previous occupier's fixtures; 6.3 landlord exclusion and no rent abatement; "
       "3.4 management fee revisable at absolute discretion; 9.1 tenant pays all stamp duty "
       "(commonly shared 50/50 in HK); 5.2 consent at absolute discretion; 4.3 deposit "
       "forfeiture; 8.1 renewal rent set by landlord.",
       "Picks neutral clauses (e.g. 11 governing law) or cites wrong numbers"],
      ["14", "Is there a rent-free period, and when does rent first become payable? [01 Lease]",
       "Yes - Schedule 2: 1 Jan 2027 to 28 Feb 2027; rent first payable 1 Mar 2027. "
       "Management Fee still payable during rent-free period (Cl. 3.2).",
       "Says no rent-free period (missed the Schedule at the end); says management fee is free"],
      ["14b", "When is the Handover Date? [01 Lease]",
       "Best answer flags the CONFLICT: Cl. 1.4 says 15 Dec 2026, Schedule 2 says 1 Dec 2026.",
       "Gives only one date with confidence"],
      ["15", "Based on the non-compete clause in the employment agreement, draft an email to the "
             "counterparty proposing to reduce the non-compete period by half. [02 Employment]",
       "Email proposing 12 -> 6 months, citing Cl. 11.1. Excellent answer notices the Schedule "
       "already gives 6 months if the Company terminates (other than for cause) and that garden "
       "leave reduces the period (Cl. 11.2).",
       "Wrong current period; invents terms; ignores the clause"],
      ["Bonus", "The tenant wants to leave as early as possible. When is the earliest date to "
                "serve notice, and the earliest termination date? [01 Lease]",
       "AMBIGUOUS (Cl. 7.1). Term starts 1 Jan 2027; first 18 months end 30 Jun 2028. "
       "(A) Notice can only be SERVED after that: serve 1 Jul 2028, terminate about "
       "1 Oct 2028. (B) TERMINATION cannot be before that: serve by about 31 Mar 2028, terminate "
       "about 30 Jun / 1 Jul 2028. A good answer presents both.",
       "Picks one reading without flagging ambiguity; date arithmetic wrong"],
      ["Bonus", "Can the Receiving Party use ChatGPT to summarise Northgate's documents? "
                "[04 Northgate]",
       "No - Cl. 2.4 prohibits uploading Confidential Information to any third-party AI "
       "service (a local model on own hardware is arguably not third-party, but worth "
       "flagging for a lawyer).",
       "Says yes / misses Cl. 2.4"],
      ]
story += [Paragraph("Questions and expected answers", H),
          tbl(qa, [11 * mm, 47 * mm, 77 * mm, 45 * mm])]
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("done")
