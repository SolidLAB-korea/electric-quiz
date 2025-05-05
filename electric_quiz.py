import re
import json
from PyPDF2 import PdfReader

# PDF 경로 설정 (리포지토리 루트에 위치)
pdf_path = "기사기출.pdf"
output_html = "index.html"

# PDF 읽기
reader = PdfReader(pdf_path)
pages = [page.extract_text() for page in reader.pages]
full_text = "\n".join(pages)

# 마지막 페이지에서 정답 문자열만 추출
answer_text = pages[-1]
answer_lines = [
    line for line in answer_text.splitlines()
    if re.match(r"^[\d\s/]+$", line.strip())
]
# 예: "22331 / 23444" → 숫자만 뽑아서 리스트로
digits = re.findall(r"\d", "".join(answer_lines))
answers = [int(d) - 1 for d in digits]  # 0-based index

# 문제 및 보 기 추출
lines = full_text.splitlines()
questions = []
current = {"question": "", "options": []}
for line in lines:
    s = line.strip()
    # 문제 번호로 시작 (예: "1. ○○○")
    if re.match(r"^\d{1,3}\.", s):
        if current["question"] and len(current["options"]) == 4:
            questions.append(current)
        current = {"question": s, "options": []}
    # 보기 (예: "1) ○○○")
    elif re.match(r"^[1-4]\)", s):
        current["options"].append(s)
# 마지막 문제 추가
if current["question"] and len(current["options"]) == 4:
    questions.append(current)

# 문제 수와 정답 수 맞추기
n = min(len(questions), len(answers))
questions, answers = questions[:n], answers[:n]

# HTML 생성
html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>전기기사 기출 퀴즈</title>
  <style>
    body {{ font-family: Arial; padding:20px; max-width:800px; margin:auto; }}
    .question {{ margin-bottom:20px; }}
    .correct {{ color: green; }}
    .incorrect {{ color: red; }}
  </style>
</head>
<body>
  <h1>전기기사 기출 퀴즈</h1>
  <div id="quiz"></div>
  <button onclick="checkAnswers()">정답 확인</button>
  <script>
    const data = {json.dumps(questions, ensure_ascii=False)};
    const answers = {json.dumps(answers)};
    const quizDiv = document.getElementById("quiz");
    data.forEach((q, i) => {{
      const div = document.createElement("div");
      div.className = "question";
      let html = `<p><b>Q${{i+1}}.</b> ${{q.question}}</p>`;
      q.options.forEach((opt, j) => {{
        html += `<label><input type="radio" name="q${{i}}" value="${{j}}"> ${{opt}}</label><br>`;
      }});
      div.innerHTML = html;
      quizDiv.appendChild(div);
    }});
    function checkAnswers() {{
      data.forEach((q, i) => {{
        const sel = document.querySelector(`input[name="q${{i}}"]:checked`);
        const p = quizDiv.children[i];
        p.classList.remove("correct","incorrect");
        if (sel) {{
          if (parseInt(sel.value) === answers[i]) p.classList.add("correct");
          else p.classList.add("incorrect");
        }}
      }});
    }}
  </script>
</body>
</html>"""

with open(output_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ {output_html} 생성 완료")
