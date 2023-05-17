# Identity Based Encryption Demo

## Goal
Through this repository we aim to show a demo of an encryption algorithm that uses Identity Based Encryption as the key exchange algorithm and them communicate between the sockets using that as the key.

## Breakdown:
1. An IBE authority is set up.
2. Each user connects to the authority and gets its private key.
3. The key is passed to the user using TLS.
4. The users can then use the PORT number of the other user as public key and the send and recieve data from each other.
   

## Todo:
- [] Create TLS connection between two servers.
- [] Setup the authority..
- [] create encryption and decryption algorithms
- [] communicate within users