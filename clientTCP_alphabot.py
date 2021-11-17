import socket as sck

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) #prepara il socket per la trasmissione TCP
    s.connect(('192.168.0.131',5000)) #trova la connessione

    while True:
        com = input("Inserisci nome comando:") #nome della senquenza sul database
        s.sendall(com.encode()) #invia il comando

if __name__=="__main__":
    main()
