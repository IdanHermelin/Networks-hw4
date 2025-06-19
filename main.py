
import os
import sys
import time
from MM1 import MM1Queue
import matplotlib.pyplot as plt

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

    # error_T = []
    # error_N = []

    # for T in range(10,101,10):
    #     print(f"Running simulation with T = {T} seconds")
    #     error_N.append(0)
    #     error_T.append(0)
    #     Theoretical_T = 1/3
    #     Theoretical_N = 2*T
    #     for i in range(20):
    #         # wait 0.01 seconds between each simulation to avoid collisions
    #         time.sleep(0.01)
    #         queue = MM1Queue(1000)
    #         queue.simulate(T, 2, 5)
    #         print(f"Simulation {i+1} completed successfully")
    #         queue.print_statistics()
    #         error_T[-1] += 100*abs(queue.average_wait_time - Theoretical_T)/Theoretical_T
    #         error_N[-1] += 100*abs(queue.num_customers_served - Theoretical_N)/Theoretical_N
    #         print("----------------------------------------")
    #     error_T[-1] /= 20
    #     error_N[-1] /= 20
    # # make it 2 different plots, one for error in average wait time and one for error in number of customers served
    # plt.figure(figsize=(12, 6))
    # plt.subplot(1, 2, 1)
    # plt.plot(range(10, 101, 10), error_T, label='Error in Average Wait Time (%)')
    # plt.xlabel('Simulation Time (seconds)')
    # plt.ylabel('Percentage Error (%)')
    # plt.title('MM1 Queue Simulation Error Analysis - Wait Time')
    # plt.legend()
    # plt.grid()

    # plt.subplot(1, 2, 2)
    # plt.gca().set_prop_cycle(color=['orange'])
    # plt.plot(range(10, 101, 10), error_N, label='Error in Number of Customers Served (%)')
    # plt.xlabel('Simulation Time (seconds)')
    # plt.ylabel('Percentage Error (%)')
    # plt.title('MM1 Queue Simulation Error Analysis - Customers Served')
    # plt.legend()
    # plt.grid()

    # plt.tight_layout()
    # plt.show()
    for i in range(5):
        # wait 0.01 seconds between each simulation to avoid collisions
        time.sleep(0.01)
        queue = MM1Queue(1000)
        queue.simulate(5, 2, 5)
        print(f"Simulation {i+1} completed successfully")
        queue.print_statistics()
        print("----------------------------------------")


if __name__ == "__main__":
    main()
