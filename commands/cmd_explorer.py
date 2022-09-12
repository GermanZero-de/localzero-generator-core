# pyright: strict
###### WORDS OF WARNING
# This implements a simple http JSON "RPC" server for the generator
#
# The keyword here is simple! You do NOT want to run this open on the
# internet. It is purely a way to get a UI for developers of the generator
# up and running, easily without having to spin up docker or anything else.
#
# More specifically this is not intented to be the RPC server that we will
# offer to the outside world. This is just a quick-dirty test bed for RPCs
# + the thing needed to provide the UI.

from typing import Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import jsonrpcserver

from climatevision.generator import RefData
from climatevision import tracing
from climatevision.server import GeneratorRpcs


def cmd_explorer(args: Any):
    finalize_traces_if_enabled = tracing.maybe_enable(args)
    rd = RefData.load()
    generator_rpcs = GeneratorRpcs(rd, finalize_traces_if_enabled)
    with open("explorer/index.html", encoding="utf-8") as index_file:
        index = index_file.read()
    with open("explorer/elm.js", encoding="utf-8") as elm_js_file:
        elm_js = elm_js_file.read()

    class ExplorerHandler(BaseHTTPRequestHandler):
        def handle_index(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(index.encode())

        def handle_elm_js(self):
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            self.end_headers()
            self.wfile.write(elm_js.encode())

        def do_POST(self):
            match self.path.split("/"):
                case ["", "api", "v0"]:
                    content_len = int(self.headers["Content-Length"])
                    if content_len < 0 or content_len > 1024 * 1024 * 5:
                        self.send_response(400)
                        return
                    request = self.rfile.read(content_len).decode()
                    response = jsonrpcserver.dispatch(
                        request,
                        methods=generator_rpcs.methods(),  # type: ignore TODO: Figure out a better way to deal with this
                    )
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(response.encode())
                case _:
                    self.send_response(404)
                    self.end_headers()

        def do_OPTIONS(self):
            print("OPTIONS", self.command)
            print(self.path.split("/"))
            self.send_response(204)
            self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

        def do_GET(self):
            print(self.command)
            print(self.path.split("/"))
            match self.path.split("/"):
                case ["", ""]:
                    self.handle_index()

                case ["", "elm.js"]:
                    self.handle_elm_js()

                case _:
                    self.send_response(404)
                    self.end_headers()

    httpd = HTTPServer(("", 4070), ExplorerHandler)
    print("Ready to go. Explore at http://localhost:4070")
    httpd.serve_forever()
