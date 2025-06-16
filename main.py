
import os
import sys

from MM1 import MM1Queue

def main():
    # arguments = sys.argv[1:]
    # if len(arguments) != 4:
    #     print("Usage: python main.py T N lambda mu")
    #     sys.exit(1)

    # T = int(arguments[0])
    # N = int(arguments[1])
    # arrival_rate = float(arguments[2])
    # service_rate = float(arguments[3])

    # queue = MM1Queue(N)
    # queue.simulate(T, arrival_rate, service_rate)

    
    for i in range(5):
        queue = MM1Queue(1000)
        queue.simulate(5, 2, 5)
        print(f"Simulation {i+1} completed successfully")
        queue.print_statistics()
        print("----------------------------------------")
        
        
if __name__ == "__main__":
    main()
