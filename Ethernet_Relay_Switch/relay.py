import socket, time

IP   = "192.168.1.100"
TCP  = 6722
CMDS = [b"1R", b"2R", b"00", b"2R", b"1R", b"00"]   # close 1, close 2, read, open 2, open 1, read

with socket.create_connection((IP, TCP), timeout=2) as s:
    for cmd in CMDS:
        s.sendall(cmd)
        reply = s.recv(16)
        print(cmd.decode(), "→", reply.decode(errors='ignore'))
        time.sleep(0.5)

