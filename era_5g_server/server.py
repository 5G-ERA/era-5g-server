from multiprocessing import Process
from typing import Any, Dict

import socketio
import ujson
from engineio.payload import Payload
from flask import Flask

from era_5g_interface.dataclasses.control_command import ControlCommand


class ArgFormatError(Exception):
    pass


class NetworkApplicationServer(Process):
    def __init__(
        self,
        port: int,
        *args,
        host: str = "0.0.0.0",
        async_handlers: bool = True,
        max_message_size: float = 5,
        **kwargs,
    ) -> None:
        """_summary_

        Args:
            port (int): The port number on which the websocket server should run.
            host (str, optional): The IP address of the interface, where the websocket server should run. Defaults to "0.0.0.0".
            async_handlers (bool, optional): Specify, if the incoming messages. Defaults to True.
            max_message_size (float, optional): The maximum size of the message to be passed in MB. Defaults to 5.
        """
        super().__init__(*args, **kwargs)

        # to get rid of ValueError: Too many packets in payload (see https://github.com/miguelgrinberg/python-engineio/issues/142)
        Payload.max_decode_packets = 50

        # the max_http_buffer_size parameter defines the max size of the message to be passed
        self.sio = socketio.Server(
            async_mode="threading",
            async_handlers=False,
            max_http_buffer_size=max_message_size * (1024**2),
            json=ujson,
        )
        self.app = Flask(__name__)
        self.app.wsgi_app = socketio.WSGIApp(self.sio, self.app.wsgi_app)  # type: ignore
        self.sio.on("connect", self.connect_data, namespace="/data")
        self.sio.on("connect", self.connect_control, namespace="/control")

        self.sio.on("command", self.command_callback_websocket, namespace="/control")

        self.sio.on("disconnect", self.disconnect_data, namespace="/data")
        self.sio.on("disconnect", self.disconnect_control, namespace="/control")
        self.port = port
        self.host = host

        # self.result_subscribers: Set[str] = LockedSet()

    def run_server(self):
        self.app.run(port=self.port, host=self.host)

    def get_sid_of_namespace(self, eio_sid: str, namespace: str):
        return self.sio.manager.sid_from_eio_sid(eio_sid, namespace)

    def get_sid_of_data(self, eio_sid: str):
        return self.get_sid_of_namespace(eio_sid, "/data")

    def get_sid_of_control(self, eio_sid: str):
        return self.get_sid_of_namespace(eio_sid, "/control")

    def connect_data(self, sid: str, environ: Dict[str, Any]):
        """_summary_ Creates a websocket connection to the client for passing
        the data.

        Raises:
            ConnectionRefusedError: Raised when attempt for connection were made
                without registering first.
        """
        print(f"Connected data. Session id: {self.sio.manager.eio_sid_from_sid(sid, '/data')}, namespace_id: {sid}")
        self.sio.send("you are connected", namespace="/data", to=sid)

    def connect_control(self, sid: str, environ: Dict[str, Any]):
        """_summary_ Creates a websocket connection to the client for passing
        control commands.

        Raises:
            ConnectionRefusedError: Raised when attempt for connection were made
                without registering first.
        """

        print(
            f"Connected control. Session id: {self.sio.manager.eio_sid_from_sid(sid, '/control')}, namespace_id: {sid}"
        )
        self.sio.send("you are connected", namespace="/control", to=sid)

    def command_callback_websocket(self, sid: str, data: Dict[str, Any]):
        eio_sid = self.sio.manager.eio_sid_from_sid(sid, "/control")
        try:
            command = ControlCommand(**data)
        except TypeError as e:
            print(f"Could not parse Control Command. {str(e)}")
            self.sio.emit(
                "control_cmd_error",
                {"error": f"Could not parse Control Command. {str(e)}"},
                namespace="/control",
                to=sid,
            )
            return

        print(
            f"Control command {command} processing: session id: {sid}"
        )  # check if the client wants to receive results
        return self.process_command(command, eio_sid)

    def process_command(self, command: ControlCommand, eio_sid: str):
        pass

    def client_disconnected(self, eio_sid):
        pass

    def disconnect_data(self, sid: str):
        eio_sid = self.sio.manager.eio_sid_from_sid(sid, "/data")
        self.client_disconnected(eio_sid)
        print(f"Client disconnected from /data namespace: session id: {sid}")

    def disconnect_control(self, sid: str):
        print(f"Client disconnected from /control namespace: session id: {sid}")
