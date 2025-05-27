import requests
import json
import time

# Wait for API to start
time.sleep(2)

base_url = "http://localhost:5000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint"""
    try:
        # Test prediction with temperature 45
        data = {"temperature": 45}
        response = requests.post(f"{base_url}/predict", 
                               json=data,
                               headers={'Content-Type': 'application/json'})
        
        print(f"Prediction test: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Prediction test failed: {e}")
        return False

def test_home():
    """Test the home endpoint"""
    try:
        response = requests.get(f"{base_url}/")
        print(f"Home endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Home test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Flask API...")
    
    # Test all endpoints
    health_ok = test_health()
    home_ok = test_home()
    prediction_ok = test_prediction()
    
    if health_ok and home_ok and prediction_ok:
        print("\n✅ All API tests passed!")
    else:
        print("\n❌ Some API tests failed!")
        exit(1) 