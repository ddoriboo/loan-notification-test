#!/usr/bin/env python3
"""
Ultimate AI 문구 생성기 통합 웹 서버
- 진짜 LLM 연동
- 타이밍 최적화
- 성과 비교 분석
"""

import http.server
import socketserver
import json
import urllib.parse
import os
from real_llm_generator import RealLLMGenerator
from enhanced_timing_analyzer import EnhancedTimingAnalyzer

class UltimateHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Use current directory instead of hardcoded path
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/ultimate_ai_message_generator_v2.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/generate':
            self.handle_generate_api()
        elif self.path == '/api/timing':
            self.handle_timing_api()
        elif self.path == '/api/compare':
            self.handle_compare_api()
        elif self.path == '/api/dashboard':
            self.handle_dashboard_api()
        else:
            self.send_error(404)
    
    def handle_generate_api(self):
        """문구 생성 API"""
        try:
            # 요청 데이터 읽기
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # 생성기 초기화 (첫 요청 시)
            if not hasattr(self.server, 'llm_generator'):
                print("🚀 Ultimate AI 생성기 초기화 중...")
                self.server.llm_generator = RealLLMGenerator(
                    "202507_.csv"
                )
                print("✅ 초기화 완료!")
            
            generator = self.server.llm_generator
            
            # 사용자 요청 구성
            user_request = {
                'description': data.get('description', ''),
                'service': data.get('service', ''),
                'tone': data.get('tone', 'promotional'),
                'keywords': data.get('keywords', []),
                'target_audience': data.get('target', '고객')
            }
            
            print(f"📝 생성 요청: {user_request}")
            
            # LLM 생성
            llm_result = generator.generate_with_llm(user_request)
            
            # 기존 메시지 매칭
            existing_matches = generator.get_relevant_high_performance_messages(user_request)
            
            # 성과 비교
            comparison = generator.compare_with_existing(user_request)
            
            # 응답 구성
            response = {
                'success': True,
                'timing': llm_result['optimal_timing'],
                'llm_generated': llm_result['generated_messages'],
                'existing_matched': [
                    {
                        'message': msg['발송 문구'],
                        'actual_rate': msg['클릭율'],
                        'service': msg['서비스명'],
                        'match_score': msg.get('relevance_score', 0) * 10,  # 0-100 스케일로 변환
                        'reasons': ['키워드 매칭', '톤앤매너 일치', '고성과 메시지']
                    }
                    for msg in existing_matches[:3]
                ],
                'comparison': {
                    'llm_average': sum(msg['predicted_rate'] for msg in llm_result['generated_messages']) / len(llm_result['generated_messages']),
                    'existing_average': sum(msg['클릭율'] for msg in existing_matches[:3]) / len(existing_matches[:3]) if existing_matches else 0,
                    'winner': 'existing' if existing_matches else 'llm',
                    'advantage': 2.5,  # 임시값
                    'insights': [
                        'LLM은 창의성과 개인화에서 우수',
                        '기존 메시지는 실제 검증된 성과',
                        '하이브리드 접근이 최적'
                    ]
                },
                'data_insights': llm_result['data_insights']
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
            print(f"❌ 생성 API 오류: {str(e)}")
            self.send_error_response(str(e))
    
    def handle_timing_api(self):
        """타이밍 분석 API"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # 타이밍 분석기 초기화
            if not hasattr(self.server, 'timing_analyzer'):
                self.server.timing_analyzer = EnhancedTimingAnalyzer(
                    "202507_.csv"
                )
            
            analyzer = self.server.timing_analyzer
            
            # 서비스별 최적 타이밍 분석
            service = data.get('service', '전체')
            recommendations = analyzer.get_optimal_timing_recommendation(target_service=service)
            
            response = {
                'success': True,
                'timing_analysis': recommendations,
                'detailed_patterns': {
                    'monthly': {'월초': 8.96, '월중': 7.72, '월말': 8.71},
                    'weekday': {'월': 7.52, '화': 8.82, '수': 8.88, '목': 8.30, '금': 8.78},
                    'payday': {'급여전': 8.96, '급여일': 8.45, '급여후': 9.41}
                }
            }
            
            self.send_json_response(response)
            
        except Exception as e:
            print(f"❌ 타이밍 API 오류: {str(e)}")
            self.send_error_response(str(e))
    
    def handle_compare_api(self):
        """성과 비교 API"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # 비교할 메시지들
            llm_messages = data.get('llm_messages', [])
            existing_messages = data.get('existing_messages', [])
            
            # 성과 비교 분석
            comparison_result = self.analyze_performance_comparison(llm_messages, existing_messages)
            
            response = {
                'success': True,
                'comparison': comparison_result
            }
            
            self.send_json_response(response)
            
        except Exception as e:
            print(f"❌ 비교 API 오류: {str(e)}")
            self.send_error_response(str(e))
    
    def analyze_performance_comparison(self, llm_messages, existing_messages):
        """성과 비교 분석"""
        llm_avg = sum(msg.get('predicted_rate', 0) for msg in llm_messages) / len(llm_messages) if llm_messages else 0
        existing_avg = sum(msg.get('actual_rate', 0) for msg in existing_messages) / len(existing_messages) if existing_messages else 0
        
        winner = 'existing' if existing_avg > llm_avg else 'llm'
        advantage = abs(existing_avg - llm_avg)
        
        insights = []
        if winner == 'existing':
            insights.extend([
                '기존 메시지는 실제 시장에서 검증된 성과',
                '실제 고객 반응 데이터를 기반으로 한 신뢰성',
                '즉시 적용 가능한 검증된 패턴'
            ])
        else:
            insights.extend([
                'LLM 생성 메시지는 창의성과 개인화에서 우수',
                '최신 트렌드와 사용자 요구사항 반영',
                '무한한 변형 가능성'
            ])
        
        # 공통 인사이트 추가
        insights.append('하이브리드 접근(기존 패턴 + LLM 창의성)이 최적')
        
        return {
            'llm_average': round(llm_avg, 1),
            'existing_average': round(existing_avg, 1),
            'winner': winner,
            'advantage': round(advantage, 1),
            'insights': insights,
            'recommendation': '기존 고성과 패턴을 베이스로 LLM의 창의성을 결합하는 것이 최적'
        }
    
    def handle_dashboard_api(self):
        """대시보드 데이터 API"""
        try:
            # 생성기 초기화 확인
            if not hasattr(self.server, 'llm_generator'):
                print("🚀 Ultimate AI 생성기 초기화 중...")
                self.server.llm_generator = RealLLMGenerator(
                    "202507_.csv"
                )
                print("✅ 초기화 완료!")
            
            generator = self.server.llm_generator
            
            # 대시보드 데이터 가져오기
            dashboard_data = generator.get_dashboard_data()
            
            # 성공 응답
            response = {
                'success': True,
                'data': dashboard_data
            }
            
            self.send_json_response(response)
            
        except Exception as e:
            self.send_error_response(str(e))
    
    def send_json_response(self, data):
        """JSON 응답 전송"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def send_error_response(self, error_message):
        """에러 응답 전송"""
        error_response = {
            'success': False,
            'error': error_message
        }
        
        self.send_response(500)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """CORS preflight 요청 처리"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_ultimate_server(port=None):
    """Ultimate 서버 실행"""
    # Railway sets PORT environment variable
    if port is None:
        port = int(os.environ.get('PORT', '8080'))
    
    # Get host from environment or use default
    host = os.environ.get('SERVER_HOST', '0.0.0.0')
    
    print("🚀 Ultimate AI 문구 생성기 서버 시작!")
    print("="*60)
    print("🎯 통합 기능:")
    print("  • 진짜 LLM 기반 문구 생성")
    print("  • 18개월 실제 데이터 학습")
    print("  • 타이밍 최적화 (월초+수요일)")
    print("  • 성과 비교 분석")
    print("  • 실시간 생성 근거 설명")
    print("="*60)
    print(f"📍 Server: {host}:{port}")
    print("🌐 브라우저에서 접속하세요!")
    print("🔄 Ctrl+C로 종료")
    print("="*60)
    
    with socketserver.TCPServer((host, port), UltimateHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Ultimate AI 서버가 종료되었습니다.")
            httpd.server_close()

if __name__ == "__main__":
    # 서버 시작
    run_ultimate_server()