def calculate_checksum(data: bytes) -> int:
    data = bytearray(data)
    if len(data) % 2 != 0:
        data.append(0)

    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i+1]
        checksum += word

    checksum = checksum & 0xFFFF
    return checksum ^ 0xFFFF

def verify_checksum(data: bytes, checksum: int) -> bool:
    data = bytearray(data)
    if len(data) % 2 != 0:
        data.append(0)

    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i+1]
        total += word

    total &= 0xFFFF
    total += checksum

    return total == 0xFFFF

def test_checksum_functions():
    # Корректные данные
    data1 = b'hello world'
    cs1 = calculate_checksum(data1)
    assert verify_checksum(data1, cs1) == True, "Test 1 failed"

    # Ошибка в одном бите
    data2 = bytearray(data1)
    data2[0] ^= 0x01
    assert verify_checksum(data2, cs1) == False, "Test 2 failed"

    # 3. Пустые данные
    data3 = b''
    cs3 = calculate_checksum(data3)
    assert verify_checksum(data3, cs3) == True, "Test 3 failed"

    print("All tests passed successfully.")

if __name__ == "__main__":
    test_checksum_functions()
