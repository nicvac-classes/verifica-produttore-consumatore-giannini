import threading
import random

DIM_BUFFER = 5
N_PRODUTTORI = 3
N_CONSUMATORI = 2
N_ORDINI = 6

buffer = [None] * DIM_BUFFER
metti = 0
togli = 0

vuoto = threading.Semaphore(DIM_BUFFER)
pieno = threading.Semaphore(0)
mutexP = threading.Semaphore(1)
mutexC = threading.Semaphore(1)


def genera_ordine():
    return f"ORD-{random.randint(10000, 99999)}"


class ProduttoreThread(threading.Thread):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx
        self.dato = genera_ordine()

    # DA IMPLEMENTARE (run)
    def run(self):
        global metti 
        ordiniGenerati = 0

        while ordiniGenerati < N_ORDINI:
            vuoto.acquire()
            mutexP.acquire()
            i_metti = metti
            metti = (metti + 1) % DIM_BUFFER
            mutexP.release()
            buffer[i_metti] = self.dato
            ordiniGenerati += 1
            self.dato = genera_ordine()
            print(f"[SHOP-{self.idx}] creato ordine {self.dato}")
            pieno.release()


class ConsumatoreThread(threading.Thread):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx

    def run(self):
        global togli
        termina = False

        while not termina:
            pieno.acquire()
            mutexC.acquire()
            i_togli = togli
            togli = (togli + 1 ) % DIM_BUFFER
            mutexC.release()
            dato = buffer[i_togli]

            if dato != None:
                print(f"[PACK-{self.idx}] prepara {dato}")
            else:
                termina = True
                print("Ricevuto messaggio None, uscita dal buffer...")

            vuoto.release()

def main():
    global metti

    produttori = [ProduttoreThread(i + 1) for i in range(N_PRODUTTORI)]
    consumatori = [ConsumatoreThread(i + 1) for i in range(N_CONSUMATORI)]

    # DA IMPLEMENTARE: start dei thread produttori e consumatori
    for p in produttori:
        p.start()
    for c in consumatori:
        c.start()

    # DA IMPLEMENTARE: join di tutti i produttori
    for p in produttori:
        p.join()
    
    print("Tutti i canali hanno terminato. Chiusura addetti...")

    # Invia un messaggio None per ogni addetto.
    for _ in range(N_CONSUMATORI):
        # DA IMPLEMENTARE: inserire None nel buffer
        vuoto.acquire()
        buffer[metti] = None
        metti = (metti+1) % DIM_BUFFER
        pieno.release()
        pass

    # DA IMPLEMENTARE: join di tutti i consumatori

    print("Magazzino chiuso.")
    for c in consumatori:
        c.join()

if __name__ == "__main__":
    main()
