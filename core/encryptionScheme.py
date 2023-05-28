import core.tools as tools
import random


def mod_inverse(a, m):
    """
    Calculates the modular inverse of a modulo m.

    Parameters:
    a (int): The number to calculate the inverse of.
    m (int): The modulus.

    Returns:
    The modular inverse of a modulo m, or None if it does not exist.
    """
    # Check if gcd(a, m) = 1, otherwise the inverse does not exist
    gcd, x, y = extended_euclidean_algorithm(a, m)
    if gcd != 1:
        return None

    # Calculate the inverse using the extended Euclidean algorithm
    return (x % m + m) % m


def extended_euclidean_algorithm(a, b):
    """
    Calculates the greatest common divisor (gcd) of a and b, as well as the
    Bezout coefficients x and y such that ax + by = gcd(a, b).

    Parameters:
    a (int): The first number.
    b (int): The second number.

    Returns:
    A tuple (gcd, x, y) such that ax + by = gcd(a, b).
    """
    # Base case
    if a == 0:
        return (b, 0, 1)

    # Recursive call
    gcd, x1, y1 = extended_euclidean_algorithm(b % a, a)

    # Calculate the Bezout coefficients
    x = y1 - (b // a) * x1
    y = x1

    return (gcd, x, y)


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
                t2 = random.randint(0, 999999)
                jacobi2 = tools.jacobi_symbol(t2, MPK)
                if (jacobi1 == 1 and jacobi2 == 1 and t1 != t2):
                    break
        else:
            while (True):
                t1 = random.randint(0, 999999)
                jacobi1 = tools.jacobi_symbol(t1, MPK)
                t2 = random.randint(0, 999999)
                jacobi2 = tools.jacobi_symbol(t2, MPK)
                if (jacobi1 == -1 and jacobi2 == -1 and t1 != t2):
                    break

        c1 = (t1 + ID * mod_inverse(t1, MPK)) % MPK
        c2 = (t2 - ID * mod_inverse(t1, MPK)) % MPK
        output.append((c1, c2))
    return output


if __name__ == "__main__":
    f = open("testcase.json")
    # test_case = json.load(f)
    # print(encrypt(input_string, test_case['params']['authority']["MPK"], test_case['params']['reciever']["ID"] ))
    print(encrypt('101', 56970261955253, 28877774692113))
