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

from dataclasses import asdict
from typing import Callable, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from generatorcore.inputs import Inputs
from generatorcore.generator import calculate
from generatorcore.refdata import RefData
from generatorcore.makeentries import make_entries, Entries

from . import monkeypatch


def cmd_explorer(args: Any):
    finalize_traces_if_enabled = monkeypatch.maybe_enable_tracing(args)
    rd = RefData.load()
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

        def json_rpc(self, f: Callable[[], object]):
            error = None
            response = None
            try:
                response = f()
            except Exception as e:
                error = e

            if error is None:
                assert response is not None
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(500)
                self.send_header("Access-Control-Allow-Origin", "*")
                # Todo: consider sending the error as a json
                self.end_headers()
                print(error)

        def handle_make_entries(self, ags: str, year: int):
            return self.json_rpc(
                lambda: finalize_traces_if_enabled(asdict(make_entries(rd, ags, year)))
            )

        def handle_calculate(
            self, ags: str, year: int, request: dict[str, float | str | int] = {}
        ):
            def calc():
                defaults = asdict(make_entries(rd, ags, year))
                defaults.update(request)
                entries = Entries(**defaults)
                inputs = Inputs(
                    facts_and_assumptions=rd.facts_and_assumptions(), entries=entries
                )
                g = calculate(inputs)
                return finalize_traces_if_enabled(g.result_dict())

            return self.json_rpc(calc)

        def do_POST(self):
            match self.path.split("/"):
                case ["", "calculate", ags, year]:
                    print("handling post")
                    content_len = int(self.headers["Content-Length"])
                    if content_len < 0 or content_len > 1024 * 1024 * 5:
                        self.send_response(400)
                        return
                    content = self.rfile.read(content_len)
                    request = json.loads(content)
                    print("got request")
                    self.handle_calculate(ags, int(year), request)
                    print("post handled")
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
                case ["", "calculate", ags, year]:
                    self.handle_calculate(ags, int(year))

                case ["", "make-entries", ags, year]:
                    self.handle_make_entries(ags, int(year))

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
