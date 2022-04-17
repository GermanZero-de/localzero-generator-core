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
import json
import dataclasses
from typing import Callable, Any
from generatorcore.inputs import Inputs
from generatorcore.generator import calculate
from generatorcore.refdata import RefData
from generatorcore.makeentries import make_entries
from http.server import HTTPServer, BaseHTTPRequestHandler


def cmd_explorer(args: Any):
    rd = RefData.load()
    with open("explorer/index.html") as index_file:
        index = index_file.read()

    class ExplorerHandler(BaseHTTPRequestHandler):
        def handle_index(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(index.encode())

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

        def handle_make_entries(self, ags: str, year: int):
            return self.json_rpc(
                lambda: dataclasses.asdict(make_entries(rd, ags, year))
            )

        def handle_calculate(self, ags: str, year: int):
            def calc():
                e = make_entries(rd, ags, year)
                inputs = Inputs(
                    facts_and_assumptions=rd.facts_and_assumptions(), entries=e
                )
                g = calculate(inputs)
                return g.result_dict()

            return self.json_rpc(calc)

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

                case _:
                    self.send_response(404)
                    self.end_headers()
                    return

    httpd = HTTPServer(("", 4070), ExplorerHandler)
    print("Ready to go. Explore at http://localhost:4070")
    httpd.serve_forever()
