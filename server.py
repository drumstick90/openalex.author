#!/usr/bin/env python3
"""
Simple HTTP server to serve the OpenAlex Author Search terminal interface.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

def main():
    """Start the HTTP server."""
    # Change to the directory containing the HTML file
    os.chdir(Path(__file__).parent)
    
    # Set up the server
    PORT = 8888
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"OpenAlex Author Search Terminal")
            print(f"================================")
            print(f"Server running at: http://localhost:{PORT}")
            print(f"Press Ctrl+C to stop the server")
            print()
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Error: Port {PORT} is already in use.")
            print("Try stopping other servers or use a different port.")
            sys.exit(1)
        else:
            raise

if __name__ == "__main__":
    main()
