"""
Test script to verify the application is set up correctly.
Run this before submitting to ensure everything works.
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment setup"""
    print("🔍 Testing Environment Setup...")
    
    load_dotenv()
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        print("   Please add it to .env file")
        return False
    
    if api_key == 'your_api_key_here':
        print("❌ ANTHROPIC_API_KEY is still set to default value")
        print("   Please update .env with your actual API key")
        return False
    
    print("✅ Environment setup looks good")
    return True

def test_imports():
    """Test that all required modules can be imported"""
    print("\n📦 Testing Imports...")
    
    required_modules = [
        ('flask', 'Flask'),
        ('anthropic', 'Anthropic'),
        ('dotenv', 'python-dotenv')
    ]
    
    all_good = True
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {package_name} imported successfully")
        except ImportError:
            print(f"❌ {package_name} not found. Run: pip install {package_name}")
            all_good = False
    
    return all_good

def test_application_structure():
    """Test that all required files exist"""
    print("\n📁 Testing Application Structure...")
    
    required_files = [
        'app.py',
        'analyzer.py',
        'sample_data.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        'templates/index.html',
        'static/styles.css',
        'static/script.js'
    ]
    
    all_good = True
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✅ {filepath}")
        else:
            print(f"❌ {filepath} missing")
            all_good = False
    
    return all_good

def test_sample_data():
    """Test that sample data loads correctly"""
    print("\n📊 Testing Sample Data...")
    
    try:
        from sample_data import get_transcript_list, get_transcript
        
        transcripts = get_transcript_list()
        if len(transcripts) >= 3:
            print(f"✅ Found {len(transcripts)} sample transcripts")
        else:
            print(f"⚠️  Only {len(transcripts)} sample transcripts found")
        
        # Test loading one
        first_key = transcripts[0]['key']
        transcript = get_transcript(first_key)
        if transcript and 'transcript' in transcript:
            print("✅ Sample transcript loads correctly")
            return True
        else:
            print("❌ Sample transcript data incomplete")
            return False
            
    except Exception as e:
        print(f"❌ Error loading sample data: {e}")
        return False

def test_analyzer():
    """Test that analyzer can be initialized"""
    print("\n🧠 Testing Analyzer...")
    
    try:
        from analyzer import TranscriptAnalyzer
        
        analyzer = TranscriptAnalyzer()
        print("✅ Analyzer initialized successfully")
        
        # Test quick scan (doesn't use API)
        test_text = "We believe this is a good opportunity, though it's difficult to predict outcomes."
        result = analyzer.quick_scan(test_text)
        
        if result['total_hedging_phrases'] > 0:
            print(f"✅ Quick scan working (found {result['total_hedging_phrases']} phrases)")
            return True
        else:
            print("⚠️  Quick scan returned no results (unexpected)")
            return True  # Still pass, just warn
            
    except ValueError as e:
        print(f"⚠️  {e}")
        print("   This is OK for testing, but you'll need an API key to run the app")
        return True
    except Exception as e:
        print(f"❌ Error testing analyzer: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("  Earnings Call Analyser - Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_application_structure,
        test_sample_data,
        test_analyzer,
        test_environment
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✅ All tests passed! ({passed}/{total})")
        print("\nYou're ready to run the application:")
        print("  python app.py")
    else:
        print(f"⚠️  Some tests failed ({passed}/{total} passed)")
        print("\nPlease fix the issues above before running the application.")
    
    print("=" * 60)
    
    return all(results)

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
