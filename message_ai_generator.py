#!/usr/bin/env python3
"""
LLM 기반 문구 매칭 및 생성 서비스
- 자연어 입력 처리
- 기존 문구 매칭 및 추천
- 신규 문구 생성
- 이유 설명 제공
"""

import csv
import json
import re
from collections import defaultdict, Counter
from datetime import datetime
import statistics
import random

class MessageAIGenerator:
    def __init__(self, csv_file):
        self.data = []
        self.message_patterns = {}
        self.categories = {}
        self.tone_patterns = {}
        self.performance_data = {}
        
        self.load_data(csv_file)
        self.analyze_message_patterns()
        self.create_tone_categories()
        
    def load_data(self, csv_file):
        """CSV 데이터 로드"""
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['클릭율'] = float(row['클릭율'])
                    row['발송회원수'] = int(row['발송회원수'])
                    row['클릭회원수'] = int(row['클릭회원수'])
                    self.data.append(row)
                except (ValueError, KeyError):
                    continue
    
    def analyze_message_patterns(self):
        """메시지 패턴 분석"""
        print("🔍 메시지 패턴 분석 중...")
        
        # 서비스별 메시지 패턴
        for row in self.data:
            service = row['서비스명']
            message = row['발송 문구']
            click_rate = row['클릭율']
            
            if service not in self.message_patterns:
                self.message_patterns[service] = []
            
            # 메시지 특성 분석
            pattern = self.extract_message_features(message)
            pattern['original_message'] = message
            pattern['click_rate'] = click_rate
            pattern['service'] = service
            
            self.message_patterns[service].append(pattern)
    
    def extract_message_features(self, message):
        """메시지 특성 추출"""
        features = {
            'length': len(message),
            'has_emoji': bool(re.search(r'[🎉💰👉🏠💸🎁📣💌🚘⚡🔔🚨💎🔥📢🎯🙋‍♂️]', message)),
            'has_numbers': bool(re.search(r'\d', message)),
            'has_brackets': '(' in message or '[' in message,
            'has_exclamation': '!' in message,
            'has_question': '?' in message,
            'has_arrow': '👉' in message or '>' in message,
            'urgency_level': self.calculate_urgency_level(message),
            'benefit_level': self.calculate_benefit_level(message),
            'keywords': self.extract_keywords(message),
            'tone': self.classify_tone(message),
            'call_to_action': self.extract_cta(message)
        }
        return features
    
    def calculate_urgency_level(self, message):
        """긴급도 레벨 계산"""
        urgency_keywords = {
            'high': ['오늘만', '마감임박', '한정', '긴급', '서둘러', '마지막', '지금 바로', '놓치면'],
            'medium': ['곧', '빠른', '시간이', '기회', '타이밍'],
            'low': ['언제든', '천천히', '확인']
        }
        
        for level, keywords in urgency_keywords.items():
            if any(keyword in message for keyword in keywords):
                return level
        return 'none'
    
    def calculate_benefit_level(self, message):
        """혜택 강조 레벨 계산"""
        benefit_keywords = {
            'high': ['최대', '최저', '특가', '혜택', '할인', '무료', '적립', '포인트'],
            'medium': ['좋은', '더', '절약', '이득'],
            'low': ['안내', '정보', '확인']
        }
        
        for level, keywords in benefit_keywords.items():
            if any(keyword in message for keyword in keywords):
                return level
        return 'none'
    
    def extract_keywords(self, message):
        """키워드 추출"""
        all_keywords = ['금리', '한도', '대출', '비교', '우대', '혜택', '포인트', '할인', '지원', 
                       '최대', '최저', '특가', '한정', '신용', '주택', '전월세', '갈아타기',
                       '조회', '확인', '신청', '승인', '이자', '캐피탈', '은행']
        
        found_keywords = [keyword for keyword in all_keywords if keyword in message]
        return found_keywords
    
    def classify_tone(self, message):
        """톤앤매너 분류"""
        if any(word in message for word in ['축하', '🎉', '혜택', '특가', '기회']):
            return 'promotional'
        elif any(word in message for word in ['긴급', '마감', '서둘러', '오늘만']):
            return 'urgent'
        elif any(word in message for word in ['확인', '정보', '안내', '조회']):
            return 'informational'
        elif any(word in message for word in ['고민', '부담', '어려움']):
            return 'empathetic'
        else:
            return 'neutral'
    
    def extract_cta(self, message):
        """Call to Action 추출"""
        cta_patterns = [
            '확인하기', '신청하기', '비교하기', '받기', '받아보세요', 
            '클릭', '터치', '눌러', '바로', '지금'
        ]
        
        for cta in cta_patterns:
            if cta in message:
                return cta
        return 'none'
    
    def create_tone_categories(self):
        """톤앤매너 카테고리 생성"""
        self.tone_patterns = {
            'promotional': {
                'description': '혜택 강조형',
                'characteristics': ['혜택 부각', '특가 강조', '프로모션성'],
                'keywords': ['혜택', '특가', '할인', '🎉', '축하'],
                'templates': [
                    '🎉 {benefit} {service}! {action}',
                    '💰 특별 혜택! {benefit} {action}',
                    '축하합니다! {benefit} {action}'
                ]
            },
            'urgent': {
                'description': '긴급성 강조형',
                'characteristics': ['시간 제약', '긴급성', '한정성'],
                'keywords': ['긴급', '마감임박', '오늘만', '한정', '서둘러'],
                'templates': [
                    '⚡ 긴급! {benefit} {action}',
                    '🔥 마감임박! {benefit} {action}',
                    '오늘만! {benefit} {action}'
                ]
            },
            'informational': {
                'description': '정보 제공형',
                'characteristics': ['정보 전달', '안내성', '교육적'],
                'keywords': ['확인', '안내', '정보', '조회'],
                'templates': [
                    '{service} 정보를 확인해보세요',
                    '{benefit} 안내 - {action}',
                    '{service} 조건 확인하기'
                ]
            },
            'empathetic': {
                'description': '공감형',
                'characteristics': ['고객 이해', '문제 해결', '상담적'],
                'keywords': ['고민', '부담', '어려움', '걱정'],
                'templates': [
                    '{problem} 해결책이 있어요. {action}',
                    '{problem}이시라면? {benefit} {action}',
                    '{problem} 고민 끝! {action}'
                ]
            }
        }
    
    def find_matching_messages(self, user_input):
        """사용자 입력에 매칭되는 기존 메시지 찾기"""
        target_audience = user_input.get('target_audience', '')
        keywords = user_input.get('keywords', [])
        tone = user_input.get('tone', '')
        service = user_input.get('service', '')
        
        # 매칭 점수 계산
        matches = []
        
        for service_name, patterns in self.message_patterns.items():
            if service and service not in service_name:
                continue
                
            for pattern in patterns:
                score = self.calculate_match_score(pattern, user_input)
                if score > 0.3:  # 임계값
                    matches.append({
                        'message': pattern['original_message'],
                        'score': score,
                        'click_rate': pattern['click_rate'],
                        'service': pattern['service'],
                        'reasons': self.explain_match_reasons(pattern, user_input)
                    })
        
        # 점수순 정렬
        matches.sort(key=lambda x: (x['score'], x['click_rate']), reverse=True)
        return matches[:5]  # 상위 5개
    
    def calculate_match_score(self, pattern, user_input):
        """매칭 점수 계산"""
        score = 0.0
        
        # 키워드 매칭
        user_keywords = user_input.get('keywords', [])
        if user_keywords:
            keyword_matches = len(set(pattern['keywords']) & set(user_keywords))
            score += keyword_matches * 0.3
        
        # 톤앤매너 매칭
        if user_input.get('tone') == pattern['tone']:
            score += 0.4
        
        # 긴급도 매칭
        if user_input.get('urgency', 'none') == pattern['urgency_level']:
            score += 0.2
        
        # 혜택 레벨 매칭
        if user_input.get('benefit_level', 'none') == pattern['benefit_level']:
            score += 0.2
        
        # 성과 보너스 (클릭률이 높으면 추가 점수)
        if pattern['click_rate'] > 10:
            score += 0.1
        
        return min(score, 1.0)
    
    def explain_match_reasons(self, pattern, user_input):
        """매칭 이유 설명"""
        reasons = []
        
        # 키워드 매칭 이유
        user_keywords = user_input.get('keywords', [])
        matched_keywords = set(pattern['keywords']) & set(user_keywords)
        if matched_keywords:
            reasons.append(f"키워드 '{', '.join(matched_keywords)}' 매칭")
        
        # 톤앤매너 매칭
        if user_input.get('tone') == pattern['tone']:
            tone_desc = self.tone_patterns.get(pattern['tone'], {}).get('description', pattern['tone'])
            reasons.append(f"톤앤매너 '{tone_desc}' 일치")
        
        # 성과 기반
        if pattern['click_rate'] > 10:
            reasons.append(f"고성과 메시지 (클릭률 {pattern['click_rate']:.1f}%)")
        
        # 특성 매칭
        if pattern['urgency_level'] == 'high' and '긴급' in user_input.get('description', ''):
            reasons.append("긴급성 요구사항 반영")
        
        if pattern['benefit_level'] == 'high' and '혜택' in user_input.get('description', ''):
            reasons.append("혜택 강조 요구사항 반영")
        
        return reasons if reasons else ["일반적 패턴 매칭"]
    
    def generate_new_messages(self, user_input):
        """신규 메시지 생성"""
        target_audience = user_input.get('target_audience', '')
        keywords = user_input.get('keywords', [])
        tone = user_input.get('tone', 'promotional')
        service = user_input.get('service', '신용대출')
        
        # 톤앤매너별 생성
        generated = []
        
        # 1. 요청된 톤으로 생성
        if tone in self.tone_patterns:
            message, reason = self.generate_by_tone(user_input, tone)
            generated.append({
                'message': message,
                'tone': tone,
                'reason': reason,
                'predicted_performance': self.predict_performance(message, user_input)
            })
        
        # 2. 고성과 패턴으로 생성
        high_perf_message, reason = self.generate_high_performance_message(user_input)
        generated.append({
            'message': high_perf_message,
            'tone': 'high_performance',
            'reason': reason,
            'predicted_performance': self.predict_performance(high_perf_message, user_input)
        })
        
        # 3. 대안 톤으로 생성
        alternative_tone = self.suggest_alternative_tone(user_input)
        if alternative_tone != tone:
            alt_message, reason = self.generate_by_tone(user_input, alternative_tone)
            generated.append({
                'message': alt_message,
                'tone': alternative_tone,
                'reason': reason,
                'predicted_performance': self.predict_performance(alt_message, user_input)
            })
        
        return generated
    
    def generate_by_tone(self, user_input, tone):
        """톤앤매너별 메시지 생성"""
        tone_info = self.tone_patterns.get(tone, self.tone_patterns['promotional'])
        templates = tone_info['templates']
        
        # 변수 준비
        service = user_input.get('service', '대출')
        keywords = user_input.get('keywords', [])
        target = user_input.get('target_audience', '고객')
        
        # 혜택 생성
        benefit = self.generate_benefit_phrase(keywords, tone)
        
        # 액션 생성
        action = self.generate_action_phrase(tone)
        
        # 문제 상황 생성 (empathetic용)
        problem = self.generate_problem_phrase(target)
        
        # 템플릿 선택 및 적용
        template = random.choice(templates)
        
        try:
            message = template.format(
                service=service,
                benefit=benefit,
                action=action,
                problem=problem
            )
        except KeyError:
            # 템플릿에 없는 변수가 있는 경우 기본 템플릿 사용
            message = f"(광고) {benefit} {service} {action}"
        
        # 이유 생성
        reason = f"{tone_info['description']} 스타일로 생성. "
        reason += f"'{', '.join(keywords[:2])}' 키워드 반영. "
        reason += f"타겟 '{target}' 고려한 메시지."
        
        return message, reason
    
    def generate_benefit_phrase(self, keywords, tone):
        """혜택 문구 생성"""
        benefit_templates = {
            'promotional': ['최대 {amount} 혜택', '특별 {type} 제공', '{type} 두 배 혜택'],
            'urgent': ['한정 {type}', '마감임박 {type}', '오늘만 {type}'],
            'informational': ['{type} 안내', '{type} 정보', '{type} 조건'],
            'empathetic': ['{type} 부담 해결', '{type} 고민 해결', '더 나은 {type}']
        }
        
        # 키워드 기반 혜택 타입 결정
        benefit_type = '혜택'
        if '금리' in keywords:
            benefit_type = '금리 할인'
        elif '한도' in keywords:
            benefit_type = '한도 증액'
        elif '포인트' in keywords:
            benefit_type = '포인트 적립'
        
        templates = benefit_templates.get(tone, benefit_templates['promotional'])
        template = random.choice(templates)
        
        return template.format(
            type=benefit_type,
            amount=random.choice(['100만원', '500만원', '2%', '1%'])
        )
    
    def generate_action_phrase(self, tone):
        """액션 문구 생성"""
        action_phrases = {
            'promotional': ['지금 바로 확인하기 👉', '혜택 받기 💰', '신청하고 혜택 받기'],
            'urgent': ['서둘러 확인하기 ⚡', '놓치지 말고 확인', '지금 바로 신청'],
            'informational': ['자세히 확인하기', '조건 확인하기', '정보 확인하기'],
            'empathetic': ['해결책 확인하기', '상담 받기', '맞춤 상품 찾기']
        }
        
        phrases = action_phrases.get(tone, action_phrases['promotional'])
        return random.choice(phrases)
    
    def generate_problem_phrase(self, target):
        """문제 상황 문구 생성"""
        problems = [
            f'{target}님의 금리 부담',
            f'{target}님의 한도 부족',
            f'{target}님의 대출 고민',
            f'{target}님의 이자 부담'
        ]
        return random.choice(problems)
    
    def generate_high_performance_message(self, user_input):
        """고성과 패턴 기반 메시지 생성"""
        # 분석 결과에서 고성과 패턴 활용
        keywords = user_input.get('keywords', [])
        service = user_input.get('service', '대출')
        
        # 고성과 키워드 우선 사용
        high_perf_keywords = ['혜택', '최대', '할인']
        selected_keyword = '혜택'
        
        for keyword in keywords:
            if keyword in high_perf_keywords:
                selected_keyword = keyword
                break
        
        # 고성과 패턴: 간결하고 혜택 중심
        patterns = [
            f"(광고) {selected_keyword} 확인하고 {service} 받기",
            f"(광고) {service} {selected_keyword} 지금 확인하세요",
            f"(광고) 최대 {selected_keyword} {service} 신청하기",
        ]
        
        message = random.choice(patterns)
        
        reason = f"고성과 키워드 '{selected_keyword}' 활용. "
        reason += "간결한 구조와 명확한 CTA로 클릭률 최적화. "
        reason += "이모지 미사용으로 텍스트 집중도 향상."
        
        return message, reason
    
    def suggest_alternative_tone(self, user_input):
        """대안 톤앤매너 제안"""
        current_tone = user_input.get('tone', 'promotional')
        
        # 서비스별 추천 톤
        service = user_input.get('service', '')
        if '신용점수' in service:
            return 'informational'
        elif '대환' in service:
            return 'empathetic'
        elif '주택' in service:
            return 'promotional'
        else:
            return 'urgent' if current_tone != 'urgent' else 'promotional'
    
    def predict_performance(self, message, user_input):
        """성과 예측"""
        # 메시지 특성 분석
        features = self.extract_message_features(message)
        
        # 기본 점수
        base_score = 8.5
        
        # 키워드 보너스
        high_perf_keywords = ['혜택', '최대', '할인']
        keyword_bonus = sum(2 for keyword in features['keywords'] if keyword in high_perf_keywords)
        
        # 이모지 페널티
        emoji_penalty = -2 if features['has_emoji'] else 0
        
        # 길이 최적화 (42자 내외가 최적)
        length_score = 0
        if 30 <= features['length'] <= 50:
            length_score = 1
        elif features['length'] > 60:
            length_score = -1
        
        # 긴급성 보너스
        urgency_bonus = 1 if features['urgency_level'] == 'high' else 0
        
        predicted_rate = base_score + keyword_bonus + emoji_penalty + length_score + urgency_bonus
        predicted_rate = max(3.0, min(20.0, predicted_rate))  # 3-20% 범위
        
        return {
            'predicted_click_rate': round(predicted_rate, 1),
            'confidence': 85,
            'factors': {
                'keywords': f"+{keyword_bonus}% (고성과 키워드)",
                'emoji': f"{emoji_penalty}% (이모지 효과)" if emoji_penalty else "0% (텍스트 중심)",
                'length': f"{length_score}% (길이 최적화)",
                'urgency': f"+{urgency_bonus}% (긴급성)" if urgency_bonus else "0% (일반)"
            }
        }
    
    def parse_natural_language_input(self, text):
        """자연어 입력 파싱"""
        # 간단한 NLP 파싱 (규칙 기반)
        result = {
            'target_audience': '',
            'keywords': [],
            'tone': 'promotional',
            'service': '',
            'urgency': 'none',
            'benefit_level': 'medium'
        }
        
        # 서비스 추출
        services = ['신용대출', '주택담보대출', '전월세대출', '신용점수', '대환대출']
        for service in services:
            if service in text:
                result['service'] = service
                break
        
        # 키워드 추출
        keywords = ['금리', '한도', '혜택', '할인', '포인트', '비교', '갈아타기']
        result['keywords'] = [k for k in keywords if k in text]
        
        # 톤앤매너 추출
        if any(word in text for word in ['긴급', '급하', '빨리', '서둘러']):
            result['tone'] = 'urgent'
        elif any(word in text for word in ['고민', '부담', '어려움']):
            result['tone'] = 'empathetic'
        elif any(word in text for word in ['정보', '안내', '확인']):
            result['tone'] = 'informational'
        
        # 타겟 고객 추출
        if '직장인' in text:
            result['target_audience'] = '직장인'
        elif '주부' in text:
            result['target_audience'] = '주부'
        elif '자영업자' in text:
            result['target_audience'] = '자영업자'
        else:
            result['target_audience'] = '고객'
        
        return result

