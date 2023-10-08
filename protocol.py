def protocol_header(room_name_size, operation, state, room_name, user_name, password) -> bytes:
    room_name = ljust_replace_space(room_name, room_name.encode("utf-8"), 8)
    user_name = ljust_replace_space(user_name, user_name.encode("utf-8"), 10)
    password = ljust_replace_space(password, password.encode("utf-8"), 11)

    return room_name_size.to_bytes(1, "big") + \
        operation.to_bytes(1, "big") + \
        state.to_bytes(1, "big") + \
        room_name.encode("utf-8") + \
        user_name.encode("utf-8") + \
        password.encode("utf-8")

def ljust_replace_space(res: str,byte_str: bytes, num: int):
    return res.ljust(num, " ") if len(byte_str) < num else res

def get_room_name_size(header) -> int:
    return header[0]

def get_operation(header) -> int:
    return header[1]

def get_state(header) -> int:
    # header = header.decode("utf-8")
    print("resonseHeader: ",header)
    return header[2]

def get_room_name(header) -> str:
    return header[3:11].decode("utf-8").replace(" ","")

def get_user_name(header) -> str:
    return header[11:21].decode("utf-8").replace(" ","")

def get_password(header) -> str:
    return header[21:].decode("utf-8").replace(" ","")