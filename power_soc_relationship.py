import pybamm
import matplotlib.pyplot as plt

num_minutes = 5

model = pybamm.lithium_ion.SPM()
solution = None
all_discharge_capacities = []

MAX_POWER_USED = 1
NUM_POWER_PARTITIONS = 4 # 4 positive powers, 4 negative, 1 zero
NUM_ACTIONS = 2 * NUM_POWER_PARTITIONS + 1

sims = []
# power = -MAX_POWER_USED
for i in range(NUM_ACTIONS):
    power = MAX_POWER_USED * (i / NUM_POWER_PARTITIONS - 1) # from max discharging to max charging
    # print("i = 4 power", power)
    action = "Charge"
    if power < 0:
        action = "Discharge"
    power = abs(power)
    if i == NUM_POWER_PARTITIONS:
        sims.append(pybamm.Simulation(model,  experiment=pybamm.Experiment([("Rest for " + str(num_minutes) + " minutes")])))
    else:
        sims.append(pybamm.Simulation(model, experiment = [(action + " at " + str(power) + "W for " + str(num_minutes) + " minutes")]))

init_soc = 0.5
soc_changes = []
soc_change_to_action_ratios = []
for i, sim in enumerate(sims):
    solution = sim.solve(starting_solution = None, initial_soc = init_soc)
    soc_change = -solution["Discharge capacity [A.h]"].entries[-1] # discharge capacity always starts with 0, 
    # - discharge capacity at the end of the solution is the change in soc
    effective_action = (i / NUM_POWER_PARTITIONS - 1)
    soc_changes.append(soc_change) 
    soc_change_to_action_ratios.append(soc_change/effective_action)


plt.plot(soc_changes)
plt.show()


plt.plot(soc_change_to_action_ratios, "o")
plt.show()
print(soc_change_to_action_ratios)
soc_change_to_action_ratios.pop(NUM_POWER_PARTITIONS) # 4 - rest where action is 0
print(sum(soc_change_to_action_ratios)/(2 * NUM_POWER_PARTITIONS))


# action --> predicted soc change relationship