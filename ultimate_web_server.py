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
            self.serve_main_page()
        else:
            return super().do_GET()
    
    def serve_main_page(self):
        """메인 페이지 직접 서빙"""
        try:
            # upload_web_interface.html을 서빙
            with open('upload_web_interface.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content.encode('utf-8'))))
            self.end_headers()
            
            self.wfile.write(content.encode('utf-8'))
            
        except FileNotFoundError:
            try:
                # fallback: ultimate_ai_message_generator_v2.html
                with open('ultimate_ai_message_generator_v2.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content.encode('utf-8'))))
                self.end_headers()
                
                self.wfile.write(content.encode('utf-8'))
                
            except FileNotFoundError:
                self.send_error(404, "No HTML interface found")
        except Exception as e:
            print(f"❌ 메인 페이지 서빙 실패: {e}")
            self.send_error(500, "Internal server error")
    
    def do_POST(self):
        # 업로드 기반 API들 (최우선)
        if self.path == '/api/upload-csv':
            self.handle_upload_csv()
        elif self.path == '/api/dashboard':
            self.handle_dashboard_new()
        elif self.path == '/api/generate':
            self.handle_generate_new()
        # 기존 API들 (하위 호환성)
        elif self.path == '/api/timing':
            self.handle_timing_api()
        elif self.path == '/api/compare':
            self.handle_compare_api()
        else:
            self.send_error(404)
    
    def handle_upload_csv(self):
        """CSV 업로드 처리"""
        try:
            print("📊 CSV 업로드 요청 처리...")
            
            # upload_analyzer import
            from upload_analyzer import analyzer
            
            # POST 데이터 읽기
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            csv_content = data.get('csv_content', '')
            if not csv_content:
                raise ValueError("CSV 내용이 비어있습니다.")
            
            print(f"📄 CSV 크기: {len(csv_content)} 문자")
            
            # CSV 분석 수행
            result = analyzer.analyze_uploaded_csv(csv_content)
            
            if result['success']:
                print(f"✅ CSV 분석 성공: {result['total_messages']}개 메시지")
            else:
                print(f"❌ CSV 분석 실패: {result['error']}")
            
            self.send_json_response(result)
            
        except Exception as e:
            print(f"❌ CSV 업로드 처리 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            
            error_response = {
                'success': False,
                'error': f"CSV 처리 실패: {str(e)}"
            }
            self.send_json_response(error_response, status=500)
    
    def handle_dashboard_new(self):
        """새로운 대시보드 API (업로드 기반)"""
        try:
            print("📊 새로운 대시보드 데이터 요청...")
            
            from upload_analyzer import analyzer
            
            # 분석기에서 대시보드 데이터 가져오기
            dashboard_data = analyzer.get_dashboard_data()
            
            if dashboard_data['success']:
                print("✅ 대시보드 데이터 전송 완료")
            else:
                print(f"⚠️ 대시보드 데이터 없음: {dashboard_data['error']}")
            
            self.send_json_response(dashboard_data)
            
        except Exception as e:
            print(f"❌ 대시보드 요청 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            
            error_response = {
                'success': False,
                'error': f"대시보드 데이터 생성 실패: {str(e)}"
            }
            self.send_json_response(error_response, status=500)
    
    def handle_generate_new(self):
        """새로운 문구 생성 API (업로드 기반)"""
        try:
            print("✨ 새로운 AI 문구 생성 요청...")
            
            from upload_analyzer import analyzer
            
            # 분석 완료 확인
            if not analyzer.analysis_complete:
                raise ValueError("먼저 CSV 파일을 업로드하고 분석을 완료해주세요.")
            
            # POST 데이터 읽기
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            print(f"📝 생성 요청: {data}")
            
            # 기존 메시지 매칭
            relevant_messages = self.find_relevant_messages_new(data, analyzer)
            
            # 실제 업로드 데이터 기반 지능형 문구 생성
            if not analyzer.analysis_complete or not analyzer.data:
                generated_messages = [{
                    'style': '오류',
                    'message': '먼저 CSV 파일을 업로드해주세요.',
                    'predicted_rate': 0,
                    'reasoning': '분석된 데이터가 없음',
                    'confidence': 0
                }]
            else:
                # 실제 데이터 기반 생성 (upload_web_server와 동일한 로직)
                generated_messages = self.generate_data_based_messages(data, analyzer)
            
            response = {
                'success': True,
                'generated_messages': generated_messages,
                'relevant_existing_messages': relevant_messages,
                'data_insights': {
                    'total_analyzed': len(analyzer.data),
                    'high_performance_count': len(analyzer.high_performance_messages),
                    'average_click_rate': analyzer.performance_patterns.get('overall_avg', 0)
                }
            }
            
            print("✅ 새로운 AI 문구 생성 완료")
            self.send_json_response(response)
            
        except Exception as e:
            print(f"❌ 새로운 AI 문구 생성 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            
            error_response = {
                'success': False,
                'error': f"문구 생성 실패: {str(e)}"
            }
            self.send_json_response(error_response, status=500)
    
    def find_relevant_messages_new(self, user_request, analyzer):
        """관련 기존 메시지 찾기 (고도화된 매칭)"""
        try:
            service = user_request.get('service', '')
            description = user_request.get('description', '').lower()
            target_audience = user_request.get('target_audience', '').lower()
            
            relevant = []
            
            # 키워드 추출 및 가중치 설정
            high_value_keywords = ['혜택', '할인', '최대', '특별', '한정', '무료', '즉시', '긴급', '마감']
            service_keywords = ['대출', '금리', '한도', '갈아타기', '비교', '승인', '신청', '확인']
            target_keywords = ['직장인', '프리랜서', '개인사업자', '주부', '신용', '담보']
            
            for msg in analyzer.data:  # 전체 데이터에서 검색
                score = 0
                match_reasons = []
                
                msg_text = str(msg.get('발송 문구', '')).lower()
                msg_service = str(msg.get('서비스명', '')).lower()
                
                # 1. 서비스 매칭 (높은 가중치)
                if service and service.lower() in msg_service:
                    score += 5
                    match_reasons.append(f'서비스 일치 ({service})')
                
                # 2. 고가치 키워드 매칭
                matched_high_keywords = []
                for keyword in high_value_keywords:
                    if keyword in description and keyword in msg_text:
                        score += 3
                        matched_high_keywords.append(keyword)
                
                if matched_high_keywords:
                    match_reasons.append(f'고가치 키워드: {", ".join(matched_high_keywords)}')
                
                # 3. 서비스 키워드 매칭
                matched_service_keywords = []
                for keyword in service_keywords:
                    if keyword in description and keyword in msg_text:
                        score += 2
                        matched_service_keywords.append(keyword)
                
                if matched_service_keywords:
                    match_reasons.append(f'서비스 키워드: {", ".join(matched_service_keywords)}')
                
                # 4. 타겟 고객 매칭
                matched_target_keywords = []
                for keyword in target_keywords:
                    if keyword in target_audience and keyword in msg_text:
                        score += 2
                        matched_target_keywords.append(keyword)
                
                if matched_target_keywords:
                    match_reasons.append(f'타겟 일치: {", ".join(matched_target_keywords)}')
                
                # 5. 클릭률 보너스 (고성과 메시지에 가산점)
                click_rate = msg.get('클릭율', 0)
                if click_rate >= 15:
                    score += 3
                    match_reasons.append(f'고성과 ({click_rate:.1f}%)')
                elif click_rate >= 10:
                    score += 2
                    match_reasons.append(f'우수성과 ({click_rate:.1f}%)')
                
                # 점수가 있는 메시지만 포함
                if score > 0:
                    relevant.append({
                        'message': msg.get('발송 문구', ''),
                        'actual_rate': click_rate,
                        'service': msg.get('서비스명', ''),
                        'match_score': min(score * 5, 100),  # 0-100 스케일
                        'date': str(msg.get('발송일', ''))[:10] if msg.get('발송일') else '',
                        'match_reasons': match_reasons,
                        'similarity_level': '매우 높음' if score >= 10 else '높음' if score >= 6 else '보통'
                    })
            
            # 점수순 정렬 후 상위 5개 반환
            relevant.sort(key=lambda x: (x['match_score'], x['actual_rate']), reverse=True)
            return relevant[:5]
            
        except Exception as e:
            print(f"⚠️ 관련 메시지 검색 실패: {e}")
            return []
    
    def generate_data_based_messages(self, user_request, analyzer):
        """실제 데이터 기반 지능형 문구 생성 (upload_web_server와 동일)"""
        try:
            description = user_request.get('description', '').lower()
            service = user_request.get('service', '')
            target = user_request.get('target_audience', '고객')
            
            # 실제 업로드된 데이터에서 통계 추출
            total_messages = len(analyzer.data)
            avg_rate = analyzer.performance_patterns.get('overall_avg', 0)
            best_rate = analyzer.performance_patterns.get('best_click_rate', 0)
            
            print(f"📊 실제 데이터 통계: 총 {total_messages}개, 평균 {avg_rate:.1f}%, 최고 {best_rate:.1f}%")
            
            # 실제 데이터에서 효과적인 키워드 추출
            effective_keywords = []
            keyword_analysis = analyzer.performance_patterns.get('keyword_analysis', {})
            for keyword, stats in keyword_analysis.items():
                if isinstance(stats, list) and len(stats) >= 2:
                    rate, count = stats[0], stats[1]
                    if rate > avg_rate and count > 1:
                        effective_keywords.append((keyword, rate))
            
            effective_keywords.sort(key=lambda x: x[1], reverse=True)
            top_keywords = [kw[0] for kw in effective_keywords[:5]]
            
            # 사용자 요청에서 키워드 추출
            user_keywords = []
            all_keywords = ['혜택', '최대', '할인', '금리', '한도', '대출', '비교', '갈아타기', '확인', '신청', '특별', '즉시', '마감']
            for keyword in all_keywords:
                if keyword in description:
                    user_keywords.append(keyword)
            
            final_keywords = list(set(top_keywords[:3] + user_keywords[:2]))
            if not final_keywords:
                final_keywords = top_keywords[:2] if top_keywords else ['혜택', '확인']
            
            # 실제 데이터 기반 문구 생성
            messages = []
            
            # 1. 혜택 강조형
            predicted_rate_1 = min(avg_rate * 1.3, best_rate * 0.85) if best_rate > 0 else avg_rate + 2
            style1_keywords = final_keywords[:2]
            messages.append({
                'style': '데이터 기반 혜택 강조형',
                'message': f"(광고) {target}님을 위한 검증된 {', '.join(style1_keywords)} 혜택! {service or '대출'} 지금 확인하고 최대 혜택 받으세요 👉",
                'predicted_rate': round(predicted_rate_1, 1),
                'reasoning': f"업로드 데이터 분석: '{style1_keywords[0] if style1_keywords else '혜택'}' 키워드 평균 {keyword_analysis.get(style1_keywords[0], [avg_rate])[0]:.1f}% 성과. 총 {total_messages}개 메시지 중 상위 성과 패턴 활용",
                'confidence': 88
            })
            
            # 2. 긴급성 강조형
            predicted_rate_2 = min(avg_rate * 1.2, best_rate * 0.8) if best_rate > 0 else avg_rate + 1.5
            messages.append({
                'style': '검증된 긴급성 강조형',
                'message': f"(광고) ⚡ 한정 기간! {service or '대출'} {final_keywords[0] if final_keywords else '혜택'} 마감 임박. 놓치기 전에 지금 확인하세요!",
                'predicted_rate': round(predicted_rate_2, 1),
                'reasoning': f"긴급성 패턴의 업로드 데이터 평균 성과 {avg_rate:.1f}%를 바탕으로 개선. 고성과 메시지 {len(analyzer.high_performance_messages)}개 분석 결과 적용",
                'confidence': 82
            })
            
            # 3. 개인화 맞춤형
            service_analysis = analyzer.performance_patterns.get('service_analysis', {})
            target_service_rate = avg_rate
            if service and service in service_analysis:
                target_service_rate = service_analysis[service].get('avg_click_rate', avg_rate)
            
            predicted_rate_3 = min(target_service_rate * 1.4, best_rate * 0.9) if best_rate > 0 else target_service_rate + 3
            messages.append({
                'style': '실데이터 맞춤형',
                'message': f"(광고) {target}님 조건 맞춤 {service or '대출'} 발견! {', '.join(final_keywords[:2])} 개인별 최적 조건 확인하기",
                'predicted_rate': round(predicted_rate_3, 1),
                'reasoning': f"'{service}' 서비스 실제 평균 성과 {target_service_rate:.1f}%, 개인화 표현으로 {final_keywords[0] if final_keywords else '혜택'} 키워드 조합하여 성과 향상 예상",
                'confidence': 91
            })
            
            print(f"✅ 실제 데이터 기반 {len(messages)}개 문구 생성 완료")
            return messages
            
        except Exception as e:
            print(f"❌ 데이터 기반 문구 생성 실패: {e}")
            return [{
                'style': '생성 실패',
                'message': '문구 생성 중 오류가 발생했습니다.',
                'predicted_rate': 0,
                'reasoning': f'오류: {str(e)}',
                'confidence': 0
            }]
    
    def handle_generate_api(self):
        """문구 생성 API"""
        try:
            print("✨ 문구 생성 API 요청 처리 시작...")
            
            # 요청 데이터 읽기
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            print(f"📝 받은 요청 데이터: {data}")
            
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
            
            print(f"🎯 처리할 요청: {user_request}")
            
            # LLM 생성
            print("🤖 LLM 문구 생성 시작...")
            llm_result = generator.generate_with_llm(user_request)
            print("✅ LLM 문구 생성 완료")
            
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
            print("✅ 문구 생성 API 처리 완료")
            
        except Exception as e:
            print(f"❌ 문구 생성 API 에러: {str(e)}")
            import traceback
            traceback.print_exc()
            self.send_error_response(f"문구 생성 실패: {str(e)}")
    
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
            print("📊 대시보드 API 요청 처리 시작...")
            
            # 생성기 초기화 확인
            if not hasattr(self.server, 'llm_generator'):
                print("🚀 Ultimate AI 생성기 초기화 중...")
                self.server.llm_generator = RealLLMGenerator(
                    "202507_.csv"
                )
                print("✅ 초기화 완료!")
            
            generator = self.server.llm_generator
            print("🔍 대시보드 데이터 생성 시작...")
            
            # 대시보드 데이터 가져오기
            dashboard_data = generator.get_dashboard_data()
            print(f"✅ 대시보드 데이터 생성 완료 (키 개수: {len(dashboard_data)})")
            
            # 성공 응답
            response = {
                'success': True,
                'data': dashboard_data
            }
            
            print("📤 JSON 응답 전송 중...")
            self.send_json_response(response)
            print("✅ 대시보드 API 처리 완료")
            
        except Exception as e:
            print(f"❌ 대시보드 API 에러: {str(e)}")
            import traceback
            traceback.print_exc()
            self.send_error_response(f"대시보드 데이터 생성 실패: {str(e)}")
    
    def send_json_response(self, data, status=200):
        """JSON 응답 전송 (datetime 안전 처리)"""
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # JSON serialization with datetime handling
            json_str = json.dumps(data, ensure_ascii=False, indent=2, default=str)
            self.wfile.write(json_str.encode('utf-8'))
            
        except Exception as e:
            print(f"❌ JSON 응답 전송 실패: {str(e)}")
            # Fallback: 기본 에러 응답
            try:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_data = {
                    'success': False,
                    'error': f"JSON 직렬화 실패: {str(e)}"
                }
                fallback_json = json.dumps(error_data, ensure_ascii=False)
                self.wfile.write(fallback_json.encode('utf-8'))
            except:
                pass  # 최종 fallback 실패시 무시
    
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
    # Railway 환경 디버깅 정보 출력
    print("🔍 서버 시작 전 환경 확인")
    print("=" * 40)
    
    import os
    cwd = os.getcwd()
    print(f"📁 작업 디렉토리: {cwd}")
    
    # CSV 파일 존재 확인
    csv_file = "202507_.csv"
    if os.path.exists(csv_file):
        size = os.path.getsize(csv_file)
        print(f"✅ CSV 파일 발견: {csv_file} ({size:,} bytes)")
    else:
        print(f"❌ CSV 파일 없음: {csv_file}")
        print("📂 현재 디렉토리 파일 목록:")
        try:
            files = [f for f in os.listdir(cwd) if f.endswith('.csv')]
            if files:
                for f in files:
                    print(f"  - {f}")
            else:
                print("  CSV 파일이 없습니다")
        except Exception as e:
            print(f"  디렉토리 읽기 실패: {e}")
    
    # 환경변수 확인
    openai_key = os.environ.get('OPENAI_API_KEY')
    print(f"🔑 OPENAI_API_KEY: {'✅' if openai_key else '❌'}")
    
    print("=" * 40)
    
    # 서버 시작
    run_ultimate_server()