# models/contribution.py

class Contribution:
    def __init__(self, user_id, contribution_type, points, date, screenshot_url):
        self.user_id = user_id
        self.contribution_type = contribution_type
        self.points = points
        self.date = date
        self.screenshot_url = screenshot_url

    def __repr__(self):
        return f"<Contribution(user_id={self.user_id}, type={self.contribution_type}, points={self.points})>"
