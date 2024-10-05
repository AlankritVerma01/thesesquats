class ExerciseContext:
    """
    Context class to switch between different exercise strategies.
    """

    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        """
        Set a different strategy.
        """
        self._strategy = strategy

    def check_exercise_form(self, joint_angles, joint_distances):
        """
        Use the selected strategy to check the exercise form.
        """
        return self._strategy.check_form(joint_angles, joint_distances)
