from datetime import datetime

class SEPLogger:

    def __init__(self, path, file_name):
        self.file_name = file_name
        self.path      = path

        try:
            with open(path + self.file_name, 'w') as file:
                file.write(f'Logging has been configured.\nThe name of the file is {self.file_name}.\nIt can be found at {self.path}{self.file_name}')

        except Exception as e:
            print(e)

    def log(self, heading, text):
        with open(self.path + self.file_name, 'a') as file:
            file.write(f'\n{heading} at {datetime.now().strftime("%H:%M:%S")}:\n{text}')

        print(f'\n{heading} at {datetime.now().strftime("%H:%M:%S")}:\n{text}')

    def get_log(self):
        with open(self.file_name, 'r') as file:
            log_array = [line.strip() for line in file.readlines()]

        return log_array