from dataclasses import dataclass, field
@dataclass
class Genere:
    GenreId : int
    Name: str

    numero_copie: float = field(default=0.0,init=False)
    numero_copie_paese: float = field(default=0.0,init=False)

    lista_id_clienti: list = field(default_factory=list)
    lista_id_clienti_paese: list = field(default_factory=list)




    def __hash__(self):
        return hash(self.GenreId)

    def __str__(self):
        return f"{self.Name}"

    def __eq__(self, other):
        return self.GenreId == other.GenreId