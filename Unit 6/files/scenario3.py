"""
Dressing Room Simulation - Scenario 3
20 customers, 3 dressing rooms, forced 6 items (load test)
"""

import threading
import time
import random
import datetime


class DressingRooms:
    """Manages dressing room using a semaphore."""

    def __init__(self, num_rooms=3):
        self.num_rooms = num_rooms
        self.semaphore = threading.Semaphore(num_rooms)
        self._lock = threading.Lock()
        self.usage_times = []

    def requestRoom(self):
        self.semaphore.acquire()

    def releaseRoom(self, usage_time):
        with self._lock:
            self.usage_times.append(usage_time)
        self.semaphore.release()

    def avg_usage_time(self):
        if not self.usage_times:
            return 0
        return sum(self.usage_times) / len(self.usage_times)


class Customer(threading.Thread):
    """Customer trying clothing items."""

    MAX_ITEMS = 6
    MIN_TIME_PER_ITEM = 1
    MAX_TIME_PER_ITEM = 3

    def __init__(self, customer_id, dressing_rooms, clothing_items=0, results=None, results_lock=None):
        super().__init__()
        self.customer_id = customer_id
        self.dressing_rooms = dressing_rooms
        self.results = results
        self.results_lock = results_lock

        # clothing_items=6 forces max load test scenario
        if clothing_items == 0:
            self.num_items = random.randint(1, self.MAX_ITEMS)
        else:
            self.num_items = min(clothing_items, 20)

    def run(self):
        arrival_time = time.time()
        print(f"  Customer {self.customer_id:02d} arrived with {self.num_items} item(s). Waiting for room...")

        self.dressing_rooms.requestRoom()
        room_start = time.time()
        wait_time = room_start - arrival_time

        print(f"  Customer {self.customer_id:02d} entered room (waited {wait_time:.2f}s).")

        for item in range(self.num_items):
            try_time = random.uniform(self.MIN_TIME_PER_ITEM, self.MAX_TIME_PER_ITEM) * 0.1
            time.sleep(try_time)

        usage_time = time.time() - room_start
        self.dressing_rooms.releaseRoom(usage_time)

        print(f"  Customer {self.customer_id:02d} left room (used room {usage_time:.2f}s).")

        if self.results is not None and self.results_lock is not None:
            with self.results_lock:
                self.results.append({
                    "customer_id": self.customer_id,
                    "num_items": self.num_items,
                    "wait_time": wait_time,
                    "usage_time": usage_time,
                })


class Scenario:
    """Manages the simulation scenario."""

    def __init__(self, num_rooms, num_customers, clothing_items):
        self.num_rooms = num_rooms
        self.num_customers = num_customers
        self.clothing_items = clothing_items

    def run(self):
        print(f"\n{'='*60}")
        print(f"SCENARIO 3 (LOAD TEST): {self.num_customers} customers, {self.num_rooms} rooms, "
              f"items={'random' if self.clothing_items == 0 else self.clothing_items}")
        print(f"{'='*60}")

        dressing_rooms = DressingRooms(num_rooms=self.num_rooms)
        results = []
        results_lock = threading.Lock()

        start_time = datetime.datetime.now()
        print(f"Scenario start: {start_time.strftime('%H:%M:%S.%f')[:-3]}\n")

        customers = [
            Customer(i + 1, dressing_rooms, self.clothing_items, results, results_lock)
            for i in range(self.num_customers)
        ]

        for c in customers:
            c.start()
            time.sleep(random.uniform(0.01, 0.10))

        for c in customers:
            c.join()

        end_time = datetime.datetime.now()
        elapsed = (end_time - start_time).total_seconds()

        total_customers = len(results)
        avg_items = sum(r["num_items"] for r in results) / total_customers if total_customers else 0
        avg_usage = sum(r["usage_time"] for r in results) / total_customers if total_customers else 0
        avg_wait = sum(r["wait_time"] for r in results) / total_customers if total_customers else 0
        max_wait = max(r["wait_time"] for r in results) if results else 0

        print(f"\n{'='*60}")
        print("SCENARIO 3 RESULTS (LOAD TEST)")
        print(f"{'='*60}")
        print(f"  Start Time          : {start_time.strftime('%H:%M:%S.%f')[:-3]}")
        print(f"  End Time            : {end_time.strftime('%H:%M:%S.%f')[:-3]}")
        print(f"  Elapsed Time        : {elapsed:.2f} seconds")
        print(f"  Number of Rooms     : {self.num_rooms}")
        print(f"  Number of Customers : {total_customers}")
        print(f"  Avg Items per Cust  : {avg_items:.2f}")
        print(f"  Avg Room Usage Time : {avg_usage:.2f} seconds")
        print(f"  Avg Wait Time       : {avg_wait:.2f} seconds")
        print(f"  Max Wait Time       : {max_wait:.2f} seconds")
        print(f"{'='*60}\n")


def scenario3():
    print("\n*** CLOTHING STORE DRESSING ROOM SIMULATION ***")
    print("Using preset values for Scenario 3 (Load Test - Max Items)\n")

    num_rooms = 3
    num_customers = 20
    clothing_items = 6   # forced max = load test

    s = Scenario(num_rooms, num_customers, clothing_items)
    s.run()


if __name__ == "__main__":
    scenario3()
