import socket
from game import ONUW
from client import Client

# Run when file has started
if __name__ == "__main__":
    print("Client - Running One Night Ultimate Werewolf...")
    while True:
        host = None
        port = None
        while True:
            host = None
            port = None
            host = input("Client: Enter host (Leave empty to quit): ")
            if host:
                try:
                    port = input("Client:  Enter port (higher than 1023) (Leave empty to quit): ")
                    if port:
                        port = int(port)
                        if port < 1024:
                            print("Invalid input - Must be higher than 1023 - Try again")
                            continue
                except:
                    print("Invalid input - Must be an integer - Try again")
                    continue
            break
        
        if host and port:
            print(f"Host: {host}; Port: {port}")
            try:
                game = ONUW(Client(host, port))
                game.run()
                print("Thanks for playing!")
            except socket.gaierror as e:
                print(e)
                print("Invalid Host - Try again")
                continue
            except socket.error as e:
                print(e)
                print("Invalid Port - Try again")
                continue
        break