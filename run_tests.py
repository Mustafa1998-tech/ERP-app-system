#!/usr/bin/env python
"""
Test runner script for the ERP project.
"""
import os
import sys
import subprocess

def main():
    """Run the test suite."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("🧪 Running ERP Project Tests...")
    print("=" * 50)
    
    # Run pytest with coverage
    cmd = [
        sys.executable, '-m', 'pytest',
        '--cov=.',
        '--cov-report=html',
        '--cov-report=term-missing',
        '--cov-fail-under=80',
        '-v'
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode

if __name__ == '__main__':
    sys.exit(main())
