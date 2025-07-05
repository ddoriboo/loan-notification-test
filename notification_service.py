#!/usr/bin/env python3
"""
개인화 맞춤 알림 서비스 웹 애플리케이션
Flask 기반 웹 서비스로 타겟율 최적화 기능 제공
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime, timedelta
import random
from simple_analyzer import SimpleNotificationAnalyzer

app = Flask(__name__)

# 전역 변수로 분석 결과 저장
analyzer = None
analysis_results = {}

# 메시지 템플릿 (분석 결과 기반)
MESSAGE_TEMPLATES = {
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
    }
}

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    """데이터 분석 페이지"""
    global analyzer, analysis_results
    
    if not analyzer:
        try:
            analyzer = SimpleNotificationAnalyzer("/mnt/c/Users/USER/Documents/notification/202507_.csv")
            analysis_results = analyzer.generate_final_report()
        except Exception as e:
            return f"분석 중 오류 발생: {str(e)}"
    
    return render_template('analyze.html', results=analysis_results)

@app.route('/api/generate_message', methods=['POST'])
def generate_message():
    """개인화 메시지 생성 API"""
    try:
        data = request.json
        service = data.get('service', '신용대환대출')
        segment = data.get('segment', '중반응')
        
        # 서비스와 세그먼트에 맞는 메시지 템플릿 선택
        if service in MESSAGE_TEMPLATES and segment in MESSAGE_TEMPLATES[service]:
            messages = MESSAGE_TEMPLATES[service][segment]
            selected_message = random.choice(messages)
        else:
            selected_message = "(광고) 맞춤 상품 정보를 확인해보세요"
        
        # 최적 발송 시간 계산
        optimal_time = calculate_optimal_send_time()
        
        # 예상 성과 계산
        expected_performance = calculate_expected_performance(service, segment)
        
        return jsonify({
            'message': selected_message,
            'optimal_time': optimal_time,
            'expected_performance': expected_performance,
            'success': True
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        })

@app.route('/api/optimize_campaign', methods=['POST'])
def optimize_campaign():
    """캠페인 최적화 API"""
    try:
        data = request.json
        target_audience = data.get('target_audience', 10000)
        service = data.get('service', '신용대환대출')
        
        # 세그먼트별 최적 배분 계산
        optimization = calculate_campaign_optimization(service, target_audience)
        
        return jsonify({
            'optimization': optimization,
            'success': True
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        })

def calculate_optimal_send_time():
    """최적 발송 시간 계산"""
    # 분석 결과에 따라 수요일이 최적
    now = datetime.now()
    days_ahead = 2 - now.weekday()  # 수요일 = 2
    
    if days_ahead <= 0:
        days_ahead += 7
    
    optimal_date = now + timedelta(days=days_ahead)
    optimal_time = optimal_date.replace(hour=10, minute=0, second=0, microsecond=0)
    
    return optimal_time.strftime('%Y-%m-%d %H:%M')

def calculate_expected_performance(service, segment):
    """예상 성과 계산"""
    # 서비스별 기본 클릭률 (분석 결과 기반)
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

def calculate_campaign_optimization(service, target_audience):
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
        expected_perf = calculate_expected_performance(service, segment)
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

if __name__ == '__main__':
    # HTML 템플릿 파일들 생성
    create_html_templates()
    
    print("🚀 개인화 맞춤 알림 서비스 시작!")
    print("http://localhost:5000 에서 확인하세요")
    app.run(debug=True, host='0.0.0.0', port=5000)

def create_html_templates():
    """HTML 템플릿 파일 생성"""
    templates_dir = 'templates'
    os.makedirs(templates_dir, exist_ok=True)
    
    # 메인 페이지 템플릿
    index_html = """
