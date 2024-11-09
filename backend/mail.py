import smtplib

class Mail:

    def __init__(self, server, port, username, password):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def __set_up__(self):
        self.smtp_connection = smtplib.SMTP(self.server, self.port)
        self.smtp_connection.ehlo()
        self.smtp_connection.starttls()
        self.smtp_connection.login(self.username, self.password)

    def send(self, to, subject, text):
        """
        Send the mail
        :param to: Receiver
        :param subject: Subject
        :param text: Message
        :return: 0 - if success else -1
        """
        try:
            self.__set_up__()
            msg = f'Subject: {subject}\n\n{text}'

            self.smtp_connection.sendmail(self.username, to, msg)
            self.smtp_connection.quit()
            return 0
        except Exception as e:
            print(e)
            return -1