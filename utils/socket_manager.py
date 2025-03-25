from fastapi_socketio import SocketManager

socket_manager = None  # Inicializar como None

def init_socket_manager(app):
    global socket_manager
    # Configura CORS directamente en Socket.IO
    socket_manager = SocketManager(
        app=app,
        mount_location="/socket.io",
        cors_allowed_origins=["http://localhost:8080"]  # Permitir solo este origen
    )

    # Manejar eventos de conexión y desconexión
    @socket_manager.on("connect")
    async def connect(sid, environ):
        print(f"Cliente conectado: {sid}")

    @socket_manager.on("disconnect")
    async def disconnect(sid):
        print(f"Cliente desconectado: {sid}")