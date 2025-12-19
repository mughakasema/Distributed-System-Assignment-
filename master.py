import socket
import pickle
import numpy as np

WORKER_IP = "192.168.56.106"
PORT = 5002

N = int(input("Enter matrix size N for NxN: "))
A = np.random.randint(0, 10, (N, N))
B = np.random.randint(0, 10, (N, N))
print("Matrix A:\n", A)
print("Matrix B:\n", B)


rows_master = (len(A) + 1) // 2
local_rows = A[:rows_master]
worker_rows = A[rows_master:]

local_result = np.dot(local_rows, B)

if worker_rows.shape[0] > 0:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((WORKER_IP, PORT))
    s.send(pickle.dumps((worker_rows, B)))

    data = s.recv(65536)
    worker_result = pickle.loads(data)
    s.close()

    final_result = np.vstack((local_result, worker_result))
else:
    final_result = local_result

print("\nResult of A x B:\n", final_result)

shutdown_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
shutdown_socket.connect((WORKER_IP, PORT))
shutdown_socket.send(b"SHUTDOWN")
shutdown_socket.close()
