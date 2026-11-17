"""
Make a fictitious Korean research-services contract (DOCX) for testing.

The contract has deliberate traps (see answer key) so we can check whether
the model finds conflicts between the body and the schedules.

Usage:
    python3 make_contracts_ko.py [output_dir]

Needs: python-docx (pip install python-docx)
"""
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

FONT = "맑은 고딕"

TITLE = "연구용역 계약서"
NOTICE = "※ 이 문서는 AI 테스트용으로 만든 가상 계약서입니다. 실제 당사자·기관과 관계없습니다."

PARTIES = [
    "발주자: 주식회사 한별유통 (이하 \"갑\"이라 한다)",
    "수행자: 주식회사 가람데이터리서치 (이하 \"을\"이라 한다)",
    "갑과 을은 아래 연구용역(이하 \"본 용역\"이라 한다)에 관하여 다음과 같이 계약을 체결한다.",
]

ARTICLES = [
    ("제1조 (목적)",
     ["본 계약은 갑의 고객 만족도 조사 및 분석 용역의 수행에 필요한 사항을 정함을 목적으로 한다."]),
    ("제2조 (용역의 범위)",
     ["① 을은 별표 1에 정한 과업을 수행한다.",
      "② 조사 대상은 갑의 최근 1년 이내 구매 고객 1,200명으로 하며, 조사 방법은 온라인 설문과 전화 면접을 병행한다."]),
    ("제3조 (계약기간)",
     ["본 계약의 기간은 2027년 1월 4일부터 2027년 6월 30일까지로 한다."]),
    ("제4조 (계약금액)",
     ["① 본 용역의 계약금액은 금 사천팔백만원(₩48,000,000)으로 하며, 부가가치세는 별도로 한다.",
      "② 대금의 지급 시기와 비율은 별표 2에 따른다."]),
    ("제5조 (대금의 지급)",
     ["① 을은 각 단계의 과업을 완료한 후 갑에게 대금 지급을 청구하고, 갑은 청구서를 받은 날부터 30일 이내에 지급한다.",
      "② 갑은 을의 결과물이 별표 1의 기준에 미달하는 경우 보완이 완료될 때까지 해당 단계의 대금 지급을 보류할 수 있다."]),
    ("제6조 (개인정보의 처리)",
     ["① 을은 본 용역 수행 중 취득한 응답자의 개인정보를 본 용역의 목적 외로 이용하거나 제3자에게 제공하여서는 아니 된다.",
      "② 을은 본 용역이 종료된 날부터 30일 이내에 응답자의 개인정보를 파기하고, 파기 확인서를 갑에게 제출한다.",
      "③ 을이 제1항 또는 제2항을 위반하여 갑에게 손해가 발생한 경우, 을은 그 손해를 배상한다."]),
    ("제7조 (비밀유지)",
     ["을은 본 계약의 이행 과정에서 알게 된 갑의 영업상 비밀을 계약기간 중 및 계약 종료 후 3년간 제3자에게 누설하여서는 아니 된다."]),
    ("제8조 (지체상금)",
     ["① 을이 별표 1의 납품 기한까지 결과물을 제출하지 못한 경우, 지체일수 1일마다 계약금액의 1천분의 1에 해당하는 지체상금을 갑에게 지급한다.",
      "② 지체상금의 총액은 계약금액의 100분의 10을 초과하지 아니한다."]),
    ("제9조 (결과물의 권리)",
     ["① 본 용역의 결과보고서 및 원자료에 대한 저작권은 갑에게 귀속한다.",
      "② 다만, 을이 본 계약 이전부터 보유한 조사 방법론과 분석 도구에 관한 권리는 을에게 유보되며, 갑은 결과물 활용에 필요한 범위에서 이를 사용할 수 있다."]),
    ("제10조 (계약의 해지)",
     ["① 갑은 을이 정당한 사유 없이 과업을 지연하거나 본 계약을 위반한 경우 서면으로 통지하고 본 계약을 해지할 수 있다.",
      "② 갑은 제1항의 사유가 없더라도 30일 전에 서면으로 통지하여 본 계약을 해지할 수 있다. 이 경우 갑은 해지일까지 을이 수행한 과업에 대한 대금을 정산하여 지급한다."]),
    ("제11조 (분쟁의 해결)",
     ["① 본 계약에 관한 분쟁은 갑과 을이 협의하여 해결한다.",
      "② 협의가 이루어지지 아니한 경우, 분쟁은 갑의 본점 소재지를 관할하는 법원을 제1심 관할법원으로 하여 해결한다.",
      "③ 본 계약에서 발생하는 모든 분쟁은 대한상사중재원의 중재규칙에 따라 중재로 최종 해결한다."]),
    ("제12조 (기타)",
     ["본 계약에서 정하지 아니한 사항은 관계 법령과 일반 상관례에 따른다."]),
]

SCHEDULE_1 = ("별표 1. 과업 일정 및 결과물", ["단계", "과업 내용", "결과물", "납품 기한"], [
    ["1단계", "조사 설계 및 설문지 확정", "조사 설계서, 설문지", "2027년 2월 5일"],
    ["2단계", "실사(온라인·전화 조사)", "원자료(데이터), 실사 보고서", "2027년 4월 30일"],
    ["3단계", "분석 및 최종 보고", "최종 결과보고서", "2027년 7월 15일"],
])

SCHEDULE_2 = ("별표 2. 대금 지급 조건 (부가가치세 포함)", ["구분", "지급 시기", "비율", "금액"], [
    ["선금", "계약 체결 후", "30%", "₩14,400,000"],
    ["중도금", "2단계 완료 후", "30%", "₩14,400,000"],
    ["잔금", "3단계 완료 후", "40%", "₩19,200,000"],
    ["합계", "", "100%", "₩48,000,000"],
])

SIGN = [
    "2026년 12월 15일",
    "갑: 주식회사 한별유통  대표이사 김가상 (인)",
    "을: 주식회사 가람데이터리서치  대표이사 이가상 (인)",
]


def set_font(doc):
    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(10.5)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)  # Korean text needs the East Asian font slot


def add_table(doc, title, header, rows):
    doc.add_heading(title, level=2)
    table = doc.add_table(rows=1, cols=len(header))
    table.style = "Table Grid"
    for cell, text in zip(table.rows[0].cells, header):
        cell.text = text
    for row in rows:
        cells = table.add_row().cells
        for cell, text in zip(cells, row):
            cell.text = text


def main(out_dir="."):
    doc = Document()
    set_font(doc)
    doc.add_heading(TITLE, level=1)
    doc.add_paragraph(NOTICE)
    for line in PARTIES:
        doc.add_paragraph(line)
    for heading, paragraphs in ARTICLES:
        doc.add_heading(heading, level=3)
        for p in paragraphs:
            doc.add_paragraph(p)
    for line in SIGN:
        doc.add_paragraph(line)
    add_table(doc, *SCHEDULE_1)
    add_table(doc, *SCHEDULE_2)

    out = Path(out_dir) / "K01_연구용역계약서_가람데이터리서치.docx"
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out)
    print(f"Saved {out}")


if __name__ == "__main__":
    main(*sys.argv[1:])
