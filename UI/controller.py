import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        SightingList = self._model.listSighting

        for s in SightingList:
            if s.datetime.year not in self._listYear:
                self._listYear.append(s.datetime.year)

        for a in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

        self._view.update_page()

    def fillDDShape(self, e):
        self._view.ddshape.options.clear()
        self._view.update_page()
        year = float(self._view.ddyear.value)
        SightingList = self._model.listSighting
        for s in SightingList:
            if s.shape not in self._listShape and s.datetime.year == year and s.shape != "":
                self._listShape.append(s.shape)
        for s in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()
        self._listShape.clear()

    def handle_graph(self, e):
        if self._view.ddyear.value is None:
            self._view.create_alert("Selezionare un anno!")
            return
        a = self._view.ddyear.value
        if self._view.ddshape.value is None or self._view.ddshape.value == "":
            self._view.create_alert("Selezionare una shape!")
            return
        s = self._view.ddshape.value

        self._view.txt_result1.controls.clear()
        self._model.buildGraph(s, a)
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_of_nodes()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.get_num_of_edges()}"))
        self._view.txt_result1.controls.append(
            ft.Text(f"I 5 archi di peso maggiore sono:"))
        first_edges = self._model.get_first_edges()
        for e in first_edges:
            self._view.txt_result1.controls.append(ft.Text(f"{e[0].id} --> {e[1].id} | weight = {e[2]['weight']}"))
        self._view.update_page()

    def handle_path(self, e):
        pass