<!DOCTYPE html>
<html>
<head>
    <title>개인화 맞춤 알림 서비스</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .btn { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px 5px; }
        .btn:hover { background: #764ba2; }
        .feature { display: inline-block; margin: 10px; padding: 20px; background: #f8f9fa; border-radius: 8px; text-align: center; width: 200px; }
        .emoji { font-size: 2em; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 개인화 맞춤 알림 서비스</h1>
            <p>대출 서비스의 타겟율을 극대화하는 AI 기반 알림 서비스</p>
        </div>
        
        <div class="card">
            <h2>🚀 서비스 기능</h2>
            <div class="feature">
                <div class="emoji">📊</div>
                <h3>데이터 분석</h3>
                <p>18개월 알림 히스토리 분석</p>
            </div>
            <div class="feature">
                <div class="emoji">🎯</div>
                <h3>고객 세그먼트</h3>
                <p>반응률 기반 3단계 분류</p>
            </div>
            <div class="feature">
                <div class="emoji">✨</div>
                <h3>개인화 메시지</h3>
                <p>세그먼트별 맞춤 문구</p>
            </div>
            <div class="feature">
                <div class="emoji">⚡</div>
                <h3>최적화</h3>
                <p>발송 시간/규모 최적화</p>
            </div>
        </div>
        
        <div class="card">
            <h2>💡 핵심 인사이트</h2>
            <ul>
                <li>📈 신용점수조회 서비스가 가장 높은 클릭률 (10.84%)</li>
                <li>🎯 '혜택' 키워드가 가장 높은 성과 (10.17%)</li>
                <li>📅 수요일 발송이 최적 (8.88% 클릭률)</li>
                <li>👥 소규모 발송이 더 효과적 (10.23% vs 6.67%)</li>
                <li>🚫 이모지 사용이 오히려 클릭률 저하 (-4.67%p)</li>
            </ul>
        </div>
        
        <div class="card">
            <h2>🛠️ 서비스 메뉴</h2>
            <a href="/analyze" class="btn">📊 데이터 분석 결과</a>
            <button onclick="generateMessage()" class="btn">✨ 개인화 메시지 생성</button>
            <button onclick="optimizeCampaign()" class="btn">🎯 캠페인 최적화</button>
        </div>
        
        <div id="messageResult" class="card" style="display:none;">
            <h3>🎉 생성된 개인화 메시지</h3>
            <div id="messageContent"></div>
        </div>
        
        <div id="campaignResult" class="card" style="display:none;">
            <h3>🎯 캠페인 최적화 결과</h3>
            <div id="campaignContent"></div>
        </div>
    </div>
    
    <script>
        function generateMessage() {
            const service = prompt("서비스를 선택하세요:\\n1. 신용대환대출\\n2. 주택담보대출비교\\n3. 신용점수조회", "신용대환대출");
            const segment = prompt("세그먼트를 선택하세요:\\n1. 고반응\\n2. 중반응\\n3. 저반응", "고반응");
            
            fetch('/api/generate_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ service: service, segment: segment })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('messageResult').style.display = 'block';
                    document.getElementById('messageContent').innerHTML = `
                        <p><strong>📱 생성된 메시지:</strong><br>${data.message}</p>
                        <p><strong>⏰ 최적 발송 시간:</strong> ${data.optimal_time}</p>
                        <p><strong>📊 예상 성과:</strong> ${data.expected_performance.expected_click_rate}% 클릭률</p>
                        <p><strong>📈 개선 효과:</strong> ${data.expected_performance.improvement_vs_average}% 포인트</p>
                    `;
                } else {
                    alert('메시지 생성 중 오류가 발생했습니다.');
                }
            });
        }
        
        function optimizeCampaign() {
            const audience = prompt("타겟 고객 수를 입력하세요:", "10000");
            const service = prompt("서비스를 선택하세요:\\n1. 신용대환대출\\n2. 주택담보대출비교\\n3. 신용점수조회", "신용대환대출");
            
            fetch('/api/optimize_campaign', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target_audience: parseInt(audience), service: service })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('campaignResult').style.display = 'block';
                    const opt = data.optimization;
                    document.getElementById('campaignContent').innerHTML = `
                        <h4>세그먼트별 최적 배분:</h4>
                        <p><strong>고반응 세그먼트:</strong> ${opt.고반응.target_count}명 → ${opt.고반응.expected_clicks}회 클릭 예상 (${opt.고반응.expected_click_rate}%)</p>
                        <p><strong>중반응 세그먼트:</strong> ${opt.중반응.target_count}명 → ${opt.중반응.expected_clicks}회 클릭 예상 (${opt.중반응.expected_click_rate}%)</p>
                        <p><strong>저반응 세그먼트:</strong> ${opt.저반응.target_count}명 → ${opt.저반응.expected_clicks}회 클릭 예상 (${opt.저반응.expected_click_rate}%)</p>
                        <hr>
                        <p><strong>🎯 전체 예상 성과:</strong> ${opt.total.expected_clicks}회 클릭 (${opt.total.expected_click_rate}%)</p>
                    `;
                } else {
                    alert('캠페인 최적화 중 오류가 발생했습니다.');
                }
            });
        }
    </script>
</body>
</html>
"""
    
    # 분석 결과 페이지 템플릿
    analyze_html = """
