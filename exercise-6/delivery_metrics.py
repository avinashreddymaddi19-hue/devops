from prometheus_client import start_http_server, Gauge, Summary
import random
import time

HIGH_LOAD = False

total_deliveries = Gauge("total_deliveries", "Current simulated delivery workload")
pending_deliveries = Gauge("pending_deliveries", "Pending deliveries")
on_the_way_deliveries = Gauge("on_the_way_deliveries", "Deliveries in transit")
average_delivery_time = Summary("average_delivery_time", "Observed delivery duration in seconds")

def simulate_delivery():
    pending = random.randint(50, 100) if HIGH_LOAD else random.randint(5, 9)
    duration = random.uniform(35, 45) if HIGH_LOAD else random.uniform(15, 25)
    on_the_way = random.randint(5, 20)
    delivered = random.randint(30, 70)
    total_deliveries.set(pending + on_the_way + delivered)
    pending_deliveries.set(pending)
    on_the_way_deliveries.set(on_the_way)
    average_delivery_time.observe(duration)
    print(f"high_load={HIGH_LOAD} pending={pending} duration={duration:.2f}s", flush=True)

if __name__ == "__main__":
    start_http_server(8000, addr="0.0.0.0")
    while True:
        simulate_delivery()
        time.sleep(1)


