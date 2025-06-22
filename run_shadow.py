#!/usr/bin/env -S python3 -B

from time import time
from common.tk_drawer import TkDrawer
from shadow.polyedr import Polyedr


tk = TkDrawer()
try:
    for name in ["test", "ccc", "cube", "box", "king", "cow"]:
        print("=============================================================")
        print(f"Начало работы с полиэдром '{name}'")
        start_time = time()
        poly = Polyedr(f"data/{name}.geom")
        poly.draw(tk)
        special_area = poly.calculate_special_area()
        print(f"Сумма площадей граней с одной 'хорошей' вершиной: {special_area:.2f}")
        delta_time = time() - start_time
        print(f"Изображение полиэдра '{name}' заняло {delta_time} сек.")
        input("Hit 'Return' to continue -> ")
    tk.root.mainloop()
except (EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()

