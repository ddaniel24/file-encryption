from pathlib import Path


# Generic file class
class File:
    def __init__(self, file_path: str):
        """
        Constructor for File object
        :type file_path: full path to file
        """
        self.file_path = file_path

    def exists(self):
        """
        Chek if the file specified by file_path exists
        :rtype: True if file exists. False otherwise
        """
        file = Path(self.file_path)
        if file.exists():
            return True

        return False

    def read_file(self):
        """
        Read the contents of a file, in binary.
        :rtype: bytearray
        """
        with open(self.file_path, 'rb') as f:
            file_stream = f.read()

        return file_stream

    def write_file(self, file_stream):
        """
        Write to a file, in binary
        """
        with open(self.file_path, 'wb') as f:
            f.write(file_stream)


class EncryptedFile(File):
    def __init__(self, file: File):
        """
        Constructor for EncryptedFile object
        """
        super().__init__(file.file_path)
        # Add by default ".enc" extension for the new encrypted file
        self.file_path = file.file_path + ".enc"


class DecryptedFile(File):
    def __init__(self, file: File):
        """
        Constructor for DecryptedFile object
        """
        super().__init__(file.file_path)

    def update_file_name(self):
        """
        Check if the file ends with ".enc" extension. Otherwise, we consider it invalid by design.
        If the file does end with ".enc", the decrypted file will need to have this extension removed.
        :rtype: False is file extension fails. True otherwise.
        """

        if not self.file_path.endswith(".enc"):
            return False

        # Remove file extension
        self.file_path = self.file_path[:-4]

        return True

