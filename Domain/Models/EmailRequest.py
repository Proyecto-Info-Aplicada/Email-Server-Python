class EmailRequest:
    def __init__(self, correlation_id, email, subject, body):
        self.correlation_id = correlation_id
        self.email = email
        self.subject = subject
        self.body = body
