import unittest
import json
import os
import sys
import tempfile
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

class TestIceCreamAPI(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create a temporary model for testing
        self.create_test_model()
    
    def create_test_model(self):
        """Create a simple test model for testing purposes."""
        # Create some dummy training data
        X = np.array([[20], [25], [30], [35], [40]])
        y = np.array([100, 150, 200, 250, 300])
        
        # Train a simple linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Create ModelCleaning directory if it doesn't exist
        os.makedirs('ModelCleaning', exist_ok=True)
        
        # Save the test model
        joblib.dump(model, 'ModelCleaning/TemperatureProfitsModel.pkl')
    
    def tearDown(self):
        """Clean up after each test method."""
        # Remove the test model file if it exists
        model_path = 'ModelCleaning/TemperatureProfitsModel.pkl'
        if os.path.exists(model_path):
            os.remove(model_path)
    
    def test_home_endpoint(self):
        """Test the home endpoint returns correct information."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('description', data)
        self.assertIn('endpoints', data)
        self.assertEqual(data['message'], 'Ice Cream Profits Prediction API')
        self.assertIn('/predict', data['endpoints'])
        self.assertIn('/health', data['endpoints'])
    
    def test_health_endpoint_with_model(self):
        """Test the health endpoint when model is loaded."""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('model_loaded', data)
        self.assertEqual(data['status'], 'healthy')
        self.assertTrue(data['model_loaded'])
    
    def test_predict_endpoint_valid_input(self):
        """Test the predict endpoint with valid temperature input."""
        test_data = {'temperature': 25.0}
        response = self.app.post('/predict', 
                                data=json.dumps(test_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('temperature', data)
        self.assertIn('predicted_profit', data)
        self.assertEqual(data['temperature'], 25.0)
        self.assertIsInstance(data['predicted_profit'], (int, float))
        self.assertGreater(data['predicted_profit'], 0)
    
    def test_invalid_endpoint(self):
        """Test accessing a non-existent endpoint."""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2) 