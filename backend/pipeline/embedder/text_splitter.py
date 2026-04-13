from langchain_text_splitters import RecursiveCharacterTextSplitter

class ArticleTextSplitter:
    """
    긴 기사 본문을 LLM과 임베딩 모델이 처리하기 좋은 크기로 쪼개주는 클래스
    """
    def __init__(self, chunk_size=500, chunk_overlap=50):
        # RecursiveCharacterTextSplitter: 문단, 문장, 공백 순으로 우선순위를 두어 텍스트를 나눔
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def split_text(self, text: str):
        """텍스트를 받아 조각(Chunk) 리스트로 반환"""
        if not text:
            return []
        return self.splitter.split_text(text)

if __name__ == "__main__":
    # 테스트용 코드
    sample_text = "안녕하세요. 이것은 테스트 데이터입니다. " * 50
    splitter = ArticleTextSplitter()
    chunks = splitter.split_text(sample_text)
    print(f"총 조각 수: {len(chunks)}")
    print(f"첫 번째 조각 미리보기: {chunks[0][:50]}...")
