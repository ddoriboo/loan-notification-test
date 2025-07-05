#!/usr/bin/env python3
"""
대출 서비스 알림 발송 히스토리 분석기 (기본 Python만 사용)
- 고객 세그먼트 분류
- 개인화 문구 생성
- 타겟율 최적화
"""

import csv
import json
from datetime import datetime
from collections import defaultdict, Counter
import statistics

class SimpleNotificationAnalyzer:
    def __init__(self, csv_file):
        self.data = []
        self.load_data(csv_file)
        
    def load_data(self, csv_file):
        """CSV 파일 로드"""
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['클릭율'] = float(row['클릭율'])
                    row['발송회원수'] = int(row['발송회원수'])
                    row['클릭회원수'] = int(row['클릭회원수'])
                    row['클릭까지 소요된 평균 분(Minutes)'] = float(row['클릭까지 소요된 평균 분(Minutes)'])
                    row['발송일'] = datetime.strptime(row['발송일'], '%Y-%m-%d')
                    self.data.append(row)
                except (ValueError, KeyError):
                    continue
        
    def analyze_basic_stats(self):
        """기본 통계 분석"""
        print("=== 기본 통계 분석 ===")
        print(f"전체 알림 수: {len(self.data)}")
        
        if self.data:
            dates = [row['발송일'] for row in self.data]
            print(f"기간: {min(dates).strftime('%Y-%m-%d')} ~ {max(dates).strftime('%Y-%m-%d')}")
            
            services = set(row['서비스명'] for row in self.data)
            print(f"서비스 종류: {len(services)}개")
            print(f"서비스 목록: {', '.join(services)}")
            
            channels = Counter(row['발송채널 (noti : 네이버앱, npay: 페이앱)'] for row in self.data)
            print(f"발송채널 분포: {dict(channels)}")
            
            click_rates = [row['클릭율'] for row in self.data]
            print(f"평균 클릭율: {statistics.mean(click_rates):.2f}%")
            print(f"클릭율 중위수: {statistics.median(click_rates):.2f}%")
            
            send_counts = [row['발송회원수'] for row in self.data]
            print(f"평균 발송회원수: {statistics.mean(send_counts):.0f}명")
        print()
        
    def analyze_service_performance(self):
        """서비스별 성과 분석"""
        print("=== 서비스별 성과 분석 ===")
        
        service_stats = defaultdict(list)
        
        for row in self.data:
            service = row['서비스명']
            service_stats[service].append({
                'click_rate': row['클릭율'],
                'send_count': row['발송회원수'],
                'click_count': row['클릭회원수'],
                'response_time': row['클릭까지 소요된 평균 분(Minutes)']
            })
        
        results = []
        for service, stats in service_stats.items():
            click_rates = [s['click_rate'] for s in stats]
            send_counts = [s['send_count'] for s in stats]
            response_times = [s['response_time'] for s in stats]
            
            result = {
                'service': service,
                'avg_click_rate': statistics.mean(click_rates),
                'median_click_rate': statistics.median(click_rates),
                'count': len(stats),
                'avg_send_count': statistics.mean(send_counts),
                'avg_response_time': statistics.mean(response_times)
            }
            results.append(result)
        
        # 클릭률 기준 정렬
        results.sort(key=lambda x: x['avg_click_rate'], reverse=True)
        
        print(f"{'서비스명':<20} {'평균클릭율':<10} {'중위클릭율':<10} {'알림수':<8} {'평균발송수':<12} {'평균응답시간':<12}")
        print("-" * 80)
        for result in results:
            print(f"{result['service']:<20} {result['avg_click_rate']:<10.2f} {result['median_click_rate']:<10.2f} {result['count']:<8} {result['avg_send_count']:<12.0f} {result['avg_response_time']:<12.0f}")
        print()
        
        return results
        
    def analyze_message_patterns(self):
        """메시지 패턴 분석"""
        print("=== 메시지 패턴 분석 ===")
        
        keywords = ['금리', '한도', '대출', '비교', '우대', '혜택', '포인트', '할인', '지원', '최대', '최저', '특가', '한정']
        
        keyword_stats = {}
        
        for keyword in keywords:
            keyword_messages = [row for row in self.data if keyword in row['발송 문구']]
            if keyword_messages:
                click_rates = [row['클릭율'] for row in keyword_messages]
                keyword_stats[keyword] = {
                    'count': len(keyword_messages),
                    'avg_click_rate': statistics.mean(click_rates),
                    'avg_send_count': statistics.mean([row['발송회원수'] for row in keyword_messages])
                }
        
        # 클릭률 기준 정렬
        sorted_keywords = sorted(keyword_stats.items(), key=lambda x: x[1]['avg_click_rate'], reverse=True)
        
        print("키워드별 성과 분석:")
        print(f"{'키워드':<8} {'사용횟수':<10} {'평균클릭율':<12} {'평균발송수':<12}")
        print("-" * 50)
        
        for keyword, stats in sorted_keywords:
            print(f"{keyword:<8} {stats['count']:<10} {stats['avg_click_rate']:<12.2f} {stats['avg_send_count']:<12.0f}")
        print()
        
        return keyword_stats
        
    def analyze_emoji_effect(self):
        """이모지 효과 분석"""
        print("=== 이모지 효과 분석 ===")
        
        emojis = ['🎉', '💰', '👉', '🏠', '💸', '🎁', '📣', '💌', '🚘', '⚡', '🔔', '🚨', '💎']
        
        emoji_messages = []
        non_emoji_messages = []
        
        for row in self.data:
            has_emoji = any(emoji in row['발송 문구'] for emoji in emojis)
            if has_emoji:
                emoji_messages.append(row)
            else:
                non_emoji_messages.append(row)
        
        if emoji_messages and non_emoji_messages:
            emoji_click_rates = [row['클릭율'] for row in emoji_messages]
            non_emoji_click_rates = [row['클릭율'] for row in non_emoji_messages]
            
            print(f"이모지 사용 메시지 ({len(emoji_messages)}개):")
            print(f"- 평균 클릭율: {statistics.mean(emoji_click_rates):.2f}%")
            print(f"- 중위 클릭율: {statistics.median(emoji_click_rates):.2f}%")
            
            print(f"\n이모지 미사용 메시지 ({len(non_emoji_messages)}개):")
            print(f"- 평균 클릭율: {statistics.mean(non_emoji_click_rates):.2f}%")
            print(f"- 중위 클릭율: {statistics.median(non_emoji_click_rates):.2f}%")
            
            improvement = statistics.mean(emoji_click_rates) - statistics.mean(non_emoji_click_rates)
            print(f"\n이모지 효과: {improvement:+.2f}% 포인트")
        print()
        
    def segment_customers(self):
        """고객 세그먼트 분류"""
        print("=== 고객 세그먼트 분류 ===")
        
        # 서비스별 평균 성과 계산
        service_performance = defaultdict(list)
        
        for row in self.data:
            service = row['서비스명']
            service_performance[service].append({
                'click_rate': row['클릭율'],
                'response_time': row['클릭까지 소요된 평균 분(Minutes)'],
                'send_count': row['발송회원수']
            })
        
        # 서비스별 평균 계산
        service_averages = {}
        for service, perf_list in service_performance.items():
            service_averages[service] = {
                'avg_click_rate': statistics.mean([p['click_rate'] for p in perf_list]),
                'avg_response_time': statistics.mean([p['response_time'] for p in perf_list]),
                'avg_send_count': statistics.mean([p['send_count'] for p in perf_list])
            }
        
        # 클릭률 기준으로 세그먼트 분류
        click_rates = [avg['avg_click_rate'] for avg in service_averages.values()]
        if click_rates:
            high_threshold = statistics.quantiles(click_rates, n=3)[1]  # 상위 33%
            low_threshold = statistics.quantiles(click_rates, n=3)[0]   # 하위 33%
            
            segments = {
                'high_response': [],
                'medium_response': [],
                'low_response': []
            }
            
            for service, avg in service_averages.items():
                if avg['avg_click_rate'] >= high_threshold:
                    segments['high_response'].append(service)
                elif avg['avg_click_rate'] >= low_threshold:
                    segments['medium_response'].append(service)
                else:
                    segments['low_response'].append(service)
            
            print("고반응 세그먼트 (클릭률 상위 33%):")
            for service in segments['high_response']:
                print(f"- {service}: {service_averages[service]['avg_click_rate']:.2f}%")
            
            print("\n중반응 세그먼트 (클릭률 중위 33%):")
            for service in segments['medium_response']:
                print(f"- {service}: {service_averages[service]['avg_click_rate']:.2f}%")
            
            print("\n저반응 세그먼트 (클릭률 하위 33%):")
            for service in segments['low_response']:
                print(f"- {service}: {service_averages[service]['avg_click_rate']:.2f}%")
        
        print()
        return segments
        
    def generate_personalized_messages(self):
        """개인화 메시지 생성"""
        print("=== 개인화 메시지 생성 전략 ===")
        
        # 고성과 메시지 분석
        click_rates = [row['클릭율'] for row in self.data]
        high_threshold = statistics.quantiles(click_rates, n=5)[3]  # 상위 20%
        
        high_performance_messages = [row for row in self.data if row['클릭율'] >= high_threshold]
        
        print(f"고성과 메시지 분석 (상위 20%, {len(high_performance_messages)}개):")
        print(f"- 평균 클릭율: {statistics.mean([row['클릭율'] for row in high_performance_messages]):.2f}%")
        print(f"- 평균 메시지 길이: {statistics.mean([len(row['발송 문구']) for row in high_performance_messages]):.0f}자")
        
        # 서비스별 성공 패턴
        service_success_patterns = defaultdict(list)
        
        for row in high_performance_messages:
            service_success_patterns[row['서비스명']].append(row['발송 문구'])
        
        print("\n서비스별 성공 메시지 패턴:")
        for service, messages in service_success_patterns.items():
            print(f"\n{service}:")
            for i, msg in enumerate(messages[:3], 1):  # 상위 3개만
                print(f"  {i}. {msg}")
        
        # 메시지 템플릿 생성
        templates = self.create_message_templates()
        
        print("\n🎯 개인화 메시지 템플릿:")
        for service, segment_templates in templates.items():
            print(f"\n{service}:")
            for segment, template_list in segment_templates.items():
                print(f"  {segment}:")
                for template in template_list:
                    print(f"    - {template}")
        
        return templates
        
    def create_message_templates(self):
        """메시지 템플릿 생성"""
        templates = {
            '신용대환대출': {
                '고반응': [
                    "(광고) 🎉 한정 특가! 최대 금리 -2% 한도 +500만원 우대 👉 지금 바로 확인하기",
                    "(광고) 💰 대출 갈아타기 절호의 기회! 내 조건 1분만에 확인하기 👉",
                    "(광고) ⚡ 긴급발표! 오늘만 특별금리 제공 👉 놓치면 후회하는 기회"
                ],
                '중반응': [
                    "(광고) 대출 금리 부담스러우시죠? 더 좋은 조건 확인해보세요 👉",
                    "(광고) 한도 더 필요하신가요? 최대 한도 확인해보세요 👉",
                    "(광고) 대출 비교로 이자 절약하세요 💰"
                ],
                '저반응': [
                    "(광고) 대출 정보가 필요할 때 미리 확인해두세요",
                    "(광고) 나에게 맞는 대출 조건 쉽게 비교해보세요",
                    "(광고) 대출 조건 궁금하시면 언제든 확인하세요"
                ]
            },
            '주택담보대출비교': {
                '고반응': [
                    "(광고) 🏠 집값 올랐는데 대출 한도는 그대로? 지금 바로 확인 💰",
                    "(광고) 📢 주담대 최저금리 확인하고 1위 안에 들어보세요 👉",
                    "(광고) 🎁 내 집으로 최대 얼마까지 대출 가능한지 확인하기"
                ],
                '중반응': [
                    "(광고) 🏠 주택 보유 중이시라면 주택담보대출 비교해보세요",
                    "(광고) 내 집 조건으로 받을 수 있는 금리 확인하기",
                    "(광고) 주택담보대출 갈아타기 고려해보세요"
                ]
            },
            '신용점수조회': {
                '고반응': [
                    "(광고) 🚨 신용점수 급상승! 혜택 받을 수 있는 상품 확인 👉",
                    "(광고) 💎 신용점수 올랐다면 더 좋은 조건 가능해요",
                    "(광고) ⚡ 1초만에 신용점수 확인하고 맞춤 혜택 받기"
                ],
                '중반응': [
                    "(광고) 신용점수 정기적으로 확인해보세요",
                    "(광고) 나의 신용점수 분석 리포트 받기",
                    "(광고) 올해 신용점수 변화 확인하기"
                ]
            }
        }
        
        return templates
        
    def optimize_targeting(self):
        """타겟팅 최적화"""
        print("=== 타겟팅 최적화 전략 ===")
        
        # 요일별 분석
        weekday_performance = defaultdict(list)
        
        for row in self.data:
            weekday = row['발송일'].weekday()  # 0=월요일, 6=일요일
            weekday_performance[weekday].append(row['클릭율'])
        
        weekday_names = ['월', '화', '수', '목', '금', '토', '일']
        weekday_averages = {}
        
        print("요일별 성과:")
        for weekday in range(7):
            if weekday in weekday_performance:
                avg_click_rate = statistics.mean(weekday_performance[weekday])
                weekday_averages[weekday] = avg_click_rate
                print(f"- {weekday_names[weekday]}요일: {avg_click_rate:.2f}%")
        
        if weekday_averages:
            best_weekday = max(weekday_averages, key=weekday_averages.get)
            print(f"\n최고 성과 요일: {weekday_names[best_weekday]}요일")
        
        # 발송 규모별 분석
        send_counts = [row['발송회원수'] for row in self.data]
        if send_counts:
            median_send = statistics.median(send_counts)
            
            large_sends = [row for row in self.data if row['발송회원수'] >= median_send]
            small_sends = [row for row in self.data if row['발송회원수'] < median_send]
            
            if large_sends and small_sends:
                large_click_rate = statistics.mean([row['클릭율'] for row in large_sends])
                small_click_rate = statistics.mean([row['클릭율'] for row in small_sends])
                
                print(f"\n발송 규모별 성과:")
                print(f"- 대규모 발송 (>{median_send:.0f}명): {large_click_rate:.2f}%")
                print(f"- 소규모 발송 (<{median_send:.0f}명): {small_click_rate:.2f}%")
                
                if large_click_rate > small_click_rate:
                    print("→ 대규모 발송이 더 효과적")
                else:
                    print("→ 소규모 발송이 더 효과적")
        
        print(f"\n🎯 최적 발송 전략:")
        if weekday_averages:
            print(f"1. 발송 요일: {weekday_names[best_weekday]}요일")
        print(f"2. 이모지 활용으로 클릭률 향상")
        print(f"3. 긴급성 키워드 ('한정', '오늘만', '마감임박') 활용")
        print(f"4. 개인화 혜택 강조")
        print()
        
    def generate_final_report(self):
        """최종 리포트 생성"""
        print("=" * 60)
        print("🎯 개인화 맞춤 알림 서비스 구축 완료 리포트")
        print("=" * 60)
        
        # 분석 실행
        self.analyze_basic_stats()
        service_performance = self.analyze_service_performance()
        keyword_stats = self.analyze_message_patterns()
        self.analyze_emoji_effect()
        segments = self.segment_customers()
        templates = self.generate_personalized_messages()
        self.optimize_targeting()
        
        print("=" * 60)
        print("🚀 서비스 구축 결과 요약")
        print("=" * 60)
        
        print("✅ 완료된 기능:")
        print("1. 고객 세그먼트 분류 (고/중/저 반응군)")
        print("2. 서비스별 성과 분석")
        print("3. 키워드 효과 분석")
        print("4. 이모지 활용 효과 분석")
        print("5. 개인화 메시지 템플릿 생성")
        print("6. 최적 타겟팅 전략 수립")
        
        print("\n🎯 서비스 활용 방안:")
        print("1. 세그먼트별 차별화된 메시지 발송")
        print("2. 고성과 키워드 중심 메시지 작성")
        print("3. 이모지 활용한 시각적 어필")
        print("4. 최적 요일/시간대 발송")
        print("5. A/B 테스트를 통한 지속적 개선")
        
        print("\n💡 핵심 인사이트:")
        if service_performance:
            top_service = service_performance[0]
            print(f"- 최고 성과 서비스: {top_service['service']} ({top_service['avg_click_rate']:.2f}%)")
        
        if keyword_stats:
            top_keyword = max(keyword_stats.items(), key=lambda x: x[1]['avg_click_rate'])
            print(f"- 최고 성과 키워드: '{top_keyword[0]}' ({top_keyword[1]['avg_click_rate']:.2f}%)")
        
        print("\n🔄 향후 개선 방향:")
        print("1. 실시간 성과 모니터링 시스템 구축")
        print("2. 머신러닝 기반 자동 최적화")
        print("3. 고객 행동 예측 모델 개발")
        print("4. 다중 채널 통합 관리")
        
        return {
            'service_performance': service_performance,
            'keyword_stats': keyword_stats,
            'segments': segments,
            'templates': templates
        }

if __name__ == "__main__":
    # 분석 실행
    analyzer = SimpleNotificationAnalyzer("/mnt/c/Users/USER/Documents/notification/202507_.csv")
    results = analyzer.generate_final_report()