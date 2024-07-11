import http.server
import socketserver
import webbrowser

PORT = 8000
#This specifies the port number on which the server will listen for incoming requests

Handler = http.server.SimpleHTTPRequestHandler
#SimpleHTTPRequestHandler is a built-in class that handles HTTP requests in a simple way, 
#serving files from the current directory and its subdirectories

with socketserver.TCPServer(("", PORT), Handler) as httpd:
#This line creates a TCP server using socketserver.TCPServer within a context manager (with statement)
#("", PORT) specifies that the server should bind to all available IP addresses ("" means all interfaces) on port 8000.
#Handler specifies that the server should use SimpleHTTPRequestHandler to handle incoming requests.
#httpd is the variable name for the server instance created by socketserver.TTCPServer
    print("Serving at port", PORT)
    webbrowser.open_new_tab(f"http://localhost:{PORT}/investing_data_fetcher.html")
    #This line opens the default web browser and navigates to the URL
    #webbrowser.open_new_tab function opens this URL in a new browser tab. This is useful for automatically displaying a specific HTML file when the server starts
    httpd.serve_forever()
    #This line starts the server and keeps it running indefinitely.
    #The serve_forever method handles incoming requests and processes them using the specified request handler
