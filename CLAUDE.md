# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Korean notification analytics and AI-powered message generation service for loan/financial services. Users upload CSV files containing notification history data, and the system analyzes performance patterns to generate optimized, personalized messages using LLM.

## Key Commands

### Running the Web Service
```bash
# Primary upload-based web server (recommended)
python3 upload_web_server.py

# Alternative integrated server (requires local CSV file)
python3 ultimate_web_server.py
```

### Direct Analysis (requires local CSV)
```bash
# Basic analysis with uploaded/local CSV
python3 simple_analyzer.py

# Enhanced timing analysis
python3 enhanced_timing_analyzer.py

# Generate visualization reports
python3 visualization_generator.py
```

## Architecture Overview

### Core Workflow
1. **CSV Upload**: Users upload notification history CSV via web interface
2. **Memory Processing**: `upload_analyzer.py` processes CSV data in memory
3. **Analysis**: Generate customer segments, timing patterns, keyword performance
4. **AI Generation**: Create personalized messages based on analysis results
5. **Results**: Return analysis reports and optimized message suggestions

### Key Components

1. **Upload & Processing**
   - `upload_web_server.py`: Main web server handling CSV uploads
   - `upload_analyzer.py`: Memory-based CSV processing and analysis
   - `upload_web_interface.html`: Web interface for file uploads

2. **Analysis Engine**
   - `simple_analyzer.py`: Core analysis engine (works with files or uploaded data)
   - `enhanced_timing_analyzer.py`: Advanced timing optimization analysis
   - Memory-based processing eliminates file dependencies

3. **AI Message Generation**
   - `real_llm_generator.py`: OpenAI API integration for creative message generation
   - Template-based generation with customer segment targeting
   - Learns from uploaded data patterns

4. **Web Interface**
   - File upload form with drag-and-drop support
   - Real-time analysis results display
   - Message generation interface
   - Export functionality for results

### Expected CSV Format
The uploaded CSV should contain columns like:
- `발송일` (Send Date)
- `서비스명` (Service Name) 
- `클릭율` (Click Rate)
- `발송회원수` (Send Count)
- `클릭회원수` (Click Count)
- `발송채널` (Send Channel)
- `메시지내용` (Message Content)

## Technical Details

### Dependencies
- **Core**: Python 3.8+ standard library only
- **Optional**: `openai>=1.0.0` for LLM message generation
- **Note**: Designed to work without external file dependencies

### Environment Variables
```bash
OPENAI_API_KEY=your-api-key-here  # Required for AI message generation
SERVER_PORT=8080                  # Default port
SERVER_HOST=0.0.0.0              # Default host
```

### Customer Segmentation Logic
Based on uploaded CSV click rate data:
- **High-response segment**: Top 33% performers
- **Mid-response segment**: Middle 33% performers  
- **Low-response segment**: Bottom 33% performers

### Analysis Features
- **Performance Analysis**: Click rates, send volumes, timing patterns
- **Keyword Analysis**: High-performing message keywords and phrases
- **Timing Optimization**: Best days, times, and seasonal patterns
- **Segment Targeting**: Personalized messages per customer segment

## Deployment

### Local Development
```bash
python3 upload_web_server.py
# Access via http://localhost:8080
```

### Production (Railway.app)
- Uses `upload_web_server.py` as main entry point
- File-independent architecture suitable for cloud deployment
- Healthcheck available at root endpoint

## Key Features

### File Upload Processing
- Drag-and-drop CSV upload interface
- Memory-based processing (no server file storage)
- Supports Korean CSV files with proper encoding
- Real-time validation and error handling

### Analysis Results
- Customer segmentation with performance metrics
- Timing optimization recommendations
- Keyword performance analysis
- ROI and improvement predictions

### AI Message Generation
- OpenAI integration for creative message variations
- Segment-specific message templates
- Performance prediction for generated messages
- Export functionality for campaign use

## Important Notes

- All interfaces and analysis are in Korean
- Designed for financial/loan service notifications
- Upload-based architecture eliminates file dependency issues
- Real data analysis drives accurate performance predictions
- Defensive security focus on notification pattern analysis