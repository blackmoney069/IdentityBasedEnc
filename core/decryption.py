import core.tools as tools


def decryption(s,r, ID, MPK):
    '''
    A function to decrypt a ciphertext.

    Parameter:
    s (pair<int>) : cipher text to be decrypted
    r (int) : secret key of the reciever
    ID (int) : the hash of the identity of the reciever
    MPK (int) : master public key of the authority

    Returns:
    M (bit): one or zero decrypted bit
    '''

    if r**2%MPK == ID%MPK:
        alpha = s[0] + 2*r
    else:
        alpha = s[1] + 2*r
    return tools.jacobi_symbol(alpha, MPK)


def decrypt_sequence(s,r, ID, MPK):
    '''
    A function to decrypt a ciphertext.

    Parameter:
    s (list of pair<int>) : list of cipher texts to be decrypted
    r (int) : secret key of the reciever
    ID (int) : the hash of the identity of the reciever
    MPK (int) : master public key of the authority

    Returns:
    M (string): string of one or zero decrypted bits
    '''
    output = ""
    for i in s:
        if r**2%MPK == ID%MPK:
            alpha = i[0] + 2*r
        else:
            alpha = i[1] + 2*r
        res = tools.jacobi_symbol(alpha, MPK)
        if(res==1):
            output+="1"
        else:
            output+="0"
    
    return output



if __name__ =="__main__":

    f = open("testcase.json")
    #test case included in json format

    input = eval("[(53199093286327, 3771170403324), (40924870912374, 16045392377559), (18703193682098, 38267069731397)]")
     
    first_bit = decrypt_sequence(input,38041879909636, 28877774692113, 56970261955253)
    # first_bit = decrypt_sequence(input,test_case["params"]["reciever"]['r'], test_case["params"]["reciever"]['ID'], test_case["params"]["authority"]['MPK'])
    print(first_bit)
