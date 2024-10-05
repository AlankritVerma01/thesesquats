# feedback_utils.py

class FeedbackManager:
    """
    Manages feedback during exercise analysis, ensuring feedback is 
    appropriately generated, stored, and displayed.
    """
    
    def __init__(self):
        # A dictionary to store feedback for joints over multiple frames
        self.feedback_log = []

    def process_feedback(self, feedback_messages):
        """
        Process and store feedback messages during the analysis.
        
        Args:
        - feedback_messages: List of feedback strings for the current frame.
        
        Returns:
        - A formatted string to be displayed on the screen, summarizing all feedback.
        """
        if feedback_messages:
            for message in feedback_messages:
                # Store feedback if it's not already in the log to avoid duplicates
                if message not in self.feedback_log:
                    self.feedback_log.append(message)
        
        # Return formatted feedback for display (could be customized further)
        return "\n".join(feedback_messages)

    def get_all_feedback(self):
        """
        Retrieve all feedback stored across the video for final summary or display.
        
        Returns:
        - A string with all feedback messages concatenated.
        """
        return "\n".join(self.feedback_log)

    def reset_feedback(self):
        """
        Clear the feedback log when needed (e.g., when starting a new analysis).
        """
        self.feedback_log = []
