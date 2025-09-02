"""
Test OpenAI API Key
Simple script to verify your API key is working
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_openai_api():
    """Test if OpenAI API key is working"""
    print("🔑 Testing OpenAI API Key...")
    print("=" * 50)
    
    try:
        # Import the config
        from core.config import config
        
        # Check if API key is set
        if not config.openai_api_key or config.openai_api_key == "your_openai_api_key_here":
            print("❌ API Key not set or still placeholder")
            print("   Please edit .env file and add your real OpenAI API key")
            print("   Format: OPENAI_API_KEY=sk-your-actual-key-here")
            return False
        
        print(f"✅ API Key found: {config.openai_api_key[:10]}...")
        print(f"✅ Model: {config.openai_model}")
        
        # Test the API
        print("\n🚀 Testing API connection...")
        
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(api_key=config.openai_api_key)
            
            # Simple test request
            response = await client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {"role": "user", "content": "Say 'API key is working!' if you can read this."}
                ],
                max_tokens=50
            )
            
            result = response.choices[0].message.content
            print(f"✅ API Response: {result}")
            print("🎉 Your OpenAI API key is working perfectly!")
            return True
            
        except Exception as e:
            print(f"❌ API Error: {e}")
            print("   Check your API key and internet connection")
            return False
    
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_openai_api())
    
    if success:
        print("\n🎯 Ready to use enhanced AI features!")
        print("   • Advanced natural language processing")
        print("   • AI-generated protocol implementations")
        print("   • Sophisticated device analysis")
    else:
        print("\n🔧 To fix:")
        print("   1. Edit .env file")
        print("   2. Replace 'your_openai_api_key_here' with your real key")
        print("   3. Run this test again")
