import json
import pickle

from http import HTTPStatus
from logging import Logger, getLogger
from http.server import BaseHTTPRequestHandler, HTTPServer

from awslambdalocal.loader import FunctionLoader


def start(
    loader: FunctionLoader,
    server_port: int = 8008,
    logger: Logger = getLogger()
):
    class RequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            datalen = int(self.headers['Content-Length'])
            data = self.rfile.read(datalen)
            event = json.loads(data)
            (result, err_type) = loader.load(event)
            print(result)

            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            if result:
                self.wfile.write(pickle.dumps(result))
            elif err_type:
                self.wfile.write(pickle.dumps(err_type))

    server = HTTPServer(('localhost', server_port), RequestHandler)
    logger.info("Server started http://localhost:%s" % (server_port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    logger.info("Server stopped.")
    