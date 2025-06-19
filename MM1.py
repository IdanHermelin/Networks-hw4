import random
import heapq
import time
import secrets
# Events
ARRIVAL = 1
DEPARTURE = 2

class MM1Queue:
    def __init__(self, N):
        self.capacity = N
        self.queue = []
        self.server_busy = False

        # Statistics
        self.num_customers_served = 0
        self.total_wait_time = 0
        self.current_time = 0
        self.average_wait_time = 0

        # Event list for the simulation
        # Using a min-heap to manage events
        self.event_list = []


    def simulate(self, simulation_time, arrival_rate, service_rate):
        random.seed(time.time())  # Seed for reproducibility

        # Schedule the first arrival
        heapq.heappush(self.event_list, (random.expovariate(arrival_rate), ARRIVAL))
        event_time, event_type = heapq.heappop(self.event_list)
        self.current_time = event_time

        while self.current_time < simulation_time:
            # Arrival event means a new packet has arrived so calculate the next arrival time
            # serve packet if server is not busy, otherwise add to queue
            if event_type == ARRIVAL:
                if not self.server_busy:
                    self.server_busy = True
                    wait_time = 0
                    service_time = random.expovariate(service_rate)

                    # if the departure time exceeds the simulation time, we do not count this customer
                    if self.current_time + service_time < simulation_time:
                        self.total_wait_time += wait_time + service_time

                    heapq.heappush(self.event_list, (self.current_time + service_time, DEPARTURE))
                else:
                    if len(self.queue) < self.capacity:
                        self.queue.append(self.current_time)
                next_arrival = self.current_time + random.expovariate(arrival_rate)
                heapq.heappush(self.event_list, (next_arrival, ARRIVAL))

            # Departure event means server finished serving a packet
            elif event_type == DEPARTURE:
                self.num_customers_served += 1
                if self.queue:
                    # Serve the next customer in the queue
                    arrival_time = self.queue.pop(0)
                    wait_time = self.current_time - arrival_time
                    service_time = random.expovariate(service_rate)

                    # if the departure time exceeds the simulation time, we do not count this customer
                    if self.current_time + service_time < simulation_time:
                        self.total_wait_time += wait_time + service_time

                    heapq.heappush(self.event_list, (self.current_time + service_time, DEPARTURE))
                else:
                    # queue empty, server becomes idle
                    self.server_busy = False
            event_time, event_type = heapq.heappop(self.event_list)
            self.current_time = event_time

    def print_statistics(self):
        if self.num_customers_served == 0:
            print("No customers were served.")
            return
        
        self.average_wait_time = self.total_wait_time / self.num_customers_served
        print(f"Total customers served: {self.num_customers_served}")
        print(f"Total wait time: {self.total_wait_time:.2f} seconds")
        print(f"Average wait time per customer: {self.average_wait_time:.2f} seconds")

    
    
