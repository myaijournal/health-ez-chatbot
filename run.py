from app import create_app

print("Starting Flask application...")

app = create_app()

if __name__ == "__main__":
    
    print("Running Flask app on http://127.0.0.1:5000")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
