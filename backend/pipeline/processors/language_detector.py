from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

class LanguageDetector:
    """
    텍스트의 주 사용 언어를 감지하는 클래스
    """
    @staticmethod
    def detect_language(text: str) -> str:
        """
        텍스트의 언어를 감지하여 'ko', 'en' 등의 두 글자 코드로 반환.
        감지할 수 없거나 너무 짧은 오류 발생 시 기본값 'unknown' 반환
        """
        if not text or len(text.strip()) < 5:
            return "unknown"
            
        try:
            lang = detect(text)
            return lang
        except LangDetectException:
            # 해시태그뿐이거나 숫자로만 이루어져 감지 실패 시
            return "unknown"
        except Exception as e:
            print(f"[LanguageDetector Error] {e}")
            return "unknown"
