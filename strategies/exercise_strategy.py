from abc import ABC, abstractmethod

class ExerciseStrategy(ABC):
    """
    Abstract Base Class for exercise strategies.
    Every exercise should implement this class and its methods.
    """

    @abstractmethod
    def check_form(self, joint_angles):
        """Check the form for the exercise based on joint angles."""
        pass