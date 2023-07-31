import socket
import threading


class Server():
    def __init__(self):
        self.server_ip = self.get_real_ip()
        self.server_port = 9998
        
        self.connected_clients = []
        self.conversation = """"""

    def Start_Server(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip,self.server_port))
        self.server_socket.listen(5)
        print("[+]Server Started")
        print("Server Running On :",self.server_ip," Port :: ",self.server_port)
        
            
    def main(self):
        try:
            while True:
                client_socket, client_addr = self.server_socket.accept()
                print(f"Accepted connection from {client_addr[0]}:{client_addr[1]}")
                self.connected_clients.append(client_socket)
            
                client_thread = threading.Thread(target= self.handle_client, args=(client_socket,))
                client_thread.start()

        except KeyboardInterrupt:
            print("Server stopped.")
    
    def handle_client(self,client_socket):
        try:
            while True:
                data = client_socket.recv(4096).decode("utf-8")
                if data != None:
                # Process the received data (you can perform any custom logic here)
                    print(f"Received data from client: {data}")
                    self.conversation += str(data) + "\n"
                    print(self.conversation)
                    
                    for client in self.connected_clients:
                        client.send(bytes(str(data),"utf-8"))
                else:
                    pass
              
        except Exception as e:
            print(f"Error: {e}")

        finally:
            client_socket.close()
            if client_socket in self.connected_clients:
                self.connected_clients.remove(client_socket)
            

    import socket

    def get_real_ip(self):
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Connect to a public server (here we use Google's public DNS server)
            s.connect(("8.8.8.8", 80))

            # Get the socket's own address, which is the local IP address of the machine
            local_ip = s.getsockname()[0]

            # Close the socket
            s.close()

            return local_ip
        except socket.error as e:
            print("Error getting the real IP address:", e)
            return None


if __name__ == "__main__":
    server = Server()
    
    
    threading.Thread(target=server.Start_Server()).start()
    threading.Thread(target=server.main()).start()
    ##error in threading run server and main like normal