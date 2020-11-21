# File encryption in Python using symmetric keys
The current project implements file encryption / decryption based on symmetric keys in Python. Symmetric key algorithms are cryptographic algorithms which use the same chryptographic key for encrypting plain text and decrypting cypher text. 

## Prerequisites
Code is written in Python 3.7.
Install all packages from _requirements.txt_ by using **pip install [package_name]**

## Usage
filecrypt.py [-e] [-d] [-o] filepath

arguments:

file: file to encrypt/decrypt
-e, --encrypt:   encrypt file
-d, --decrypt:   decrypt file
-o, --overwrite:  overwrite the new file, if it already exists

### Encryption 
Files are encrypted in a new file, with ".enc" extension appended.
Command example:
**filecrypt.py -e test.txt**
will output **test.txt.enc** (encrypted file)

### Decryption 
Only ".enc" files are valid for decryption. Files are decrypted in a new file, with the ".enc" extension removed.
Command example:
**filecrypt.py -d test.txt.enc**
will output **test.txt** (decrypted file)
