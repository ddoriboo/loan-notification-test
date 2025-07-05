#!/usr/bin/env python3
"""
간단한 HTTP 서버 (Flask 대신)
Python 기본 라이브러리만 사용
"""

import http.server
import socketserver
import json
import urllib.parse
from message_ai_generator import MessageAIGenerator
import os

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/mnt/c/Users/USER/Documents/notification", **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/ai_message_generator_updated.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/generate':
            self.handle_generate_api()
        else:
            self.send_error(404)
    
    def handle_generate_api(self):
        try:
            # 요청 데이터 읽기
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # JSON 파싱
            data = json.loads(post_data.decode('utf-8'))
            
            # MessageAIGenerator 초기화 (첫 요청 시)
            if not hasattr(self.server, 'generator'):
                print("🔄 AI 생성기 초기화 중...")
                self.server.generator = MessageAIGenerator("202507_.csv")
                print("✅ 초기화 완료!")
            
            generator = self.server.generator
            
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
            
            # 기존 문구 매칭
            matching_results = generator.find_matching_messages(parsed_input)
            
            # 신규 문구 생성
            generated_results = generator.generate_new_messages(parsed_input)
            
            # 응답 데이터
            response = {
                'success': True,
                'parsed_input': parsed_input,
                'matching': matching_results,
                'generated': generated_results
            }
            
            # HTTP 응답
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")
            
            error_response = {
                'success': False,
                'error': str(e)
            }
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        # CORS preflight 요청 처리
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8000):
    """서버 실행"""
    with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 AI 문구 생성기 서버 시작!")
        print(f"📍 URL: http://localhost:{port}")
        print(f"🌐 브라우저에서 접속하세요!")
        print(f"🔄 Ctrl+C로 종료")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 서버가 종료되었습니다.")
            httpd.server_close()

if __name__ == "__main__":
    # 작업 디렉토리 변경
    os.chdir("/mnt/c/Users/USER/Documents/notification")
    run_server()