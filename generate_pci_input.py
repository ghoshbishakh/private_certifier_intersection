#!/usr/bin/env python
# encoding:UTF-8
"""
Implement the ElGamal Digital Signature Scheme.
Algorithm
Key Generation
1. Select a large random prime p and a generator α of Z∗p.
2. Generate a random integer x such that 1≤x≤p−2. 
3. Compute y = α**x mod p.
4. A’s public key is (p, α, y).
5. A’s private key is x.
Signature Generation
A generates a signature for a message m (0 ≤ m < p−1) as follows:
1. Generatea random integer k such that 1≤k≤p−2 and gcd(k,p−1)=1.
2. Compute r = α**k mod p.
3. Compute k**−1 mod (p − 1).
4. Computes=k**−1(m−xr)mod(p−1). 
5. A’s signature for m is the pair (r, s),
Signature Verification
A signature (r, s) produced by A can be verified as follows:
1. Verify that 1 ≤ r ≤ (p−1); if not return False.
2. Compute v1 = (y**r)(r**s) mod p. 
3. Compute v2 = α**m mod p. 
4. Return v1 = v2.
"""
import Crypto.Util.number as num
import random
import p3_pair

def egKey(s, p ,g):
    # p,g = p3_pair.pair(s)
    x = random.randint(1, p-2)
    y = pow(g,x,p)
    return p, g, x, y

""" Signature Generation 
"""
def egGen(p, g, x, m):
    while 1:
        k = random.randint(1,p-2)
        if num.GCD(k,p-1)==1: break
    r = pow(g,k,p)
    l = num.inverse(k, p-1)
    s = l*(m-x*r)%(p-1)
    return r,s

""" Signature Verification 
"""
def egVer(p, g,	y, r, s, m):
    if r < 1 or r > p-1 : return False
    v1 = pow(y,r,p)%p * pow(r,s,p)%p
    v2 = pow(g,m,p)
    return v1 == v2


def get_bin(x, n):
    res = list(format(x, 'b').zfill(n))
    res = [int(a) for a in res]
    res.reverse()
    return res

#####################################################################
# Tests

if __name__ == "__main__":
    N = 128

    # assume size of b set is less
    a = 20
    b = 20

    common = 2


    # Trust anchor generating signatures for party a

    # select prime and generator
    p,g = p3_pair.pair(N - 1)


    puba = []
    pria = []
    rr = []
    ss = []
    message = 99

    g_raised_m = pow(g, message, p)

    for i in range(a):
        prime, gen, private, public = egKey(N-1, p, g) # it gives safe prime from N bit prime as 2N + 1
        print "prime,gen,private,public", prime,gen,private,public

        puba.append(public)
        pria.append(private)

        print "Message: ", message


        rri, ssi = egGen(prime,gen,private, message)
        rr.append(rri)
        ss.append(ssi)

        isValid = egVer(prime, gen, public, rr[i], ss[i], message)
        print "Valid Signature: " ,  isValid

    print("-------------------------")
    print "rr", ss
    print "ss", ss
    print("==========================================================")


    # Signatures are received by the Holder, it computes
    pub_a_raised_r = []
    s_a_vals = []
    s_a_strs = []
    r_a_stars = []
    r_a_star_strs = []
    for i in range(a):
        pub_a_raised_r.append(pow(puba[i], rr[i], p))
    
        s_a_vals.append(get_bin(ss[i], N))
        s_a_str = [ str(x) for x in s_a_vals[i] ]
        s_a_strs.append(" ".join(s_a_str))

        r_a_star = [ pow(rr[i], (2**x), p) for  x in range(N) ]
        r_a_stars.append(r_a_star)
        
        r_a_star_str = [ str(x) for x in r_a_star ]
        r_a_star_strs.append(" ".join(r_a_star_str))

    print(s_a_strs)
    print(r_a_star_strs)
    # public input by A are -------->
    # prime, gen, r_a_star
    # private input by A are ---->
    # pub_a_raised_r, s_a

    print("======= Public Inputs  {prime} {generator} {g_raised_m} {a} {b} {r_a_stars} ==============")
    public_input = "{prime} {generator} {g_raised_m} {a} {b} {message} {r_a_stars}".format(prime=p, generator=g, g_raised_m=g_raised_m, a=a, b=b, message=message, r_a_stars=" ".join(r_a_star_strs))
    print(public_input)

    with open("Programs/Public-Input/tanegotiation", "w") as f:
        f.write(public_input)
    
    print("======= Private Inputs by A ==============")
    public_input_input_a = "{pub_a} {pub_a_raised_r} {s_a}".format(pub_a=" ".join([str(x) for x in puba]), pub_a_raised_r=" ".join([str(x) for x in pub_a_raised_r]), s_a=" ".join(s_a_strs))
    print(public_input_input_a)
    with open("Player-Data/Input-P0-0", "w") as f:
        f.write(public_input_input_a)

    print("-----------------------------------------")

    # B receives r_a_i values, and computes pub_b^r_a_i
    pubb = puba[:b] # NEED TO CHANGE IT BY RANDOMLY SAMPLING c ELEMENTS FROM puba and generating rest

    # CHANGING SECOND ELEMENT
    prime, gen, private, public = egKey(N-1, p, g) # it gives safe prime from N bit prime as 2N + 1
    pubb[1] = public

    if(a < b):
        for i in range(b-a):
            prime, gen, private, public = egKey(N-1, p, g) # it gives safe prime from N bit prime as 2N + 1
            pubb.append(public)
    

    pub_b_raised_r = []

    for ia in range(a):
        for ib in range(b):
            pub_b_raised_r.append(str(pow(pubb[ib], rr[ia], p)))
            # print(ia,ib)
            # print(pub_a_raised_r[ia], str(pow(pubb[ib], rr[ia], p)))


    print("======= Private Inputs by B ==============")
    public_input_input_a = "{pub_b_raised_r}".format(pub_b_raised_r=" ".join(pub_b_raised_r))
    print(public_input_input_a)
    print("-----------------------------------------")
    with open("Player-Data/Input-P1-0", "w") as f:
        f.write(public_input_input_a)

    print(p)
    # print("-------------------------")
    # # Tests
    # print("r^s = ", pow(rr, ss, prime) )
    
    # print(r_a_star)
    # res = 1
    # for b in range(N):
    #     res = res * ((int(s_a[b]) * r_a_star[b]) + (1 - int(s_a[b]))) % prime
    # print(res)
