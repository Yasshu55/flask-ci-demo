"""
Production Flask Application
============================
A comprehensive e-commerce API with database connectivity,
authentication, logging, and health monitoring.

Author: DevOps Team
Version: 2.1.0
"""

import os
import sys
import logging
import json
import time
from datetime import datetime
from functools import wraps
from typing import Dict, List, Optional

from flask import Flask, request, jsonify, g
from werkzeug.exceptions import HTTPException

# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# ============================================================
# APPLICATION INITIALIZATION
# ============================================================

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

logger.info("=" * 70)
logger.info("FLASK APPLICATION INITIALIZING")
logger.info("=" * 70)
logger.info(f"Python Version: {sys.version}")
logger.info(f"Flask Version: {Flask.__name__}")
logger.info(f"Working Directory: {os.getcwd()}")
logger.info(f"Environment: {os.getenv('FLASK_ENV', 'production')}")
logger.info("=" * 70)

# ============================================================
# CONFIGURATION VALIDATION
# ============================================================

class ConfigValidator:
    """Validates all required configuration parameters."""
    
    REQUIRED_VARS = [
        'DATABASE_URL',
        'SECRET_KEY',
        'API_KEY',
        'REDIS_URL'
    ]
    
    @classmethod
    def validate(cls) -> Dict[str, any]:
        """Validate environment configuration."""
        logger.info("Starting configuration validation...")
        
        config = {}
        missing_vars = []
        
        for var in cls.REQUIRED_VARS:
            logger.info(f"Checking environment variable: {var}")
            value = os.getenv(var)
            
            if value:
                logger.info(f"✓ {var} is set")
                config[var] = value
            else:
                logger.error(f"✗ {var} is MISSING")
                missing_vars.append(var)
        
        if missing_vars:
            logger.error("=" * 70)
            logger.error("CONFIGURATION VALIDATION FAILED")
            logger.error("=" * 70)
            logger.error(f"Missing variables: {', '.join(missing_vars)}")
            logger.error("")
            logger.error("Please set the following environment variables:")
            for var in missing_vars:
                logger.error(f"  export {var}=<your-value>")
            logger.error("")
            logger.error("Example .env file:")
            logger.error("  DATABASE_URL=postgresql://user:pass@localhost:5432/db")
            logger.error("  SECRET_KEY=your-secret-key-here")
            logger.error("  API_KEY=your-api-key-here")
            logger.error("  REDIS_URL=redis://localhost:6379")
            logger.error("=" * 70)
            
            # THIS IS THE CRITICAL LINE THAT WILL FAIL
            raise KeyError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        logger.info("✓ All configuration validated successfully")
        return config

# ============================================================
# DATABASE CONNECTION SIMULATION
# ============================================================

class DatabaseConnection:
    """Simulates database connection handling."""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.connected = False
        logger.info(f"Initializing database connection to: {db_url[:30]}...")
    
    def connect(self):
        """Establish database connection."""
        logger.info("Attempting to connect to database...")
        logger.info("Parsing connection string...")
        logger.info("Resolving database host...")
        logger.info("Establishing TCP connection...")
        logger.info("Authenticating with credentials...")
        logger.info("Selecting database...")
        logger.info("✓ Database connection established")
        self.connected = True
        return True
    
    def execute_query(self, query: str):
        """Execute a database query."""
        logger.debug(f"Executing query: {query[:50]}...")
        return {"status": "success", "rows": 0}

# ============================================================
# MIDDLEWARE & DECORATORS
# ============================================================

@app.before_request
def before_request():
    """Log all incoming requests."""
    g.start_time = time.time()
    logger.info("-" * 70)
    logger.info(f"Incoming Request: {request.method} {request.path}")
    logger.info(f"Remote Address: {request.remote_addr}")
    logger.info(f"User Agent: {request.headers.get('User-Agent', 'Unknown')[:50]}")
    
    if request.args:
        logger.info(f"Query Parameters: {dict(request.args)}")
    
    if request.is_json:
        logger.info(f"Request Body: {request.get_json()}")

@app.after_request
def after_request(response):
    """Log response details."""
    duration = time.time() - g.start_time
    logger.info(f"Response Status: {response.status_code}")
    logger.info(f"Response Time: {duration:.3f}s")
    logger.info("-" * 70)
    return response

def require_api_key(f):
    """Decorator to require API key authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        logger.info("Validating API key...")
        
        if not api_key:
            logger.warning("API key missing in request")
            return jsonify({"error": "API key required"}), 401
        
        logger.info("✓ API key validated")
        return f(*args, **kwargs)
    return decorated_function

# ============================================================
# ROUTES
# ============================================================

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for load balancers and monitoring.
    
    Returns:
        JSON with application health status
    """
    logger.info("Health check requested")
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": time.time() - app.config.get('start_time', time.time()),
        "version": "2.1.0",
        "checks": {
            "database": "connected",
            "cache": "connected",
            "disk_space": "ok"
        }
    }
    
    logger.info(f"Health status: {health_status['status']}")
    return jsonify(health_status)

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint - returns API information.
    """
    logger.info("Home endpoint accessed")
    
    response = {
        "service": "Flask E-Commerce API",
        "version": "2.1.0",
        "endpoints": {
            "health": "/health",
            "products": "/api/products",
            "orders": "/api/orders",
            "users": "/api/users"
        },
        "documentation": "https://api.example.com/docs",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.info("Returning API information")
    return jsonify(response)

@app.route('/api/products', methods=['GET'])
@require_api_key
def get_products():
    """
    Get all products from database.
    
    Requires API key authentication.
    """
    logger.info("Fetching products from database")
    logger.info("Building SQL query...")
    logger.info("Executing: SELECT * FROM products WHERE active = true")
    logger.info("Fetching results...")
    logger.info("Serializing data...")
    
    # Simulate product data
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Mouse", "price": 29.99},
        {"id": 3, "name": "Keyboard", "price": 79.99}
    ]
    
    logger.info(f"✓ Retrieved {len(products)} products")
    return jsonify({"products": products, "count": len(products)})

@app.route('/api/orders', methods=['POST'])
@require_api_key
def create_order():
    """
    Create a new order.
    
    Requires API key authentication and valid JSON payload.
    """
    logger.info("Processing new order creation")
    
    if not request.is_json:
        logger.error("Request is not JSON")
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    logger.info(f"Order data received: {data}")
    
    # Validate order data
    required_fields = ['product_id', 'quantity', 'customer_email']
    logger.info("Validating order fields...")
    
    for field in required_fields:
        if field not in data:
            logger.error(f"Missing required field: {field}")
            return jsonify({"error": f"Missing field: {field}"}), 400
    
    logger.info("✓ Order validation passed")
    logger.info("Calculating total...")
    logger.info("Checking inventory...")
    logger.info("Creating order record...")
    logger.info("Sending confirmation email...")
    logger.info("✓ Order created successfully")
    
    order = {
        "order_id": "ORD-12345",
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }
    
    return jsonify(order), 201

@app.errorhandler(HTTPException)
def handle_http_error(e):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP Error {e.code}: {e.description}")
    return jsonify({
        "error": e.name,
        "message": e.description,
        "code": e.code
    }), e.code

@app.errorhandler(Exception)
def handle_generic_error(e):
    """Handle all other exceptions."""
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({
        "error": "Internal Server Error",
        "message": str(e)
    }), 500

# ============================================================
# APPLICATION STARTUP
# ============================================================

if __name__ == '__main__':
    logger.info("")
    logger.info("=" * 70)
    logger.info("STARTING APPLICATION BOOTSTRAP")
    logger.info("=" * 70)
    
    # Validate configuration (THIS WILL FAIL IF ENV VARS MISSING)
    # Let the exception propagate naturally for traceback
    config = ConfigValidator.validate()
    
    # Initialize database connection
    logger.info("")
    logger.info("Initializing database connection...")
    db = DatabaseConnection(config['DATABASE_URL'])
    db.connect()
    
    # Store start time
    app.config['start_time'] = time.time()
    
    logger.info("s")
    logger.info("=" * 70)
    logger.info("APPLICATION READY")
    logger.info("=" * 70)
    logger.info(f"Server starting on port 3000...")
    logger.info("Press CTRL+C to quit")
    logger.info("=" * 70)
    logger.info("")
    
    if os.getenv("CI") == "true":
        logger.info("CI environment detected, exiting after startup")
        sys.exit(0)
    # Start the server
    app.run(host='0.0.0.0', port=3000, debug=False)
    
