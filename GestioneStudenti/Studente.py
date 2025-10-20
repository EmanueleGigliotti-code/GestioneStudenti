import random

nomi_maschili = ['Luca', 'Marco', 'Andrea', 'Matteo', 'Francesco', 'Giovanni', 'Alessandro', 'Davide', 'Simone', 'Gabriele',
                 'Federico', 'Riccardo', 'Lorenzo', 'Tommaso', 'Emanuele', 'Daniele', 'Nicola', 'Stefano', 'Antonio', 'Fabio',
                 'Paolo', 'Giuseppe', 'Vincenzo', 'Roberto', 'Salvatore', 'Claudio', 'Enrico', 'Michele', 'Alberto', 'Maurizio']

nomi_femminili = ['Giulia', 'Francesca', 'Sara', 'Martina', 'Chiara', 'Alessia', 'Valentina', 'Federica', 'Elena', 'Ilaria',
                  'Laura', 'Simona', 'Angela', 'Anna', 'Maria', 'Sofia', 'Claudia', 'Veronica', 'Camilla', 'Eleonora',
                  'Paola', 'Cristina', 'Silvia', 'Barbara', 'Roberta', 'Alice', 'Marta', 'Beatrice', 'Nicole', 'Elisa']

cognomi = ['Rossi', 'Russo', 'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci', 'Marino', 'Greco',
           'Bruno', 'Gallo', 'Conti', 'De Luca', 'Mancini', 'Costa', 'Giordano', 'Rizzo', 'Lombardi', 'Moretti',
           'Barbieri', 'Fontana', 'Santoro', 'Mariani', 'Rinaldi', 'Caruso', 'Ferraro', 'Fabbri', 'Galli', 'Martini',
           'Leone', 'Longo', 'Gentile', 'Martinelli', 'Serra', 'Villa', 'Cattaneo', 'Sala', 'Pellegrini', 'Farina',
           'Orlando', 'Sanna', 'Piras', 'Lopes', 'Grassi', 'De Santis', 'Monti', 'Bellini', 'Marchetti', 'Valentini']

comportamenti = ['Ottimo', 'Buono', 'Sufficiente', 'Scarso']

class Studente:
    id_counter = 1
    
    def __init__(self, id, nome, cognome, eta, genere, ore_studio, assenze, media_voti, comportamento):
#Ho creato id_counter come variabile globale della classe e mi serve all'interno del codice locale e non dal db in modo che riesco a fare l'autoincrement. Mentre da db 
#vado ad utilizzare direttamente la dichiarazione self.id = id poichè nel db è previsto l'autoincrement
        if id is not None:
            self.id = id
        else:
            self.id = Studente.id_counter
            Studente.id_counter += 1

        self.nome = nome
        self.cognome = cognome
        self.eta = eta
        self.genere = genere
        self.ore_studio = ore_studio
        self.assenze = assenze
        self.media_voti = media_voti
        self.comportamento = comportamento
        self.esito_finale = self.calcola_esito()

    def calcola_esito(self):
        if self.comportamento == 'Scarso' or self.media_voti <= 5.3 or self.assenze >= 220:
            return 'Bocciato'
        return 'Promosso'
    
    def __str__(self):
        return f"{self.id} - {self.nome} {self.cognome}, {self.eta} anni, {self.genere}, Media: {self.media_voti}, Esito: {self.esito_finale}"
    
    @classmethod #Annotazione che mi evita di utilizzare il self per i singoli oggetti ma la utilizzo sull'intera classe
    def genera_studente(cls):
        genere = random.choice(['M', 'F'])
        nome = random.choice(nomi_maschili if genere == 'M' else nomi_femminili)
        cognome = random.choice(cognomi)
        eta = random.randint(14, 20) 
        ore_studio = round(random.uniform(0, 8), 1)
        assenze = random.randint(0, 250)
        media_voti = round(random.uniform(5, 10), 1)
        comportamento = random.choice(comportamenti)
        return cls(None, nome, cognome, eta, genere, ore_studio, assenze, media_voti, comportamento)
