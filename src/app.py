def get_app_info():
    """Return basic application information."""
    return {
        "name": "Jenkins Pipeline Demo",
        "version": "1.0.0",
        "environment": "development"
    }

def perform_calculation(a, b):
    """Perform a sample calculation."""
    return a + b

def validate_configuration(config):
    """Validate the application configuration."""
    required_fields = ["app_env", "db_engine"]
    return all(field in config for field in required_fields)

if __name__ == "__main__":
    # Sample usage
    app_info = get_app_info()
    print(f"Running {app_info['name']} v{app_info['version']} in {app_info['environment']}")
    
    # Sample calculation
    result = perform_calculation(5, 3)
    print(f"Sample calculation result: {result}")
    
    # Configuration validation
    sample_config = {
        "app_env": "development",
        "db_engine": "sqlite"
    }
    is_valid = validate_configuration(sample_config)
    print(f"Configuration valid: {is_valid}")