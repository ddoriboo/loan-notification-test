#!/usr/bin/env python3
"""
CSV 업로드 디버깅 스크립트
업로드된 CSV가 제대로 분석되는지 확인
"""

from upload_analyzer import analyzer

# 간단한 테스트 CSV 생성
test_csv = """서비스명,클릭율,발송 문구,발송일,요일
신용대출,12.5,"(광고) 특별 혜택 대출 확인하세요",2025-01-01,수
주택담보대출,8.3,"(광고) 주택담보대출 금리 비교",2025-01-02,목"""

print("=== CSV 업로드 디버깅 테스트 ===")
print(f"테스트 CSV:\n{test_csv}")
print()

# 분석기 초기화 확인
print(f"초기 analyzer.data 길이: {len(analyzer.data)}")
print(f"초기 analyzer.analysis_complete: {analyzer.analysis_complete}")
print()

# CSV 분석 실행
print("CSV 분석 시작...")
result = analyzer.analyze_uploaded_csv(test_csv)

print("\n=== 분석 결과 ===")
print(f"성공 여부: {result.get('success', False)}")
print(f"메시지 수: {result.get('total_messages', 0)}")
print(f"analyzer.data 길이: {len(analyzer.data)}")

if analyzer.data:
    print("\n실제 데이터:")
    for i, row in enumerate(analyzer.data):
        print(f"  {i+1}. 서비스: {row.get('서비스명')}, 클릭률: {row.get('클릭율')}%, 요일: {row.get('요일')}")

# 대시보드 데이터 테스트
print("\n=== 대시보드 데이터 테스트 ===")
dashboard = analyzer.get_dashboard_data()
if dashboard['success']:
    print("✅ 대시보드 데이터 생성 성공")
    time_analysis = dashboard['data']['time_analysis']
    print(f"요일별 분석: {time_analysis}")
else:
    print(f"❌ 대시보드 생성 실패: {dashboard['error']}")