#!/usr/bin/env python3
"""
CSV 업로드 기반 알림 문구 분석기
- 파일 배포 의존성 제거
- 사용자가 직접 CSV 업로드
- 메모리 기반 데이터 처리
"""

import csv
import json
import io
import os
from datetime import datetime
import statistics
import re

class UploadAnalyzer:
    def __init__(self):
        self.data = []
        self.high_performance_messages = []
        self.performance_patterns = {}
        self.analysis_complete = False
        
    def analyze_uploaded_csv(self, csv_content):
        """업로드된 CSV 내용 분석"""
        try:
            print("📊 업로드된 CSV 분석 시작...")
            print(f"📄 CSV 내용 미리보기: {csv_content[:200]}...")
            
            # 데이터 완전 초기화
            self.data = []
            self.high_performance_messages = []
            self.performance_patterns = {}
            self.analysis_complete = False
            
            # CSV 파싱
            csv_file = io.StringIO(csv_content)
            reader = csv.DictReader(csv_file)
            
            print(f"📋 CSV 헤더: {reader.fieldnames}")
            
            # 행별 처리
            for i, row in enumerate(reader):
                try:
                    # 필드명 정규화 (다양한 형식 지원)
                    normalized_row = self.normalize_fields(row)
                    
                    # 데이터 타입 변환
                    processed_row = self.process_row(normalized_row)
                    
                    if processed_row:
                        self.data.append(processed_row)
                            
                except Exception as e:
                    print(f"⚠️ 행 {i+1} 처리 실패: {e}")
                    continue
            
            if not self.data:
                raise Exception("유효한 데이터가 없습니다. CSV 형식을 확인해주세요.")
            
            # 성과 패턴 분석
            self.analyze_patterns()
            
            self.analysis_complete = True
            
            print(f"✅ 분석 완료: {len(self.data)}개 메시지, 고성과 {len(self.high_performance_messages)}개")
            
            return {
                'success': True,
                'total_messages': len(self.data),
                'high_performance_count': len(self.high_performance_messages),
                'summary': self.get_summary()
            }
            
        except Exception as e:
            print(f"❌ CSV 분석 실패: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def normalize_fields(self, row):
        """필드명 정규화 (다양한 CSV 형식 지원)"""
        # 가능한 필드명 매핑
        field_mappings = {
            '클릭율': ['클릭율', '클릭률', 'CTR', 'click_rate', 'clickrate'],
            '발송 문구': ['발송 문구', '문구', 'message', '내용', 'content', '알림내용'],
            '서비스명': ['서비스명', '서비스', 'service', 'service_name', '상품명'],
            '발송일': ['발송일', '발송날짜', 'date', 'send_date', '날짜'],
            '요일': ['요일', 'weekday', 'day'],
            '발송회원수': ['발송회원수', 'send_count', '발송수'],
            '클릭회원수': ['클릭회원수', 'click_count', '클릭수']
        }
        
        normalized = {}
        
        for standard_field, possible_names in field_mappings.items():
            for possible_name in possible_names:
                if possible_name in row:
                    normalized[standard_field] = row[possible_name]
                    break
            
            # 기본값 설정
            if standard_field not in normalized:
                if standard_field == '클릭율':
                    normalized[standard_field] = '0'
                elif standard_field == '발송 문구':
                    normalized[standard_field] = '기본 문구'
                elif standard_field == '서비스명':
                    normalized[standard_field] = '기타'
                else:
                    normalized[standard_field] = ''
        
        return normalized
    
    def process_row(self, row):
        """행 데이터 처리 및 타입 변환 (JSON serializable)"""
        try:
            processed = {}
            
            # 클릭률 변환
            click_rate_str = str(row.get('클릭율', '0')).strip()
            if click_rate_str.replace('.', '').replace('%', '').isdigit():
                click_rate = float(click_rate_str.replace('%', ''))
                processed['클릭율'] = click_rate if click_rate <= 100 else click_rate / 100
            else:
                processed['클릭율'] = 0.0
            
            # 텍스트 필드
            processed['발송 문구'] = str(row.get('발송 문구', '')).strip()
            processed['서비스명'] = str(row.get('서비스명', '')).strip()
            
            # 날짜 처리 (JSON serializable 문자열로 저장)
            date_str = str(row.get('발송일', '')).strip()
            if date_str:
                try:
                    # 다양한 날짜 형식 지원
                    parsed_date = None
                    for date_format in ['%Y-%m-%d', '%Y.%m.%d', '%Y/%m/%d']:
                        try:
                            parsed_date = datetime.strptime(date_str, date_format)
                            break
                        except ValueError:
                            continue
                    
                    if parsed_date:
                        processed['발송일'] = parsed_date.strftime('%Y-%m-%d')  # 문자열로 저장
                        processed['발송일_객체'] = parsed_date  # 내부 계산용 (JSON에서 제외)
                    else:
                        processed['발송일'] = datetime.now().strftime('%Y-%m-%d')
                        processed['발송일_객체'] = datetime.now()
                except:
                    processed['발송일'] = datetime.now().strftime('%Y-%m-%d')
                    processed['발송일_객체'] = datetime.now()
            else:
                processed['발송일'] = datetime.now().strftime('%Y-%m-%d')
                processed['발송일_객체'] = datetime.now()
            
            # 요일 처리
            weekday = str(row.get('요일', '')).strip()
            if not weekday:
                weekday_num = processed['발송일_객체'].weekday()
                weekdays = ['월', '화', '수', '목', '금', '토', '일']
                weekday = weekdays[weekday_num]
            processed['요일'] = weekday
            
            # 숫자 필드들
            processed['발송회원수'] = self.safe_int(row.get('발송회원수', '0'))
            processed['클릭회원수'] = self.safe_int(row.get('클릭회원수', '0'))
            
            return processed
            
        except Exception as e:
            print(f"⚠️ 행 처리 실패: {e}")
            return None
    
    def safe_int(self, value):
        """안전한 정수 변환"""
        try:
            return int(float(str(value).replace(',', '')))
        except:
            return 0
    
    def analyze_patterns(self):
        """성과 패턴 분석"""
        try:
            # 고성과 메시지 기준 동적 계산
            all_rates = [row.get('클릭율', 0) for row in self.data if row.get('클릭율', 0) > 0]
            if all_rates:
                avg_rate = sum(all_rates) / len(all_rates)
                high_performance_threshold = max(avg_rate * 1.2, 8.0)  # 평균의 120% 또는 최소 8%
                print(f"📈 고성과 기준: {high_performance_threshold:.1f}% (평균: {avg_rate:.1f}%)")
                
                # 고성과 메시지 수집 (상위 20% 또는 기준 이상)
                sorted_data = sorted(self.data, key=lambda x: x.get('클릭율', 0), reverse=True)
                top_20_percent = max(len(sorted_data) // 5, 10)  # 상위 20% 또는 최소 10개
                
                self.high_performance_messages = []
                for row in sorted_data[:top_20_percent]:
                    if row.get('클릭율', 0) >= high_performance_threshold:
                        self.high_performance_messages.append(row)
                
                print(f"✅ 고성과 메시지: {len(self.high_performance_messages)}개 (최고: {sorted_data[0].get('클릭율', 0):.1f}%)")
            
            # 서비스별 분석 (JSON serializable)
            service_analysis = {}
            for row in self.data:
                service = row.get('서비스명', '기타')
                if service not in service_analysis:
                    service_analysis[service] = {
                        'messages': [],
                        'total_clicks': 0,
                        'count': 0
                    }
                
                # datetime 객체 제외한 정리된 메시지 데이터 추가
                clean_row = {}
                for key, value in row.items():
                    if key == '발송일_객체':
                        continue  # 내부 계산용 객체 제외
                    elif isinstance(value, (int, float, str, bool)) or value is None:
                        clean_row[key] = value
                    else:
                        clean_row[key] = str(value)
                
                service_analysis[service]['messages'].append(clean_row)
                service_analysis[service]['total_clicks'] += row.get('클릭율', 0)
                service_analysis[service]['count'] += 1
            
            # 서비스별 평균 계산
            for service in service_analysis:
                count = service_analysis[service]['count']
                total = service_analysis[service]['total_clicks']
                service_analysis[service]['avg_click_rate'] = total / count if count > 0 else 0
                
                # 상위 메시지만 유지 (안전한 정렬)
                try:
                    service_analysis[service]['messages'].sort(
                        key=lambda x: float(x.get('클릭율', 0)), reverse=True
                    )
                    service_analysis[service]['messages'] = service_analysis[service]['messages'][:5]
                except Exception as e:
                    print(f"⚠️ 서비스 {service} 메시지 정렬 실패: {e}")
                    service_analysis[service]['messages'] = service_analysis[service]['messages'][:5]
            
            # 키워드 분석
            keywords = ['혜택', '최대', '할인', '금리', '한도', '대출', '비교', '갈아타기', '확인', '신청']
            keyword_performance = {}
            
            for keyword in keywords:
                keyword_messages = [
                    row for row in self.data 
                    if keyword in str(row.get('발송 문구', ''))
                ]
                
                if keyword_messages:
                    rates = [row.get('클릭율', 0) for row in keyword_messages]
                    avg_rate = sum(rates) / len(rates) if rates else 0
                    keyword_performance[keyword] = [avg_rate, len(keyword_messages)]
            
            # 요일별 분석
            weekday_analysis = {}
            weekdays = ['월', '화', '수', '목', '금', '토', '일']
            
            for day in weekdays:
                day_messages = [row for row in self.data if row.get('요일') == day]
                if day_messages:
                    rates = [row.get('클릭율', 0) for row in day_messages]
                    avg_rate = sum(rates) / len(rates) if rates else 0
                    weekday_analysis[day] = {
                        'avg_click_rate': avg_rate,
                        'count': len(day_messages)
                    }
                else:
                    weekday_analysis[day] = {'avg_click_rate': 0, 'count': 0}
            
            # 전체 통계
            all_rates = [row.get('클릭율', 0) for row in self.data]
            overall_avg = sum(all_rates) / len(all_rates) if all_rates else 0
            best_rate = max(all_rates) if all_rates else 0
            
            self.performance_patterns = {
                'service_analysis': service_analysis,
                'keyword_analysis': keyword_performance,
                'time_analysis': weekday_analysis,
                'overall_avg': overall_avg,
                'best_click_rate': best_rate
            }
            
        except Exception as e:
            print(f"❌ 패턴 분석 실패: {e}")
            # 기본 패턴 설정
            self.performance_patterns = {
                'service_analysis': {},
                'keyword_analysis': {},
                'time_analysis': {},
                'overall_avg': 0,
                'best_click_rate': 0
            }
    
    def get_dashboard_data(self):
        """대시보드용 데이터 반환 (JSON serializable)"""
        if not self.analysis_complete:
            return {
                'success': False,
                'error': '먼저 CSV 파일을 업로드하고 분석을 완료해주세요.'
            }
        
        # JSON serializable 형태로 변환
        clean_high_performance = []
        for msg in self.high_performance_messages[:10]:
            clean_msg = {}
            for key, value in msg.items():
                # datetime 객체 제외 및 안전한 변환
                if key == '발송일_객체':
                    continue  # 내부 계산용 객체 제외
                elif key == '발송일' and hasattr(value, 'strftime'):
                    clean_msg[key] = value.strftime('%Y-%m-%d')
                elif isinstance(value, (int, float, str, bool)) or value is None:
                    clean_msg[key] = value
                else:
                    # 기타 객체는 문자열로 변환
                    clean_msg[key] = str(value)
            clean_high_performance.append(clean_msg)
        
        # 서비스 분석 데이터 정리
        clean_service_analysis = {}
        service_analysis = self.performance_patterns.get('service_analysis', {})
        for service, data in service_analysis.items():
            clean_service_data = {
                'count': data.get('count', 0),
                'avg_click_rate': data.get('avg_click_rate', 0),
                'messages': []
            }
            
            # 메시지 데이터 정리
            for msg in data.get('messages', []):
                clean_msg = {}
                for key, value in msg.items():
                    if key == '발송일_객체':
                        continue
                    elif isinstance(value, (int, float, str, bool)) or value is None:
                        clean_msg[key] = value
                    else:
                        clean_msg[key] = str(value)
                clean_service_data['messages'].append(clean_msg)
            
            clean_service_analysis[service] = clean_service_data
        
        return {
            'success': True,
            'data': {
                'summary': {
                    'total_messages': len(self.data),
                    'avg_click_rate': self.performance_patterns.get('overall_avg', 0),
                    'best_click_rate': self.performance_patterns.get('best_click_rate', 0),
                    'high_performance_count': len(self.high_performance_messages)
                },
                'service_analysis': clean_service_analysis,
                'keyword_analysis': self.performance_patterns.get('keyword_analysis', {}),
                'time_analysis': self.performance_patterns.get('time_analysis', {}),
                'high_performance_messages': clean_high_performance
            }
        }
    
    def get_summary(self):
        """분석 요약 정보"""
        if not self.data:
            return {}
        
        all_rates = [row.get('클릭율', 0) for row in self.data]
        
        return {
            'total_messages': len(self.data),
            'avg_click_rate': sum(all_rates) / len(all_rates) if all_rates else 0,
            'max_click_rate': max(all_rates) if all_rates else 0,
            'min_click_rate': min(all_rates) if all_rates else 0,
            'high_performance_count': len(self.high_performance_messages),
            'services_count': len(set(row.get('서비스명', '') for row in self.data))
        }

# 전역 분석기 인스턴스
analyzer = UploadAnalyzer()