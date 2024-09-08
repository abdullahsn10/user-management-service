from uvicorn import run
from src.main import app
from src.grpc.server.user_service_server import serve

if __name__ == "__main__":
    # run(app, host="0.0.0.0", port=8000)
    serve()
