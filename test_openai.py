#!/usr/bin/env python3
"""
OpenAI API 연결 테스트 스크립트
"""

import os
import sys

print("=== OpenAI API 테스트 ===")
print()

# 환경변수 확인
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    print("❌ OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
    print("   설정 방법: export OPENAI_API_KEY='your-api-key-here'")
    sys.exit(1)

print(f"✅ API 키 발견: {api_key[:7]}...")

# OpenAI 라이브러리 확인
try:
    import openai
    print("✅ OpenAI 라이브러리 설치됨")
except ImportError:
    print("❌ OpenAI 라이브러리가 설치되지 않았습니다.")
    print("   설치 방법: pip install openai")
    sys.exit(1)

# API 연결 테스트
try:
    client = openai.OpenAI(api_key=api_key)
    
    # 간단한 테스트 메시지
    print("\n🤖 GPT-4에게 테스트 질문 중...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "한국어로 짧게 대답하세요."},
            {"role": "user", "content": "대출 마케팅 메시지를 한 줄로 작성해주세요."}
        ],
        max_tokens=100
    )
    
    print("\n✅ OpenAI API 연결 성공!")
    print(f"📝 응답: {response.choices[0].message.content}")
    print("\n이제 upload_web_server.py를 실행하면 실제 LLM을 사용합니다!")
    
except Exception as e:
    print(f"\n❌ OpenAI API 오류: {e}")
    print("   - API 키가 유효한지 확인하세요")
    print("   - OpenAI 계정에 크레딧이 있는지 확인하세요")