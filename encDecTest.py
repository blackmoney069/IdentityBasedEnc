import core.authorityRoles as authorityRoles
import random
import core.tools as tools
import core.encryptionScheme as encryption
import core.decryption as decryption

# Authority Parameters
# authority_MPK = 713
# auth_P = 31
# auth_P = 23

auth = authorityRoles.Authority()
authority_MPK, auth_P, auth_Q = auth.send_MPK()
print("P-Q test", auth_P*auth_Q==authority_MPK)

# Reciever Parameters
identity = "bains"
hashed_id =  tools.hashIdentity(identity, authority_MPK)
sec_key = auth.keyGeneration(identity)


test_int = random.getrandbits(8)
bit_sequence = (bin(test_int)[2:]).zfill(8)
print("To be encrypted:", bit_sequence, test_int)

arr = encryption.encrypt(bit_sequence, authority_MPK, hashed_id)
# print(arr)

decrypted_seq = decryption.decrypt_sequence(arr, sec_key, hashed_id, authority_MPK)

print("The sequence decrypted is", decrypted_seq, int(decrypted_seq, 2))






