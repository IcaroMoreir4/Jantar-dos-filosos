### Problema do Jantar dos Filósofos - Solução de Dijkstra

O código implementa a solução proposta por Edsger Dijkstra para o clássico problema do jantar dos filósofos.

#### Componentes Principais

1. **Constantes e Estados:**
    - `NUM_FILOSOFOS`: Número total de filósofos na mesa.
    - `ESTADO_PENSANDO`, `ESTADO_COMENDO`, `ESTADO_FOME`: Estados possíveis de um filósofo.
    - `TEMPO_COMENDO_MAX`, `TEMPO_PENSANDO_MAX`: Limites de tempo para comer e pensar.

```python
NUM_FILOSOFOS = 5
ESTADO_PENSANDO = 0
ESTADO_COMENDO = 1
ESTADO_FOME = 2
TEMPO_COMENDO_MAX = 3
TEMPO_PENSANDO_MAX = 2
```

2. **Classe `JantarDosFilosofos`:**
    - Gerencia os estados dos filósofos e a lógica para pegar e devolver garfos.
    - `mutex`: Semáforo para garantir acesso exclusivo às variáveis compartilhadas.
    - `sinal`: Lista de semáforos, um para cada filósofo, usado para notificar quando é possível comer.

```python
class JantarDosFilosofos:
    def __init__(self):
        self.estados = [ESTADO_PENSANDO] * NUM_FILOSOFOS
        self.mutex = threading.Semaphore(1)
        self.sinal = [threading.Semaphore(0) for _ in range(NUM_FILOSOFOS)]
```

3. **Métodos da Classe:**
    - `pegar_garfos(filosofo_id)`: Filósofo tenta pegar os garfos.
    - `devolver_garfos(filosofo_id)`: Filósofo devolve os garfos após comer.
    - `testar(filosofo_id)`: Verifica se um filósofo pode começar a comer sem causar impasses.

```python
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
                self.estados[(filosofofo_id - 1) % NUM_FILOSOFOS] != ESTADO_COMENDO):
            self.estados[filosofo_id] = ESTADO_COMENDO
            self.sinal[filosofo_id].release()
```

4. **Funções dos Filósofos:**
    - `filosofo(jantar, filosofo_id)`: Função que representa o comportamento de um filósofo.
    - `pensar(filosofo_id)`: Simula o estado de pensamento do filósofo.
    - `comer(filosofo_id)`: Simula o estado de comer do filósofo.

```python
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
```

5. **Inicialização e Execução:**
    - Cria uma instância do `JantarDosFilosofos` e threads para cada filósofo.

```python
if __name__ == "__main__":
    jantar = JantarDosFilosofos()
    filosofos = [threading.Thread(target=filosofo, args=(jantar, i)) for i in range(NUM_FILOSOFOS)]

    for filosofo_thread in filosofos:
        filosofo_thread.start()

    for filosofo_thread in filosofos:
        filosofo_thread.join()
```

Esta implementação utiliza semáforos para garantir a exclusão mútua e evitar impasses, tornando a execução dos filósofos mais segura em ambientes concorrentes.