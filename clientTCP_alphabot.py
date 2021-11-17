#tcp
#f"!list" -> f"list:{dict.keys()}"

import socket as sck

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect(('192.168.0.131',5000))

    while True:
        com = input("Inserisci comando e tempo:")
        #pot1 = input("Inserisi potenza motore A:")
        #pot2 = input("Inserisi potenza motore B:")
        s.sendall(com.encode())

        #risp = s.recv(4096)
        #risp = risp.decode()
        
        #print(risp)

        """
        data = s.recvfrom(4096)
        data = data.decode()
        data = data.split(":")

        if data[0] == 0:
            print("Ho fatto bene")
        elif data[1] == 1:
            print("Ho sbagliato")
            ris = input("Hai capito l'errore:")   #devo dire si --> 0 || no --> 1
            s.sendall(ris.decode())
        """


if __name__=="__main__":
    main()