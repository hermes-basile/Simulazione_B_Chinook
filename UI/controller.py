import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.result1 = None
        self.result2 = None

    def fill_DD(self):


        self._view._ddPaese.options.clear()
        self._view._ddPaese.value = None
        self.result1 = None

        lista_da_caricare = self._model.lista_paesi()

        for elemento in lista_da_caricare:
            self._view._ddPaese.options.append(
                ft.dropdown.Option(
                    text=str(elemento),
                    data=elemento,
                    on_click=self.readResult1
                )
            )

    def readResult1(self, e):
        self.result1 = e.control.data

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        scelta_utente = self.result1

        if scelta_utente is None:
            self._view._txt_result.controls.append(ft.Text(
                "Attenzione prima di proseguire è necessario scegliere un opzione del dropdown", color="red"))
            self._view.update_page()
            return

        self._view._txt_result.controls.append(
            ft.Text("Stiamo creando il grafo, aspetta qualche secondo.."))
        self._view.update_page()

        self._model.crea_grafo(scelta_utente)
        self._view._txt_result.controls.clear()

        # scrivere all'utente che è tutto ok, nodi e archi
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato. ", color="green"))

        self._view._txt_result.controls.append(ft.Text(
            f"Il grafo ha {self._model.num_nodi()} nodi e {self._model.num_archi()} archi."))

        self.fill_DD_nodi()


        self._view.update_page()

    def handleStampaInfo(self, e):
        if self._model.num_nodi() == 0:
            self._view._txt_result.controls.append(
                ft.Text("Devi prima creare il grafo, o selezionare dei filtri in modo che esistano i nodi.",
                        color="red")
            )
            self._view.update_page()
            return

        nodo, grado = self._model.genere_grado_maggiore()
        nodo1, peso = self._model.genere_con_maggior_peso()
        lista_archi = self._model.best_5_archi()
        nodo_venduto, vendite = self._model.genere_piu_venduto()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Il nodo con grado massimo è {nodo} con grado: {grado}"))
        self._view._txt_result.controls.append(ft.Text(f"il nodo con maggior peso incidente è {nodo1} con peso: {peso}"))
        self._view._txt_result.controls.append(ft.Text(f"il genere più venduto è {nodo_venduto} con {vendite} copie."))

        if len(lista_archi) == 0:
            self._view._txt_result.controls.append(ft.Text(f"Spiacente la lista degli archi è vuota"))
        else:
            for i,tupla in enumerate(lista_archi):
                self._view._txt_result.controls.append(ft.Text(f"{i+1}. {tupla[0]} -- {tupla[1]} con peso: {tupla[2]['weight']}"))
        self._view._txt_result.controls.append(ft.Text(f""))
        self._view.update_page()

    def fill_DD_nodi(self):

        self._view._ddGenere.options.clear()
        self._view._ddGenere.value = None
        self.result2 = None

        lista_nodi = list(self._model._grafo.nodes())
        lista_da_caricare = sorted(lista_nodi, key=lambda nodo:nodo.Name)

        # se l'elemento è formato da oggetti classe
        for elemento in lista_da_caricare:
            self._view._ddGenere.options.append(
                ft.dropdown.Option(
                    text=str(elemento),
                    data=elemento,
                    on_click=self.readResult1
                )
            )

    def readResult2(self, e):
        self.result2 = e.control.data


    def handleTrovaGruppo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.num_nodi() == 0:
            self._view._txt_result.controls.append(
                ft.Text("Devi prima creare il grafo, o selezionare dei filtri in modo che esistano i nodi.",
                        color="red")
            )
            self._view.update_page()
            return

        self._view._txt_result.controls.clear()

        scelta_utente2 = self.result1

        # controllo se è tutto ok
        if scelta_utente2 is None:
            self._view._txt_result.controls.append(ft.Text(
                "Attenzione prima di proseguire è necessario scegliere un opzione del dropdown", color="red"))
            self._view.update_page()

            return




        txt_in = self._view._txtInN.value

        # controllo se ha scritto qualcosa
        if txt_in is None or txt_in.strip() == "":
            self._view._txt_result.controls.append(ft.Text(
                "Devi inserire un valore valido", color="red"))
            self._view.update_page()
            return

        try:
            number = int(txt_in)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text(
                "Attenzione, gli unici caratteri ammessi sono da 0 a 9: puoi inserire solo numeri", color="red"))
            self._view._txtInN.value = ""
            self._view.update_page()
            return

        # controllo eventuali vincoli della traccia
        if number <= 1:
            self._view._txt_result.controls.append(
                ft.Text("Il numero deve essere almeno 1", color="red")
            )
            self._view.update_page()
            return

        self._view._txt_result.controls.append(ft.Text(f"Tutti i dati inseriti sono coerenti", color="green"))

        if number > self._model.num_nodi():
            self._view._txt_result.controls.append(
                ft.Text("Il numero richiesto supera i nodi disponibili", color="red")
            )
            self._view.update_page()
            return

        try:
            soluzione, copie_totali = self._model.crea_albero(scelta_utente2, number)

        except Exception as errore:
            print("Errore nella ricorsione:", errore)
            self._view._txt_result.controls.append(
                ft.Text("Errore durante il calcolo", color="red")
            )
            self._view.update_page()
            return

        # 4. CONTROLLO SOLUZIONE VUOTA
        if not soluzione:
            self._view._txt_result.controls.append(
                ft.Text("Nessuna soluzione trovata", color="red")
            )
            self._view.update_page()
            return

        # 5. STAMPA RISULTATI
        soluzione_ordinata = sorted(soluzione, key=lambda nodo:nodo.Name)


        self._view._txt_result.controls.append(ft.Text(f"Di seguito la soluzione della ricorsione: \n"))

        for i,nodo in enumerate(soluzione_ordinata):
            self._view._txt_result.controls.append(ft.Text(f"{i+1}. {nodo} con {nodo.numero_copie_paese} copie vendute, con {len(nodo.lista_id_clienti_paese)} clienti."))

        self._view._txt_result.controls.append(ft.Text(f"Quindi sono stati trovati {len(soluzione)} generi, la loro somma di copie vendute è {copie_totali}"))
        self._view._txt_result.controls.append(ft.Text(f""))

        self._view.update_page()
