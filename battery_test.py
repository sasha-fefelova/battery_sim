import pybamm
import time

num_minutes = 10

model = pybamm.lithium_ion.SPM()
solution = None
all_discharge_capacities = []

class ErrorCallback(pybamm.callbacks.Callback):
    def on_experiment_infeasible(self, logs):
        print("INFEASIBLE")
        # return False
    def on_experiment_error(self, logs):
        print("Error")
    # def on_experiment_end(self, logs):
    #     print(f"We are at the end of the simulation. Logs are ")

callback = ErrorCallback()
experiemnt = pybamm.Experiment([("Discharge at C/2 for " + str(1000) + " minutes")])
sim = pybamm.Simulation(model, experiment = experiemnt)
solution = sim.solve(starting_solution = solution, callbacks = callback) 


# for i in range(30):
#     before_time_step = time.perf_counter()
#     if i % 3 == 0:
#         experiemnt = pybamm.Experiment([("Discharge at C/10 for " + str(num_minutes) + " minutes")])
#     elif i % 3 == 1:
#         experiemnt = pybamm.Experiment([("Rest for " + str(num_minutes) + " minutes")])
#     else: 
#         experiemnt = pybamm.Experiment([("Charge at C/10 for " + str(num_minutes) + " minutes")])

#     sim = pybamm.Simulation(model, experiment = experiemnt)
#     before_sim = time.perf_counter()
#     solution = sim.solve(starting_solution = solution) # SLOW STEP
#     print("simulation time: ",  time.perf_counter() - before_sim, " time step time: ", time.perf_counter() - before_time_step, " non-simulation time: ", before_sim - before_time_step)


