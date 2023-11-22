import threading
import time
import random

NUM_FILOSOFOS = 5
ESTADO_PENSANDO = 0
ESTADO_COMENDO = 1
ESTADO_FOME = 2
TEMPO_COMENDO_MAX = 3
TEMPO_PENSANDO_MAX = 2

class JantarDosFilosofos:
    def __init__(self):
        self.estados = [ESTADO_PENSANDO] * NUM_FILOSOFOS
        self.mutex = threading.Semaphore(1)
        self.sinal = [threading.Semaphore(0) for _ in range(NUM_FILOSOFOS)]

    def pegar_garfos(self, filosofo_id):
        self.mutex.acquire()
        self.estados[filosofo_id] = ESTADO_FOME
        self.testar(filosofo_id)
        self.mutex.release()
        self.sinal[filosofo_id].acquire()

    def devolver_garfos(self, filosofo_id):
        self.mutex.acquire()
        self.estados[filosofo_id] = ESTADO_PENSANDO
        self.testar((filosofo_id + 1) % NUM_FILOSOFOS)
        self.testar((filosofo_id - 1) % NUM_FILOSOFOS)
        self.mutex.release()

    def testar(self, filosofo_id):
        if (self.estados[filosofo_id] == ESTADO_FOME and
                self.estados[(filosofo_id + 1) % NUM_FILOSOFOS] != ESTADO_COMENDO and
                self.estados[(filosofo_id - 1) % NUM_FILOSOFOS] != ESTADO_COMENDO):
            self.estados[filosofo_id] = ESTADO_COMENDO
            self.sinal[filosofo_id].release()

def filosofo(jantar, filosofo_id):
    while True:
        jantar.pegar_garfos(filosofo_id)
        comer(filosofo_id)
        jantar.devolver_garfos(filosofo_id)
        pensar(filosofo_id)

def pensar(filosofo_id):
    print(f"Filósofo {filosofo_id} está pensando.")
    time.sleep(random.uniform(0, TEMPO_PENSANDO_MAX))

def comer(filosofo_id):
    print(f"Filósofo {filosofo_id} está comendo.")
    time.sleep(random.uniform(0, TEMPO_COMENDO_MAX))

if __name__ == "__main__":
    jantar = JantarDosFilosofos()
    filosofos = [threading.Thread(target=filosofo, args=(jantar, i)) for i in range(NUM_FILOSOFOS)]

    for filosofo_thread in filosofos:
        filosofo_thread.start()

    for filosofo_thread in filosofos:
        filosofo_thread.join()
