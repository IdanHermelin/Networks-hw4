import random
import heapq
import time
import sys
import secrets
# Events
ARRIVAL = 1
DEPARTURE = 2

class LoadBalancer:
    def __init__(self, capacities:list, probabilities:list, service_rates:list, arrival_rate:float):
        self.capacities = capacities
        self.probabilities = probabilities
        self.service_rates = service_rates
        self.arrival_rate = arrival_rate
        
        # Statistics
        self.A = 0  # Total number of customers served
        self.B = 0  # Total number of customers who got thrown
        self.Tend = 0 # Time of departure of the last customer
        self.Tw = 0 # Average waiting time excluding the service time for serviced customers
        self.Ts = 0 # Average service time for serviced customers


    def simulate(self, simulation_time):
        M = len(self.capacities)
        # build the M queues
        self.queues = [MM1Queue(capacity) for capacity in self.capacities]
        
        # simulate balancer first
        arrivals = [(random.expovariate(self.arrival_rate), ARRIVAL)]
        current_time = arrivals[0][0]  # Start time of the first arrival

        # Generate arrival events until the simulation time is reached
        while current_time < simulation_time:
            next_arrival = current_time + random.expovariate(self.arrival_rate)
            if next_arrival >= simulation_time:
                break
            arrivals.append((next_arrival, ARRIVAL))
            current_time = arrivals[-1][0]

        # Create event lists for each server
        servers_sampled = random.choices(range(M), weights=self.probabilities, k=len(arrivals))
        for i,arrival in enumerate(arrivals):
            # Choose a server based on the probabilities
            self.queues[servers_sampled[i]].event_list.append(arrival)

        # Simulate each server one at a time
        for i in range(M):
            self.queues[i].simulate(simulation_time, self.service_rates[i])
            
        # Aggregate statistics from all queues
        self.A = sum(queue.num_customers_served for queue in self.queues)
        self.B = sum(queue.num_thrown for queue in self.queues)
        self.Tend = max(queue.last for queue in self.queues)
        self.Ts = sum(queue.total_service_time for queue in self.queues) / self.A if self.A > 0 else 0
        self.Tw = sum(queue.total_wait_time for queue in self.queues) / self.A if self.A > 0 else 0

        
        
        
class MM1Queue:
    def __init__(self, N, event_list=None):
        self.capacity = N
        self.queue = []
        self.server_busy = False
        if event_list is None:
            self.event_list = []
        else:
            self.event_list = event_list        # Statistics
        self.last = 0
        self.num_thrown = 0
        self.num_customers_served = 0
        self.total_service_time = 0
        self.total_wait_time = 0
        self.current_time = 0
        self.average_wait_time = 0
        self.average_service_time = 0
    def simulate(self, simulation_time, service_rate):
        if not self.event_list:
            return
        heapq.heapify(self.event_list)
        
        while self.event_list:
            event_time, event_type = heapq.heappop(self.event_list)
            
            if event_time >= simulation_time:
                break
                
            self.current_time = event_time
            # At each step process the next event ordered by time

            # Arrival event means a new packet has arrived so calculate the next arrival time
            # serve packet if server is not busy, otherwise add to queue
            if event_type == ARRIVAL:
                if not self.server_busy:
                    self.server_busy = True
                    wait_time = 0
                    service_time = random.expovariate(service_rate)

                    # if the departure time exceeds the simulation time, we do not count this customer
                    if self.current_time + service_time < simulation_time:
                        self.total_service_time += service_time
                        self.total_wait_time += wait_time

                    heapq.heappush(self.event_list, (self.current_time + service_time, DEPARTURE))
                else:
                    if len(self.queue) < self.capacity:
                        self.queue.append(self.current_time)
                    else:
                        self.num_thrown += 1

            # Departure event means server finished serving a packet
            elif event_type == DEPARTURE:
                self.num_customers_served += 1
                self.last = self.current_time
                if self.queue:
                    # Serve the next customer in the queue
                    arrival_time = self.queue.pop(0)
                    wait_time = self.current_time - arrival_time
                    service_time = random.expovariate(service_rate)                    # if the departure time exceeds the simulation time, we do not count this customer
                    if self.current_time + service_time < simulation_time:
                        self.total_service_time += service_time
                        self.total_wait_time += wait_time
                    heapq.heappush(self.event_list, (self.current_time + service_time, DEPARTURE))
                else:
                    # queue empty, server becomes idle
                    self.server_busy = False
        

    def print_statistics(self):
        if self.num_customers_served == 0:
            print("No customers were served.")
            return
        self.average_service_time = self.total_service_time / self.num_customers_served
        self.average_wait_time = self.total_wait_time / self.num_customers_served
        


def main():
    random.seed(time.time())
    args = sys.argv[1:]
    if len(args) < 5:
        print("Error: Not enough arguments.")
        sys.exit(1)

    T = float(args[0])
    M = int(args[1])
    P = list(map(float, args[2:2+M]))
    λ = float(args[2+M])
    Q = list(map(float, args[3+M:3+2*M]))
    μ = list(map(float, args[3+2*M:3+3*M]))

    # Restriction 1: Sum of P₁ ... Pₘ must be 1
    if not abs(sum(P) - 1.0) < 1e-6:
        print("Error: Probabilities P₁ ... Pₘ must sum to 1.")
        sys.exit(1)

    # Restriction 2: All rates must be positive
    if λ <= 0 or any(q <= 0 for q in Q) or any(mu <= 0 for mu in μ):
        print("Error: All rates (λ, Q₁ ... Qₘ, μ₁ ... μₘ) must be positive.")
        sys.exit(1)

    # Restriction 3: Number of servers M ≥ 1
    if M < 1:
        print("Error: Number of servers M must be at least 1.")
        sys.exit(1)

    # Restriction 4: All input values must be provided
    if len(P) != M or len(Q) != M or len(μ) != M:
        print("Error: Incorrect number of parameters for servers.")
        sys.exit(1)

    # Create the load balancer
    load_balancer = LoadBalancer(capacities=Q, probabilities=P, service_rates=μ, arrival_rate=λ)
    load_balancer.simulate(T)
    print(f"{load_balancer.A} {load_balancer.B} {load_balancer.Tend:.4f} {load_balancer.Tw:.4f} {load_balancer.Ts:.4f}")

if __name__ == "__main__":
    main()
