from pathlib import Path


# Generic file class
class File:
    def __init__(self, file_path: str):
        self.file_path = file_path

    # Check is file specified by file_path exists
    def exists(self):
        file = Path(self.file_path)
        if file.exists():
            return True

        return False

    # Read the contents of a file, in binary
    def read_file(self):
        with open(self.file_path, 'rb') as f:
            file_stream = f.read()

        return file_stream

    # Write to a file, in binary
    def write_file(self, file_stream):
        with open(self.file_path, 'wb') as f:
            f.write(file_stream)


# Class for file to be encrypted
class EncryptedFile(File):
    def __init__(self, file: File):
        super().__init__(file.file_path)
        self.file_path = file.file_path + ".enc"


# Class for file to be decrypted
class DecryptedFile(File):
    def __init__(self, file: File):
        super().__init__(file.file_path)

    # Remove ".enc" from file name
    def update_file_name(self):
        # Check first if the file end with ".enc" extension. Otherwise, we consider it invalid.
        if not self.file_path.endswith(".enc"):
            return False

        # Remove file extension
        self.file_path = self.file_path[:-4]

        return True

