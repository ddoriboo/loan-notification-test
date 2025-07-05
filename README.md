# 📊 Smart Notification Message Analyzer & AI Generator

> CSV 기반 알림 메시지 성과 분석 및 AI 메시지 생성 시스템

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 프로젝트 개요

금융 서비스 알림 메시지의 성과를 데이터 기반으로 분석하고, AI를 활용하여 최적화된 새로운 메시지를 생성하는 웹 기반 분석 도구입니다.

### ✨ 핵심 기능

- **📊 CSV 업로드 분석**: 드래그앤드롭으로 간편한 성과 데이터 분석
- **🏆 고성과 메시지 식별**: 동일 문구 집계 및 성과 기준 명시
- **🔑 다차원 분석**: 키워드, 서비스별, 시간대별 성과 패턴 분석
- **🤖 AI 메시지 생성**: OpenAI GPT-4o 기반 데이터 드리븐 메시지 생성
- **📝 자연어 인사이트**: AI가 분석한 실용적 개선 제안 리포트
- **📱 반응형 UI**: 모바일부터 데스크톱까지 최적화된 사용자 경험

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 저장소 클론
git clone https://github.com/ddoriboo/loan-notification-test.git
cd loan-notification-test

# OpenAI API 키 설정 (선택사항)
export OPENAI_API_KEY="your-api-key-here"
# 또는 upload_web_server.py 파일에서 DIRECT_API_KEY 설정
```

### 2. 서버 실행

```bash
# Python 서버 시작
python upload_web_server.py
# 또는
python ultimate_web_server.py
```

### 3. 웹 브라우저 접속

```
http://localhost:8000
```

### 4. CSV 데이터 업로드

지원하는 CSV 형식:
```csv
서비스명,클릭율,발송 문구,발송일,요일,발송회원수,클릭회원수
신용대출,12.5,"(광고) 특별 혜택 대출 확인하세요",2025-01-01,수,1000,125
주택담보대출,8.3,"(광고) 주택담보대출 금리 비교",2025-01-02,목,1500,124
```

## 📋 시스템 요구사항

- **Python**: 3.8 이상
- **필수 패키지**: `openai` (AI 기능 사용시)
- **브라우저**: Chrome, Firefox, Safari, Edge (최신 버전)
- **메모리**: 최소 512MB RAM
- **파일 크기**: 최대 10MB CSV 파일

## 🏗️ 아키텍처

```
Frontend (HTML/CSS/JS) → Python HTTP Server → CSV Analyzer → OpenAI API
```

### 핵심 컴포넌트

- **`upload_web_server.py`**: 메인 웹 서버 및 API 엔드포인트
- **`upload_analyzer.py`**: 데이터 분석 및 패턴 인식 엔진
- **`upload_web_interface.html`**: 반응형 프론트엔드 인터페이스

## 📊 주요 기능 상세

### 1. 고성과 메시지 분석
- **동적 임계값**: 평균 클릭률의 120% 이상 또는 최소 8%
- **집계 분석**: 동일 문구의 발송 횟수, 총 성과, 기간별 분석
- **성과 기준**: 상위 20% 메시지 중 기준 만족 후보 선별

### 2. AI 메시지 생성
- **데이터 기반**: 업로드된 실제 성과 데이터 활용
- **3가지 스타일**: 혜택 강조형, 긴급성 강조형, 개인화 맞춤형
- **예상 클릭률**: 기존 패턴 분석을 통한 성과 예측
- **근거 제시**: 각 메시지별 생성 논리 및 신뢰도 표시

### 3. 다차원 성과 분석

#### 키워드 분석
- **분석 대상**: 혜택, 최대, 할인, 금리, 한도, 대출 등 13개 키워드
- **성과 지표**: 평균 클릭률, 사용 빈도, 효과도 점수
- **시각화**: 🟢 12%+ (매우 효과적), 🟡 8-12% (효과적), 🔴 8% 미만 (개선 필요)

#### 서비스별 분석
- **성과 비교**: 서비스별 평균 클릭률 및 메시지 수
- **베스트 메시지**: 각 서비스의 상위 5개 고성과 메시지
- **개선 방향**: 저성과 서비스 식별 및 벤치마킹 가이드

#### 시간대 분석
- **요일별 성과**: 월~일요일별 평균 클릭률 및 발송 건수
- **최적 타이밍**: 가장 효과적인 발송 요일 식별
- **패턴 인사이트**: 시간대별 고객 행동 패턴 분석

### 4. 자연어 인사이트 리포트
AI가 생성하는 6가지 카테고리별 인사이트:

- **📊 전체 성과 개요**: 전반적인 성과 수준 및 분포 분석
- **🏷️ 서비스별 성과**: 최고/최저 성과 서비스 및 개선 방향
- **🔑 효과적인 키워드**: 고성과 키워드 및 활용 가이드
- **📅 요일별 성과**: 최적 발송 타이밍 및 패턴 분석
- **🏆 고성과 메시지 패턴**: 반복 사용된 검증 메시지 분석
- **💡 개선 제안**: 구체적이고 실행 가능한 개선 방안

## 📱 사용자 인터페이스

### 탭 기반 네비게이션
- **📊 분석 요약**: 전체 성과 지표 및 요일별 차트
- **💬 고성과 메시지**: 집계된 고성과 메시지 및 선정 기준
- **🔑 키워드 분석**: 효과적인 키워드 성과 분석
- **🏷️ 서비스별 분석**: 서비스별 상세 성과 비교
- **📝 인사이트 리포트**: AI 생성 자연어 분석 리포트
- **✨ 문구 생성**: AI 기반 최적화된 메시지 생성

### 스마트 기능
- **요약 오버레이**: 다른 탭 접근시 상단에 핵심 지표 표시
- **반응형 디자인**: 모바일, 태블릿, 데스크톱 최적화
- **실시간 피드백**: 로딩 상태, 에러 처리, 성공 알림

## 🛠️ API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/api/upload-csv` | POST | CSV 파일 업로드 및 분석 |
| `/api/dashboard` | POST | 대시보드 데이터 조회 |
| `/api/generate` | POST | AI 메시지 생성 |
| `/api/insights` | POST | 자연어 인사이트 생성 |

