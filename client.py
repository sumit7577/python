import socket
from request import Request
from response import Response
import time

class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.id = 1

    def send_request(self):
        while True:
            try:
                op_code = int(input("Enter Operation Code [0-5]: "))
                operand_one = int(input("Enter Operand One: "))
                operand_two = int(input("Enter Operand Two: "))

                request = Request(op_code,self.id, operand_one, operand_two)
                request_bytes = request.encode()
                start_time = time.time()

                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket object
                client_socket.connect((self.host, self.port))  # Connect to server

                client_socket.send(request_bytes)  # Send request to server
                response_bytes = client_socket.recv(1024)  # Receive response from server

                # Decode and print response
                result = Response.decode(response_bytes)
                response_hex = ' '.join(f'{byte:02x}' for byte in response_bytes)
                print(response_hex)
                print(f'Response: #{result.request_id} {result.result} (error: {result.error_code}) (time elapsed: {round((time.time()- start_time),3)}sec)')

                client_socket.close()  # Close connection with server

                # Ask user whether to resend request
                resend = input("Do you want to resend the request? (y/n): ")
                if resend.lower() == 'y':
                    self.id +=1
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter valid integer values.")

if __name__ == "__main__":
    HOST = '127.0.0.1'  # localhost
    PORT = 12345  # Port to connect to
    client = TCPClient(HOST, PORT)
    client.send_request()
