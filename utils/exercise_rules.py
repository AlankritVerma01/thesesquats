from strategies.exercise_context import ExerciseContext
from strategies.pullup_strategy import PullUpStrategy
from strategies.squat_strategy import SquatStrategy
from strategies.bench_press_strategy import BenchPressStrategy
from strategies.easy_exercise_strategy import EasyExerciseStrategy  # Import the new strategy

from strategies.bicep_curl_strategy import BicepCurlStrategy
from strategies.lunge_strategy import LungeStrategy
from strategies.overhead_press_strategy import OverheadPressStrategy

def get_exercise_strategy(exercise_type):
    """
    Return the appropriate exercise strategy based on the selected exercise type.
    """
    if exercise_type == 'Pull-up':
        return PullUpStrategy()
    elif exercise_type == 'Squat':
        return SquatStrategy()
    elif exercise_type == 'Bench Press':
        return BenchPressStrategy()
    elif exercise_type == 'Easy Exercise':  # Add the new easy exercise
        return EasyExerciseStrategy()
    elif exercise_type == 'Squat':
        return SquatStrategy()
    elif exercise_type == 'Bicep Curl':
        return BicepCurlStrategy()
    elif exercise_type == 'Lunge':
        return LungeStrategy()
    elif exercise_type == 'Overhead Press':
        return OverheadPressStrategy()
    else:
        raise ValueError(f"Exercise type {exercise_type} is not supported")

def check_exercise_form(exercise_type, joint_angles, joint_distances=None):
    """
    This function will be called from `app.py` and it will manage which strategy to use.
    It runs the form-checking logic based on the exercise type.
    """
    # Get the strategy for the selected exercise
    strategy = get_exercise_strategy(exercise_type)
    
    # Create the context with the selected strategy
    exercise_context = ExerciseContext(strategy)

    # Check the form using the selected strategy
    feedback = exercise_context.check_exercise_form(joint_angles, joint_distances)

    return feedback
