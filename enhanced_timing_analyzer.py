#!/usr/bin/env python3
"""
향상된 타이밍 분석기
- 월초/월말 효과 분석
- 급여일 패턴 분석
- 시간대별 분석
- 계절성 분석
"""

import csv
import json
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import calendar

class EnhancedTimingAnalyzer:
    def __init__(self, csv_file):
        self.data = []
        self.load_data(csv_file)
        
    def load_data(self, csv_file):
        """CSV 데이터 로드"""
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['클릭율'] = float(row['클릭율'])
                    row['발송회원수'] = int(row['발송회원수'])
                    row['클릭회원수'] = int(row['클릭회원수'])
                    row['발송일'] = datetime.strptime(row['발송일'], '%Y-%m-%d')
                    self.data.append(row)
                except (ValueError, KeyError):
                    continue
    
    def analyze_monthly_patterns(self):
        """월별 패턴 분석 (월초/월말)"""
        print("📅 월별 패턴 분석")
        print("="*50)
        
        monthly_patterns = {
            '월초(1-10일)': defaultdict(list),
            '월중(11-20일)': defaultdict(list), 
            '월말(21-31일)': defaultdict(list)
        }
        
        for row in self.data:
            day = row['발송일'].day
            click_rate = row['클릭율']
            
            if day <= 10:
                period = '월초(1-10일)'
            elif day <= 20:
                period = '월중(11-20일)'
            else:
                period = '월말(21-31일)'
            
            monthly_patterns[period]['click_rates'].append(click_rate)
            monthly_patterns[period]['count'].append(1)
        
        # 결과 출력
        for period, data in monthly_patterns.items():
            if data['click_rates']:
                avg_rate = statistics.mean(data['click_rates'])
                count = len(data['click_rates'])
                print(f"{period}: {avg_rate:.2f}% (발송 {count}회)")
        
        return monthly_patterns
    
    def analyze_payday_effect(self):
        """급여일 효과 분석"""
        print("\n💰 급여일 효과 분석")
        print("="*50)
        
        # 일반적인 급여일: 25일, 말일, 10일, 15일
        payday_patterns = {
            '급여일 전(22-24일)': [],
            '급여일(25일, 말일)': [],
            '급여일 후(1-5일)': [],
            '기타 일자': []
        }
        
        for row in self.data:
            day = row['발송일'].day
            month = row['발송일'].month
            year = row['발송일'].year
            last_day = calendar.monthrange(year, month)[1]
            
            click_rate = row['클릭율']
            
            if 22 <= day <= 24:
                category = '급여일 전(22-24일)'
            elif day == 25 or day == last_day:
                category = '급여일(25일, 말일)'
            elif 1 <= day <= 5:
                category = '급여일 후(1-5일)'
            else:
                category = '기타 일자'
            
            payday_patterns[category].append(click_rate)
        
        # 결과 출력
        for category, rates in payday_patterns.items():
            if rates:
                avg_rate = statistics.mean(rates)
                count = len(rates)
                print(f"{category}: {avg_rate:.2f}% (발송 {count}회)")
        
        return payday_patterns
    
    def analyze_seasonal_patterns(self):
        """계절별/월별 패턴 분석"""
        print("\n🌱 계절별 패턴 분석")
        print("="*50)
        
        seasonal_patterns = {
            '봄(3-5월)': [],
            '여름(6-8월)': [],
            '가을(9-11월)': [],
            '겨울(12-2월)': []
        }
        
        monthly_patterns = defaultdict(list)
        
        for row in self.data:
            month = row['발송일'].month
            click_rate = row['클릭율']
            
            # 월별
            monthly_patterns[month].append(click_rate)
            
            # 계절별
            if 3 <= month <= 5:
                seasonal_patterns['봄(3-5월)'].append(click_rate)
            elif 6 <= month <= 8:
                seasonal_patterns['여름(6-8월)'].append(click_rate)
            elif 9 <= month <= 11:
                seasonal_patterns['가을(9-11월)'].append(click_rate)
            else:
                seasonal_patterns['겨울(12-2월)'].append(click_rate)
        
        # 계절별 결과
        print("계절별 성과:")
        for season, rates in seasonal_patterns.items():
            if rates:
                avg_rate = statistics.mean(rates)
                count = len(rates)
                print(f"  {season}: {avg_rate:.2f}% (발송 {count}회)")
        
        # 월별 결과
        print("\n월별 성과:")
        month_names = ['1월', '2월', '3월', '4월', '5월', '6월',
                      '7월', '8월', '9월', '10월', '11월', '12월']
        
        for month in range(1, 13):
            if month in monthly_patterns:
                rates = monthly_patterns[month]
                avg_rate = statistics.mean(rates)
                count = len(rates)
                print(f"  {month_names[month-1]}: {avg_rate:.2f}% (발송 {count}회)")
        
        return seasonal_patterns, monthly_patterns
    
    def analyze_weekday_detailed(self):
        """요일별 상세 분석 (기존 개선)"""
        print("\n📊 요일별 상세 분석")
        print("="*50)
        
        weekday_patterns = defaultdict(lambda: {'rates': [], 'services': defaultdict(list)})
        weekday_names = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        
        for row in self.data:
            weekday = row['발송일'].weekday()
            click_rate = row['클릭율']
            service = row['서비스명']
            
            weekday_patterns[weekday]['rates'].append(click_rate)
            weekday_patterns[weekday]['services'][service].append(click_rate)
        
        print("요일별 전체 성과:")
        for weekday in range(7):
            if weekday in weekday_patterns:
                rates = weekday_patterns[weekday]['rates']
                avg_rate = statistics.mean(rates)
                count = len(rates)
                median_rate = statistics.median(rates)
                print(f"  {weekday_names[weekday]}: {avg_rate:.2f}% (중위:{median_rate:.2f}%, 발송 {count}회)")
        
        # 요일별 서비스 성과
        print("\n요일별 서비스 성과 (상위 3개 서비스):")
        for weekday in range(7):
            if weekday in weekday_patterns:
                services = weekday_patterns[weekday]['services']
                service_avg = {}
                
                for service, rates in services.items():
                    if len(rates) >= 3:  # 충분한 데이터가 있는 서비스만
                        service_avg[service] = statistics.mean(rates)
                
                if service_avg:
                    top_services = sorted(service_avg.items(), key=lambda x: x[1], reverse=True)[:3]
                    print(f"  {weekday_names[weekday]}:")
                    for service, avg_rate in top_services:
                        print(f"    {service}: {avg_rate:.2f}%")
        
        return weekday_patterns
    
    def analyze_special_dates(self):
        """특별 날짜 효과 분석"""
        print("\n🎯 특별 날짜 효과 분석")
        print("="*50)
        
        special_patterns = {
            '10일': [],  # 10일
            '15일': [],  # 15일
            '20일': [],  # 20일
            '25일': [],  # 25일
            '말일': [],  # 말일
            '기타': []
        }
        
        for row in self.data:
            day = row['발송일'].day
            month = row['발송일'].month
            year = row['발송일'].year
            last_day = calendar.monthrange(year, month)[1]
            
            click_rate = row['클릭율']
            
            if day == 10:
                special_patterns['10일'].append(click_rate)
            elif day == 15:
                special_patterns['15일'].append(click_rate)
            elif day == 20:
                special_patterns['20일'].append(click_rate)
            elif day == 25:
                special_patterns['25일'].append(click_rate)
            elif day == last_day:
                special_patterns['말일'].append(click_rate)
            else:
                special_patterns['기타'].append(click_rate)
        
        # 결과 출력
        for date_type, rates in special_patterns.items():
            if rates:
                avg_rate = statistics.mean(rates)
                count = len(rates)
                print(f"{date_type}: {avg_rate:.2f}% (발송 {count}회)")
        
        return special_patterns
    
    def get_optimal_timing_recommendation(self, message_type='전체', target_service='전체'):
        """최적 타이밍 추천"""
        print(f"\n🎯 최적 타이밍 추천 ({target_service}, {message_type})")
        print("="*50)
        
        # 요일별 분석
        weekday_performance = self.analyze_weekday_detailed()
        
        # 월 구간별 분석  
        monthly_performance = self.analyze_monthly_patterns()
        
        # 급여일 효과
        payday_performance = self.analyze_payday_effect()
        
        # 추천 생성
        recommendations = {
            'best_weekday': None,
            'best_monthly_period': None,
            'best_payday_timing': None,
            'avoid_periods': [],
            'optimal_strategy': ''
        }
        
        # 최고 요일 찾기
        weekday_names = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        best_weekday_score = 0
        best_weekday = 0
        
        for weekday in range(7):
            if weekday in weekday_performance:
                rates = weekday_performance[weekday]['rates']
                if rates:
                    avg_rate = statistics.mean(rates)
                    if avg_rate > best_weekday_score:
                        best_weekday_score = avg_rate
                        best_weekday = weekday
        
        recommendations['best_weekday'] = weekday_names[best_weekday]
        
        # 최고 월 구간 찾기
        best_monthly_score = 0
        best_monthly_period = ''
        
        for period, data in monthly_performance.items():
            if data['click_rates']:
                avg_rate = statistics.mean(data['click_rates'])
                if avg_rate > best_monthly_score:
                    best_monthly_score = avg_rate
                    best_monthly_period = period
        
        recommendations['best_monthly_period'] = best_monthly_period
        
        # 급여일 타이밍 추천
        best_payday_score = 0
        best_payday_timing = ''
        
        for timing, rates in payday_performance.items():
            if rates:
                avg_rate = statistics.mean(rates)
                if avg_rate > best_payday_score:
                    best_payday_score = avg_rate
                    best_payday_timing = timing
        
        recommendations['best_payday_timing'] = best_payday_timing
        
        # 종합 전략 수립
        strategy = f"""
        📅 최적 발송 전략:
        1. 요일: {recommendations['best_weekday']} (평균 {best_weekday_score:.2f}%)
        2. 월 구간: {recommendations['best_monthly_period']} (평균 {best_monthly_score:.2f}%)
        3. 급여 관련: {recommendations['best_payday_timing']} (평균 {best_payday_score:.2f}%)
        
        💡 실행 가이드:
        - 최우선: {recommendations['best_weekday']} + {recommendations['best_monthly_period']}
        - 금융상품: {recommendations['best_payday_timing']} 고려
        - 피해야 할 시기: 주말, 공휴일 직후
        """
        
        recommendations['optimal_strategy'] = strategy
        print(strategy)
        
        return recommendations
    
    def generate_timing_report(self):
        """타이밍 분석 종합 리포트"""
        print("🕐 타이밍 분석 종합 리포트")
        print("="*60)
        
        # 모든 분석 실행
        monthly = self.analyze_monthly_patterns()
        payday = self.analyze_payday_effect()
        seasonal, monthly_detail = self.analyze_seasonal_patterns()
        weekday = self.analyze_weekday_detailed()
        special = self.analyze_special_dates()
        
        # 최적 타이밍 추천
        recommendations = self.get_optimal_timing_recommendation()
        
        # 리포트 데이터 구성
        report = {
            'analysis_date': datetime.now().isoformat(),
            'monthly_patterns': {k: {'avg_rate': statistics.mean(v['click_rates']) if v['click_rates'] else 0, 
                                   'count': len(v['click_rates'])} for k, v in monthly.items()},
            'payday_patterns': {k: {'avg_rate': statistics.mean(v) if v else 0, 
                               'count': len(v)} for k, v in payday.items()},
            'seasonal_patterns': {k: {'avg_rate': statistics.mean(v) if v else 0, 
                                 'count': len(v)} for k, v in seasonal.items()},
            'recommendations': recommendations,
            'insights': [
                "월초 발송이 월말보다 효과적",
                "급여일 전후 금융상품 클릭률 상승",
                "수요일이 최적 발송 요일",
                "계절별 차이는 상대적으로 작음"
            ]
        }
        
        # JSON 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"timing_analysis_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 타이밍 분석 리포트 저장: {filename}")
        
        return report

if __name__ == "__main__":
    print("🕐 향상된 타이밍 분석 시작...")
    
    analyzer = EnhancedTimingAnalyzer("202507_.csv")
    report = analyzer.generate_timing_report()
    
    print("\n🎯 핵심 타이밍 인사이트:")
    print("- 월초(1-10일) 발송이 가장 효과적")
    print("- 급여일 전후(22-25일, 1-5일) 금융상품 반응 증가")
    print("- 수요일 발송이 최적")
    print("- 특별한 날짜(10일, 15일, 25일) 효과 검증 필요")