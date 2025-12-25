import random
from typing import List, Tuple


class PlanningAgent:
    """
    An agent that gets a goal, breaks it into sub-tasks, 
    executes each step and reflects on success and retries if needed.
    """
    
    def __init__(self, success_rate: float = 0.7):
        """
        Initialize the PlanningAgent.
        
        Args:
            success_rate: Probability of success for each action (0.0 to 1.0)
        """
        self.history: List[Tuple[str, bool]] = []
        self.success_rate = max(0.0, min(1.0, success_rate))  # Clamp between 0 and 1

    def perceive_goal(self, goal: str) -> str:
        """
        Perceive and validate the goal.
        
        Args:
            goal: The goal to be achieved
            
        Returns:
            The validated goal string
            
        Raises:
            ValueError: If goal is empty or invalid
        """
        if not goal or not isinstance(goal, str) or not goal.strip():
            raise ValueError("Goal must be a non-empty string")
        return goal.strip()

    def plan(self, goal: str) -> List[str]:
        """
        Break goal into ordered steps.
        
        Args:
            goal: The goal to plan for
            
        Returns:
            List of ordered steps to achieve the goal
        """
        return [
            f"Research {goal}",
            f"Draft outline for {goal}",
            f"Create final output for {goal}"
        ]

    def act(self, steps: List[str]) -> List[Tuple[str, bool]]:
        """
        Execute steps and return success/failure results.
        
        Args:
            steps: List of steps to execute
            
        Returns:
            List of tuples (step, success_status)
        """
        results = [
            (step, random.random() < self.success_rate) 
            for step in steps
        ]
        self.history.extend(results)
        return results

    def reflect(self, results: List[Tuple[str, bool]]) -> List[str]:
        """
        Reflect on results and identify steps that need retrying.
        
        Args:
            results: List of (step, success) tuples from act()
            
        Returns:
            List of steps that need to be retried
        """
        retries = [step for step, success in results if not success]
        return retries

    def get_execution_summary(self) -> dict:
        """
        Get a summary of all executed steps.
        
        Returns:
            Dictionary with execution statistics
        """
        if not self.history:
            return {"total": 0, "successful": 0, "failed": 0, "success_rate": 0.0}
        
        total = len(self.history)
        successful = sum(1 for _, success in self.history if success)
        failed = total - successful
        success_rate = successful / total if total > 0 else 0.0
        
        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "success_rate": success_rate
        }


if __name__ == "__main__":
    # Example usage
    agent = PlanningAgent(success_rate=0.7)

    goal = agent.perceive_goal("Write AI blog post")
    steps = agent.plan(goal)
    results = agent.act(steps)
    retries = agent.reflect(results)

    print("Steps attempted:", results)
    print("Retry steps:", retries)
    print("Execution summary:", agent.get_execution_summary())
