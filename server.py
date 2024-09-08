from src.grpc.user_service.server.user_service_server import serve
from uvicorn import run
from src.main import app
import threading


def start_web_server():
    """
    Runs the FastAPI server
    """
    run(app, host="0.0.0.0", port=8000)


def start_grpc_server():
    """
    Runs the gRPC server
    """
    serve()


if __name__ == "__main__":
    web_server_thread = threading.Thread(target=start_web_server)
    grpc_server_thread = threading.Thread(target=start_grpc_server)

    web_server_thread.start()
    grpc_server_thread.start()

    web_server_thread.join()
    grpc_server_thread.join()
