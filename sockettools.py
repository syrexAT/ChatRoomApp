#funktinon schireben die eine komplette zeile einliest im sokcet
def read_line_from_socket(s):
    result = []
    while True:
        #wenn der socket gteschlossen ist liefert .recv(1) einen b'' 
        ch = s.recv(1)
        if ch == b'':
            return None
        if ch == b'\n':
            break
        if ch != b'\r':
            result.append(ch)
    return b''.join(result).decode('utf-8')
