class TextBox:
    def __init__(self):
        self.messages = []

    def post_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []