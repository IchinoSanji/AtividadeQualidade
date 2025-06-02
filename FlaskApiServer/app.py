import os
import logging
from flask import Flask, request, jsonify, render_template

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# In-memory storage for items
items = []

@app.route('/')
def index():
    """Serve the main HTML interface"""
    return render_template('index.html')

@app.route('/items', methods=['GET'])
def get_items():
    """Get all items - returns JSON list of items"""
    try:
        app.logger.debug(f"GET /items - returning {len(items)} items")
        return jsonify({
            'success': True,
            'items': items,
            'count': len(items)
        }), 200
    except Exception as e:
        app.logger.error(f"Error getting items: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve items'
        }), 500

@app.route('/items', methods=['POST'])
def add_item():
    """Add a new item - expects JSON with 'name' field"""
    try:
        # Check if request contains JSON
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        if 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Field "name" is required'
            }), 400
        
        name = data['name']
        
        # Validate name field
        if not isinstance(name, str) or not name.strip():
            return jsonify({
                'success': False,
                'error': 'Field "name" must be a non-empty string'
            }), 400
        
        # Create new item
        new_item = {
            'id': len(items) + 1,
            'name': name.strip()
        }
        
        # Check for duplicate names
        if any(item['name'].lower() == new_item['name'].lower() for item in items):
            return jsonify({
                'success': False,
                'error': 'Item with this name already exists'
            }), 409
        
        items.append(new_item)
        
        app.logger.debug(f"POST /items - added item: {new_item}")
        
        return jsonify({
            'success': True,
            'item': new_item,
            'message': 'Item added successfully'
        }), 201
        
    except Exception as e:
        app.logger.error(f"Error adding item: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to add item'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
