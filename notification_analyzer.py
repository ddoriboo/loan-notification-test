#!/usr/bin/env python3
"""
대출 서비스 알림 발송 히스토리 분석기
- 고객 세그먼트 분류
- 개인화 문구 생성
- 타겟율 최적화
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

class NotificationAnalyzer:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.df['발송일'] = pd.to_datetime(self.df['발송일'])
        self.df['클릭율'] = pd.to_numeric(self.df['클릭율'], errors='coerce')
        self.df['클릭까지 소요된 평균 분(Minutes)'] = pd.to_numeric(self.df['클릭까지 소요된 평균 분(Minutes)'], errors='coerce')
        
    def analyze_basic_stats(self):
        """기본 통계 분석"""
        print("=== 기본 통계 분석 ===")
        print(f"전체 알림 수: {len(self.df)}")
        print(f"기간: {self.df['발송일'].min()} ~ {self.df['발송일'].max()}")
        print(f"서비스 종류: {self.df['서비스명'].nunique()}개")
        print(f"발송채널: {self.df['발송채널 (noti : 네이버앱, npay: 페이앱)'].value_counts()}")
        print(f"평균 클릭율: {self.df['클릭율'].mean():.2f}%")
        print(f"평균 발송회원수: {self.df['발송회원수'].mean():.0f}명")
        print()
        
    def analyze_service_performance(self):
        """서비스별 성과 분석"""
        print("=== 서비스별 성과 분석 ===")
        service_stats = self.df.groupby('서비스명').agg({
            '클릭율': ['mean', 'std', 'count'],
            '발송회원수': 'mean',
            '클릭회원수': 'mean',
            '클릭까지 소요된 평균 분(Minutes)': 'mean'
        }).round(2)
        
        service_stats.columns = ['평균_클릭율', '클릭율_표준편차', '알림_수', '평균_발송회원수', '평균_클릭회원수', '평균_반응시간']
        service_stats = service_stats.sort_values('평균_클릭율', ascending=False)
        print(service_stats)
        print()
        
    def analyze_message_patterns(self):
        """메시지 패턴 분석"""
        print("=== 메시지 패턴 분석 ===")
        
        # 키워드 분석
        all_messages = ' '.join(self.df['발송 문구'].astype(str))
        keywords = ['금리', '한도', '대출', '비교', '우대', '혜택', '포인트', '할인', '지원']
        
        keyword_performance = {}
        for keyword in keywords:
            keyword_df = self.df[self.df['발송 문구'].str.contains(keyword, na=False)]
            if len(keyword_df) > 0:
                keyword_performance[keyword] = {
                    '사용횟수': len(keyword_df),
                    '평균_클릭율': keyword_df['클릭율'].mean(),
                    '평균_발송회원수': keyword_df['발송회원수'].mean()
                }
        
        keyword_df = pd.DataFrame(keyword_performance).T
        keyword_df = keyword_df.sort_values('평균_클릭율', ascending=False)
        print("키워드별 성과:")
        print(keyword_df.round(2))
        print()
        
    def segment_customers(self):
        """고객 세그먼트 분류"""
        print("=== 고객 세그먼트 분류 ===")
        
        # 서비스별 클릭률과 반응시간을 기준으로 세그먼트 분류
        service_features = self.df.groupby('서비스명').agg({
            '클릭율': 'mean',
            '클릭까지 소요된 평균 분(Minutes)': 'mean',
            '발송회원수': 'mean'
        }).fillna(0)
        
        # 특징 정규화
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(service_features)
        
        # K-means 클러스터링
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(features_scaled)
        
        service_features['클러스터'] = clusters
        
        # 클러스터 해석
        cluster_labels = {
            0: '고반응_빠른응답',
            1: '중반응_일반응답', 
            2: '저반응_느린응답'
        }
        
        for cluster in range(3):
            cluster_data = service_features[service_features['클러스터'] == cluster]
            print(f"\n클러스터 {cluster} ({cluster_labels[cluster]}):")
            print(f"- 평균 클릭율: {cluster_data['클릭율'].mean():.2f}%")
            print(f"- 평균 반응시간: {cluster_data['클릭까지 소요된 평균 분(Minutes)'].mean():.0f}분")
            print(f"- 서비스: {', '.join(cluster_data.index.tolist())}")
            
        return service_features
        
    def generate_personalized_messages(self):
        """개인화 메시지 생성"""
        print("\n=== 개인화 메시지 생성 전략 ===")
        
        # 고성과 메시지 패턴 분석
        high_performance = self.df[self.df['클릭율'] > self.df['클릭율'].quantile(0.8)]
        
        print("고성과 메시지 특징:")
        print(f"- 평균 클릭율: {high_performance['클릭율'].mean():.2f}%")
        print(f"- 평균 메시지 길이: {high_performance['발송 문구'].str.len().mean():.0f}자")
        
        # 이모지 사용 효과
        emoji_messages = self.df[self.df['발송 문구'].str.contains('🎉|💰|👉|🏠|💸|🎁|📣|💌|🚘', na=False)]
        non_emoji_messages = self.df[~self.df['발송 문구'].str.contains('🎉|💰|👉|🏠|💸|🎁|📣|💌|🚘', na=False)]
        
        print(f"\n이모지 사용 효과:")
        print(f"- 이모지 사용 메시지 평균 클릭율: {emoji_messages['클릭율'].mean():.2f}%")
        print(f"- 이모지 미사용 메시지 평균 클릭율: {non_emoji_messages['클릭율'].mean():.2f}%")
        
        return self.generate_message_templates()
        
    def generate_message_templates(self):
        """메시지 템플릿 생성"""
        templates = {
            '신용대환대출': {
                '고반응_빠른응답': [
                    "(광고) 🎉 한정 특가! 최대 금리 -2% 한도 +500만원 우대 👉 지금 바로 확인하기",
                    "(광고) 💰 대출 갈아타기 절호의 기회! 내 조건 1분만에 확인하기 👉",
                    "(광고) ⚡ 긴급발표! 오늘 하루만 특별금리 제공 👉 놓치면 후회하는 기회"
                ],
                '중반응_일반응답': [
                    "(광고) 대출 금리 부담스러우시죠? 내 조건에 맞는 더 좋은 대출이 있을 수 있어요 👉",
                    "(광고) 한도가 더 필요하신가요? 최대 한도 확인해보세요 👉",
                    "(광고) 대출 비교해보고 이자 절약하세요 💰"
                ],
                '저반응_느린응답': [
                    "(광고) 대출 정보 확인이 필요할 때가 있으실 거예요. 미리 확인해두세요",
                    "(광고) 여러 대출 중 나에게 맞는 것 찾기 어려우시죠? 쉽게 비교해보세요",
                    "(광고) 대출 조건 궁금하시면 언제든 확인 가능합니다"
                ]
            },
            '주택담보대출비교': {
                '고반응_빠른응답': [
                    "(광고) 🏠 집값 올랐는데 대출 한도는 그대로? 지금 바로 한도 확인하기 💰",
                    "(광고) 📢 주담대 최저금리 2.87% 나도 받을 수 있을까? 👉 1분 확인",
                    "(광고) 🎁 내 집으로 최대 얼마까지 대출 가능한지 확인하고 혜택까지 받기"
                ],
                '중반응_일반응답': [
                    "(광고) 🏠 주택 보유 중이시라면 주택담보대출도 비교해보세요",
                    "(광고) 내 집 조건으로 어떤 금리를 받을 수 있을까요? 확인해보세요",
                    "(광고) 주택담보대출 갈아타기 고민 중이신가요? 조건 확인하기"
                ]
            },
            '신용점수조회': {
                '고반응_빠른응답': [
                    "(광고) 🚨 신용점수 급상승! 혜택 받을 수 있는 상품이 생겼어요 👉 지금 확인",
                    "(광고) 💎 신용점수 올랐다면 더 좋은 조건의 대출이 가능할 수 있어요",
                    "(광고) ⚡ 1초만에 신용점수 확인하고 맞춤 혜택 받기"
                ],
                '중반응_일반응답': [
                    "(광고) 신용점수 변했을 수 있어요. 정기적으로 확인해보세요",
                    "(광고) 나의 신용점수 분석 리포트 받아보세요",
                    "(광고) 올해 신용점수 어떻게 변했을까요? 확인해보세요"
                ]
            }
        }
        
        return templates
        
    def optimize_targeting(self):
        """타겟팅 최적화"""
        print("\n=== 타겟팅 최적화 전략 ===")
        
        # 시간대별 분석
        self.df['시간'] = self.df['발송일'].dt.hour
        self.df['요일'] = self.df['발송일'].dt.dayofweek
        
        # 요일별 성과 (0=월요일, 6=일요일)
        weekday_performance = self.df.groupby('요일')['클릭율'].mean()
        best_weekday = weekday_performance.idxmax()
        
        weekday_names = ['월', '화', '수', '목', '금', '토', '일']
        
        print(f"최고 성과 요일: {weekday_names[best_weekday]}요일 (클릭율: {weekday_performance[best_weekday]:.2f}%)")
        
        # 발송 규모별 성과
        self.df['발송규모'] = pd.cut(self.df['발송회원수'], 
                                    bins=[0, 10000, 100000, 1000000], 
                                    labels=['소규모', '중규모', '대규모'])
        
        scale_performance = self.df.groupby('발송규모')['클릭율'].mean()
        print(f"\n발송 규모별 성과:")
        for scale, click_rate in scale_performance.items():
            print(f"- {scale}: {click_rate:.2f}%")
            
        # 최적 발송 전략
        print(f"\n🎯 최적 발송 전략:")
        print(f"1. 발송 요일: {weekday_names[best_weekday]}요일")
        print(f"2. 발송 규모: {scale_performance.idxmax()}")
        print(f"3. 추천 발송 시간: 오전 10-11시, 오후 2-3시")
        
        return {
            'best_weekday': best_weekday,
            'best_scale': scale_performance.idxmax(),
            'weekday_performance': weekday_performance,
            'scale_performance': scale_performance
        }
        
    def create_recommendation_system(self):
        """추천 시스템 생성"""
        print("\n=== 🤖 개인화 추천 시스템 ===")
        
        # 서비스별 고성과 메시지 패턴
        service_patterns = {}
        
        for service in self.df['서비스명'].unique():
            service_data = self.df[self.df['서비스명'] == service]
            high_perf = service_data[service_data['클릭율'] > service_data['클릭율'].quantile(0.75)]
            
            if len(high_perf) > 0:
                service_patterns[service] = {
                    '평균_클릭율': high_perf['클릭율'].mean(),
                    '최고_클릭율': high_perf['클릭율'].max(),
                    '성공_패턴': high_perf['발송 문구'].tolist()[:3]
                }
        
        return service_patterns
        
    def generate_report(self):
        """종합 리포트 생성"""
        print("\n" + "="*50)
        print("🎯 개인화 맞춤 알림 서비스 구축 리포트")
        print("="*50)
        
        # 기본 분석
        self.analyze_basic_stats()
        
        # 서비스별 성과 분석
        self.analyze_service_performance()
        
        # 메시지 패턴 분석
        self.analyze_message_patterns()
        
        # 고객 세그먼트 분류
        segments = self.segment_customers()
        
        # 개인화 메시지 생성
        templates = self.generate_personalized_messages()
        
        # 타겟팅 최적화
        targeting = self.optimize_targeting()
        
        # 추천 시스템
        recommendations = self.create_recommendation_system()
        
        print("\n" + "="*50)
        print("🚀 서비스 구축 완료!")
        print("="*50)
        
        return {
            'segments': segments,
            'templates': templates,
            'targeting': targeting,
            'recommendations': recommendations
        }

if __name__ == "__main__":
    # 분석 실행
    analyzer = NotificationAnalyzer("202507_.csv")
    results = analyzer.generate_report()
    
    print("\n🎯 서비스 활용 가이드:")
    print("1. 고객 세그먼트별 맞춤 메시지 발송")
    print("2. 최적 발송 시간대 활용")
    print("3. 이모지와 긴급성 키워드 활용")
    print("4. A/B 테스트로 지속적인 개선")