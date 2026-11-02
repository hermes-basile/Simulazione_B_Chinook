import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP - Simulazione B - Generi musicali e preferenze dei clienti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._txt_result = None

        self._ddPaese = None
        self._btnCreaGrafo = None
        self._btnStampaInfo = None

        self._ddGenere = None
        self._txtInN = None
        self._btnTrovaGruppo = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP - Simulazione B - Generi musicali e preferenze dei clienti", color="blue", size=24)
        self._page.controls.append(self._title)

        # riga 1: punto 1
        self._ddPaese = ft.Dropdown(label="Paese")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo",
                                              on_click=self._controller.handleCreaGrafo)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa Info",
                                               on_click=self._controller.handleStampaInfo)

        row1 = ft.Row([ft.Container(self._ddPaese, width=250),
                       ft.Container(self._btnCreaGrafo, width=200),
                       ft.Container(self._btnStampaInfo, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # riga 2: punto 2
        self._ddGenere = ft.Dropdown(label="Genere di partenza")
        self._txtInN = ft.TextField(label="N")
        self._btnTrovaGruppo = ft.ElevatedButton(text="Trova gruppo generi",
                                                 on_click=self._controller.handleTrovaGruppo)

        row2 = ft.Row([ft.Container(self._ddGenere, width=300),
                       ft.Container(self._txtInN, width=150),
                       ft.Container(self._btnTrovaGruppo, width=220)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
