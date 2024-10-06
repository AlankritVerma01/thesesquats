# feedback_utils.py

class FeedbackManager:
    """
    Manages feedback during exercise analysis, ensuring feedback is 
    appropriately generated, stored, and displayed.
    """
    
    def __init__(self):
        # A set to store active feedback messages
        self.active_feedback = set()
        # A list to store all feedback messages for summary
        self.feedback_log = []

    def update_feedback(self, feedback_messages):
        """
        Update the active feedback messages based on the current frame.

        Args:
        - feedback_messages: List of feedback strings for the current frame.

        Returns:
        - A list of current active feedback messages.
        """
        # Convert feedback_messages to a set
        feedback_set = set(feedback_messages)

        # Remove messages that are no longer present
        self.active_feedback = self.active_feedback.intersection(feedback_set)

        # Identify new messages
        new_messages = feedback_set - self.active_feedback

        # Add new messages to active_feedback and feedback_log
        for message in new_messages:
            self.active_feedback.add(message)
            self.feedback_log.append(message)

        return list(self.active_feedback)

    def get_all_feedback(self):
        """
        Retrieve all feedback stored across the video for final summary or display.
        
        Returns:
        - A string with all feedback messages concatenated.
        """
        return "\n".join(set(self.feedback_log))

    def reset_feedback(self):
        """
        Clear the feedback log when needed (e.g., when starting a new analysis).
        """
        self.active_feedback = set()
        self.feedback_log = []
