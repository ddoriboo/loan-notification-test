#!/usr/bin/env python3
"""
Railway 시작 스크립트 - upload_web_server.py 강제 실행
"""

import sys
import os

def main():
    """upload_web_server.py 강제 실행"""
    print("🔧 Railway Start Script")
    print("=" * 40)
    print("📍 Forcing execution of upload_web_server.py")
    print("🚫 NOT running ultimate_web_server.py")
    print("=" * 40)
    
    # 현재 디렉토리 확인
    cwd = os.getcwd()
    print(f"📁 Current directory: {cwd}")
    
    # 필요한 파일들 확인
    required_files = ['upload_web_server.py', 'upload_analyzer.py', 'upload_web_interface.html']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            
    print("=" * 40)
    
    # 환경변수 포트 확인
    port = os.environ.get('PORT', '8080')
    print(f"🔌 Using PORT: {port}")
    
    # upload_web_server.py를 직접 실행
    print("🚀 Starting UPLOAD server (not Ultimate server)...")
    
    try:
        # 명시적으로 upload_web_server 모듈 import
        import upload_web_server
        
        # 직접 서버 실행 함수 호출
        upload_web_server.run_upload_server(port=int(port))
        
    except ImportError as e:
        print(f"❌ Failed to import upload_web_server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Upload server startup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()