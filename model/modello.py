from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._idMap = {}
        self._listSighting = []
        self._listShape = []

        self._grafo = nx.DiGraph()
        self._nodes = []
        self._edges = []

        self.loadSighting()
        self.loadShapes()

    def loadSighting(self):
        self._listSighting = DAO.get_all_sightings()

    def loadShapes(self):
        self._listShape = DAO.getAllShapes()

    @property
    def listSighting(self):
        return self._listSighting

    @property
    def listShape(self):
        return self._listShape

    def buildGraph(self, s, a):
        self._grafo.clear()
        self._nodes.clear()
        for x in self._listSighting:
            if x.shape == s and str(x.datetime.year) == a:
                self._nodes.append(x)

        self._grafo.add_nodes_from(self._nodes)

        #edges modo programmatico

        for i in range(0, len(self._nodes) - 1):
            for j in range(i + 1, len(self._nodes)):
                if self._nodes[i].state == self._nodes[j].state and self._nodes[i].longitude < self._nodes[j].longitude:
                    weight = self._nodes[j].longitude - self._nodes[i].longitude
                    self._grafo.add_edge(self._nodes[i], self._nodes[j], weight=weight)
                elif self._nodes[i].state == self._nodes[j].state and self._nodes[i].longitude > self._nodes[
                    j].longitude:
                    weight = self._nodes[i].longitude - self._nodes[j].longitude
                    self._grafo.add_edge(self._nodes[j], self._nodes[i], weight=weight)

    def get_first_edges(self):
        sorted_edges = sorted(self._grafo.edges(data=True), key=lambda edge: edge[2].get('weight'), reverse=True)
        return sorted_edges[0:5]
    def get_nodes(self):
        return self._grafo.nodes()

    #def get_edges(self):
     #   return list(self._grafo.edges(data=True))

    def get_num_of_nodes(self):
        return self._grafo.number_of_nodes()

    def get_num_of_edges(self):
        return self._grafo.number_of_edges()