#Librerie
import urllib2, re, time, sys, random
from threading import Thread

#Banner
print '''
    ______                __                __      ____  __                        _____                                 
   / ____/___  ________  / /_  ____  ____  / /__   / __ \/ /_  ____  ____  ___     / ___/_________  ____  ____  ___  _____
  / /_  / __ \/ ___/ _ \/ __ \/ __ \/ __ \/ //_/  / /_/ / __ \/ __ \/ __ \/ _ \    \__ \/ ___/ __ \/ __ \/ __ \/ _ \/ ___/
 / __/ / /_/ / /__/  __/ /_/ / /_/ / /_/ / /<    / ____/ / / / /_/ / / / /  __/   ___/ / /__/ /_/ / / / / / / /  __/ /    
/_/    \____/\___/\___/_____/\____/\____/_/|_|  /_/   /_/ /_/\____/_/ /_/\___/   /____/\___/\____/_/ /_/_/ /_/\___/_/ 
'''

#Oggetto per fare richieste http
global opener
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'lu=XXX; fr=XXX; c_user=XXX; xs=XXX;'))
opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'))

#Funzione per ottenere il nome corrispondente ad un numero
def fbCheck(numero):
	response = opener.open("https://m.facebook.com/search/top/?q=%d" % numero)
	page_source = str(response.read())	
	nome = re.compile("<td class=\"bl\"><a[^<]*>([^<]+)").findall(page_source)
	if len(nome)>0:
		sys.stdout.write(str(numero)+" = "+str(nome[0])+"\n")
		with open("lista.txt", "a") as myfile:
			myfile.write(str(numero)+" = "+str(nome[0])+"\n")

#Controlla la connessione a facebook.com e termina il programma se fallisce
def controllaConnessione():
	try:
		sys.stdout.write("Sto controllando se riesco a collegarmi a Facebook...\n")
		ret = urllib2.urlopen('https://m.facebook.com/')
		sys.stdout.write("Connessione riuscita!\n")
	except Exception, e:
		print "Non riesco a connettermi a Facebook: "+str(e)+"!\nControlla le impostazioni di rete!\n\nUscendo..."
		sys.exit()

#Controllo se Facebook e' on
controllaConnessione()
#Chiedo la modalita' di scansione (range, file o numero parziale)
mode = input("\n\nScegli la modalita':\n1. Range\n2. Da file\nScelta: ")
if mode == 1:
	threads = input("\nThread: ")
	startn	= input("Numero di partenza: ")
	endn	= input("Numero di fine: ")
	finiti	= 0
	print "\n"
	if endn-startn+1>0:
		class newThread(Thread):
			def __init__(self):
				Thread.__init__(self)
				self.daemon = True
				self.start()
			def run(self):
				global threads, startn, endn, finiti
				while True:
					#Richiesta http
					if startn<=endn:
						fbCheck(startn)
						startn=startn+1
					else:
						finiti=finiti+1
						break
		for nt in range(threads):
			newThread()
			startn=startn+1
		try:
			while True:
				if finiti>=threads:
					print "\nFinito!...\n"
					exit()
				time.sleep(1)
		except KeyboardInterrupt:
			print "\nUscendo...\n"
	else:
		print "\nIl numero iniziale deve essere inferiore o uguale a quello finale! Uscendo...\n"
elif mode == 2:
	filename = raw_input("\nInput file: ")
	file=open(filename)
	file=file.readlines()
	numerolinea=0
	numerolineamax=len(file)
	threads = input("Thread: ")
	finiti=0
	print "\n"
	class newThread(Thread):
		def __init__(self):
			Thread.__init__(self)
			self.daemon = True
			self.start()
		def run(self):
			global numerolinea,numerolineamax,finiti
			while True:
				#Richiesta http
				if numerolinea<numerolineamax:
					numero=file[numerolinea].rstrip()
					fbCheck(int(numero))
					numerolinea=numerolinea+1
				else:
					finiti=finiti+1
					break
	for nt in range(threads):
		newThread()
		numerolinea=numerolinea+1
	try:
		while True:
			if finiti>=threads:
				print "\nFinito!...\n"
				exit()
			time.sleep(1)
	except KeyboardInterrupt:
		print "\nUscendo...\n"
else:
	print "Inserisci una scelta valida! Uscendo...\n"
