from app import app
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Use PORT env var if set, else default to 8080
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1")
    if debug_mode:
        print("WARNING: Debug mode is enabled! Do not use debug mode in production environments.")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
