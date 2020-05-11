input1 = b'\xe0\x32\x3b'
input2= b'\x80\x07\x00'

result = int.from_bytes(input1, byteorder="little", signed=False)
print(result)

result = int.from_bytes(input2, byteorder="little", signed=False)
print(result)
