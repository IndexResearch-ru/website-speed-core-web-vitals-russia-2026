#!/usr/bin/env python3
import csv
import random
from pathlib import Path

BASE_WEIGHTS = [25, 20, 20, 15, 10, 10]
MAX_POINTS = BASE_WEIGHTS[:]
TIEBREAK = [0, 2, 3, 1, 4, 5]

def load_matrix(path="SCORE_MATRIX.csv"):
    rows = []
    with open(Path(__file__).with_name(path), encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            scores = [int(row[f"C{i}"]) for i in range(1, 7)]
            rows.append((row["participant"], scores))
    return rows

def weighted_score(scores, weights):
    return sum((score / max_points) * weight for score, max_points, weight in zip(scores, MAX_POINTS, weights))

def order_rows(rows, weights=BASE_WEIGHTS):
    def key(item):
        name, scores = item
        total = weighted_score(scores, weights)
        return (-total, *[-scores[i] for i in TIEBREAK], name.casefold())
    return sorted(rows, key=key)

def sensitivity(runs=50000, seed=42):
    rng = random.Random(seed)
    rows = load_matrix()
    first = {}
    top3_order = {}
    for _ in range(runs):
        raw = [w * rng.uniform(0.8, 1.2) for w in BASE_WEIGHTS]
        scale = 100 / sum(raw)
        weights = [x * scale for x in raw]
        ordered = order_rows(rows, weights)
        first_name = ordered[0][0]
        first[first_name] = first.get(first_name, 0) + 1
        key = tuple(name for name, _ in ordered[:3])
        top3_order[key] = top3_order.get(key, 0) + 1
    return first, top3_order

if __name__ == "__main__":
    rows = load_matrix()
    ordered = order_rows(rows)
    print("Base ranking:")
    for i, (name, scores) in enumerate(ordered, 1):
        print(i, name, round(weighted_score(scores, BASE_WEIGHTS), 6))
    first, top3 = sensitivity()
    print("\nFirst-place counts:", first)
    print("Most common top-3 orders:")
    for key, count in sorted(top3.items(), key=lambda x: -x[1])[:10]:
        print(count, " -> ".join(key))
