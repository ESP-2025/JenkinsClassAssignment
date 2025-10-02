import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import get_app_info, perform_calculation, validate_configuration

class TestApp(unittest.TestCase):
    def test_get_app_info(self):
        """Test the get_app_info function"""
        info = get_app_info()
        self.assertEqual(info["name"], "Jenkins Pipeline Demo")
        self.assertEqual(info["version"], "1.0.0")
        self.assertEqual(info["environment"], "development")

    def test_perform_calculation(self):
        """Test the perform_calculation function"""
        result = perform_calculation(5, 3)
        self.assertEqual(result, 8)
        
        result = perform_calculation(-1, 1)
        self.assertEqual(result, 0)
        
        result = perform_calculation(0, 0)
        self.assertEqual(result, 0)

    def test_validate_configuration(self):
        """Test the validate_configuration function"""
        valid_config = {
            "app_env": "development",
            "db_engine": "sqlite"
        }
        self.assertTrue(validate_configuration(valid_config))
        
        invalid_config = {
            "app_env": "development"
            # missing db_engine
        }
        self.assertFalse(validate_configuration(invalid_config))

if __name__ == '__main__':
    unittest.main()