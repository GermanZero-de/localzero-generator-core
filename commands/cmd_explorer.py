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
import sys
import json
from generatorcore.inputs import Inputs
from generatorcore.generator import calculate
from generatorcore.refdata import RefData
from generatorcore.makeentries import make_entries
from http.server import HTTPServer, BaseHTTPRequestHandler


def cmd_explorer(args):
    rd = RefData.load()
    with open("explorer/index.html") as index_file:
        index = index_file.read()

    class ExplorerHandler(BaseHTTPRequestHandler):
        def handle_index(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(index.encode())

        def handle_calculate(self, ags, year):
            error = None
            response = ""
            try:
                e = make_entries(rd, ags, year)
                inputs = Inputs(
                    facts_and_assumptions=rd.facts_and_assumptions(), entries=e
                )
                g = calculate(inputs)
                response = json.dumps(g.result_dict())
            except Exception as e:
                error = e

            if error is None:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                self.send_response(500)
                print(error)

        def do_GET(self):
            print(self.command)
            print(self.path.split("/"))
            match self.path.split("/"):
                case ["", "calculate", ags, year]:
                    self.handle_calculate(ags, int(year))

                case ["", ""]:
                    self.handle_index()

                case other:
                    self.send_response(404)
                    self.end_headers()
                    return

    httpd = HTTPServer(("", 4070), ExplorerHandler)
    httpd.serve_forever()
