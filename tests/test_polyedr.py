import unittest
from unittest.mock import patch, mock_open

from shadow.polyedr import Polyedr, Facet
from common.r3 import R3


class TestPolyedr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        fake_file_content = """200.0	45.0	45.0	30.0
8	4	16
-0.5	-0.5	0.5
-0.5	0.5	0.5
0.5	0.5	0.5
0.5	-0.5	0.5
-0.5	-0.5	-0.5
-0.5	0.5	-0.5
0.5	0.5	-0.5
0.5	-0.5	-0.5
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5"""
        fake_file_path = 'data/holey_box.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

    def test_num_vertexes(self):
        self.assertEqual(len(self.polyedr.vertexes), 8)

    def test_num_facets(self):
        self.assertEqual(len(self.polyedr.facets), 4)

    def test_num_edges(self):
        self.assertEqual(len(self.polyedr.edges), 16)

    def test_projection_area_triangle(self):
        """Проверка площади проекции треугольной грани"""
        triangle_vertexes = [
            R3(0.0, 0.0, 0.0),
            R3(1.0, 0.0, 0.0),
            R3(0.0, 1.0, 0.0)
        ]
        facet = Facet(triangle_vertexes)
        self.assertAlmostEqual(facet.projection_area(), 0.5)

    def test_projection_area_square(self):
        """Проверка площади проекции квадратной грани"""
        square_vertexes = [
            R3(0.0, 0.0, 0.0),
            R3(1.0, 0.0, 0.0),
            R3(1.0, 1.0, 0.0),
            R3(0.0, 1.0, 0.0)
        ]
        facet = Facet(square_vertexes)
        self.assertAlmostEqual(facet.projection_area(), 1.0)

    def test_projection_area_degenerate(self):
            """Проверка площади вырожденной грани (меньше 3 вершин)"""
            degenerate_vertexes = [
                R3(0.0, 0.0, 0.0),
                R3(1.0, 0.0, 0.0)
            ]
            facet = Facet(degenerate_vertexes)
            self.assertEqual(facet.projection_area(), 0.0)
    
    def test_calculate_area_simple_case(self):
        fake_file_content = """1.0 0.0 0.0 0.0
3 1 3
3.0 0.0 0.0
3.0 3.0 0.0
0.0 3.0 0.0
3 1 2 3"""
        with patch('shadow.polyedr.open', new=mock_open(read_data=fake_file_content)) as _file:
            polyedr = Polyedr('dummy_path')
            self.assertAlmostEqual(polyedr.calculate_area(), 4.5)

    def test_calculate_area_no_good_vertices(self):
        square_vertexes = [
            R3(0.0, 1.0, 0.0),
            R3(1.0, 0.0, 0.0),
            R3(1.0, 1.0, 0.0),
            R3(0.0, 0.5, 0.0)
        ]
        polyedr = Polyedr.__new__(Polyedr)
        polyedr.facets = [Facet(square_vertexes)]
        polyedr.scale = 1.0
        self.assertAlmostEqual(polyedr.calculate_area(), 0.0)
