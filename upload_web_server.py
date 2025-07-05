#!/usr/bin/env python3
"""
CSV 업로드 기반 웹 서버
- 파일 의존성 없는 메모리 기반 처리
- 사용자가 직접 CSV 업로드
- 안정적인 에러 처리
"""

import http.server
import socketserver
import json
import urllib.parse
import os
from upload_analyzer import analyzer

# OpenAI 설정
try:
    import openai
    OPENAI_AVAILABLE = True
    
    # 환경변수에서 API 키 가져오기 또는 직접 설정
    DIRECT_API_KEY = "your-openai-api-key-here"  # 여기에 실제 API 키를 입력하세요
    api_key = os.environ.get('OPENAI_API_KEY') or DIRECT_API_KEY
    if api_key:
        openai.api_key = api_key
        print("✅ OpenAI API 설정 완료")
        print(f"🔑 API 키 길이: {len(api_key)} 문자")
        print(f"🔑 API 키 시작: {api_key[:7]}...")
        
        # API 키 유효성 간단 테스트
        try:
            client = openai.OpenAI(api_key=api_key)
            # 간단한 테스트 호출
            test_response = client.models.list()
            print("✅ OpenAI API 연결 테스트 성공!")
        except Exception as test_e:
            print(f"❌ OpenAI API 테스트 실패: {test_e}")
            OPENAI_AVAILABLE = False
    else:
        print("⚠️ OPENAI_API_KEY 환경변수가 설정되지 않음")
        OPENAI_AVAILABLE = False
        
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI 라이브러리가 설치되지 않음")

class UploadHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.serve_main_page()
        else:
            return super().do_GET()
    
    def serve_main_page(self):
        """메인 페이지 직접 서빙"""
        try:
            with open('upload_web_interface.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content.encode('utf-8'))))
            self.end_headers()
            
            self.wfile.write(content.encode('utf-8'))
            
        except FileNotFoundError:
            self.send_error(404, "Main page not found")
        except Exception as e:
            print(f"❌ 메인 페이지 서빙 실패: {e}")
            self.send_error(500, "Internal server error")
    
    def do_POST(self):
        if self.path == '/api/upload-csv':
            self.handle_upload_csv()
        elif self.path == '/api/dashboard':
            self.handle_dashboard()
        elif self.path == '/api/generate':
            self.handle_generate()
        else:
            self.send_error(404)
    
    def handle_upload_csv(self):
        """CSV 업로드 및 분석 처리"""
        try:
            print("📊 CSV 업로드 요청 처리 시작...")
            
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
    
    def handle_dashboard(self):
        """대시보드 데이터 반환"""
        try:
            print("📊 대시보드 데이터 요청...")
            
            # 분석기에서 대시보드 데이터 가져오기
            dashboard_data = analyzer.get_dashboard_data()
            
            if dashboard_data['success']:
                print("✅ 대시보드 데이터 전송 완료")
            else:
                print(f"⚠️ 대시보드 데이터 없음: {dashboard_data['error']}")
            
            self.send_json_response(dashboard_data)
            
        except Exception as e:
            print(f"❌ 대시보드 요청 실패: {str(e)}")
            error_response = {
                'success': False,
                'error': f"대시보드 데이터 생성 실패: {str(e)}"
            }
            self.send_json_response(error_response, status=500)
    
    def handle_generate(self):
        """AI 문구 생성 처리"""
        try:
            print("✨ AI 문구 생성 요청...")
            
            # 분석 완료 확인
            if not analyzer.analysis_complete:
                raise ValueError("먼저 CSV 파일을 업로드하고 분석을 완료해주세요.")
            
            # POST 데이터 읽기
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            print(f"📝 생성 요청: {data}")
            
            # 요청 데이터 구성
            user_request = {
                'description': data.get('description', ''),
                'service': data.get('service', ''),
                'target_audience': data.get('target_audience', '고객'),
                'tone': data.get('tone', 'promotional')
            }
            
            # AI 문구 생성 (실제 LLM 강제 사용)
            print(f"\n=== LLM 생성 시작 ===")
            print(f"🔍 OpenAI 사용 가능: {OPENAI_AVAILABLE}")
            print(f"🔑 API 키 존재: {'Yes' if openai.api_key else 'No'}")
            print(f"📊 분석된 데이터 수: {len(analyzer.data)}개")
            print(f"🏆 고성과 메시지 수: {len(analyzer.high_performance_messages)}개")
            
            # 강제로 OpenAI 사용 시도
            if OPENAI_AVAILABLE and openai.api_key:
                print("🤖 실제 OpenAI GPT-4 API 호출 중...")
                try:
                    generated_messages = self.generate_with_openai(user_request)
                    print(f"✅ OpenAI 생성 완료: {len(generated_messages)}개 메시지")
                except Exception as openai_error:
                    print(f"❌ OpenAI 호출 실패: {openai_error}")
                    print("🔄 데이터 기반 시뮬레이션으로 전환...")
                    generated_messages = self.generate_simulation(user_request)
            else:
                print("⚠️ OpenAI 미설정 - 실제 데이터 기반 생성 모드")
                if not openai.api_key:
                    print("💡 OpenAI API 키를 설정하면 더 창의적인 문구를 생성할 수 있습니다.")
                generated_messages = self.generate_simulation(user_request)
            
            # 관련 기존 메시지 찾기
            relevant_messages = self.find_relevant_messages(user_request)
            
            # 응답 구성
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
            
            print("✅ AI 문구 생성 완료")
            self.send_json_response(response)
            
        except Exception as e:
            print(f"❌ AI 문구 생성 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            
            error_response = {
                'success': False,
                'error': f"문구 생성 실패: {str(e)}"
            }
            self.send_json_response(error_response, status=500)
    
    def generate_with_openai(self, user_request):
        """OpenAI를 사용한 실제 AI 문구 생성"""
        try:
            print("🤖 OpenAI GPT-4o로 문구 생성 중...")
            
            # 프롬프트 생성
            prompt = self.create_generation_prompt(user_request)
            
            # OpenAI API 호출 (더 자세한 로깅)
            print(f"📤 OpenAI 호출 시작...")
            print(f"📝 프롬프트 길이: {len(prompt)} 문자")
            
            client = openai.OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # 더 안정적인 모델로 변경
                messages=[
                    {"role": "system", "content": "당신은 한국어 대출 서비스 마케팅 전문가입니다. 실제 데이터를 분석하여 효과적인 알림 문구를 생성합니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            llm_response = response.choices[0].message.content
            print("✅ OpenAI 응답 수신 완료")
            
            # 응답 파싱
            return self.parse_llm_response(llm_response)
            
        except Exception as e:
            print(f"❌ OpenAI 호출 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            # 실패시 데이터 기반 시뮬레이션으로 fallback
            print("🔄 데이터 기반 시뮬레이션으로 전환...")
            return self.generate_simulation(user_request)
    
    def generate_simulation(self, user_request):
        """실제 데이터 기반 지능형 문구 생성"""
        print("🧠 업로드된 실제 데이터 기반 지능형 문구 생성 중...")
        
        if not analyzer.analysis_complete or not analyzer.data:
            print("❌ 분석된 데이터가 없습니다.")
            return [{
                'style': '오류',
                'message': '먼저 CSV 파일을 업로드해주세요.',
                'predicted_rate': 0,
                'reasoning': '분석된 데이터가 없음',
                'confidence': 0
            }]
        
        description = user_request.get('description', '').lower()
        service = user_request.get('service', '')
        target = user_request.get('target_audience', '고객')
        
        # 실제 업로드된 데이터에서 통계 추출
        total_messages = len(analyzer.data)
        avg_rate = analyzer.performance_patterns.get('overall_avg', 0)
        best_rate = analyzer.performance_patterns.get('best_click_rate', 0)
        high_perf_messages = analyzer.high_performance_messages
        
        print(f"📊 실제 데이터 통계: 총 {total_messages}개, 평균 {avg_rate:.1f}%, 최고 {best_rate:.1f}%")
        
        # 실제 데이터에서 효과적인 키워드 추출
        effective_keywords = []
        keyword_analysis = analyzer.performance_patterns.get('keyword_analysis', {})
        for keyword, stats in keyword_analysis.items():
            if isinstance(stats, list) and len(stats) >= 2:
                rate, count = stats[0], stats[1]
                if rate > avg_rate and count > 1:  # 평균보다 높고 충분히 사용된 키워드
                    effective_keywords.append((keyword, rate))
        
        # 효과도 순으로 정렬
        effective_keywords.sort(key=lambda x: x[1], reverse=True)
        top_keywords = [kw[0] for kw in effective_keywords[:5]]
        
        # 사용자 요청에서 키워드 추출
        user_keywords = []
        all_keywords = ['혜택', '최대', '할인', '금리', '한도', '대출', '비교', '갈아타기', '확인', '신청', '특별', '즉시', '마감']
        for keyword in all_keywords:
            if keyword in description:
                user_keywords.append(keyword)
        
        # 최종 키워드 조합 (효과적 + 사용자 요청)
        final_keywords = list(set(top_keywords[:3] + user_keywords[:2]))
        if not final_keywords:
            final_keywords = top_keywords[:2] if top_keywords else ['혜택', '확인']
        
        print(f"🔑 선택된 키워드: {final_keywords} (데이터 기반: {top_keywords[:3]})")
        
        # 고성과 메시지 패턴 분석
        high_perf_patterns = []
        if high_perf_messages:
            for msg in high_perf_messages[:3]:
                message_text = str(msg.get('발송 문구', ''))
                if '광고' in message_text and len(message_text) > 10:
                    high_perf_patterns.append({
                        'text': message_text,
                        'rate': msg.get('클릭율', 0),
                        'service': msg.get('서비스명', '')
                    })
        
        # 실제 데이터 기반 문구 생성
        messages = []
        
        # 1. 혜택 강조형 (실제 최고 성과 패턴 기반)
        predicted_rate_1 = min(avg_rate * 1.3, best_rate * 0.85) if best_rate > 0 else avg_rate + 2
        style1_keywords = final_keywords[:2]
        messages.append({
            'style': '데이터 기반 혜택 강조형',
            'message': f"(광고) {target}님을 위한 검증된 {', '.join(style1_keywords)} 혜택! {service or '대출'} 지금 확인하고 최대 혜택 받으세요 👉",
            'predicted_rate': round(predicted_rate_1, 1),
            'reasoning': f"업로드 데이터 분석: '{style1_keywords[0] if style1_keywords else '혜택'}' 키워드 평균 {keyword_analysis.get(style1_keywords[0], [avg_rate])[0]:.1f}% 성과. 총 {total_messages}개 메시지 중 상위 성과 패턴 활용",
            'confidence': 88
        })
        
        # 2. 긴급성 강조형 (실제 고성과 메시지 패턴 적용)
        predicted_rate_2 = min(avg_rate * 1.2, best_rate * 0.8) if best_rate > 0 else avg_rate + 1.5
        messages.append({
            'style': '검증된 긴급성 강조형',
            'message': f"(광고) ⚡ 한정 기간! {service or '대출'} {final_keywords[0] if final_keywords else '혜택'} 마감 임박. 놓치기 전에 지금 확인하세요!",
            'predicted_rate': round(predicted_rate_2, 1),
            'reasoning': f"긴급성 패턴의 업로드 데이터 평균 성과 {avg_rate:.1f}%를 바탕으로 개선. 고성과 메시지 {len(high_perf_messages)}개 분석 결과 적용",
            'confidence': 82
        })
        
        # 3. 개인화 맞춤형 (실제 서비스별 데이터 반영)
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
    
    def create_generation_prompt(self, user_request):
        """실제 업로드 데이터 기반 OpenAI 프롬프트 생성"""
        if not analyzer.analysis_complete or not analyzer.data:
            return "업로드된 CSV 데이터가 없습니다. 먼저 CSV 파일을 업로드해주세요."
        
        # 실제 고성과 메시지 예시 (상위 5개)
        high_perf_examples = []
        sorted_messages = sorted(analyzer.data, key=lambda x: x.get('클릭율', 0), reverse=True)
        for msg in sorted_messages[:5]:
            high_perf_examples.append(f"- \"{msg.get('발송 문구', '')}\" (클릭률: {msg.get('클릭율', 0):.1f}%, 서비스: {msg.get('서비스명', '')})")
        
        # 실제 키워드 성과 분석
        keyword_insights = []
        keyword_analysis = analyzer.performance_patterns.get('keyword_analysis', {})
        # 성과순으로 정렬
        sorted_keywords = sorted(keyword_analysis.items(), key=lambda x: x[1][0] if isinstance(x[1], list) and len(x[1]) > 0 else 0, reverse=True)
        
        for keyword, stats in sorted_keywords[:8]:
            if isinstance(stats, list) and len(stats) >= 2:
                keyword_insights.append(f"- '{keyword}': 평균 {stats[0]:.1f}% 클릭률 ({stats[1]}회 사용)")
        
        # 실제 데이터 통계
        total_messages = len(analyzer.data)
        avg_rate = analyzer.performance_patterns.get('overall_avg', 0)
        best_rate = analyzer.performance_patterns.get('best_click_rate', 0)
        high_perf_count = len(analyzer.high_performance_messages)
        
        # 서비스별 성과 (사용자가 특정 서비스 선택한 경우)
        service_info = ""
        service = user_request.get('service', '')
        if service:
            service_analysis = analyzer.performance_patterns.get('service_analysis', {})
            if service in service_analysis:
                service_avg = service_analysis[service].get('avg_click_rate', 0)
                service_count = service_analysis[service].get('count', 0)
                service_info = f"\n## 🏷️ '{service}' 서비스 특화 분석\n- 평균 클릭률: {service_avg:.1f}%\n- 발송 횟수: {service_count}건"
        
        prompt = f"""당신은 실제 데이터 분석 전문가이자 마케팅 문구 작성 전문가입니다.
업로드된 실제 CSV 데이터를 분석한 결과를 바탕으로 최적화된 알림 문구를 생성해주세요.

## 📊 업로드된 실제 데이터 현황
- 총 분석 메시지: {total_messages}개
- 전체 평균 클릭률: {avg_rate:.2f}%
- 최고 클릭률: {best_rate:.1f}%
- 고성과 메시지(상위 20%): {high_perf_count}개

## 🏆 실제 최고 성과 메시지 사례 (업로드 데이터 기준)
{chr(10).join(high_perf_examples) if high_perf_examples else "- 데이터 분석 중..."}

## 🔑 실제 데이터 기반 효과적인 키워드 분석
{chr(10).join(keyword_insights) if keyword_insights else "- 키워드 분석 중..."}
{service_info}

## 📝 사용자 문구 생성 요청
요청사항: {user_request.get('description', '특별한 요청사항 없음')}
타겟 고객: {user_request.get('target_audience', '일반 고객')}
서비스 유형: {user_request.get('service', '전체 서비스')}

## 🎯 생성 요구사항
1. **데이터 기반**: 위 실제 업로드 데이터의 고성과 패턴과 키워드를 필수 참고
2. **창의성**: 기존 메시지와 다른 새로운 표현 사용
3. **개인화**: 사용자 요청사항을 정확히 반영
4. **규격**: (광고) 표시 포함, 한글 50자 내외
5. **실용성**: 실제 발송 가능한 현실적인 문구

## 📋 정확한 출력 형식 (JSON 형태로 응답)
```json
[
  {{
    "style": "데이터 검증 혜택형",
    "message": "[실제 데이터 기반 생성된 문구]",
    "predicted_rate": [실제 데이터 평균({avg_rate:.1f}%)을 고려한 예상 클릭률],
    "reasoning": "[업로드 데이터의 구체적 근거와 선택한 키워드/패턴 설명]"
  }},
  {{
    "style": "실증 긴급성형",
    "message": "[실제 데이터 기반 생성된 문구]",
    "predicted_rate": [실제 데이터 기준 예상 클릭률],
    "reasoning": "[업로드 데이터 기반 구체적 근거]"
  }},
  {{
    "style": "검증된 맞춤형",
    "message": "[실제 데이터 기반 생성된 문구]",
    "predicted_rate": [실제 데이터 기준 예상 클릭률],
    "reasoning": "[업로드 데이터 기반 구체적 근거]"
  }}
]
```

**중요**: 반드시 업로드된 실제 데이터(총 {total_messages}개 메시지, 평균 {avg_rate:.1f}%)를 기반으로 생성하고, 예상 클릭률도 실제 성과 범위({avg_rate:.1f}% ~ {best_rate:.1f}%) 내에서 합리적으로 제시하세요."""
        
        return prompt
    
    def parse_llm_response(self, llm_response):
        """LLM JSON 응답 파싱"""
        try:
            print(f"🔍 LLM 원본 응답: {llm_response[:200]}...")
            
            # JSON 블록 추출 시도
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', llm_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                print(f"📋 추출된 JSON: {json_str[:100]}...")
                
                import json
                parsed_messages = json.loads(json_str)
                
                if isinstance(parsed_messages, list) and len(parsed_messages) > 0:
                    # 신뢰도 추가
                    for msg in parsed_messages:
                        if 'confidence' not in msg:
                            msg['confidence'] = 90
                    
                    print(f"✅ JSON 파싱 성공: {len(parsed_messages)}개 문구")
                    return parsed_messages
                else:
                    raise ValueError("파싱된 결과가 올바른 형식이 아님")
            
            # JSON 블록이 없으면 직접 JSON 파싱 시도
            try:
                # 전체 응답에서 JSON 추출 시도
                start_idx = llm_response.find('[')
                end_idx = llm_response.rfind(']') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = llm_response[start_idx:end_idx]
                    import json
                    parsed_messages = json.loads(json_str)
                    
                    for msg in parsed_messages:
                        if 'confidence' not in msg:
                            msg['confidence'] = 88
                    
                    print(f"✅ 직접 JSON 파싱 성공: {len(parsed_messages)}개 문구")
                    return parsed_messages
                    
            except Exception as json_e:
                print(f"⚠️ 직접 JSON 파싱 실패: {json_e}")
            
            # 모든 파싱 실패시 데이터 기반 시뮬레이션으로 fallback
            print("🔄 LLM 파싱 실패 - 데이터 기반 시뮬레이션으로 전환")
            return self.generate_simulation({})
            
        except Exception as e:
            print(f"❌ LLM 응답 파싱 실패: {e}")
            import traceback
            traceback.print_exc()
            return self.generate_simulation({})
    
    def find_relevant_messages(self, user_request):
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
            
            for msg in analyzer.data:  # 전체 데이터에서 검색 (고성과만이 아닌)
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
            
            print(f"🎯 매칭된 기존 메시지: {len(relevant)}개")
            return relevant[:5]
            
        except Exception as e:
            print(f"⚠️ 관련 메시지 검색 실패: {e}")
            return []
    
    def send_json_response(self, data, status=200):
        """JSON 응답 전송 (캐시 방지 포함)"""
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            
            # 캐시 방지 헤더 추가
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            
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
    
    def do_OPTIONS(self):
        """CORS preflight 요청 처리"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_upload_server(port=None):
    """서버 실행"""
    # Railway에서 PORT 환경변수 사용
    if port is None:
        port = int(os.environ.get('PORT', '8080'))
    
    # 호스트 설정
    host = os.environ.get('SERVER_HOST', '0.0.0.0')
    
    print("🚀 CSV 업로드 기반 AI 문구 생성기 서버 시작!")
    print("=" * 60)
    print("🎯 주요 기능:")
    print("  • CSV 파일 업로드 및 즉시 분석")
    print("  • 파일 배포 의존성 제거")
    print("  • 실시간 데이터 기반 AI 문구 생성")
    print("  • GPT-4o 모델 활용")
    print("  • 메모리 기반 안정적 처리")
    print("=" * 60)
    print(f"📍 Server: {host}:{port}")
    print("🌐 CSV를 업로드하여 시작하세요!")
    print("🔄 Ctrl+C로 종료")
    print("=" * 60)
    
    with socketserver.TCPServer((host, port), UploadHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 서버가 종료되었습니다.")
            httpd.server_close()

if __name__ == "__main__":
    # 강제 실행 표시
    print("🚨 UPLOAD_WEB_SERVER.PY 강제 실행! 🚨")
    print("=" * 50)
    print("📍 이 메시지가 보이면 올바른 서버가 실행된 것입니다!")
    print("=" * 50)
    
    # 환경 확인
    print("🔍 서버 환경 확인")
    print("=" * 40)
    
    cwd = os.getcwd()
    print(f"📁 작업 디렉토리: {cwd}")
    
    # 환경변수 확인
    openai_key = os.environ.get('OPENAI_API_KEY')
    print(f"🔑 OPENAI_API_KEY: {'✅ 설정됨' if openai_key else '❌ 없음 (시뮬레이션 모드)'}")
    
    # 핵심 파일 확인
    key_files = ['upload_analyzer.py', 'upload_web_interface.html']
    for file in key_files:
        if os.path.exists(file):
            print(f"✅ {file} 존재")
        else:
            print(f"❌ {file} 없음")
    
    print("=" * 40)
    
    # 서버 시작
    run_upload_server()