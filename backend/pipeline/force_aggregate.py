import os
import sys
from datetime import datetime

# 프로젝트 루트 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pipeline.processors.stats_aggregator import TrendsAggregator

def run_force_aggregation():
    print("==================================================")
    print("🚀 [Engine] Trend Analysis & Aggregation Start 🚀")
    print("==================================================")
    
    try:
        aggregator = TrendsAggregator()
        print("[Engine] Aggregating all monthly trends...")
        aggregator.aggregate_all()
        
        print("==================================================")
        print("✅ [Engine] Aggregation Completed Successfully! ")
        print("==================================================")
    except Exception as e:
        print(f"❌ [Engine] Error during aggregation: {str(e)}")

if __name__ == "__main__":
    run_force_aggregation()