### 예시 요청/응답

#### CSV 업로드
```javascript
// 요청
POST /api/upload-csv
{
  "csv_content": "서비스명,클릭율,발송 문구,발송일,요일\n신용대출,12.5,\"특별혜택\",2025-01-01,수"
}

// 응답
{
  "success": true,
  "total_messages": 100,
  "high_performance_count": 15,
  "summary": { ... }
}
```

#### AI 메시지 생성
```javascript
// 요청
POST /api/generate
{
  "description": "주택담보대출 금리 인하 혜택",
  "service": "주택담보대출",
  "target_audience": "직장인",
  "tone": "promotional"
}

// 응답
{
  "success": true,
  "generated_messages": [
    {
      "style": "데이터 기반 혜택형",
      "message": "(광고) 직장인님을 위한 검증된 금리, 혜택! 주택담보대출 지금 확인하고 최대 혜택 받으세요 👉",
      "predicted_rate": 12.3,
      "reasoning": "업로드 데이터 분석: '금리' 키워드 평균 11.8% 성과. 총 100개 메시지 중 상위 성과 패턴 활용",
      "confidence": 88
    }
  ]
}
```

## 🔧 개발자 가이드

### 프로젝트 구조
```
notification/
├── upload_web_server.py       # 메인 웹 서버
├── ultimate_web_server.py     # 대체 웹 서버
├── upload_analyzer.py         # 데이터 분석 엔진
├── upload_web_interface.html  # 프론트엔드 UI
├── CLAUDE.md                  # 개발 가이드
└── README.md                  # 이 파일
```

### 핵심 클래스

#### UploadAnalyzer
```python
class UploadAnalyzer:
    def analyze_uploaded_csv(self, csv_content)  # CSV 분석
    def aggregate_high_performance_messages()   # 동일 문구 집계
    def generate_natural_language_insights()    # 인사이트 생성
    def get_dashboard_data()                    # 대시보드 데이터
```

