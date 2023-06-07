import core.tools as tools
import random


def encrypt(string, MPK, ID):
    '''
    This function will return the encrypted array of tuples

    Parameter:
    string (string) : the bianry string to be encrypted (will be used as a key).
    MPK (int) :  Master public key of the authority.
    ID (int) : hashed identity of the reciever .

    Returns:
    a list of tuples that have the c1,c2 pair of each bit
    '''
    output = []
    for i in string:
        t1 = None
        t2 = None
        if (i == "1"):
            while (True):
                t1 = random.randint(0, 999999)
                jacobi1 = tools.jacobi_symbol(t1, MPK)
                if (jacobi1 == 1):
                    break
            while (True):
                t2 = random.randint(0, 999999)
                jacobi2 = tools.jacobi_symbol(t2, MPK)
                if (jacobi2 == 1 and t1 != t2):
                    break
        else:
            while (True):
                t1 = random.randint(0, 999999)
                jacobi1 = tools.jacobi_symbol(t1, MPK)
                if (jacobi1 == -1):
                    break
            while (True):
                t2 = random.randint(0, 999999)
                jacobi2 = tools.jacobi_symbol(t2, MPK)
                if (jacobi2 == -1 and t1 != t2):
                    break

        c1 = (t1 + (ID * tools.mod_inverse(t1, MPK)))%MPK
        c2 = (t2 - (ID * tools.mod_inverse(t2, MPK)))%MPK
        output.append((c1, c2))
    return output


if __name__ == "__main__":
    f = open("testcase.json")
    # test_case = json.load(f)
    # print(encrypt(input_string, test_case['params']['authority']["MPK"], test_case['params']['reciever']["ID"] ))
    print(encrypt('101', 56970261955253, 28877774692113))
