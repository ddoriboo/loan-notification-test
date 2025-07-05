#!/usr/bin/env python3
"""
Railway 환경 디버깅 스크립트
실제 환경에서 파일 경로와 존재 여부 확인
"""

import os
import sys

def debug_railway_environment():
    """Railway 환경 정보 출력"""
    print("🔍 Railway 환경 디버깅")
    print("=" * 50)
    
    # 현재 작업 디렉토리
    cwd = os.getcwd()
    print(f"📁 현재 작업 디렉토리: {cwd}")
    
    # 환경변수 확인
    openai_key = os.environ.get('OPENAI_API_KEY')
    print(f"🔑 OPENAI_API_KEY: {'✅ 설정됨' if openai_key else '❌ 없음'}")
    if openai_key:
        print(f"    길이: {len(openai_key)} 문자")
    
    port = os.environ.get('PORT', '8080')
    print(f"🔌 PORT: {port}")
    
    # 파일 시스템 확인
    print(f"\n📂 현재 디렉토리 파일 목록:")
    try:
        files = os.listdir(cwd)
        for file in sorted(files):
            if file.endswith('.csv'):
                file_path = os.path.join(cwd, file)
                size = os.path.getsize(file_path)
                print(f"  📄 {file} ({size:,} bytes)")
            elif file.endswith('.py'):
                print(f"  🐍 {file}")
            elif file.endswith('.html'):
                print(f"  🌐 {file}")
    except Exception as e:
        print(f"  ❌ 디렉토리 읽기 실패: {e}")
    
    # 특정 파일 존재 확인
    print(f"\n🎯 핵심 파일 확인:")
    key_files = [
        '202507_.csv',
        'real_llm_generator.py',
        'ultimate_web_server.py',
        'ultimate_ai_message_generator_v2.html'
    ]
    
    for file in key_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size:,} bytes)")
        else:
            print(f"  ❌ {file} 없음")
    
    # CSV 파일 상세 정보
    csv_file = '202507_.csv'
    if os.path.exists(csv_file):
        print(f"\n📊 CSV 파일 상세 정보:")
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                print(f"  헤더: {first_line}")
                
                # 행 수 계산
                f.seek(0)
                lines = sum(1 for line in f) - 1  # 헤더 제외
                print(f"  데이터 행 수: {lines:,}개")
                
        except Exception as e:
            print(f"  ❌ CSV 읽기 실패: {e}")
    
    # Python 버전 및 모듈 확인
    print(f"\n🐍 Python 환경:")
    print(f"  버전: {sys.version}")
    print(f"  실행 경로: {sys.executable}")
    
    # 중요 모듈 import 테스트
    modules_to_test = ['csv', 'json', 'datetime', 'statistics']
    print(f"\n📦 모듈 import 테스트:")
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
    
    # OpenAI 모듈 특별 테스트
    try:
        import openai
        print(f"  ✅ openai (버전: {openai.__version__ if hasattr(openai, '__version__') else 'Unknown'})")
    except ImportError as e:
        print(f"  ❌ openai: {e}")

if __name__ == "__main__":
    debug_railway_environment()