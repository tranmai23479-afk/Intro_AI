
"""
Greedy Best-First Search (GBFS) cho bai toan thu gom rac.

Trang thai: (vi tri hien tai, tap diem thu gom da thu gom)
Trang thai dau: (Depot, {})
Dich: da thu gom tat ca cac diem va quay ve Depot.

GBFS uu tien trang thai co h(n) nho nhat, khong cong g(n) vao
gia tri uu tien.

Quy uoc:
- Di chuyen giua hai diem theo duong ngan nhat trong D.
- Neu duong di ngang qua diem thu gom khac, diem do cung duoc
  tinh la da thu gom.
- Khi tat ca diem da duoc thu gom, xe quay ve Depot.
"""

import heapq
import itertools
import time

from build_map import (
    DEPOT,
    BINS,
    shortest_paths,
    h,
    full_route,
    street_path,
)


def bins_on_path(path, bins):
    """Tra ve cac diem thu gom xuat hien tren duong di."""
    return frozenset(node for node in path if node in bins)


def gbfs(D, depot=DEPOT, bins=BINS, log=None):
    """
    Tra ve dict gom:
    route, distance, expanded, generated, time_ms.

    route la danh sach cac diem dich duoc chon.
    full_route(route) se mo rong thanh duong di day du tren ban do.
    """
    all_bins = frozenset(bins)
    start = (depot, frozenset())

    counter = itertools.count()
    t0 = time.perf_counter()

    h0 = h(depot, all_bins, D, depot)

    # Phan tu: (h, thu tu sinh, state, g, route)
    pq = [(h0, next(counter), start, 0, [depot])]

    best_g = {start: 0}
    closed = set()

    expanded = 0
    generated = 1

    while pq:
        hval, _, state, g, route = heapq.heappop(pq)

        if state in closed:
            continue

        closed.add(state)
        expanded += 1

        current, visited = state

        if log is not None:
            log.append({
                "step": expanded,
                "current": current,
                "visited": sorted(visited),
                "g": g,
                "h": hval,
                "frontier": len(pq),
            })

        # Muc tieu: da thu gom tat ca va quay ve Depot
        if visited == all_bins and current == depot:
            return {
                "route": route,
                "distance": g,
                "expanded": expanded,
                "generated": generated,
                "time_ms": (time.perf_counter() - t0) * 1000,
            }

        unvisited = all_bins - visited

        if unvisited:
            # Xet cac diem chua thu gom theo thu tu BINS
            candidates = [b for b in bins if b in unvisited]
        else:
            # Da thu gom het: quay ve Depot
            candidates = [depot]

        for nxt in candidates:
            # Duong di ngan nhat tren do thi
            segment = street_path(current, nxt)
            step_cost = D[current][nxt]
            new_g = g + step_cost

            # Cap nhat cac diem thu gom da di qua tren duong
            newly_visited = bins_on_path(segment, all_bins)
            new_visited = visited | newly_visited

            new_state = (nxt, new_visited)

            if new_state in closed:
                continue

            if new_g >= best_g.get(new_state, float("inf")):
                continue

            best_g[new_state] = new_g

            remaining = all_bins - new_visited
            new_h = h(nxt, remaining, D, depot)

            heapq.heappush(
                pq,
                (
                    new_h,
                    next(counter),
                    new_state,
                    new_g,
                    route + [nxt],
                ),
            )
            generated += 1

    return None


def print_result(result, D):
    if result is None:
        print("Khong tim thay lo trinh.")
        return

    route = result["route"]

    print("\n========== KET QUA GBFS ==========")
    print("Cac diem dich duoc chon:")

    for a, b in zip(route, route[1:]):
        print(f"  {a:18s} -> {b:18s} {D[a][b]:>3} m")

    print("\nDuong di day du (bao gom cac diem di ngang qua):")
    print("  " + " -> ".join(full_route(route)))

    print(f"\nTong quang duong : {result['distance']} m")
    print(f"So trang thai mo rong : {result['expanded']}")
    print(f"So trang thai da sinh : {result['generated']}")
    print(f"Thoi gian chay : {result['time_ms']:.3f} ms")


if __name__ == "__main__":
    D = shortest_paths()

    log = []
    result = gbfs(D, log=log)

    print_result(result, D)

    print("\nNhat ky 5 trang thai dau:")
    for item in log[:5]:
        print(
            f"  Step {item['step']:>2}: "
            f"{item['current']:18s} "
            f"g={item['g']:<4} "
            f"h={item['h']:<4} "
            f"frontier={item['frontier']}"
        )
