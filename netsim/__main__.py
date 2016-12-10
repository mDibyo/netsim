from .simulator import Simulator


if __name__ == '__main__':
    simulator = Simulator(0.000001, [], [])
    simulator.run(1)

