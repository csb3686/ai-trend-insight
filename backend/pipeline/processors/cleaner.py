import re
from bs4 import BeautifulSoup

class DataCleaner:
    """
    HTML 찌꺼기와 불필요한 공백, 특수문자를 제거하는 클래스
    """
    @staticmethod
    def clean_html(raw_html: str) -> str:
        """BeautifulSoup을 이용해 HTML 태그 제거 및 순수 텍스트 추출"""
        if not raw_html:
            return ""
            
        # HTML 태그 속성('<')이 의심되지 않는 단순 문자열일 경우 BS4 파싱 생략 (경고창 방지)
        if "<" not in raw_html:
            return raw_html.strip()
        
        # lxml이나 html.parser 등을 사용 가능 (내장 html.parser 사용)
        soup = BeautifulSoup(raw_html, "html.parser")
        return soup.get_text(separator=" ", strip=True)

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """여러 개의 공백, 탭, 줄바꿈을 하나의 공백으로 치환"""
        if not text:
            return ""
        # \s+ 정규식을 이용해 모든 공백 문자를 단일 스페이스로 변경
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def clean_text(raw_text: str) -> str:
        """파이프라인 전체 프로세스 (HTML 제거 -> 공백 정규화)"""
        if not raw_text:
            return ""
        
        # 1단계: HTML 태그 제거
        text = DataCleaner.clean_html(raw_text)
        
        # 2단계: 공백 정규화
        text = DataCleaner.normalize_whitespace(text)
        
        return text

    @staticmethod
    def is_valid_text(text: str, min_length: int = 50) -> bool:
        """
        텍스트가 통계에 사용할 만큼 충분한 의미(길이)를 가지는지 판별
        """
        if not text:
            return False
        return len(text) >= min_length
