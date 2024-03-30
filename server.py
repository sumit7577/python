import socket
from request import Request
from response import Response

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def handle_request(self, client_socket, client_address):
        request_bytes = client_socket.recv(1024)  # Receive request from client
        request = Request.decode(request_bytes)  # Decode request
        
        # Handle request
        result = request.compute()
        operand = request.get_operands(request.op_code)
        request_hex = ""

        for index,byte in enumerate(request_bytes):
            if index==0:
                request_hex += str(byte)+ " "
            else:
                request_hex += '{:02x} '.format(byte)

        print(f"Request #{request.request_id}: {request.operand_one} {operand} {request.operand_two}")
        print(request_hex)

        error_code = 0 if request.tml > 0 else 127

        response = Response(result,error_code,request.request_id)
        response_bytes = response.encode()
        client_socket.send(response_bytes)

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket object
        server_socket.bind((self.host, self.port))  # Bind to address and port
        server_socket.listen(5)  # Listen for incoming connections

        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()  # Accept client connection

            # Handle client request in a new thread
            self.handle_request(client_socket, client_address)

if __name__ == "__main__":
    HOST = '127.0.0.1'  # localhost
    PORT = 12345  # Port to listen on
    server = TCPServer(HOST, PORT)
    server.start()
