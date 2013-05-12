from client import Client

class HumbugStream(object):
    """
    A Humbug stream-like object
    """

    def __init__(self, type, to, subject, email=None, client=None):
        if client:
            self.client = client
        elif email:
            self.client = Client(email=email)
        else:
            raise RuntimeError("email or client not specified.")

        self.type = type
        self.to = to
        self.subject = subject

    def write(self, content):
        message = {"type": self.type,
                   "to": self.to,
                   "subject": self.subject,
                   "content": content}
        self.client.send_message(message)

    def flush(self):
        pass
