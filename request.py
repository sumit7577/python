class Request:
    def __init__(self, op_code, request_id,operand_one, operand_two):
        self.op_code = op_code
        self.request_id = request_id
        self.operand_one = operand_one
        self.operand_two = operand_two
        self.op_name = self.get_op_name(op_code)
        self.op_name_length = len(self.get_op_name(op_code)) *2
        self.tml = len(self.encode_without_tml()) -1


    def compute(self):
        result = None
        if self.op_code == 0:
            result = self.operand_one * self.operand_two
        elif self.op_code == 1:
            result = self.operand_one / self.operand_two
        elif self.op_code == 2:
            result = self.operand_one | self.operand_two
        elif self.op_code == 3:
            result = self.operand_one & self.operand_two
        elif self.op_code == 4:
            result = self.operand_one - self.operand_two
        elif self.op_code == 5:
            result = self.operand_one + self.operand_two
        return result
    
    
    @staticmethod
    def get_operands(opCode):
        result = None
        if opCode == 0:
            result = "*"
        elif opCode == 1:
            result = "/"
        elif opCode == 2:
            result = "|"
        elif opCode == 3:
            result = "&"
        elif opCode == 4:
            result = "-"
        elif opCode == 5:
            result = "+"
        return result
    
    
    def get_op_name(self, op_code):
        if op_code == 0:
            return "multiplication"
        elif op_code == 1:
            return "division"
        elif op_code == 2:
            return "or"
        elif op_code == 3:
            return "and"
        elif op_code == 4:
            return "subtraction"
        elif op_code == 5:
            return "addition"
        else:
            return "unknown"
        

    def encode(self):
        # Convert fields to bytes
        tml_bytes = self.tml.to_bytes(1,byteorder="big")
        op_code_bytes = self.op_code.to_bytes(1, byteorder='big')
        request_id_bytes = self.request_id.to_bytes(2, byteorder='big')
        op_name_length_bytes = self.op_name_length.to_bytes(1, byteorder='big')
        op_name_bytes = self.op_name.encode('utf-16be')
        operand_one_bytes = self.operand_one.to_bytes(4, byteorder='big')
        operand_two_bytes = self.operand_two.to_bytes(4, byteorder='big')

        # Concatenate bytes
        encoded_request = tml_bytes + op_code_bytes +\
                          operand_one_bytes + operand_two_bytes +\
                          request_id_bytes + \
                          op_name_length_bytes + op_name_bytes
        return encoded_request
    
    
    def encode_without_tml(self):
        op_name_bytes = self.op_name.encode('utf-16be')
        operand_one_bytes = self.operand_one.to_bytes(4, byteorder='big')
        operand_two_bytes = self.operand_two.to_bytes(4, byteorder='big')
        # Concatenate bytes
        encoded_request = self.op_code.to_bytes(1, byteorder='big') + \
                          self.request_id.to_bytes(2, byteorder='big') + \
                          len(op_name_bytes).to_bytes(1, byteorder='big') + \
                          operand_one_bytes + \
                          operand_two_bytes
        return encoded_request
    

    @classmethod
    def decode(cls, request_bytes):
        op_code = int.from_bytes(request_bytes[1:2], byteorder='big')
        operand_one = int.from_bytes(request_bytes[2:6], byteorder='big')
        operand_two = int.from_bytes(request_bytes[6:10], byteorder='big')
        request_id = int.from_bytes(request_bytes[10:12], byteorder='big')
        #op_name_length = int.from_bytes(request_bytes[11:12], byteorder='big')
        #op_name = request_bytes[12:].decode('utf-16be')
        return cls(op_code, request_id, operand_one, operand_two)
