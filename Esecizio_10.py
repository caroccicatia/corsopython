# Esercizi 20/06/2025

## ESERCIZIO 1
## **TEST FINALE OOP - "La Battaglia dei Regni"**
### **Obiettivo**
# Realizza un **gioco a turni da terminale** in cui il **giocatore** 
# e una **IA** si sfidano con eserciti medievali. 
# Ogni giocatore ha un **budget** iniziale per acquistare soldati. 
# Gli eserciti combattono in più **round**, e dopo ogni battaglia si ricevono nuove risorse da spendere. 
# Vince chi elimina tutte le unità nemiche.
# ---
###  **Requisiti strutturali (OOP)**
####  **Classe Astratta: `Soldato`**

# * Attributi protetti: `_nome`, `_costo`, `_attacco`, `_difesa`, `_salute`
# * Metodo astratto: `attacca(avversario)`
# * Metodi comuni:
#   * `difenditi(danno)`
#   * `è_vivo() → bool`
#   * `stato() → stampa salute e ruolo`

#### **Classi Derivate:**

# Ciascuna classe implementa il metodo `attacca()` con logiche **diverse** (polimorfismo):
# 1. **Cavaliere**
#    * Alto costo, alta difesa, attacco medio
#    * 20% di possibilità di **colpo critico** (attacco × 2)

# 2. **Arciere**
#    * Costo medio, attacco alto, bassa difesa
#    * Attacca **per primo** in ogni scontro 1v1

# 3. **Guaritore**
#    * Costo medio, bassa difesa e attacco
#    * Invece di attaccare, **cura un alleato vivo random**

# 4. **Mago**
#    * Costo alto, attacco variabile (10–40), difesa bassa
#    * 25% di chance di **saltare il turno** per stanchezza

# ---
### **Sistema di gioco**
### **Fase iniziale: Preparazione**
# * Ogni giocatore ha un **budget iniziale di 1000 monete**
# * Può acquistare soldati scegliendo nome e tipo
# * I soldati vanno salvati in una lista `esercito`

#### **Ciclo di gioco: Round**
# * Ogni round:
#   1. I soldati vivi si scontrano in ordine (es. primo contro primo)
#   2. I danni sono calcolati in base agli attacchi e difese
#   3. I caduti vengono rimossi dall'esercito
# * Alla fine del round:
#   * Ogni giocatore riceve **+300 monete**
#   * Può **acquistare nuovi soldati**
# * Il gioco termina quando **uno dei due eserciti è vuoto**

#### **Vittoria**
# Mostrare messaggio finale con:
# * Vincitore
# * Numero di round giocati
# * Numero di soldati rimasti

# ---
### **Requisiti tecnici obbligatori**
#  Uso di `ABC` e `@abstractmethod`
#  Incapsulamento corretto (`__attributi` e proprietà dove necessario)
#  Override del metodo `attacca()` in ciascuna sottoclasse
#  Gestione delle liste e scontri in funzioni
#  Interfaccia da **terminali** con menu e input controllati
#  Buona **organizzazione del codice**: classi, funzioni, pulizia
# ---

from abc import ABC, abstractmethod
from random import randint, choice, sample

