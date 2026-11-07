# Garbage Truck Routing: GBFS vs A*

Python 3.x. Install: pip install -r requirements.txt
No random numbers are used. Ties are broken by a fixed bin order and an
insertion counter, so results are identical on every run.

Run:
  python build_map.py     # draws map.png, tables.png, distance_matrix.csv
  python gbfs.py
  python astar.py
  python brute_force.py

Expected results (running time depends on the machine):
  GBFS         252 m   7 expanded    28 generated
  A*           217 m  63 expanded   208 generated
  Brute force  217 m  362,880 permutations
  h(start) = 186 m
