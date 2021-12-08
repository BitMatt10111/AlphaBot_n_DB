# AlphaBot and DB
Hi there!
In this repository you can find scripts to make AlphaBot move with DataBase in SQlite.

## Step 1 - Write a TCP Client in Python

```
s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s.connect(('192.168.0.131',5000))
while True:
	com = input("Inserisci nome comando:")
	s.sendall(com.encode())
```
This very short script allow us to:

- set up the socket for the trasmission
- connect the client to the server
- take as input the name sequence (ex: Square)
- send the message to the server

## Step 2 - Write a TCP Server in Python

```
s=sck.socket(sck.AF_INET,sck.SOCK_STREAM)
s.bind(("192.168.0.131",5000))
s.listen()
while True:
	connection, address=s.accept()
	client=Client_Manager(connection,address)
	client.start()
```
This script, located in the main function, allow us to:

- set up the socket for the trasmission
- receive the connection request from the client
- create and run the thread to manage the client

```
def run(self):
	while self.running:
		msg=self.connection.recv(4096).decode()
		conn = sqlite3.connect("movements.db")
		cur = conn.cursor()
		cur.execute(f"SELECT sequenza FROM movements WHERE nome = '{msg}'")
		comandi = cur.fetchall()[0][0]
		l_comandi=comandi.split(":")
		for comando in l_comandi:
			c=comando[0]
		if c!="S":
			sec=float(comando[1:])
		if c[0] == "F":
			self.alpha.forward(sec)
		elif c[0] == "S":
			self.alpha.stop()
		elif c[0] == "B":
			self.alpha.backward(sec)
		elif c[0] == "R":
			self.alpha.right(sec)
		elif c[0] == "L":
			self.alpha.left(sec)
		else:
			logging.debug("Errore di sintassi")
```
This script is the function that allow us to manage the client:

- receive the message from the client
- connect the python file to the SQLite database file
- make a query to get the sequence from the movement name
- split the sequence and call the function for each basic movement also saying the duration in second

## Step 3 - Setup

The last step is setup a database with a table with sequences names and the related sequence.
|ciao
After that the job is done and your alphabot is ready to go!
