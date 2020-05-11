input1 = b'\x3a\x06\x00'
input2= b'\x80\x07\x00'

result = int.from_bytes(input1, byteorder="little", signed=False)
print(result)

result = int.from_bytes(input2, byteorder="little", signed=False)
print(result)
