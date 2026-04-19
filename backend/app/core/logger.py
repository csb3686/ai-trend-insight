import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class CustomLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CustomLogger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        # 프로젝트 루트 경로 찾기 (backend 폴더 기준 상위)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        log_dir = os.path.join(base_dir, 'backend', 'logs')
        
        # 로그 디렉토리 생성
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.logger = logging.getLogger("AITrendInsight")
        self.logger.setLevel(logging.INFO)

        # 이미 핸들러가 설정되어 있다면 스킵 (중복 방지)
        if not self.logger.handlers:
            # 1. 파일 핸들러 설정 (날짜별 로테이션, 7일 보관)
            log_file = os.path.join(log_dir, 'pipeline.log')
            file_handler = TimedRotatingFileHandler(
                log_file, when='midnight', interval=1, backupCount=7, encoding='utf-8'
            )
            file_formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

            # 2. 콘솔 핸들러 설정 (터미널 출력용)
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

def get_logger():
    return CustomLogger().get_logger()
