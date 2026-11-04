"""
Greedy Best-First Search (GBFS) cho bai toan thu gom rac, chay tren map trong build_map.py

Trang thai : (vi tri hien tai, tap thung da tham)
Trang thai dau : (Depot, {})
Dich       : da tham du moi thung va quay ve Depot
Hanh dong  : di toi 1 thung chua tham (chi phi = khoang cach ngan nhat D);
             khi het thung thi quay ve Depot
GBFS chon trang thai co f(n) = h(n) nho nhat, KHONG xet g(n).
h(n) dung chung voi A*: min(khoang cach ve Depot, 30), Depot = 0 (xem build_map.h).
"""
import heapq
import itertools
import time

from build_map import DEPOT, BINS, shortest_paths, h


def gbfs(D, depot=DEPOT, bins=BINS, log=None):
    """
    Tra ve dict: route, distance, expanded, generated, time_ms.
    Neu truyen log (list) thi moi lan mo rong trang thai se ghi 1 dong
    (dung de lam animation sau nay).
    """
    all_bins = frozenset(bins)
    start = (depot, frozenset())
    counter = itertools.count()          # tie-break on dinh, tranh so sanh tuple khac kieu

    t0 = time.perf_counter()
    h0 = h(depot, list(all_bins), D, depot)
    pq = [(h0, next(counter), start, 0, [depot])]   # (h, thu tu, trang thai, g, duong di)
    closed = set()
    expanded = 0
    generated = 1

    while pq:
        hval, _, state, g, path = heapq.heappop(pq)
        if state in closed:
            continue
        closed.add(state)
        expanded += 1
        cur, visited = state

        if log is not None:
            log.append({"step": expanded, "current": cur, "visited": sorted(visited),
                        "h": hval, "g": g, "frontier": len(pq)})

        # kiem tra dich: da tham het va dang o Depot (sau khi quay ve)
        if visited == all_bins and cur == depot:
            return {"route": path, "distance": g, "expanded": expanded,
                    "generated": generated,
                    "time_ms": (time.perf_counter() - t0) * 1000}

        unvisited = all_bins - visited
        if unvisited:
            # duyet theo thu tu co dinh cua BINS (khong duyet truc tiep set) de khi
            # nhieu trang thai bang h thi ket qua van nhu nhau o moi lan chay
            successors = [(b, (b, visited | {b})) for b in bins if b in unvisited]
        else:
            successors = [(depot, (depot, visited))]       # buoc cuoi: ve Depot

        for nxt, nstate in successors:
            if nstate in closed:
                continue
            ng = g + D[cur][nxt]
            nh = h(nxt, list(all_bins - nstate[1]), D, depot)
            heapq.heappush(pq, (nh, next(counter), nstate, ng, path + [nxt]))
            generated += 1

    return None


def print_result(res, D):
    print("Lo trinh GBFS:")
    r = res["route"]
    for a, b in zip(r, r[1:]):
        print(f"  {a:16s} -> {b:16s} {D[a][b]:>3d}m")
    print(f"Tong quang duong : {res['distance']} m")
    print(f"So trang thai mo rong : {res['expanded']}  (sinh ra: {res['generated']})")
    print(f"Thoi gian : {res['time_ms']:.3f} ms")


if __name__ == "__main__":
    D = shortest_paths()
    log = []
    res = gbfs(D, log=log)
    print_result(res, D)
    print("\nNhat ky 5 buoc dau (step, vi tri, h, g, frontier):")
    for e in log[:5]:
        print(f"  {e['step']:>2d}  {e['current']:16s} h={e['h']:<4} g={e['g']:<4} frontier={e['frontier']}")