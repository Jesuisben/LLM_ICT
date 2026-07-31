# =====================================================================
# 이미지 파일과 연관된 유틸리티 모듈
# =====================================================================
from pathlib import Path

from chapter04_vision.image_quiz.image_quiz import (
    image_quiz
)
# =====================================================================
# 지원하는 이미지 확장자
IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".gif"
}
# =====================================================================
# 지정한 폴더 안의 이미지 목록을 반환한다.
# =====================================================================
def get_image_list(image_dir):
    image_folder = Path(image_dir)

    if not image_folder.exists():
        raise FileNotFoundError(f"폴더가 존재하지 않습니다.\n{image_folder}")

    # 파일 항목 중에 IMAGE_EXTENSIONS 속해 있는 모든 파일들을 추출
    image_list = sorted(
        [
            file
            for file in image_folder.iterdir()
            if file.is_file()
            and file.suffix.lower() in IMAGE_EXTENSIONS
        ]
    )

    return image_list
# =====================================================================
# 모든 이미지에 대하여 퀴즈를 생성해주는 함수
# =====================================================================
def create_all_quiz(image_list):
    results = []

    for image in image_list:
        quiz = image_quiz(str(image))
        quiz_dict = {
            "image": image.name,
            "quiz": quiz
        }
        print(quiz_dict)

        results.append(
            quiz_dict
        )

    return results


# =====================================================================
# 다음 항목들은 현재 사용이 되고 있지 않습니다.
# =====================================================================
# 이미지들의 파일 이름 목록만 반환해주는 함수
# =====================================================================
def get_image_names(image_dir):
    return [file.name for file in get_image_list(image_dir)]

# =====================================================================
# 이미지 개수를 반환해주는 함수
# =====================================================================
def image_count(image_dir):
    return len(get_image_list(image_dir))
# =====================================================================