<!DOCTYPE html>
<html>
<head>
    <title>분석 결과 - 개인화 맞춤 알림 서비스</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .btn { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px 5px; }
        .btn:hover { background: #764ba2; }
        .stat { display: inline-block; margin: 10px; padding: 15px; background: #f8f9fa; border-radius: 8px; text-align: center; min-width: 150px; }
        .stat-value { font-size: 2em; font-weight: bold; color: #667eea; }
        .stat-label { font-size: 0.9em; color: #666; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f8f9fa; }
        .highlight { background-color: #e3f2fd; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 데이터 분석 결과</h1>
            <p>18개월간 알림 발송 히스토리 종합 분석</p>
            <a href="/" class="btn">← 홈으로</a>
        </div>
        
        <div class="card">
            <h2>📈 주요 통계</h2>
            <div class="stat">
                <div class="stat-value">1,497</div>
                <div class="stat-label">전체 알림 수</div>
            </div>
            <div class="stat">
                <div class="stat-value">8.45%</div>
                <div class="stat-label">평균 클릭률</div>
            </div>
            <div class="stat">
                <div class="stat-value">8</div>
                <div class="stat-label">서비스 종류</div>
            </div>
            <div class="stat">
                <div class="stat-value">120K</div>
                <div class="stat-label">평균 발송 수</div>
            </div>
        </div>
        
        <div class="card">
            <h2>🎯 서비스별 성과</h2>
            <table>
                <tr>
                    <th>서비스명</th>
                    <th>평균 클릭률</th>
                    <th>알림 수</th>
                    <th>성과 등급</th>
                </tr>
                <tr class="highlight">
                    <td>신용점수조회</td>
                    <td>10.84%</td>
                    <td>312</td>
                    <td>🥇 최고</td>
                </tr>
                <tr>
                    <td>신용대환대출</td>
                    <td>8.92%</td>
                    <td>668</td>
                    <td>🥈 우수</td>
                </tr>
                <tr>
                    <td>주택담보대출비교</td>
                    <td>7.83%</td>
                    <td>103</td>
                    <td>🥉 양호</td>
                </tr>
                <tr>
                    <td>중고차론</td>
                    <td>7.45%</td>
                    <td>23</td>
                    <td>👍 양호</td>
                </tr>
                <tr>
                    <td>전월세대출비교</td>
                    <td>7.28%</td>
                    <td>38</td>
                    <td>👍 양호</td>
                </tr>
                <tr>
                    <td>신용대출비교</td>
                    <td>5.74%</td>
                    <td>311</td>
                    <td>⚠️ 개선 필요</td>
                </tr>
            </table>
        </div>
        
        <div class="card">
            <h2>🔤 키워드 성과</h2>
            <table>
                <tr>
                    <th>키워드</th>
                    <th>사용 횟수</th>
                    <th>평균 클릭률</th>
                    <th>추천도</th>
                </tr>
                <tr class="highlight">
                    <td>혜택</td>
                    <td>321</td>
                    <td>10.17%</td>
                    <td>🔥 강력 추천</td>
                </tr>
                <tr>
                    <td>최대</td>
                    <td>347</td>
                    <td>9.12%</td>
                    <td>👍 추천</td>
                </tr>
                <tr>
                    <td>할인</td>
                    <td>19</td>
                    <td>8.46%</td>
                    <td>👍 추천</td>
                </tr>
                <tr>
                    <td>금리</td>
                    <td>656</td>
                    <td>7.70%</td>
                    <td>✅ 사용 권장</td>
                </tr>
            </table>
        </div>
        
        <div class="card">
            <h2>🎭 이모지 효과 분석</h2>
            <div class="stat">
                <div class="stat-value">6.66%</div>
                <div class="stat-label">이모지 사용 시</div>
            </div>
            <div class="stat">
                <div class="stat-value">11.34%</div>
                <div class="stat-label">이모지 미사용 시</div>
            </div>
            <p><strong>⚠️ 주의:</strong> 이모지 사용 시 클릭률이 4.67%p 감소합니다. 텍스트 중심의 메시지가 더 효과적입니다.</p>
        </div>
        
        <div class="card">
            <h2>⏰ 최적 발송 전략</h2>
            <ul>
                <li>🗓️ <strong>최적 발송 요일:</strong> 수요일 (8.88% 클릭률)</li>
                <li>👥 <strong>발송 규모:</strong> 소규모 발송 권장 (10.23% vs 6.67%)</li>
                <li>🎯 <strong>키워드 활용:</strong> '혜택', '최대', '할인' 중심</li>
                <li>📱 <strong>메시지 길이:</strong> 42자 내외 (고성과 메시지 기준)</li>
            </ul>
        </div>
        
        <div class="card">
            <h2>🚀 서비스 활용 가이드</h2>
            <ol>
                <li><strong>세그먼트별 메시지 차별화:</strong> 고/중/저 반응군별 다른 톤앤매너 적용</li>
                <li><strong>키워드 최적화:</strong> '혜택', '최대' 등 고성과 키워드 활용</li>
                <li><strong>발송 타이밍:</strong> 수요일 오전 10-11시 발송 권장</li>
                <li><strong>A/B 테스트:</strong> 지속적인 메시지 최적화</li>
                <li><strong>성과 모니터링:</strong> 실시간 클릭률 추적 및 개선</li>
            </ol>
        </div>
    </div>
</body>
</html>
"""
    
    # 파일 저장
    with open(f'{templates_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    with open(f'{templates_dir}/analyze.html', 'w', encoding='utf-8') as f:
        f.write(analyze_html)
    
    print("HTML 템플릿 파일이 생성되었습니다.")