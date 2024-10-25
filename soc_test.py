import pybamm

model = pybamm.lithium_ion.SPM()

POWER_USED = 0.5
# max soc = 4.2?
# min soc = 3.3 V
num_minutes = 5

sim_discharge = pybamm.Simulation(model, experiment = [("Discharge at " + str(POWER_USED) + "W for " + str(num_minutes) + " minutes")])
sim_rest = pybamm.Simulation(model, experiment=pybamm.Experiment([("Rest for " + str(num_minutes) + " minutes")]))
sim_charge = pybamm.Simulation(model, experiment=[("Charge at " + str(POWER_USED) + "W for " + str(num_minutes) + " minutes")])

sim_discharge.build_for_experiment(initial_soc = 0.5)
sim_rest.build_for_experiment()
sim_charge.build_for_experiment()

simulations = [sim_discharge, sim_rest, sim_charge]

solution = None
action = 0

for i in range(30):
    print(i)
    solution = simulations[action].solve(starting_solution = solution) # TODO
print(solution["Total lithium capacity [A.h]"].data)
solution.plot(["Voltage [V]"])
solution.plot(["Discharge capacity [A.h]"])
solution.plot(['Positive electrode capacity [A.h]'])
solution.plot(["Discharge energy [W.h]"])

solution.plot(['Throughput capacity [A.h]'])

# issue: power not linear with voltage but linear with discharge capacity?
# need power to change in voltage/change in soc conversion for upper bounds + degradation cost formula??


# still confused -- need for degradation cost - can wait
# add more actions
# add more observations (current, voltage, soc??, price, stuff like that)
# - how will the model know the price? not rly an input - needs to be part of the state... or something
# but should like know it before
# need to predict step based on the price - should be from outside the model? 
    # it could be from outside, just reading from a different file at each time step
    # but need to know when deciding what action to take tho???