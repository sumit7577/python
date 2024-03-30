class Response:
    def __init__(self, result,error, request_id):
        self.result = result
        self.error_code = error
        self.request_id = request_id
        self.tml = len(self.encode_with_tml()) +1

    def encode(self):
        # Convert fields to bytes
        tml_bytes = self.tml.to_bytes(1, byteorder='big')
        result_bytes = self.result.to_bytes(4, byteorder='big', signed=True)
        error_code_bytes = self.error_code.to_bytes(1, byteorder='big')
        request_id_bytes = self.request_id.to_bytes(2, byteorder='big')

        # Concatenate bytes
        encoded_response = tml_bytes + result_bytes + error_code_bytes + request_id_bytes
        return encoded_response
    
    def encode_with_tml(self):
        # Convert fields to bytes
        result_bytes = self.result.to_bytes(4, byteorder='big', signed=True)
        error_code_bytes = self.error_code.to_bytes(1, byteorder='big')
        request_id_bytes = self.request_id.to_bytes(2, byteorder='big')

        # Concatenate bytes
        encoded_response = result_bytes + error_code_bytes + request_id_bytes
        return encoded_response


    @classmethod
    def decode(cls, response_bytes):
        # Extract fields from bytes
        tml = int.from_bytes(response_bytes[0:1], byteorder='big')
        result = int.from_bytes(response_bytes[1:5], byteorder='big', signed=True)
        error_code = int.from_bytes(response_bytes[5:6], byteorder='big')
        request_id = int.from_bytes(response_bytes[6:8], byteorder='big')

        return cls(result,error_code, request_id)
