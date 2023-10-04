def protocol_header(room_name_size, operation, state, room_name, password) -> bytes:

    if len(room_name.encode("utf-8")) < 8:
        room_name = room_name.ljust(8, " ")
    
    if len(password.encode("utf-8")) < 21:
        password = password.ljust(21, " ")

    return room_name_size.to_bytes(1, "big") + \
        operation.to_bytes(1, "big") + \
        state.to_bytes(1, "big") + \
        room_name.encode("utf-8") + \
        password.encode("utf-8")

def get_room_name_size(header) -> int:
    return header[0]

def get_operation(header) -> int:
    return header[1]

def get_state(header) -> int:
    return header[2]

def get_room_name(header) -> str:
    return header[3:11].decode("utf-8").replace(" ","")

def get_password(header) -> str:
    return header[11:].decode("utf-8").replace(" ","")
