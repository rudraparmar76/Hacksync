class DebateState:
    def __init__(self):
        self.turns = []

    def add(self, role, text):
        self.turns.append(f"{role}: {text}")

    def transcript(self):
        return "\n".join(self.turns)

    def last(self):
        return self.turns[-1] if self.turns else ""