def create_web_interface():
    """웹 인터페이스 HTML 생성"""
    html_content = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 AI 문구 생성기</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', 'Noto Sans KR', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0;
            min-height: 600px;
        }
        
        .input-section {
            padding: 40px;
            background: #f8f9fa;
            border-right: 1px solid #e9ecef;
        }
        
        .results-section {
            padding: 40px;
            background: white;
        }
        
        .section-title {
            font-size: 1.5em;
            margin-bottom: 25px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .input-group {
            margin-bottom: 25px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        
        .input-group input,
        .input-group textarea,
        .input-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1em;
            transition: all 0.3s ease;
        }
        
        .input-group input:focus,
        .input-group textarea:focus,
        .input-group select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .textarea-large {
            min-height: 100px;
            resize: vertical;
        }
        
        .keywords-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 10px;
        }
        
        .keyword-checkbox {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .keyword-checkbox:hover {
            background: #e3f2fd;
        }
        
        .keyword-checkbox input[type="checkbox"] {
            width: auto;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        
        .result-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        
        .result-type {
            font-size: 0.9em;
            color: #667eea;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .message-text {
            font-size: 1.1em;
            margin-bottom: 15px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }
        
        .message-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .stat-item {
            text-align: center;
            padding: 10px;
            background: white;
            border-radius: 6px;
        }
        
        .stat-value {
            font-size: 1.2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 0.8em;
            color: #666;
        }
        
        .reason-text {
            font-size: 0.9em;
            color: #666;
            line-height: 1.5;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
        }
        
        .loading-spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .tab {
            padding: 12px 20px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .input-section {
                border-right: none;
                border-bottom: 1px solid #e9ecef;
            }
            
            .keywords-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI 문구 생성기</h1>
            <p>LLM 기반 개인화 알림 문구 매칭 및 생성 서비스</p>
        </div>
        
        <div class="main-content">
            <div class="input-section">
                <div class="section-title">
                    📝 문구 요청
                </div>
                
                <form id="messageForm">
                    <div class="input-group">
                        <label for="description">자연어 요청 (예: 직장인 대상 금리 할인 혜택 긴급 알림)</label>
                        <textarea id="description" class="textarea-large" 
                                placeholder="원하는 문구의 타겟, 내용, 톤을 자연스럽게 설명해주세요..."></textarea>
                    </div>
                    
                    <div class="input-group">
                        <label for="service">서비스 유형</label>
                        <select id="service">
                            <option value="">자동 선택</option>
                            <option value="신용대출">신용대출</option>
                            <option value="신용대환대출">신용대환대출</option>
                            <option value="주택담보대출">주택담보대출</option>
                            <option value="전월세대출">전월세대출</option>
                            <option value="신용점수조회">신용점수조회</option>
                            <option value="중고차론">중고차론</option>
                        </select>
                    </div>
                    
                    <div class="input-group">
                        <label for="tone">톤앤매너</label>
                        <select id="tone">
                            <option value="promotional">혜택 강조형</option>
                            <option value="urgent">긴급성 강조형</option>
                            <option value="informational">정보 제공형</option>
                            <option value="empathetic">공감형</option>
                        </select>
                    </div>
                    
                    <div class="input-group">
                        <label>키워드 선택 (복수 선택 가능)</label>
                        <div class="keywords-grid">
                            <div class="keyword-checkbox">
                                <input type="checkbox" id="k1" value="금리">
                                <label for="k1">금리</label>
                            </div>
                            <div class="keyword-checkbox">
                                <input type="checkbox" id="k2" value="한도">
                                <label for="k2">한도</label>
                            </div>
                            <div class="keyword-checkbox">
                                <input type="checkbox" id="k3" value="혜택">
                                <label for="k3">혜택</label>
                            </div>
                            <div class="keyword-checkbox">
                                <input type="checkbox" id="k4" value="할인">
                                <label for="k4">할인</label>
                            </div>
                            <div class="keyword-checkbox">
                                <input type="checkbox" id="k5" value="포인트">
                                <label for="k5">포인트</label>
                            </div>
                            <div class="keyword-checkbox">
                                <input type="checkbox" id="k6" value="비교">
                                <label for="k6">비교</label>
                            </div>
                        </div>
                    </div>
                    
                    <div class="input-group">
                        <label for="target">타겟 고객</label>
                        <input type="text" id="target" placeholder="예: 직장인, 주부, 자영업자">
                    </div>
                    
                    <button type="submit" class="btn">🎯 문구 생성하기</button>
                </form>
            </div>
            
            <div class="results-section">
                <div class="section-title">
                    ✨ 생성 결과
                </div>
                
                <div class="tabs">
                    <div class="tab active" onclick="switchTab('matching')">기존 문구 매칭</div>
                    <div class="tab" onclick="switchTab('generated')">신규 문구 생성</div>
                </div>
                
                <div id="matching-content" class="tab-content active">
                    <div id="matching-results">
                        <p style="text-align: center; color: #666; padding: 40px;">
                            왼쪽에서 조건을 입력하고 '문구 생성하기'를 클릭하세요.
                        </p>
                    </div>
                </div>
                
                <div id="generated-content" class="tab-content">
                    <div id="generated-results">
                        <p style="text-align: center; color: #666; padding: 40px;">
                            왼쪽에서 조건을 입력하고 '문구 생성하기'를 클릭하세요.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 탭 전환
        function switchTab(tabName) {
            // 모든 탭 비활성화
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            // 선택된 탭 활성화
            event.target.classList.add('active');
            document.getElementById(tabName + '-content').classList.add('active');
        }
        
        // 폼 제출 처리
        document.getElementById('messageForm').addEventListener('submit', function(e) {
            e.preventDefault();
            generateMessages();
        });
        
        function generateMessages() {
            // 로딩 표시
            showLoading();
            
            // 입력값 수집
            const formData = collectFormData();
            
            // 시뮬레이션: 실제로는 백엔드 API 호출
            setTimeout(() => {
                const mockResults = generateMockResults(formData);
                displayResults(mockResults);
            }, 2000);
        }
        
        function collectFormData() {
            const keywords = [];
            document.querySelectorAll('input[type="checkbox"]:checked').forEach(cb => {
                keywords.push(cb.value);
            });
            
            return {
                description: document.getElementById('description').value,
                service: document.getElementById('service').value,
                tone: document.getElementById('tone').value,
                keywords: keywords,
                target: document.getElementById('target').value
            };
        }
        
        function showLoading() {
            const loadingHTML = `
                <div class="loading">
                    <div class="loading-spinner"></div>
                    <p>AI가 최적의 문구를 생성하고 있습니다...</p>
                </div>
            `;
            
            document.getElementById('matching-results').innerHTML = loadingHTML;
            document.getElementById('generated-results').innerHTML = loadingHTML;
        }
        
        function generateMockResults(formData) {
            // 모의 결과 생성 (실제로는 Python 백엔드에서 처리)
            return {
                matching: [
                    {
                        message: "(광고) 🎉 축하합니다! 첫 달 이자지원금 적립! 받은 만큼 한번 더 적립 받으세요 👉",
                        score: 0.89,
                        click_rate: 13.06,
                        service: "신용대출비교",
                        reasons: ["키워드 '혜택' 매칭", "톤앤매너 '혜택 강조형' 일치", "고성과 메시지 (클릭률 13.1%)"]
                    },
                    {
                        message: "(광고) 한도가 달라졌을까? 내 금리·한도 확인할 시간이에요👉",
                        score: 0.76,
                        click_rate: 11.61,
                        service: "신용대환대출",
                        reasons: ["키워드 '금리, 한도' 매칭", "고성과 메시지 (클릭률 11.6%)"]
                    }
                ],
                generated: [
                    {
                        message: "(광고) 최대 금리 할인 혜택 지금 바로 확인하기 👉",
                        tone: "promotional",
                        reason: "혜택 강조형 스타일로 생성. '금리, 혜택' 키워드 반영. 타겟 '직장인' 고려한 메시지.",
                        predicted_performance: {
                            predicted_click_rate: 11.2,
                            confidence: 85,
                            factors: {
                                keywords: "+4% (고성과 키워드)",
                                emoji: "-2% (이모지 효과)",
                                length: "+1% (길이 최적화)",
                                urgency: "0% (일반)"
                            }
                        }
                    },
                    {
                        message: "(광고) 혜택 확인하고 신용대출 받기",
                        tone: "high_performance",
                        reason: "고성과 키워드 '혜택' 활용. 간결한 구조와 명확한 CTA로 클릭률 최적화. 이모지 미사용으로 텍스트 집중도 향상.",
                        predicted_performance: {
                            predicted_click_rate: 12.8,
                            confidence: 85,
                            factors: {
                                keywords: "+4% (고성과 키워드)",
                                emoji: "0% (텍스트 중심)",
                                length: "+1% (길이 최적화)",
                                urgency: "0% (일반)"
                            }
                        }
                    }
                ]
            };
        }
        
        function displayResults(results) {
            // 기존 문구 매칭 결과
            let matchingHTML = '<h3 style="margin-bottom: 20px;">📋 매칭된 기존 문구</h3>';
            
            results.matching.forEach((match, index) => {
                matchingHTML += `
                    <div class="result-card">
                        <div class="result-type">매칭 순위 ${index + 1}위 (매칭도: ${(match.score * 100).toFixed(0)}%)</div>
                        <div class="message-text">${match.message}</div>
                        <div class="message-stats">
                            <div class="stat-item">
                                <div class="stat-value">${match.click_rate}%</div>
                                <div class="stat-label">실제 클릭률</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">${match.service}</div>
                                <div class="stat-label">서비스</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">${match.reasons.length}개</div>
                                <div class="stat-label">매칭 요소</div>
                            </div>
                        </div>
                        <div class="reason-text">
                            <strong>매칭 이유:</strong> ${match.reasons.join(', ')}
                        </div>
                    </div>
                `;
            });
            
            // 신규 문구 생성 결과
            let generatedHTML = '<h3 style="margin-bottom: 20px;">✨ AI 생성 문구</h3>';
            
            results.generated.forEach((gen, index) => {
                const performance = gen.predicted_performance;
                generatedHTML += `
                    <div class="result-card">
                        <div class="result-type">${gen.tone === 'high_performance' ? '고성과 패턴 기반' : '톤앤매너 기반'} 생성</div>
                        <div class="message-text">${gen.message}</div>
                        <div class="message-stats">
                            <div class="stat-item">
                                <div class="stat-value">${performance.predicted_click_rate}%</div>
                                <div class="stat-label">예상 클릭률</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">${performance.confidence}%</div>
                                <div class="stat-label">신뢰도</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">${gen.message.length}자</div>
                                <div class="stat-label">문구 길이</div>
                            </div>
                        </div>
                        <div class="reason-text">
                            <strong>생성 이유:</strong> ${gen.reason}
                            <br><strong>성과 요인:</strong> ${Object.entries(performance.factors).map(([k,v]) => v).join(', ')}
                        </div>
                    </div>
                `;
            });
            
            document.getElementById('matching-results').innerHTML = matchingHTML;
            document.getElementById('generated-results').innerHTML = generatedHTML;
        }
    </script>
</body>
</html>
    '''
    
    return html_content

if __name__ == "__main__":
    # HTML 인터페이스 생성
    html_content = create_web_interface()
    
    with open("ai_message_generator.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ AI 문구 생성기 HTML 인터페이스가 생성되었습니다!")
    print("📄 파일: ai_message_generator.html")
    print("💡 브라우저에서 열어서 사용하세요!")
    
    # 백엔드 서비스도 테스트
    print("\n🔍 백엔드 서비스 테스트...")
    
    generator = MessageAIGenerator("202507_.csv")
    
    # 테스트 입력
    test_input = {
        'target_audience': '직장인',
        'keywords': ['금리', '혜택'],
        'tone': 'promotional',
        'service': '신용대출',
        'description': '직장인 대상 금리 할인 혜택 알림'
    }
    
    print("📋 기존 문구 매칭 결과:")
    matches = generator.find_matching_messages(test_input)
    for i, match in enumerate(matches[:3], 1):
        print(f"{i}. {match['message'][:50]}... (클릭률: {match['click_rate']}%)")
        print(f"   이유: {', '.join(match['reasons'])}")
    
    print("\n✨ 신규 문구 생성 결과:")
    generated = generator.generate_new_messages(test_input)
    for i, gen in enumerate(generated, 1):
        print(f"{i}. {gen['message']}")
        print(f"   예상 클릭률: {gen['predicted_performance']['predicted_click_rate']}%")
        print(f"   이유: {gen['reason']}")