# debug_imports.py (place in root directory)
import os
import sys

print("🔍 Debugging imports...")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print(f"Files in current directory: {os.listdir('.')}")

# Try to import config
try:
    from config import settings
    print("✅ SUCCESS: Imported config!")
    print(f"Settings: {settings.SECRET_KEY}")
except ImportError as e:
    print(f"❌ FAILED: {e}")

    # Try different import approaches
    print("\n🔄 Trying alternative imports...")
    try:
        import config
        print("✅ Alternative import worked!")
    except ImportError as e2:
        print(f"❌ Alternative also failed: {e2}")
