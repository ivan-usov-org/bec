import os
import pty
import sys
import threading

from flask import (
    Flask,
    request,
    redirect,
    jsonify,
    render_template,
)
from flask_socketio import SocketIO, join_room

__version__ = "1.0"

app = Flask(
    __name__,
    static_url_path="",
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
    template_folder=os.path.join(os.path.dirname(__file__), "static"),
)
app.config["SECRET_KEY"] = "nosecret"
socketio = SocketIO(app)


@app.route("/")
def initiate_session():
    return render_template("index.html")


@socketio.on("attach")
def xterm_connected(data):
    w, h = data["w"], data["h"]
    socketio.emit("ready")

    pid, fd = pty.fork()

    if pid == 0:
        os.execvp("bec", ["bec"])
    else:

        @socketio.on("terminal_input")
        def xterm_receive_terminal_input(data):
            os.write(fd, data["input"].encode())

        def send_output(fd):
            while True:
                output = os.read(fd, 1024)
                socketio.emit("terminal_output", output)

        output_dispatcher_thread = threading.Thread(target=send_output, args=(fd,))
        output_dispatcher_thread.daemon = True
        output_dispatcher_thread.start()


def main():
    socketio.run(app)