#### HTTP 요청 핸들러
```python
class UploadHTTPRequestHandler:
    def handle_upload_csv()    # CSV 업로드 처리
    def handle_dashboard()     # 대시보드 요청
    def handle_generate()      # AI 생성 요청
    def handle_insights()      # 인사이트 요청
```

### 확장 가이드

#### 새로운 분석 지표 추가
```python
# upload_analyzer.py에서 analyze_patterns() 메서드 확장
def analyze_patterns(self):
    # 기존 분석 로직
    
    # 새로운 분석 추가
    new_analysis = self.analyze_new_metric()
    self.performance_patterns['new_metric'] = new_analysis
```

#### 새로운 API 엔드포인트 추가
```python
# 서버 파일에서 do_POST() 메서드 확장
def do_POST(self):
    if self.path == '/api/new-endpoint':
        self.handle_new_feature()
    # 기존 엔드포인트들
```

## 🔒 보안 고려사항

- **데이터 보안**: 업로드된 CSV는 메모리에서만 처리, 파일 시스템에 저장하지 않음
- **API 키 보호**: 환경변수 또는 설정 파일을 통한 OpenAI API 키 관리
- **입력 검증**: CSV 파일 타입 및 크기 제한, 내용 sanitization
- **HTTPS**: 프로덕션 환경에서 SSL/TLS 적용 권장

## 🚀 성능 최적화

### 현재 성능 지표
- **CSV 처리**: 1,000건 기준 3초 이내
- **대시보드 로딩**: 2초 이내  
- **AI 생성**: 15초 이내
- **최대 파일 크기**: 10MB (약 50,000행)

### 최적화 방법
- **메모리 관리**: 대용량 파일 처리시 청크 단위 처리
- **캐싱**: 분석 결과 메모리 캐싱으로 재조회 성능 향상
- **비동기 처리**: AI API 호출시 non-blocking 처리

## 🧪 테스트

### 테스트 데이터
프로젝트에 포함된 `debug_csv.py`로 기본 기능 테스트:
```bash
python debug_csv.py
```

### 샘플 CSV 형식
```csv
서비스명,클릭율,발송 문구,발송일,요일,발송회원수,클릭회원수
신용대출,15.2,"(광고) 🎯 신용대출 특별 금리 혜택! 지금 바로 확인하세요",2024-12-01,일,2000,304
주택담보대출,11.8,"(광고) 주택담보대출 최저 금리 비교 서비스",2024-12-02,월,1500,177
개인사업자대출,9.3,"(광고) 개인사업자를 위한 맞춤 대출 상품",2024-12-03,화,1000,93
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 지원 및 문의

- **Issues**: [GitHub Issues](https://github.com/ddoriboo/loan-notification-test/issues)
- **Documentation**: `CLAUDE.md` 파일 참조
- **API 문서**: 각 엔드포인트별 상세 스펙은 소스 코드 주석 참조

## 🗺️ 로드맵

### 🎯 단기 계획 (1-3개월)
- [ ] A/B 테스트 지원
- [ ] 실시간 분석 대시보드
- [ ] 데이터 내보내기 기능
- [ ] 성능 최적화 (대용량 파일)

### 🚀 중기 계획 (3-6개월)
- [ ] 자체 ML 모델 개발
- [ ] 다채널 지원 (SMS, Push, Email)
- [ ] RESTful API 제공
- [ ] 팀 협업 기능

### 🌟 장기 비전 (6개월+)
- [ ] 산업별 특화 분석
- [ ] 다국어 지원
- [ ] CRM 통합
- [ ] 자동화된 최적화 에이전트

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🙏 감사의 말

- **OpenAI**: GPT-4o API 제공
- **Python Community**: 오픈소스 라이브러리 생태계
- **Claude Code**: 개발 과정에서의 AI 어시스턴트 지원

---

<div align="center">

**⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요! ⭐**

Made with ❤️ for Data-Driven Marketing

</div>