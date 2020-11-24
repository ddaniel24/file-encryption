"""
filecrypt - encryption / decryption based on symmetric keys

usage: filecrypt [parameters] filename

Run filecrypt -h or filecrypt --help for parameters

Encryption: an existing file is encrypted using an user-defined passphrase. Encryption creates a new file with ".enc"
extension appended.
Example:
    original file (plain): text.txt
    encrypted file to be created: test.txt.enc
    command: filecrypt --encrypt test.txt

Decryption: an existing file is decrypted using an user-defined passphrase. Only ".enc" files are accepted for
decryption. Extension is removed, with no other extra checks.
Example:
    original file (encrypted): text.txt.enc
    decrypted file to be created: text.txt
    command: filecrypt --decrypt test.txt.enc

"""

import sys
import argparse
import getpass
from modules.file import File, EncryptedFile, DecryptedFile
from modules.encryption import Cryptography


def main():
    desc = "Encrypt or decrypt a specific file using a passphrase."
    usage = "%(prog)s [-e] [-d] [-o] file"
    epilog = "Check Github page for usage examples"
    parser = argparse.ArgumentParser(description=desc, usage=usage, epilog=epilog)

    # Add the command line arguments
    parser.add_argument("-e", "--encrypt", action='store_true', default=False, help="encrypt file")
    parser.add_argument("-d", "--decrypt", action='store_true', default=False, help="decrypt file")
    parser.add_argument("-o", "--overwrite", action='store_true', default=False,
                        help="overwrite the new file, if it already exists")
    parser.add_argument("file", type=str,
                        help='file to encrypt/decrypt (can either be file name only, if file is located in the same '
                             'folder as the script, or full path to file)')

    args = parser.parse_args()

    # Check correct value of arguments
    if args.encrypt and args.decrypt:
        print("Cannot have both -e and -d arguments.")
        parser.print_help()
        sys.exit()

    if not args.encrypt and not args.decrypt:
        print("Must specify one of the arguments -e or -d.")
        parser.print_help()
        sys.exit()

    file = File(args.file)

    # Bool value to know if we overwrite the new file or not
    overwrite = args.overwrite

    # Check is file actually exists
    if not file.exists():
        print("The specified file '{0}' cannot be found. Check the path and try again.".format(file.file_path))
        sys.exit()

    # Encrypt section
    if args.encrypt:
        encrypted_file = EncryptedFile(file)

        display_file_overwrite_prompt(encrypted_file, overwrite)

        crypt = Cryptography(file, encrypted_file)

        # Ask for passphrase and confirmation. Check for the same input.
        match = False
        passphrase = ""
        while not match:
            passphrase = getpass.getpass(prompt="Input passphrase for encryption: ")
            passphrase_confirmation = getpass.getpass(prompt="Confirm passphrase for encryption: ")
            if passphrase == passphrase_confirmation:
                match = True
            else:
                print("Passphrases do not match. Try again.")

        crypt.set_passphrase(passphrase)

        crypt.encrypt()

        print("Done. Encrypted file saved in '{0}'".format(encrypted_file.file_path))

    # Decrypt section
    if args.decrypt:
        decrypted_file = DecryptedFile(file)

        # Remove the ".enc" file extension, in order to get the decrypted file name
        if not decrypted_file.update_file_name():
            print("File '{0}' is not a valid '.enc' encrypted file.".format(decrypted_file.file_path))
            sys.exit()

        display_file_overwrite_prompt(decrypted_file, overwrite)

        crypt = Cryptography(file, decrypted_file)

        # Ask for decryption passphrase
        passphrase = getpass.getpass(prompt="Input passphrase for decryption: ")

        crypt.set_passphrase(passphrase)

        if not crypt.decrypt():
            print("Invalid passphrase. File decryption failed.")
        else:
            print("Done. Decrypted file saved in '{0}'".format(decrypted_file.file_path))


def display_file_overwrite_prompt(file: File, overwrite: bool):
    """
    Method to ask the user for file overwrite confirmation, in case -o argument is not used
    :param file: file to check if it already exists or not
    :param overwrite: True if -o argument has been passed, False otherwise
    """
    if file.exists() and not overwrite:
        answer = ""
        # Make sure we only get y or n as an answer
        while answer not in ["y", "n"]:
            answer = str(input("File '{0}' exists. Overwrite? [y/n] ".format(file.file_path))).lower()[0]

        if answer == "n":
            print("Nothing to do.")
            sys.exit()


if __name__ == '__main__':
    main()
