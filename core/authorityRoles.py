import random
import core.tools as tools
import json

def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

class Authority:
    def __init__(self):
        '''
        Function to setup the authority and define the public and private variables
        '''
        self._P = None
        self._Q = None
        self.MPK = None
        while(True): 
            p = random.randint(1000000,9999999)
            if(p%4==3) and (is_prime(n=p)):
                break
        
        # Change: different loops for p and q choosing
        while(True):
            q = random.randint(1000000,9999999)
            if q%4==3 and is_prime(n=q):
                break
        self._P = p
        self._Q = q
        self.MPK = p*q

    
    def send_MPK(self):
        '''
        Return the value of M to anyone accessing the Authority
        '''
        return self.MPK
    # ToDo: remove _P and _Q from return statement, only for testing purpose

    
    def keyGeneration(self, identity_string):
        '''
        This will calculate the value of a such that the jacobi of a is 1 and a represents the identity string

        Parameters:
            identity_string (string): provided to the authority to generate a private key for the user

        Returns:
            r (int): secret key for the user
        '''
        a = tools.hashIdentity(identity_string, self.MPK)%self.MPK
        r = pow(a,(self.MPK+5-self._P-self._Q)//8, self.MPK)

        # print("R Square Test-", (r**2%self.MPK == a%self.MPK))
        # print("R Square Test-", (r**2%self.MPK == -a%self.MPK))
        return r
    

def rootVerification(MPK, r, identity_string):
        '''
        This is the function that will verify if the roots provided to the user are correct

        Parameters:
            MPK (int): the master public key of the authority
            r (int) : the secret root provided to the user
            identity_string (string) : a string that contains the identity of the user

        Returns:
            boolean if the roots provided are correct
        '''
        a = tools.hashIdentity(identity_string, MPK)
        if(r**2%MPK == a%MPK):
            print("positive correct")
        elif(r**2%MPK == -a%MPK):
            print("negative correct")
        else:
            print("Not correct") 

if __name__ == "__main__":
    auth = Authority()
    MPK = auth.send_MPK()
    r = auth.keyGeneration('bains')
    rootVerification(MPK, r, identity_string='bains')
