import time
import random

class TaskAgent:
    """Represents an autonomous task that acts as an agent in the system."""
    def __init__(self, name, dependencies):
        self.name = name
        self.dependencies = dependencies # List of task names this task depends on
        self.state = "PENDING" # PENDING, READY, EXECUTING, COMPLETED
        self.execution_time = random.randint(1, 3) # Simulate work duration
        self.time_spent_executing = 0

    def __repr__(self):
        return f"TaskAgent({self.name}, State: {self.state})"

    def update_state(self, all_agents_status):
        """Each agent independently updates its state based on dependencies and current status."""
        if self.state == "COMPLETED":
            return

        if self.state == "PENDING":
            # Leaderless: Agent checks its own dependencies
            all_deps_completed = True
            for dep_name in self.dependencies:
                if all_agents_status.get(dep_name) != "COMPLETED":
                    all_deps_completed = False
                    break
            if all_deps_completed:
                self.state = "READY" # Agent becomes ready when dependencies are met
                print(f"[{self.name}] became READY.")
            else:
                print(f"[{self.name}] is PENDING, waiting for dependencies: {self.dependencies}")

        elif self.state == "READY":
            # Simulate starting execution
            self.state = "EXECUTING" # Agent starts executing when ready
            print(f"[{self.name}] started EXECUTING.")

        elif self.state == "EXECUTING":
            self.time_spent_executing += 1
            print(f"[{self.name}] is EXECUTING ({self.time_spent_executing}/{self.execution_time}).")
            if self.time_spent_executing >= self.execution_time:
                self.state = "COMPLETED" # Agent completes after its work is done
                print(f"[{self.name}] COMPLETED its task.")

# Define the graph of task dependencies
# This represents the "graph-based orchestration" where relationships are explicit.
task_dependencies = {
    "TaskA": [],
    "TaskB": ["TaskA"],
    "TaskC": ["TaskA"],
    "TaskD": ["TaskB", "TaskC"],
    "TaskE": ["TaskD"]
}

# Initialize agents based on the defined graph
agents = {name: TaskAgent(name, deps) for name, deps in task_dependencies.items()}

print("--- Starting Leaderless Graph-Based Orchestration Simulation ---")

# Simulation loop
max_steps = 20
for step in range(1, max_steps + 1):
    print(f"\n--- Simulation Step {step} ---")

    # Get current status of all agents. This global view is used by agents to check dependencies.
    # In a real distributed system, this would be achieved via communication between agents.
    current_agents_status = {name: agent.state for name, agent in agents.items()}

    # Each agent independently updates its state.
    # The iteration order here is for simulation purposes; in reality, agents would act concurrently.
    for agent_name in sorted(agents.keys()): # Sort for consistent output
        agent = agents[agent_name]
        agent.update_state(current_agents_status) # Leaderless: Agent decides its own state based on neighbors (dependencies)

    # Check if all tasks are completed
    all_completed = all(agent.state == "COMPLETED" for agent in agents.values())
    if all_completed:
        print("\n--- All tasks completed! ---")
        break

    time.sleep(0.5) # Simulate time passing between steps

if not all_completed:
    print("\n--- Simulation ended, not all tasks completed. ---")
