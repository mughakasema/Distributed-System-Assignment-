import socket
import pickle
import numpy as np

HOST = "0.0.0.0"
PORT = 5002

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"[WORKER] Waiting for master on port {PORT}...")

while True:
    conn, addr = server.accept()
    print(f"[WORKER] Connected to master: {addr}")

    data = conn.recv(65536)

    if data == b"SHUTDOWN":
        print(f"[WORKER] Shutdown signal received. Exiting...")
        conn.close()
        server.close()
        break

    worker_rows, B = pickle.loads(data)

    print(f"[WORKER] Received rows: {worker_rows.shape}, B: {B.shape}")

    result = np.dot(worker_rows, B)

    conn.send(pickle.dumps(result))

    print(f"[WORKER] Sent computed result back to master \n")

    conn.close()
