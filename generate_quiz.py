import fitz  # PyMuPDF
import os
import re
import json

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = [page.get_text() for page in doc]
    return pages

def parse_questions_and_answers(pages):
    questions = []
    answers = {}

    # Extract answers from last page(s)
    for i in range(len(pages)-1, -1, -1):
        lines = pages[i].splitlines()
        for line in lines:
            match = re.findall(r"(\d{1,3})[\s.:\-]*(\(?[1-5]\)?)", line)
            for num, ans in match:
                answers[int(num)] = ans.replace("(", "").replace(")", "")
        if len(answers) > 200:
            break

    # Extract questions
    q_pattern = re.compile(r"^(\d{1,3})[.\)]\s*(.+)")
    opt_pattern = re.compile(r"^\(?([1-5])\)\s*(.+)")

    current_q = None
    for page in pages[:-1]:
        lines = page.splitlines()
        for line in lines:
            q_match = q_pattern.match(line)
            opt_match = opt_pattern.match(line)
            if q_match:
                if current_q:
                    questions.append(current_q)
                current_q = {
                    "number": int(q_match.group(1)),
                    "question": q_match.group(2),
                    "options": []
                }
            elif opt_match and current_q:
                current_q["options"].append(opt_match.group(2))
    if current_q:
        questions.append(current_q)

    # Merge with answers
    for q in questions:
        q["answer"] = answers.get(q["number"], "?")
    return questions

def generate_html(questions, output_path="index.html"):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head><meta charset='utf-8'><title>전기기사 퀴즈</title></head><body>")
        f.write("<h1>전기기사 기출 퀴즈</h1>")
        for q in questions:
            f.write(f"<div><h3>{q['number']}. {q['question']}</h3><ul>")
            for i, opt in enumerate(q['options'], start=1):
                f.write(f"<li>{i}. {opt}</li>")
            f.write(f"</ul><p><strong>정답: {q['answer']}</strong></p></div><hr>")
        f.write("</body></html>")

if __name__ == "__main__":
    pdf_file = "기출문제.pdf"
    if os.path.exists(pdf_file):
        pages = extract_text_from_pdf(pdf_file)
        questions = parse_questions_and_answers(pages)
        generate_html(questions)
        print(f"{len(questions)}개의 문제를 index.html로 생성했습니다.")
    else:
        print("기출문제.pdf 파일이 존재하지 않습니다.")
