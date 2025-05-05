import fitz  # PyMuPDF
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def save_index_html(content):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    pdf_file = "quiz.pdf"  # 파일명은 사용자가 올려야 함
    if not Path(pdf_file).exists():
        print(f"'{pdf_file}' not found.")
        exit(1)

    text = extract_text_from_pdf(pdf_file)

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>전기기사 퀴즈</title>
</head>
<body>
    <h1>전기기사 기출문제</h1>
    <pre>{text}</pre>
</body>
</html>"""

    save_index_html(html_content)
    print("index.html created.")
