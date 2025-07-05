#!/usr/bin/env python3
"""
AI 문구 생성기 웹 서비스
Flask 기반 API 서버
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from message_ai_generator import MessageAIGenerator

app = Flask(__name__)
CORS(app)  # CORS 허용

# 글로벌 변수
generator = None

@app.route('/')
def index():
    """메인 페이지"""
    return send_from_directory('.', 'ai_message_generator_updated.html')

@app.route('/api/generate', methods=['POST'])
def generate_messages():
    """메시지 생성 API"""
    global generator
    
    try:
        # 첫 요청 시 생성기 초기화
        if generator is None:
            print("🔄 AI 생성기 초기화 중...")
            generator = MessageAIGenerator("/mnt/c/Users/USER/Documents/notification/202507_.csv")
            print("✅ 초기화 완료!")
        
        # 요청 데이터 파싱
        data = request.json
        print(f"📝 요청 데이터: {data}")
        
        # 자연어 입력 파싱
        parsed_input = generator.parse_natural_language_input(data.get('description', ''))
        
        # 사용자 입력으로 덮어쓰기
        if data.get('service'):
            parsed_input['service'] = data['service']
        if data.get('tone'):
            parsed_input['tone'] = data['tone']
        if data.get('keywords'):
            parsed_input['keywords'] = data['keywords']
        if data.get('target'):
            parsed_input['target_audience'] = data['target']
        
        parsed_input['description'] = data.get('description', '')
        
        print(f"🔍 파싱된 입력: {parsed_input}")
        
        # 기존 문구 매칭
        matching_results = generator.find_matching_messages(parsed_input)
        print(f"📋 매칭 결과 수: {len(matching_results)}")
        
        # 신규 문구 생성
        generated_results = generator.generate_new_messages(parsed_input)
        print(f"✨ 생성 결과 수: {len(generated_results)}")
        
        # 응답 데이터 구성
        response = {
            'success': True,
            'parsed_input': parsed_input,
            'matching': matching_results,
            'generated': generated_results
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_message():
    """메시지 분석 API"""
    global generator
    
    try:
        data = request.json
        message = data.get('message', '')
        
        if generator is None:
            generator = MessageAIGenerator("/mnt/c/Users/USER/Documents/notification/202507_.csv")
        
        # 메시지 특성 분석
        features = generator.extract_message_features(message)
        
        # 성과 예측
        mock_input = {'keywords': features['keywords'], 'tone': features['tone']}
        performance = generator.predict_performance(message, mock_input)
        
        response = {
            'success': True,
            'message': message,
            'features': features,
            'performance': performance
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 AI 문구 생성기 웹 서비스 시작!")
    print("📍 URL: http://localhost:5000")
    print("🌐 브라우저에서 접속하세요!")
    
    # Flask 앱 실행
    app.run(debug=True, host='0.0.0.0', port=5000)