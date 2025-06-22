from math import pi
from common.r3 import R3
from common.tk_drawer import TkDrawer


class Edge:
    """ Ребро полиэдра """
    # Параметры конструктора: начало и конец ребра (точки в R3)

    def __init__(self, beg, fin):
        self.beg, self.fin = beg, fin


class Facet:
    """ Грань полиэдра """
    # Параметры конструктора: список вершин

    def __init__(self, vertexes):
        self.vertexes = vertexes

    def projection_area(self):
        """Вычисляет площадь проекции грани на плоскость XY"""
        if len(self.vertexes) < 3:
            return 0.0

        # Проекции вершин (игнорируем z-координату)
        points = [(v.x, v.y) for v in self.vertexes]

        # Вычисляем площадь многоугольника по формуле шнурков
        area = 0.0
        n = len(points)
        for i in range(n):
            x_i, y_i = points[i]
            x_j, y_j = points[(i + 1) % n]
            area += (x_i * y_j) - (x_j * y_i)

        return abs(area) / 2.0


class Polyedr:
    """ Полиэдр """
    # Параметры конструктора: файл, задающий полиэдр

    def __init__(self, file):

        # списки вершин, рёбер и граней полиэдра
        self.vertexes, self.edges, self.facets = [], [], []

        # список строк файла
        with open(file) as f:
            for i, line in enumerate(f):
                if i == 0:
                    # обрабатываем первую строку; buf - вспомогательный массив
                    buf = line.split()
                    # коэффициент гомотетии
                    self.scale = c = float(buf.pop(0))
                    # углы Эйлера, определяющие вращение
                    alpha, beta, gamma = (float(x) * pi / 180.0 for x in buf)
                elif i == 1:
                    # во второй строке число вершин, граней и рёбер полиэдра
                    nv, nf, ne = (int(x) for x in line.split())
                elif i < nv + 2:
                    # задание всех вершин полиэдра
                    x, y, z = (float(x) for x in line.split())
                    self.vertexes.append(R3(x, y, z).rz(
                        alpha).ry(beta).rz(gamma) * c)
                else:
                    # вспомогательный массив
                    buf = line.split()
                    # количество вершин очередной грани
                    size = int(buf.pop(0))
                    # массив вершин этой грани
                    vertexes = [self.vertexes[int(n) - 1] for n in buf]
                    # задание рёбер грани
                    for n in range(size):
                        self.edges.append(Edge(vertexes[n - 1], vertexes[n]))
                    # задание самой грани
                    self.facets.append(Facet(vertexes))

    # Метод изображения полиэдра
    def draw(self, tk):
        tk.clean()
        tk.draw_line(R3(-1000.0, 2.0, 0.0) * self.scale,
                     R3(1000.0, 2.0, 0.0) * self.scale)
        for e in self.edges:
            tk.draw_line(e.beg, e.fin)

    def calculate_special_area(self):
        total_area = 0.0

        for facet in self.facets:
            good_count = 0
            for vertex in facet.vertexes:
                if vertex.is_good():
                    good_count += 1

            if good_count == 1:
                total_area += facet.projection_area()

        return total_area
