#!/usr/bin/env python3
"""
디버깅용 테스트 스크립트
Railway 배포시 백엔드 API가 제대로 작동하는지 확인
"""

import json
import sys
import traceback

def test_llm_generator():
    """LLM 생성기 테스트"""
    try:
        print("🔍 LLM 생성기 테스트 시작...")
        
        from real_llm_generator import RealLLMGenerator
        
        # 생성기 초기화
        generator = RealLLMGenerator("202507_.csv")
        print("✅ 생성기 초기화 완료")
        
        # 대시보드 데이터 테스트
        dashboard_data = generator.get_dashboard_data()
        print("✅ 대시보드 데이터 생성 완료")
        
        # 데이터 구조 검증
        required_keys = ['summary', 'service_analysis', 'keyword_analysis', 'time_analysis', 'high_performance_messages']
        for key in required_keys:
            if key in dashboard_data:
                print(f"✅ {key}: OK")
            else:
                print(f"❌ {key}: 누락")
        
        # 요약 데이터 확인
        summary = dashboard_data.get('summary', {})
        print(f"\n📊 요약 데이터:")
        print(f"- 총 메시지: {summary.get('total_messages', 'N/A')}")
        print(f"- 평균 클릭률: {summary.get('avg_click_rate', 'N/A')}")
        print(f"- 최고 클릭률: {summary.get('best_click_rate', 'N/A')}")
        print(f"- 고성과 메시지: {summary.get('high_performance_count', 'N/A')}")
        
        # 키워드 분석 확인
        keyword_analysis = dashboard_data.get('keyword_analysis', {})
        print(f"\n🔑 키워드 분석 (상위 5개):")
        for i, (keyword, stats) in enumerate(list(keyword_analysis.items())[:5]):
            print(f"- {keyword}: {stats}")
        
        # 시간대 분석 확인
        time_analysis = dashboard_data.get('time_analysis', {})
        print(f"\n⏰ 시간대 분석:")
        for day, data in time_analysis.items():
            print(f"- {day}: {data}")
        
        return True
        
    except Exception as e:
        print(f"❌ 테스트 실패: {str(e)}")
        print(f"상세 오류:")
        traceback.print_exc()
        return False

def test_api_server():
    """API 서버 테스트"""
    try:
        print("\n🌐 API 서버 테스트...")
        
        from ultimate_web_server import UltimateHTTPRequestHandler
        print("✅ 서버 모듈 임포트 성공")
        
        return True
        
    except Exception as e:
        print(f"❌ 서버 테스트 실패: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Railway 배포 디버깅 테스트")
    print("=" * 50)
    
    # 환경 확인
    import os
    openai_key = os.environ.get('OPENAI_API_KEY')
    if openai_key:
        print(f"✅ OPENAI_API_KEY 설정됨 (길이: {len(openai_key)})")
    else:
        print("❌ OPENAI_API_KEY 환경변수 없음")
    
    # CSV 파일 확인
    if os.path.exists("202507_.csv"):
        print("✅ CSV 데이터 파일 존재")
    else:
        print("❌ CSV 데이터 파일 없음")
    
    print("\n" + "=" * 50)
    
    # 테스트 실행
    llm_test = test_llm_generator()
    api_test = test_api_server()
    
    print("\n" + "=" * 50)
    print("📋 테스트 결과 요약:")
    print(f"- LLM 생성기: {'✅ 성공' if llm_test else '❌ 실패'}")
    print(f"- API 서버: {'✅ 성공' if api_test else '❌ 실패'}")
    
    if llm_test and api_test:
        print("\n🎉 모든 테스트 통과! 서비스가 정상 작동해야 합니다.")
        sys.exit(0)
    else:
        print("\n💥 일부 테스트 실패! Railway 로그를 확인하세요.")
        sys.exit(1)