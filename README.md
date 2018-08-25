# SecureFileSharing

It is required to build an online Secure File Sharing System
1. The sharing of files should be through a public folder over a public cloud storage provider (onedrive, google drive, dropbox, .....)
2. All files stored on the folder must be encrypted using AES-128
3. The creator of the file chooses the encryption key using a RNG on his own machine, and stores it locally
4. The file must start with a header including the creator ID, the creator email, and the file size, followed by the encrypted data. This ID must be unique
5. Each user who wants to access the file must first send a request to the file owner, the request will contain the request ID and , the requester ID and email and the requester public key (2048 RSA). The file owner if wishes, sends the file decryption key encrypted by the requester public key.
6. The requester can then decrypt the file encryption key using his private key and then decrypts the file itself.
