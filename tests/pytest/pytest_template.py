"""
Filename : TEST-DM-XXX.py
Title : 테스트 제목
Desc : 테스트 상세
"""

import os

import dotenv
import socketio

from base.model.data import Message

# Note.1 Global Vars
sio = socketio.Client(logger=False, engineio_logger=False)
capture_list = []
capture_count = 0

# Note.2 Load ENV Vars
dev_env_path = "../dev.env"
dotenv.load_dotenv(dev_env_path)

# Note.3 Const Vars
RUN_SERVER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # base/tests
PYTEST_LOG_FILE_PATH = os.path.join(
    os.path.expanduser("~"), "logs", f"{os.environ['BASE_APP_NAME']}-{os.environ['BASE_LOG_FILE']}"
)
PYTEST_PID = os.getpid()


########################################
# Note. WebSocket Client Event Handler
########################################
@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print(f"The connection failed! {data}")


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.on("on_message")
def on_message(data):
    global capture_list
    global capture_count

    message = Message.parse_obj(data)
    if capture_count and message.data["text"]:
        capture_list.append(message.data["text"])
        capture_count -= 1


def init_socket():
    header = {"Content-Type": "application/json", "Authorization": ""}
    auths = {}

    host = os.environ["BASE_WEBSOCKET_HOST"]
    port = os.environ["BASE_WEBSOCKET_PORT"]
    sio.connect(f"http://{host}:{port}", headers=header, auth=auths)
    sio.sleep(1)


def emit(text: str, count: int = 0):
    global capture_list
    global capture_count

    if count:
        capture_list.clear()
        capture_count = count

    message = Message(data={"text": text})
    sio.emit("on_message", data=message.dict())


########################################
# Note.  Init Function
########################################
def init_env():
    os.environ["BASE_LOG_FILE"] = f"{__file__.split('/')[-1].replace('.py', '')}.log"
    os.environ["BASE_WEBSOCKET_HOST"] = "0.0.0.0"
    os.environ["BASE_WEBSOCKET_PORT"] = "9090"


def remove_log():
    global PYTEST_LOG_FILE_PATH
    if os.path.exists(PYTEST_LOG_FILE_PATH):
        os.remove(PYTEST_LOG_FILE_PATH)


########################################
# Note.  Pytest Function
########################################


def test_init():
    init_env()
    remove_log()
    init_socket()


def test_dm_000():
    """
    샘플 예시
    :return:
    """
    pass


def test_disconnect():
    sio.disconnect()
