class FileManager:
    @staticmethod
    def read(f_name):
        with open(f_name, 'r+') as f:
            return f.read()

    @staticmethod
    def write(f_name, string):
        with open(f_name, 'w+') as f:
            f.write(string)