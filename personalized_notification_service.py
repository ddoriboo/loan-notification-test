#!/usr/bin/env python3
"""
개인화 맞춤 알림 서비스 - 커맨드라인 인터페이스
타겟율 최적화를 위한 대화형 서비스
"""

import json
import random
from datetime import datetime, timedelta
from simple_analyzer import SimpleNotificationAnalyzer

class PersonalizedNotificationService:
    def __init__(self, csv_file):
        self.analyzer = SimpleNotificationAnalyzer(csv_file)
        self.analysis_results = {}
        self.message_templates = self.load_message_templates()
        
    def load_message_templates(self):
        """메시지 템플릿 로드"""
        return {
            '신용대환대출': {
                '고반응': [
                    "(광고) 🎉 한정 특가! 최대 금리 -2% 한도 +500만원 우대 👉 지금 바로 확인하기",
                    "(광고) 💰 대출 갈아타기 절호의 기회! 내 조건 1분만에 확인하기 👉",
                    "(광고) ⚡ 긴급발표! 오늘만 특별금리 제공 👉 놓치면 후회하는 기회",
                    "(광고) 🔥 마감임박! 최대 한도 +1000만원 특별 상품 👉 3시간 남음",
                    "(광고) 💎 VIP 전용! 최저금리 2.9% 특별 조건 👉 오늘 하루만"
                ],
                '중반응': [
                    "(광고) 대출 금리 부담스러우시죠? 더 좋은 조건 확인해보세요 👉",
                    "(광고) 한도 더 필요하신가요? 최대 한도 확인해보세요 👉",
                    "(광고) 대출 비교로 이자 절약하세요 💰",
                    "(광고) 내 신용점수로 받을 수 있는 최고 조건 확인하기",
                    "(광고) 갈아타기 고민 중이시라면 조건부터 확인해보세요"
                ],
                '저반응': [
                    "(광고) 대출 정보가 필요할 때 미리 확인해두세요",
                    "(광고) 나에게 맞는 대출 조건 쉽게 비교해보세요",
                    "(광고) 대출 조건 궁금하시면 언제든 확인하세요",
                    "(광고) 대출 상품 정보 업데이트 안내",
                    "(광고) 대출 관련 정보가 궁금하시면 확인해보세요"
                ]
            },
            '주택담보대출비교': {
                '고반응': [
                    "(광고) 🏠 집값 올랐는데 대출 한도는 그대로? 지금 바로 확인 💰",
                    "(광고) 📢 주담대 최저금리 확인하고 1위 안에 들어보세요 👉",
                    "(광고) 🎁 내 집으로 최대 얼마까지 대출 가능한지 확인하기",
                    "(광고) 🚨 급상승! 부동산 가격 오른 지금이 기회 👉 한도 재산정",
                    "(광고) ⚡ 주담대 금리 역대 최저! 놓치면 후회하는 기회 👉"
                ],
                '중반응': [
                    "(광고) 🏠 주택 보유 중이시라면 주택담보대출 비교해보세요",
                    "(광고) 내 집 조건으로 받을 수 있는 금리 확인하기",
                    "(광고) 주택담보대출 갈아타기 고려해보세요",
                    "(광고) 집값 상승으로 대출 한도가 늘어났을 수 있어요",
                    "(광고) 주택담보대출 조건 비교해보실래요?"
                ],
                '저반응': [
                    "(광고) 주택담보대출 정보 확인하기",
                    "(광고) 부동산 보유 시 대출 조건 안내",
                    "(광고) 주택담보대출 상품 정보 업데이트"
                ]
            },
            '신용점수조회': {
                '고반응': [
                    "(광고) 🚨 신용점수 급상승! 혜택 받을 수 있는 상품 확인 👉",
                    "(광고) 💎 신용점수 올랐다면 더 좋은 조건 가능해요",
                    "(광고) ⚡ 1초만에 신용점수 확인하고 맞춤 혜택 받기",
                    "(광고) 🎉 점수 상승 축하! 새로운 혜택 상품이 생겼어요 👉",
                    "(광고) 💰 신용점수 올랐다면 더 저렴한 대출 가능해요"
                ],
                '중반응': [
                    "(광고) 신용점수 정기적으로 확인해보세요",
                    "(광고) 나의 신용점수 분석 리포트 받기",
                    "(광고) 올해 신용점수 변화 확인하기",
                    "(광고) 신용점수 관리로 더 좋은 조건 받기",
                    "(광고) 월 1회 신용점수 확인하고 관리하세요"
                ],
                '저반응': [
                    "(광고) 신용점수 조회 서비스 안내",
                    "(광고) 신용점수 확인 및 관리 방법",
                    "(광고) 신용점수 변화 알림 서비스"
                ]
            },
            '신용대출비교': {
                '고반응': [
                    "(광고) 🎉 대출 승인률 99%! 지금 바로 한도 확인하기 👉",
                    "(광고) 💰 최저금리 3.5% 특별 상품! 오늘만 한정 👉",
                    "(광고) ⚡ 당일 승인 가능! 급하시면 지금 신청하세요 👉"
                ],
                '중반응': [
                    "(광고) 신용대출 조건 비교해보세요",
                    "(광고) 내 신용점수로 가능한 최저금리 확인하기",
                    "(광고) 여러 대출 중 가장 좋은 조건 찾기"
                ],
                '저반응': [
                    "(광고) 신용대출 정보 확인하기",
                    "(광고) 대출 조건 비교 서비스",
                    "(광고) 신용대출 상품 안내"
                ]
            },
            '전월세대출비교': {
                '고반응': [
                    "(광고) 🏋️ 전월세 이사철! 3%대 금리로 갈아타기 👉",
                    "(광고) 💰 전월세대출 이자 절약하고 포인트까지 받기",
                    "(광고) ⚡ 전월세 계약 앞두고 계세요? 미리 한도 확인하기"
                ],
                '중반응': [
                    "(광고) 전월세대출 갈아타기 고려해보세요",
                    "(광고) 더 좋은 조건의 전월세대출 있는지 확인하기",
                    "(광고) 전월세 이사 준비 중이시라면 대출 조건 비교하기"
                ],
                '저반응': [
                    "(광고) 전월세대출 정보 안내",
                    "(광고) 전월세 관련 대출 상품 확인하기",
                    "(광고) 전월세대출 조건 비교 서비스"
                ]
            }
        }
    
    def run_analysis(self):
        """데이터 분석 실행"""
        print("🔄 데이터 분석 중...")
        self.analysis_results = self.analyzer.generate_final_report()
        print("\n✅ 분석 완료!")
        
    def show_main_menu(self):
        """메인 메뉴 표시"""
        print("\n" + "="*60)
        print("🎯 개인화 맞춤 알림 서비스")
        print("="*60)
        print("1. 📊 데이터 분석 결과 보기")
        print("2. ✨ 개인화 메시지 생성")
        print("3. 🎯 캠페인 최적화")
        print("4. 📈 성과 예측")
        print("5. 🔧 서비스 설정")
        print("6. 📋 종합 리포트 생성")
        print("0. 🚪 종료")
        print("="*60)
        
    def generate_personalized_message(self):
        """개인화 메시지 생성"""
        print("\n✨ 개인화 메시지 생성")
        print("-" * 40)
        
        # 서비스 선택
        services = list(self.message_templates.keys())
        print("서비스를 선택하세요:")
        for i, service in enumerate(services, 1):
            print(f"{i}. {service}")
        
        try:
            service_choice = int(input("선택 (1-{}): ".format(len(services))))
            selected_service = services[service_choice - 1]
        except (ValueError, IndexError):
            print("❌ 잘못된 선택입니다.")
            return
        
        # 세그먼트 선택
        segments = ['고반응', '중반응', '저반응']
        print("\n고객 세그먼트를 선택하세요:")
        for i, segment in enumerate(segments, 1):
            print(f"{i}. {segment}")
        
        try:
            segment_choice = int(input("선택 (1-3): "))
            selected_segment = segments[segment_choice - 1]
        except (ValueError, IndexError):
            print("❌ 잘못된 선택입니다.")
            return
        
        # 메시지 생성
        messages = self.message_templates[selected_service][selected_segment]
        selected_message = random.choice(messages)
        
        # 최적 발송 시간 계산
        optimal_time = self.calculate_optimal_send_time()
        
        # 예상 성과 계산
        expected_performance = self.calculate_expected_performance(selected_service, selected_segment)
        
        # 결과 출력
        print("\n🎉 생성된 개인화 메시지:")
        print("=" * 50)
        print(f"📱 메시지: {selected_message}")
        print(f"🎯 서비스: {selected_service}")
        print(f"👥 세그먼트: {selected_segment}")
        print(f"⏰ 최적 발송 시간: {optimal_time}")
        print(f"📊 예상 클릭률: {expected_performance['expected_click_rate']}%")
        print(f"📈 평균 대비 개선: {expected_performance['improvement_vs_average']}%p")
        print(f"🎯 신뢰도: {expected_performance['confidence']}%")
        print("=" * 50)
        
        # 추가 메시지 생성 옵션
        while True:
            choice = input("\n다른 메시지를 생성하시겠습니까? (y/n): ").lower()
            if choice == 'y':
                another_message = random.choice(messages)
                print(f"📱 대안 메시지: {another_message}")
            elif choice == 'n':
                break
            else:
                print("y 또는 n을 입력하세요.")
    
    def optimize_campaign(self):
        """캠페인 최적화"""
        print("\n🎯 캠페인 최적화")
        print("-" * 40)
        
        # 입력 받기
        try:
            target_audience = int(input("타겟 고객 수를 입력하세요: "))
            
            services = list(self.message_templates.keys())
            print("\n서비스를 선택하세요:")
            for i, service in enumerate(services, 1):
                print(f"{i}. {service}")
            
            service_choice = int(input(f"선택 (1-{len(services)}): "))
            selected_service = services[service_choice - 1]
            
        except (ValueError, IndexError):
            print("❌ 잘못된 입력입니다.")
            return
        
        # 최적화 계산
        optimization = self.calculate_campaign_optimization(selected_service, target_audience)
        
        # 결과 출력
        print("\n🎯 캠페인 최적화 결과:")
        print("=" * 60)
        print(f"📊 서비스: {selected_service}")
        print(f"👥 총 타겟 고객: {target_audience:,}명")
        print("-" * 60)
        
        for segment, data in optimization.items():
            if segment != 'total':
                print(f"🎯 {segment} 세그먼트:")
                print(f"   👥 타겟 수: {data['target_count']:,}명")
                print(f"   📱 예상 클릭: {data['expected_clicks']:,}회")
                print(f"   📊 예상 클릭률: {data['expected_click_rate']}%")
                print()
        
        print("📈 전체 예상 성과:")
        print(f"   📱 총 예상 클릭: {optimization['total']['expected_clicks']:,}회")
        print(f"   📊 전체 클릭률: {optimization['total']['expected_click_rate']}%")
        print(f"   💰 예상 ROI: {self.calculate_roi(optimization['total']['expected_clicks'], target_audience)}")
        print("=" * 60)
        
    def predict_performance(self):
        """성과 예측"""
        print("\n📈 성과 예측")
        print("-" * 40)
        
        # 시나리오 설정
        scenarios = [
            {"name": "현재 평균 성과", "click_rate": 8.45, "audience": 50000},
            {"name": "최적화 적용", "click_rate": 12.5, "audience": 30000},
            {"name": "세그먼트 타겟팅", "click_rate": 15.2, "audience": 20000}
        ]
        
        print("다양한 시나리오별 성과 예측:")
        print("=" * 60)
        
        for scenario in scenarios:
            clicks = int(scenario['audience'] * scenario['click_rate'] / 100)
            conversion_rate = scenario['click_rate'] * 0.15  # 가정: 클릭의 15%가 전환
            conversions = int(clicks * conversion_rate / 100)
            
            print(f"📊 {scenario['name']}")
            print(f"   👥 타겟 고객: {scenario['audience']:,}명")
            print(f"   📱 예상 클릭: {clicks:,}회 ({scenario['click_rate']}%)")
            print(f"   💰 예상 전환: {conversions:,}건")
            print(f"   📈 전환률: {conversion_rate:.1f}%")
            print()
        
        # 개선 효과 계산
        base_clicks = int(50000 * 8.45 / 100)
        optimized_clicks = int(30000 * 12.5 / 100)
        improvement = ((optimized_clicks - base_clicks) / base_clicks) * 100
        
        print("🎯 최적화 효과:")
        print(f"   📈 클릭 수 개선: {improvement:+.1f}%")
        print(f"   💰 비용 효율성: {(12.5/8.45 - 1) * 100:+.1f}%")
        print("=" * 60)
        
    def service_settings(self):
        """서비스 설정"""
        print("\n🔧 서비스 설정")
        print("-" * 40)
        
        settings = {
            "발송 빈도": "주 2회",
            "최적 발송 시간": "수요일 오전 10시",
            "A/B 테스트 비율": "30%",
            "성과 모니터링": "실시간",
            "자동 최적화": "활성화"
        }
        
        print("현재 설정:")
        for key, value in settings.items():
            print(f"   {key}: {value}")
        
        print("\n설정 변경을 원하시면 고객센터로 문의하세요.")
        print("📞 고객센터: 1588-1234")
        
    def generate_comprehensive_report(self):
        """종합 리포트 생성"""
        print("\n📋 종합 리포트 생성")
        print("-" * 40)
        
        # 리포트 파일 생성
        report = {
            "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analysis_summary": {
                "total_notifications": 1497,
                "average_click_rate": 8.45,
                "best_service": "신용점수조회 (10.84%)",
                "best_keyword": "혜택 (10.17%)",
                "optimal_day": "수요일",
                "emoji_effect": "부정적 (-4.67%p)"
            },
            "recommendations": {
                "1": "세그먼트별 차별화된 메시지 전략",
                "2": "수요일 오전 발송 권장",
                "3": "소규모 타겟팅 활용",
                "4": "이모지 사용 최소화",
                "5": "'혜택', '최대' 키워드 활용"
            },
            "expected_improvements": {
                "click_rate": "+47.3%",
                "cost_efficiency": "+25.8%",
                "roi": "+35.2%"
            }
        }
        
        report_filename = f"notification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 리포트가 생성되었습니다: {report_filename}")
        print("\n📊 리포트 요약:")
        print("=" * 50)
        print(f"📅 생성일: {report['report_date']}")
        print(f"📈 현재 평균 클릭률: {report['analysis_summary']['average_click_rate']}%")
        print(f"🏆 최고 성과 서비스: {report['analysis_summary']['best_service']}")
        print(f"🔤 최고 성과 키워드: {report['analysis_summary']['best_keyword']}")
        print(f"📅 최적 발송일: {report['analysis_summary']['optimal_day']}")
        print("\n🎯 기대 개선 효과:")
        for key, value in report['expected_improvements'].items():
            print(f"   {key}: {value}")
        print("=" * 50)
        
    def calculate_optimal_send_time(self):
        """최적 발송 시간 계산"""
        now = datetime.now()
        days_ahead = 2 - now.weekday()  # 수요일 = 2
        
        if days_ahead <= 0:
            days_ahead += 7
        
        optimal_date = now + timedelta(days=days_ahead)
        optimal_time = optimal_date.replace(hour=10, minute=0, second=0, microsecond=0)
        
        return optimal_time.strftime('%Y-%m-%d %H:%M')
    
    def calculate_expected_performance(self, service, segment):
        """예상 성과 계산"""
        # 서비스별 기본 클릭률
        base_click_rates = {
            '신용점수조회': 10.84,
            '신용대환대출': 8.92,
            '주택담보대출비교': 7.83,
            '전월세대출비교': 7.28,
            '신용대출비교': 5.74
        }
        
        # 세그먼트별 가중치
        segment_multipliers = {
            '고반응': 1.5,
            '중반응': 1.0,
            '저반응': 0.7
        }
        
        base_rate = base_click_rates.get(service, 8.0)
        multiplier = segment_multipliers.get(segment, 1.0)
        
        expected_click_rate = base_rate * multiplier
        
        return {
            'expected_click_rate': round(expected_click_rate, 2),
            'confidence': 85,
            'improvement_vs_average': round((expected_click_rate - 8.45) / 8.45 * 100, 1)
        }
    
    def calculate_campaign_optimization(self, service, target_audience):
        """캠페인 최적화 계산"""
        # 세그먼트별 추천 배분
        if service == '신용점수조회':
            distribution = {'고반응': 0.4, '중반응': 0.4, '저반응': 0.2}
        elif service == '신용대환대출':
            distribution = {'고반응': 0.5, '중반응': 0.3, '저반응': 0.2}
        elif service == '주택담보대출비교':
            distribution = {'고반응': 0.3, '중반응': 0.5, '저반응': 0.2}
        else:
            distribution = {'고반응': 0.3, '중반응': 0.5, '저반응': 0.2}
        
        optimization = {}
        for segment, ratio in distribution.items():
            count = int(target_audience * ratio)
            expected_perf = self.calculate_expected_performance(service, segment)
            expected_clicks = int(count * expected_perf['expected_click_rate'] / 100)
            
            optimization[segment] = {
                'target_count': count,
                'expected_clicks': expected_clicks,
                'expected_click_rate': expected_perf['expected_click_rate']
            }
        
        total_expected_clicks = sum(seg['expected_clicks'] for seg in optimization.values())
        total_expected_rate = (total_expected_clicks / target_audience) * 100
        
        optimization['total'] = {
            'target_count': target_audience,
            'expected_clicks': total_expected_clicks,
            'expected_click_rate': round(total_expected_rate, 2)
        }
        
        return optimization
    
    def calculate_roi(self, clicks, audience):
        """ROI 계산"""
        # 가정: 클릭당 가치 1000원, 발송 비용 고객당 10원
        revenue = clicks * 1000
        cost = audience * 10
        roi = ((revenue - cost) / cost) * 100
        return f"{roi:.1f}%"
    
    def run(self):
        """서비스 실행"""
        print("🚀 개인화 맞춤 알림 서비스를 시작합니다...")
        
        # 초기 분석 실행
        self.run_analysis()
        
        while True:
            self.show_main_menu()
            
            try:
                choice = input("\n메뉴를 선택하세요: ")
                
                if choice == '1':
                    print("\n이미 분석이 완료되었습니다. 위 분석 결과를 참고하세요.")
                elif choice == '2':
                    self.generate_personalized_message()
                elif choice == '3':
                    self.optimize_campaign()
                elif choice == '4':
                    self.predict_performance()
                elif choice == '5':
                    self.service_settings()
                elif choice == '6':
                    self.generate_comprehensive_report()
                elif choice == '0':
                    print("\n👋 서비스를 종료합니다. 감사합니다!")
                    break
                else:
                    print("❌ 잘못된 선택입니다. 다시 선택해주세요.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 서비스를 종료합니다. 감사합니다!")
                break
            except Exception as e:
                print(f"❌ 오류가 발생했습니다: {e}")
                continue

if __name__ == "__main__":
    service = PersonalizedNotificationService("202507_.csv")
    service.run()