import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.lista_nodi_totale = DAO.getAllNodes()

        self.idMapObject = {}
        for nodo in self.lista_nodi_totale:
            self.idMapObject[nodo.GenreId] = nodo

        self._grafo = nx.Graph()


    def lista_paesi(self):
        lista = DAO.lista_paesi()
        return lista

    def crea_grafo(self, paese):
        self._grafo.clear()

        lista_id = DAO.getNodi(paese)

        lista_nodi = []

        for id_nodo in lista_id:
            nodo = self.idMapObject[id_nodo]
            DAO.fillListaCopieVendute(nodo)
            DAO.fillListaClienti(nodo)
            DAO.fillListaCopieVendutePaese(nodo, paese)
            DAO.fillListaClientiPaese(nodo, paese)
            lista_nodi.append(nodo)

        self._grafo.add_nodes_from(lista_nodi)

        self.add_archi_model()

    def add_archi_model(self):
        lista_nodi = list(self._grafo.nodes())

        for i in range(len(lista_nodi)):
            for j in range(i + 1, len(lista_nodi)):

                u = lista_nodi[i]
                v = lista_nodi[j]
                set_u_clienti_paese = set(u.lista_id_clienti_paese)
                set_v_clienti_paese = set(v.lista_id_clienti_paese)
                set_clienti_comuni = set_u_clienti_paese & set_v_clienti_paese

                if len(set_clienti_comuni) > 0 :
                    peso = len(set_clienti_comuni)
                    self._grafo.add_edge(u, v, weight=peso)



    def genere_grado_maggiore(self):
        if self._grafo.number_of_nodes() == 0:
            return None, 0

        nodo = max(self._grafo.nodes(), key=lambda n: self._grafo.degree(n))

        return nodo, self._grafo.degree(nodo)

    def genere_con_maggior_peso(self):
        if self._grafo.number_of_nodes() == 0:
            return None, 0

        nodo = max(self._grafo.nodes(), key=lambda n: self._grafo.degree(n, weight="weight"))

        return nodo, self._grafo.degree(nodo, weight="weight")

    def best_5_archi(self):
        lista_archi = []
        for u, v, dati in self._grafo.edges(data=True):
            # Metto gli artisti in ordine alfabetico
            if u.Name > v.Name:
                u, v = v, u
            lista_archi.append((u, v, dati))

        return sorted(lista_archi, key=lambda arco: (-arco[2]["weight"], arco[0].Name, arco[1].Name))[:5]


    def genere_piu_venduto(self):
        lista_nodi = list(self._grafo.nodes())
        nodo_ottimo = None
        ottimo = -1
        if len(lista_nodi) == 0:
            return None, -1

        for nodo in lista_nodi:
            if nodo is None:
                nodo_ottimo = nodo
                ottimo = nodo.numero_copie_paese
            if nodo.numero_copie > ottimo:
                nodo_ottimo = nodo
                ottimo = nodo.numero_copie_paese


        return nodo_ottimo, ottimo

    def crea_albero(self, source, N):
        self.soluzione = []

        self.copie_vendute = -1

        # attiva ricorsione
        self.ricorsione([source], N)

        # ritorna soluzione finale
        return self.soluzione, self.copie_vendute

    def ricorsione(self, parziale, N):
        if len(parziale) == N:

            # condizione di miglioramento
            if self.conta_copie(parziale) > self.copie_vendute:
                self.copie_vendute = self.conta_copie(parziale)
                self.soluzione = copy.deepcopy(parziale)
            return

        set_candidati = set()
        for nodo_parziale in parziale:
            for vicino in self._grafo.neighbors(nodo_parziale):
                peso = self._grafo[nodo_parziale][vicino]["weight"]
                if peso >= 2:
                    set_candidati.add(vicino)

        for candidato in set_candidati:
                parziale.append(candidato)
                self.ricorsione(parziale, N)
                parziale.pop()

    def conta_copie(self, parziale):
        count = 0
        for nodo_parziale in parziale:
            count += nodo_parziale.numero_copie_paese
        print(count)
        return count






    def num_nodi(self):
        return len(self._grafo.nodes)

    def num_archi(self):
        return len(self._grafo.edges)