####  **Classe Astratta: `Soldato`**
class Soldato(ABC):
    costo = 0
    def __init__(self, nome):
        self.__nome = nome
        self.__costo = Soldato.costo
        self.__attacco = 0
        self.__difesa = 0
        self.__salute = 0
    
    def get_nome(self):
        return self.__nome
    def get_salute(self):
        return self.__salute
    def get_attacco(self):
        return self.__attacco
    def get_difesa(self):
        return self.__difesa
    def get_costo(self):
        return self.__costo 
    

    def set_attacco(self, valore):
        if isinstance(valore, int): self.__attacco = valore
    def set_difesa(self, valore):
        if isinstance(valore, int): self.__difesa = valore
    def set_salute(self, valore):
        if isinstance(valore, int): self.__salute = valore


    @abstractmethod
    def attacca_avversario(self, party = None):
        pass

    def difenditi(self, danni):
        if isinstance(danni, int): 
            danno_effettivo = max(0, danni//2 - self.__difesa) # Così evito che se difesa > danni, non abbia danno negativo
            if danno_effettivo == 0: print(f'{self.__nome} NON HA PRESO DANNI!')
            else: 
                self.__salute -= danno_effettivo
                print(f'{self.__nome} si è DIFESO e ha perso {danno_effettivo} HP!')

    def subisci_danni(self, danni):
        if isinstance(danni, int): 
            danno_effettivo = max(0, danni - self.__difesa) # Così evito che se difesa > danni, non abbia danno negativo
            self.__salute -= danno_effettivo
            if self.__salute < 0: self.__salute = 0
        print(f'{self.__nome} ha perso {danno_effettivo} HP!')

    def cura(self, punti):
        self.__salute = min(100, self.__salute + punti)

    def vivo(self):
        vivo = False if self.__salute == 0 else True
        return vivo

    def stato(self):
        print(f'{self.__nome}:', '█'*self.__salute,f'{self.__salute} HP')

    def descrizione(self):
        pass

#### **Classi Derivate:**
class Cavaliere(Soldato):
    costo = 150
    def __init__(self, nome):
        super().__init__(nome)
        self.__nome = nome
        self.__costo = Cavaliere.costo
        self.set_attacco(20)
        self.set_difesa(15)
        self.set_salute(100)

    def attacca_avversario(self, party = None):
        print(f'Il Cavaliere {self.__nome} attacca l\'avversario con la sua spada!')
        roll = randint(1, 10)
        if 1 < randint(1, 100) < 20: 
            print('DANNO CRITICO!')
            danni = (self.get_attacco()+roll)*2
        else: 
            danni = self.get_attacco() + roll
        return danni
    
    def descrizione(self):
        return "Cavaliere → Alta difesa, attacco medio. 20% di colpo critico (danno x2)."
    
class Arciere(Soldato):
    costo = 100
    def __init__(self, nome):
        super().__init__(nome)
        self.__nome = nome
        self.__costo = Arciere.costo
        self.set_attacco(30)
        self.set_difesa(1)
        self.set_salute(80)

    def attacca_avversario(self, party = None):
        print(f'L\'Arciere {self.__nome} scaglia una freccia verso l\'avversario!')
        if 1 < randint(1, 100) < 30: 
            print(f'{self.__nome} SCAGLIA DUE FRECCE!')
            danni = 0
            for _ in range(2):
                roll = randint(1, 8)
                danni += self.get_attacco() + roll
        else: 
            roll = randint(1, 8)
            danni = self.get_attacco() + roll
        return danni
    
    def descrizione(self):
        return "Arciere → Alto attacco, bassa difesa. Attacca sempre per primo. 30% Chance di doppio colpo."
    
class Mago(Soldato):
    costo = 140
    def __init__(self, nome):
        super().__init__(nome)
        self.__nome = nome
        self.__costo = Soldato.costo
        self.set_difesa(4)
        self.set_salute(85)

    def attacca_avversario(self, party = None):
        danni = 0
        if 1 < randint(1, 100) < 15:
            print(f'Il Mago {self.__nome} è stanco e non attacca...')
        else: 
            print(f'Il Mago {self.__nome} lancia un missile magico verso l\'avversario!')
            danni = randint(10, 40)
        return danni
    
    def descrizione(self):
        return "Mago → Attacco magico variabile (10-40). 15% di possibilità di saltare il turno per stanchezza."

class Guaritore(Soldato):
    costo = 90
    def __init__(self, nome):
        super().__init__(nome)
        self.__nome = nome
        self.__costo = Guaritore.costo
        self.set_attacco(5)
        self.set_difesa(8)
        self.set_salute(90)   

    def attacca_avversario(self, party = None):
        alleati_vivi = [soldato for soldato in party if soldato.vivo()]
        target = choice(alleati_vivi)
        target.cura(self.get_attacco())
        if target == self:
            print(f'Il Guaritore {self.get_nome()} ha curato sé stesso di {self.get_attacco()} HP.')
        else:
            print(f'Il Guaritore {self.get_nome()} ha curato {target.get_nome()} di {self.get_attacco()} HP.')
    
    def descrizione(self):
        return "Guaritore → Cura un alleato casuale, può anche curare sé stesso."


### **Sistema di gioco**
### **Fase iniziale: Crezione Eserciti
def stampa_esercito(esercito):
    for i, soldato in enumerate(esercito, 1):
            print(f"{i}. {soldato.get_nome()} - {soldato.__class__.__name__} | Salute: {soldato.get_salute()}, Attacco: {soldato.get_attacco()}, Difesa: {soldato.get_difesa()}")

def allestisci_esercito(budget, esercito = None):
    if esercito is None: 
        esercito = []

    while True:
        ingresso = input(f'Cosa vuoi fare?\n1) Aggiungi soldato (Budget: {budget})\n2) Pronto alla battaglia!\n')
        if ingresso == '1':
            soldato = input(f'Quale soldato vuoi aggiungere al tuo esercito?\n1) Cavaliere ({Cavaliere.costo} m.o.)\n2) Arciere ({Arciere.costo} m.o)\n3) Guaritore ({Guaritore.costo} m.o)\n4) Mago ({Mago.costo} m.o.)\n')
            nomi_soldati = [ "Alberico", "Bonifacio", "Corrado", "Domenico", "Ezzelino",
            "Francesco", "Gherardo", "Ildebrando", "Jacopo", "Lanfranco",
            "Manfredo", "Nicolò", "Ottaviano", "Rainaldo", "Sibaldo",
            "Tancredi", "Ugolino", "Vitale", "Zanobi", "Lodovico",]
            if soldato == '1': 
                if budget >= Cavaliere.costo: 
                    nuovo = Cavaliere(choice(nomi_soldati))
                    esercito.append(nuovo)
                    budget -= Cavaliere.costo
                else: print('Avido! Non hai le monete d\'oro necessarie.')
            elif soldato == '2': 
                if budget >= Arciere.costo:
                    nuovo = Arciere(choice(nomi_soldati))
                    esercito.append(nuovo)
                    budget -= Arciere.costo
                else: print('Avido! Non hai le monete d\'oro necessarie.')
            elif soldato == '3': 
                if budget >= Guaritore.costo: 
                    nuovo = Guaritore(choice(nomi_soldati))
                    esercito.append(nuovo)
                    budget -= Guaritore.costo
                else: print('Avido! Non hai le monete d\'oro necessarie.')
            elif soldato == '4': 
                if budget >= Mago.costo:
                    nuovo = Mago(choice(nomi_soldati)) 
                    esercito.append(nuovo)
                    budget -= Mago.costo
                else: print('Avido! Non hai le monete d\'oro necessarie.')
            else: print('Selezione non valida.')
            print(f"\nHai arruolato {nuovo.get_nome()} - {nuovo.descrizione()}")
            print(f"Salute: {nuovo.get_salute()}, Attacco: {nuovo.get_attacco()}, Difesa: {nuovo.get_difesa()}\n")
        elif ingresso == '2' or budget == 0: 
            print('Iniziamo.\n')
            print("\nEcco il tuo esercito schierato:")
            stampa_esercito(esercito)
            return esercito, budget
        else: print('Selezione non valida.')


def genera_esercito_IA(esercito, budget_IA, esercito_IA = None):
    if esercito_IA is None:
        esercito_IA = []

    numero_soldati = len(esercito)
    classi = [Cavaliere, Mago, Arciere, Guaritore]
    nomi = [ "Ezzelino", "Mastino","Ugolino", "Corrado","Rainaldo","Tiberto",    
    "Azzolino","Malvino", "Astolfo","Grimaldo","Manfredi", "Gualtiero",  
    "Lupo", "Ferrando",  "Mordrano", 'Frenesio', 'Poldo', 'Bruto', 'Lerico']

    while budget_IA >= min(cls.costo for cls in classi):
        classe = choice(classi)
        if budget_IA >= classe.costo:
            nuovo = classe(choice(nomi))
            esercito_IA.append(nuovo)
            budget_IA -= classe.costo

    print('\nL\'esercito del Regno di Nys si staglia all\'orizzonte:')
    stampa_esercito(esercito_IA)
    return esercito_IA, budget_IA

## Fase Combattimento a turni: 

def combattimento(sfidante_1, sfidante_2, sfidanti, sfidanti_IA):
    print(f'\n{sfidante_1.get_nome()} e {sfidante_2.get_nome()} combattono all\'ultimo sangue!')
    combattenti = [sfidante_1, sfidante_2]

    # Gestione Guaritore VS Guaritore
    if isinstance(sfidante_1, Guaritore) and isinstance(sfidante_2, Guaritore):
        print(f'\nI due guaritori {sfidante_1.get_nome()} e {sfidante_2.get_nome()} si fissano con rispetto...')
        print("Iniziano a pregare le loro divinità per la salvezza del regno...")

        vincitore = choice([sfidante_1, sfidante_2])
        perdente = sfidante_2 if vincitore == sfidante_1 else sfidante_1

        print(f"La divinità ascolta {vincitore.get_nome()}!")
        print(f"{perdente.get_nome()} cade colpito da una luce divina.\n")

        perdente.subisci_danni(999)  # uccisione diretta
        return vincitore
    
    # Gestione priorità Arciere
    if isinstance(sfidante_1, Arciere) or isinstance(sfidante_2, Arciere):
        if isinstance(sfidante_1, Arciere) and isinstance(sfidante_2, Arciere): attaccante = choice(combattenti)
        elif isinstance(sfidante_1, Arciere): attaccante = sfidante_1
        else: attaccante = sfidante_2 
    else: attaccante = choice(combattenti)
    difensore = sfidante_1 if attaccante == sfidante_2 else sfidante_2
    turno = 1

    while True: 
            print(f'---ROUND {turno}---')
            if isinstance(attaccante, Guaritore):
                attaccante.attacca_avversario(sfidanti if attaccante in sfidanti else sfidanti_IA)
                danni = 0
            else:
                danni = attaccante.attacca_avversario()
            if 1 < randint(1, 100) < 10: difensore.difenditi(danni)
            else: difensore.subisci_danni(danni) 
            vivo_attaccante = attaccante.vivo()
            vivo_difensore = difensore.vivo()
            difensore.stato() 
            attaccante.stato()

            if not vivo_difensore:
                print(f'{attaccante.get_nome()} ha vinto lo scontro!!!\n')
                return attaccante
            
            if isinstance(difensore, Guaritore):
                difensore.attacca_avversario(sfidanti if difensore in sfidanti else sfidanti_IA)
                danni = 0
            else:
                danni = difensore.attacca_avversario()
            if 1 < randint(1, 100) < 10: attaccante.difenditi(danni)
            else: attaccante.subisci_danni(danni) 
            vivo_attaccante = attaccante.vivo()
            vivo_difensore = difensore.vivo()
            difensore.stato() 
            attaccante.stato()

            if not vivo_attaccante:
                print(f'{difensore.get_nome()} ha vinto lo scontro!!!\n')
                return difensore
            
            turno += 1  

## Gestione dei round di combattimento

def torneo(esercito, esercito_IA):

    numero_combattimenti = max(len(esercito), len(esercito_IA))
    sfidanti = esercito.copy()
    sfidanti_IA = esercito_IA.copy()
    fight = 0
    while fight <= numero_combattimenti:
        if fight <= len(sfidanti)-1: sfidante_1 = sfidanti[fight]
        else: sfidante_1 = choice(sfidanti)
        if fight <= len(sfidanti_IA)-1: sfidante_2 = sfidanti_IA[fight]
        else: sfidante_2 = choice(sfidanti_IA)

        vincitore = combattimento(sfidante_1, sfidante_2, sfidanti, sfidanti_IA)
        if vincitore == sfidante_1: 
            esercito_IA.remove(sfidante_2)
        else: esercito.remove(sfidante_1)
        fight +=1

    if len(esercito) > 0 and len(esercito_IA) > 0:
        print('La battaglia si è conclusa!')
        print('I sopravvissuti del Regno della Luce,')
        stampa_esercito(esercito)
        print('si riorganizzano.\n')

        print('Le canaglie del regno delle ombre')
        stampa_esercito(esercito_IA)
        print('si riorganizzano.\n')
    
    elif len(esercito_IA) == 0: 
        print('Il regno di Lux VINCE!')
        stampa_esercito(esercito)
        print('sono in giubilo!\n')
        print('----HAI VINTO---')
    elif len(esercito) == 0:
        print('Il regno di Nyx VINCE!')
        stampa_esercito(esercito_IA)
        print('affilano le lame per la prossima conquista!\n')
        print('----GAME OVER---')

    return esercito, esercito_IA

## Gioco 'La Guerra di Lux e Nyx'

def GuerraLuxeNyx():
    print('Re di Lux, la resa dei conti con il Regno di Nyx è alle porte!\nE\' il momento di organizzare l\'esercito!')
    budget = 1000
    budget_IA = 1000
    esercito = []
    esercito_IA = []
    round = 1

    esercito, budget = allestisci_esercito(budget, esercito)
    esercito_IA, budget_IA = genera_esercito_IA(esercito, budget_IA, esercito_IA)

    while True:
        print(f'---ROUND {round}---')
        esercito, esercito_IA = torneo(esercito, esercito_IA)

        if len(esercito) == 0 or len(esercito_IA) == 0:
            break
        budget += 300
        budget_IA += 300
        print("\n--- Fine del round. Preparati al prossimo! ---\n")
        print(f"Hai ricevuto +300 monete. Totale: {budget}")
        esercito, budget = allestisci_esercito(esercito, budget)
        esercito_IA, budget_IA = genera_esercito_IA(esercito_IA, budget_IA)

        round_counter += 1

    print('\nGrazie per aver giocato!')



GuerraLuxeNyx()


