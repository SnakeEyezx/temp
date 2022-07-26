from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        time = datetime.datetime.now()
        response_data = ("Time: %s\nRequest: %s\n" % (time, self.path)).encode()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response_data)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), MyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("The End")
