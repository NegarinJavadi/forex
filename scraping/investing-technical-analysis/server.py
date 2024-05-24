import http.server
import socketserver
import webbrowser

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    webbrowser.open_new_tab(f"http://localhost:{PORT}/investing_data_fetcher.html")
    httpd.serve_forever()
