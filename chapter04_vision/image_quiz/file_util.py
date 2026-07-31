# ============================================================
# Markdown 파일 생성 모듈
# ============================================================
def make_markdown(results):
    md = "# GPT Vision 이미지 퀴즈\n\n"

    for item in results:
        md += f"## {item['image']}\n\n"
        md += item["quiz"]
        md += "\n\n---\n\n"
    return md
# ============================================================
# Markdown 파일 생성 모듈
# ============================================================
def load_descriptions(file_path):
    descriptions = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # 빈 줄은 건너뛰기
            if not line:
                continue

            key, value = line.split("=", 1)
            descriptions[key.strip()] = value.strip()

    return descriptions
# ============================================================