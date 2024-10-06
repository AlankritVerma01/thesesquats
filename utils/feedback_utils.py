# feedback_utils.py

import time

class FeedbackManager:
    def __init__(self):
        self.active_feedback = {}
        self.all_feedback = set()
        self.last_feedback_time = 0
        self.cooldown = 3  # Minimum time in seconds between feedback updates
        self.current_feedback_message = None
        self.feedback_priority = {
            # Define priority levels for different feedback messages
            # Lower number means higher priority
            "Keep your back straight": 1,
            "Bend your knees more": 2,
            "Extend your arms fully": 3,
            "Right elbow not detected": 1,
            "Left elbow not detected": 1,
            # Add other feedback types as needed
        }

    def update_feedback(self, violations):
        current_time = time.time()
        # Check if cooldown period has elapsed
        if current_time - self.last_feedback_time < self.cooldown and self.current_feedback_message:
            return [self.current_feedback_message]

        # Remove resolved feedback
        resolved_issues = set(self.active_feedback.keys()) - set(violations)
        for issue in resolved_issues:
            del self.active_feedback[issue]

        # Add new violations
        for violation in violations:
            if violation not in self.active_feedback:
                self.active_feedback[violation] = {
                    'timestamp': current_time,
                    'message': violation,
                    'priority': self.get_feedback_priority(violation)
                }
                self.all_feedback.add(violation)

        # Determine the highest priority feedback message
        if self.active_feedback:
            highest_priority_issue = min(
                self.active_feedback.values(),
                key=lambda x: x['priority']
            )
            self.current_feedback_message = highest_priority_issue['message']
        else:
            self.current_feedback_message = None

        self.last_feedback_time = current_time
        return [self.current_feedback_message] if self.current_feedback_message else []

    def get_feedback_priority(self, feedback_message):
        # Assign priority based on message content
        for key in self.feedback_priority:
            if key in feedback_message:
                return self.feedback_priority[key]
        return 999  # Default low priority

    def reset_feedback(self):
        self.active_feedback = {}
        self.all_feedback = set()
        self.last_feedback_time = 0
        self.current_feedback_message = None

    def get_all_feedback(self):
        return "\n".join(self.all_feedback)
