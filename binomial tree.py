def xrange(stop,start=0,step=1):
    while start < stop :
        yield start
        start += step
    
def binomialCallEuropean(s,k,T,r,q,sigma,n,call=True,style='digital'):
    import numpy as np
    from math import exp,sqrt 
    dt = T /n
    n = n+1
    u = exp(sigma * sqrt(dt))
    d = 1.0 / u
    p = (exp((r-q) * dt) - d) / (u - d)
    v = np.zeros(n*n).reshape(n,n)  # bulid init matrix (zeros) 
    
    # bulid stock price
    for i in xrange(n):
        for j in xrange(n):
            if i >= j : 
                v[j,i] = u**(i-j) * (d**j) * s
            else : 
                v[j,i] = 0.0
    
    print('stock price tree :\n {}'.format(np.round(v,2)))
    print('\n')
    # fix last shape problem  
    if call is True : 
        if style == 'digital':
            v[:,-1] = np.where(v[:,-1]-k>0,1,0)
        else :
            v[:,-1] = np.where(v[:,-1]-k>0,v[:,-1]-k,0) # European call 
    else :
        if style == 'digital':
            v[:,-1] = np.where(v[:,-1]-k>0,1,0)
        else :
            v[:,-1] = np.where(k-v[:,-1]>0,k-v[:,-1],0) # European put
    
    for i in range(n,0,-1):
        for j in range(n,0,-1):
            if i <= j and i-2 >= 0:
                v[i-2,j-2] = exp(-r * dt) * ((1-p) * v[i-1,j-1] + p * v[i-2,j-1])
                
    print('premium :')
    return np.round(v,4)

'''
# s,k,T,r,q,sigma,n,call=True
print((binomialCallEuropean(25.95,26.2,0.25,0.04,0.03,0.05,5)))

stock price tree :
 [[25.95 26.24 26.54 26.84 27.14 27.44]
 [ 0.   25.66 25.95 26.24 26.54 26.84]
 [ 0.    0.   25.38 25.66 25.95 26.24]
 [ 0.    0.    0.   25.09 25.38 25.66]
 [ 0.    0.    0.    0.   24.82 25.09]
 [ 0.    0.    0.    0.    0.   24.54]]


premium :
[[0.5313 0.7106 0.8838 0.996  0.998  1.    ]
 [0.     0.3397 0.5262 0.7661 0.998  1.    ]
 [0.     0.     0.1394 0.2689 0.5185 1.    ]
 [0.     0.     0.     0.     0.     0.    ]
 [0.     0.     0.     0.     0.     0.    ]
 [0.     0.     0.     0.     0.     0.    ]]
'''
