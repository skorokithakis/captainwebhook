# -*- coding: utf-8 -*-
import argparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess
import sys
import threading


URL_PREFIX = "/webhook/"


def get_handler(key, command):
    key = URL_PREFIX + key
    if not key.endswith("/"):
        key += "/"

    class PullHandler(BaseHTTPRequestHandler):
        pull_in_progress = False

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

        def _pull(self):
            PullHandler.pull_in_progress = True
            subprocess.call(command, shell=True)
            PullHandler.pull_in_progress = False

        def do_GET(self):
            if not self.path.endswith("/"):
                self.path += "/"
            if self._constant_time_compare(self.path, key):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                if PullHandler.pull_in_progress:
                    self.wfile.write('{"status": "Another pull is already in progress."}')
                else:
                    self.wfile.write('{"status": "ok"}')
                    t = threading.Thread(target=self._pull)
                    t.daemon = True
                    t.start()
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Page not found.")

            return
        do_POST = do_GET
    return PullHandler


def main():
    parser = argparse.ArgumentParser(description='Run a command when a webhook is triggered.')
    parser.add_argument('command', help='the command to run when the URL is requested')
    parser.add_argument('-k', '--key', default="changeme", help='the secret key that will trigger a pull')
    parser.add_argument('-p', '--port', type=int, default=48743, help='the port to listen on')
    parser.add_argument('-i', '--interface', dest='interface', default="0.0.0.0",
                       help='the interface to listen on')

    args = parser.parse_args()

    try:
        server = HTTPServer((args.interface, args.port), get_handler(args.key, args.command))
    except:
        print "Could not start server, invalid interface or port specified."
        sys.exit(1)

    print "Starting server...\nTrigger URL: http://%s:%s%s%s/\nCommand: %s" % (args.interface, args.port, URL_PREFIX, args.key, args.command)
    try:
        server.serve_forever()
    except:
        server.socket.close()

if __name__ == "__main__":
    main()
