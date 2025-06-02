from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

items = []

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask API Test Interface</title>
    <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1 class="mb-4">Flask API Test Interface</h1>
        
        <!-- Add Item Form -->
        <div class="card mb-4">
            <div class="card-header">
                <h5>Add New Item</h5>
            </div>
            <div class="card-body">
                <form id="addItemForm">
                    <div class="mb-3">
                        <label for="itemName" class="form-label">Item Name</label>
                        <input type="text" class="form-control" id="itemName" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Add Item</button>
                </form>
            </div>
        </div>

        <!-- Items List -->
        <div class="card">
            <div class="card-header d-flex justify-content-between">
                <h5>Items List</h5>
                <button class="btn btn-outline-secondary btn-sm" onclick="loadItems()">Refresh</button>
            </div>
            <div class="card-body">
                <div id="itemsList"></div>
            </div>
        </div>

        <!-- Messages -->
        <div id="messages" class="mt-3"></div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function showMessage(message, type = 'info') {
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
            setTimeout(() => messagesDiv.innerHTML = '', 3000);
        }

        async function loadItems() {
            try {
                const response = await fetch('/items');
                const items = await response.json();
                
                const itemsList = document.getElementById('itemsList');
                if (items.length === 0) {
                    itemsList.innerHTML = '<p class="text-muted">No items found</p>';
                } else {
                    itemsList.innerHTML = items.map((item, index) => 
                        `<div class="border-bottom py-2">
                            <strong>Item ${index + 1}:</strong> ${item.name}
                        </div>`
                    ).join('');
                }
            } catch (error) {
                showMessage('Error loading items: ' + error.message, 'danger');
            }
        }

        document.getElementById('addItemForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('itemName').value.trim();
            
            if (!name) {
                showMessage('Please enter an item name', 'warning');
                return;
            }

            try {
                const response = await fetch('/items', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name: name })
                });

                const result = await response.json();
                
                if (response.ok) {
                    showMessage(result.message, 'success');
                    document.getElementById('itemName').value = '';
                    loadItems();
                } else {
                    showMessage(result.error, 'danger');
                }
            } catch (error) {
                showMessage('Error adding item: ' + error.message, 'danger');
            }
        });

        // Load items when page loads
        loadItems();
    </script>
</body>
</html>
    ''')

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    items.append({'name': data['name']})
    return jsonify({'message': 'Item added'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
