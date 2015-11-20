# -*- coding: utf-8 -*-
import argparse
try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    from urlparse import urlparse, parse_qsl
except ImportError:
    from urllib.parse import urlparse, parse_qsl
import subprocess
import sys
import threading


URL_PREFIX = "/webhook/"


def get_handler(args):
    key = URL_PREFIX + args.key
    if not key.endswith("/"):
        key += "/"

    class CommandHandler(BaseHTTPRequestHandler):
        exec_in_progress = False

        def _constant_time_compare(self, val1, val2):
            """
            Mitigate timing attacks on the URL.
            """
            if len(val1) != len(val2):
                return False

            result = 0
            for x, y in zip(val1, val2):
                result |= ord(x) ^ ord(y)
            return result == 0

        def _exec(self, parameters):
            CommandHandler.exec_in_progress = True
            if args.template:
                try:
                    subprocess.call(args.command.format(**parameters), shell=True)
                except KeyError:
                    print("Could not execute command, required parameters not passed.")
            else:
                subprocess.call(args.command, shell=True)
            CommandHandler.exec_in_progress = False

        def do_GET(self):
            url = urlparse(self.path)
            path = url.path
            parameters = dict(parse_qsl(url.query))

            if not path.endswith("/"):
                self.path += "/"

            if self._constant_time_compare(path, key):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                if CommandHandler.exec_in_progress:
                    self.wfile.write(b'{"status": "Another command is already in progress."}')
                else:
                    self.wfile.write(b'{"status": "ok"}')
                    t = threading.Thread(target=self._exec, args=[parameters])
                    t.daemon = True
                    t.start()
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Page not found.")

            return
        do_POST = do_GET
    return CommandHandler


def main():
    parser = argparse.ArgumentParser(description='Run a command when a webhook is triggered.')
    parser.add_argument('command', help='the command to run when the URL is requested')
    parser.add_argument('-k', '--key', default="changeme", help='the secret key that will trigger the command')
    parser.add_argument('-t', '--template', action="store_true", help='whether to use template formatting based on the query string parameters')
    parser.add_argument('-p', '--port', type=int, default=48743, help='the port to listen on')
    parser.add_argument('-i', '--interface', default="0.0.0.0", help='the interface to listen on')

    args = parser.parse_args()

    try:
        server = HTTPServer((args.interface, args.port), get_handler(args))
    except:
        print("Could not start server, invalid interface or port specified.")
        sys.exit(1)

    print("Starting server...\nTrigger URL: http://%s:%s%s%s/\nCommand: %s" % (args.interface, args.port, URL_PREFIX, args.key, args.command))
    try:
        server.serve_forever()
    except:
        server.socket.close()

if __name__ == "__main__":
    main()
