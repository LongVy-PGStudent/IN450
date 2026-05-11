"""
Unit 7 assigment
Implements Bubble Sort (baseline) and an optimized version,
then compares both against Merge Sort across small, medium, and large datasets.

Bubble Sort reference:
  GeeksforGeeks. (2024). Bubble Sort Algorithm. https://www.geeksforgeeks.org/bubble-sort/

Merge Sort reference:
  GeeksforGeeks. (2024). Merge Sort Algorithm. https://www.geeksforgeeks.org/merge-sort/
"""

import time
import random
import copy

# ── Dataset generation ─────────────────────────────────────────────────────────
random.seed(42)
SMALL  = [random.randint(1, 10_000) for _ in range(10)]
MEDIUM = [random.randint(1, 100_000) for _ in range(1_000)]
LARGE  = [random.randint(1, 1_000_000) for _ in range(10_000)]

# ── Bubble Sort (original | baseline) ─────────────────────────────────────────
def bubble_sort(arr):
    """
    Standard bubble sort.
    Source: GeeksforGeeks – https://www.geeksforgeeks.org/bubble-sort/
    Time complexity: O(n²) average and worst case.
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# ── Optimised Bubble Sort (deep copy) ────────────────────────────────
def bubble_sort_optimized(arr):
    """
    Optimized bubble sort with early-exit flag.
    If a full pass makes no swaps the list is already sorted; stop immediately.
    This turns best-case from O(n²) to O(n) on already-sorted or nearly-sorted data.
    Source: GeeksforGeeks – https://www.geeksforgeeks.org/bubble-sort/
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:          # No swaps ⇒ array is sorted
            break
    return arr

# ── Merge Sort (alternative) ────────────────────────────────────────
def merge_sort(arr):
    """
    Merge sort | divide and conquer.
    Source: GeeksforGeeks | https://www.geeksforgeeks.org/merge-sort/
    Time complexity: O(n log n) in all cases.
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# ── Benchmark ───────────────────────────────────────────────────────────
def benchmark(label, func, data):
    data_copy = copy.deepcopy(data)
    start = time.perf_counter()
    func(data_copy)
    elapsed = time.perf_counter() - start
    print(f"  {label:<30s}: {elapsed:.6f} s")
    return elapsed

# ── Main code ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    datasets = [
        ("Small  (10 items)",    SMALL),
        ("Medium (1,000 items)", MEDIUM),
        ("Large  (10,000 items)",LARGE),
    ]

    results = {}
    print("=" * 60)
    print("  SORTING ALGORITHM BENCHMARK")
    print("=" * 60)

    for ds_label, dataset in datasets:
        print(f"\n[{ds_label}]")
        t1 = benchmark("Bubble Sort (baseline)",   bubble_sort,           dataset)
        t2 = benchmark("Bubble Sort (optimized)",  bubble_sort_optimized, dataset)
        t3 = benchmark("Merge Sort",               merge_sort,            dataset)
        results[ds_label] = {"bubble": t1, "bubble_opt": t2, "merge": t3}

    print("\n" + "=" * 60)
    print("  IMPROVEMENT SUMMARY")
    print("=" * 60)
    for label, r in results.items():
        pct_bubble = (r["bubble"] - r["bubble_opt"]) / r["bubble"] * 100 if r["bubble"] else 0
        pct_merge  = (r["bubble"] - r["merge"])      / r["bubble"] * 100 if r["bubble"] else 0
        print(f"\n{label}")
        print(f"  Optimized bubble vs baseline : {pct_bubble:+.1f}%")
        print(f"  Merge sort   vs baseline     : {pct_merge:+.1f}%")
    print()
