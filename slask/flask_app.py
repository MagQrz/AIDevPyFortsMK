from contextlib import redirect_stdout, redirect_stderr
import io
import threading

from slask import server

class FlaskApp:
    def __init__(self, debug=False):
        self.debug = debug
    
    def run(self):
        dummy_stream = io.StringIO()
        with redirect_stdout(dummy_stream), redirect_stderr(dummy_stream):
            server.run(debug=self.debug)
    
    def run_in_thread(self):
        flask_thread = threading.Thread(target=self.run, daemon=True)
        flask_thread.start()