import core.tools as tools
a = 196     # hash ID
r = 262     # Root for the user with ID string = "bains"
n = 713     # MPK of the authority
p = 31      # secret parameter p of auth
q = 23      # secret parameter q of auth



t1 = 666455     #parameters t1 and t2 chosen at random
t2 = 258038

print( "3 mod 4 test", p%4==3 and q%4==3)
print("Jacobi test",tools.jacobi_symbol(t1,n), tools.jacobi_symbol(t2,n) )
print(tools.jacobi_symbol(a,n))

print("modInverse test", tools.mod_inverse(t1, n), tools.mod_inverse(t2, n))

c1 = (t1 + (a * tools.mod_inverse(t1, n)))%n
c2 =  (t2 - (a * tools.mod_inverse(t2, n)))%n
print("c1 value",c1 )
print("c2 value",c2 )

print("alpha values", c1+2*r, c2+2*r)
print("output bit", tools.jacobi_symbol(c1+2*r, n), tools.jacobi_symbol(c2+2*r, n))