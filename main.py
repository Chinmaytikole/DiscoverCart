import sys
import os

# Add the DiscoverCart directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'MINIMALSITE'))

# Import the app from DiscoverCart
from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
