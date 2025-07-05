#!/usr/bin/env python3
"""
Railway 시작 스크립트 - upload_web_server.py 강제 실행
"""

import sys
import os

def main():
    """upload_web_server.py 실행"""
    print("🚀 Starting upload-based AI message generator...")
    print("📍 Force running upload_web_server.py")
    
    # upload_web_server.py를 직접 import하고 실행
    try:
        from upload_web_server import run_upload_server
        run_upload_server()
    except ImportError as e:
        print(f"❌ Failed to import upload_web_server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()