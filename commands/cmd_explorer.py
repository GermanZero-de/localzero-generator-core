# pyright: strict reportMissingTypeStubs=true
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

import dataclasses
from typing import Callable, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import jsonrpcserver

from climatevision import generator
from climatevision.generator import Inputs, RefData
from climatevision import tracing


class CoreGeneratorRpcs:
    rd: RefData
    finalize_traces_if_enabled: Callable[[Any], Any]

    def __init__(self, rd: RefData, finalize_traces_if_enabled: Callable[[Any], Any]):
        self.rd = rd
        self.finalize_traces_if_enabled = finalize_traces_if_enabled

    def make_entries(self, ags: str, year: int) -> jsonrpcserver.Result:
        return jsonrpcserver.Success(
            self.finalize_traces_if_enabled(
                dataclasses.asdict(generator.make_entries(self.rd, ags, year))
            )
        )

    def calculate(
        self, ags: str, year: int, overrides: dict[str, int | float | str]
    ) -> jsonrpcserver.Result:
        defaults = dataclasses.asdict(generator.make_entries(self.rd, ags, year))
        defaults.update(overrides)
        entries = generator.Entries(**defaults)
        inputs = Inputs(
            facts_and_assumptions=self.rd.facts_and_assumptions(), entries=entries
        )
        g = generator.calculate(inputs)
        return jsonrpcserver.Success(self.finalize_traces_if_enabled(g.result_dict()))

    def methods(self) -> dict[str, Callable[[Any], jsonrpcserver.Result]]:
        return {"make-entries": self.make_entries, "calculate": self.calculate}  # type: ignore


def cmd_explorer(args: Any):
    finalize_traces_if_enabled = tracing.maybe_enable(args)
    rd = RefData.load()
    core_rpcs = CoreGeneratorRpcs(rd, finalize_traces_if_enabled)
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
                        request, methods=core_rpcs.methods()
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
