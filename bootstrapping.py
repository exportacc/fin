def bootsrapping(target , fre):
    '''
    target : data 
        - index (time : float)
        - zero rate (initialization is zero)
    fre : frequency
    --------------------
    st : start bootstrap
    
    '''
    st = target.index[target['index'] < 1][-1] + 1
    for per in xrange(st,target.shape[0]):
        s = np.zeros(per-1)
        for num in xrange(1,per+1):
            if num != per: 
                s[num-1] = 1/np.power((1 + target['zero rate'][num]/fre),fre*target['index'][num])  
            elif num == per :
                bottom = 1 - ((target['price'][per]/fre)*np.sum(s))
                top = (1 + target['price'][per]/fre)
                target['zero rate'][per] = (np.power(top/bottom,1/per)-1)*fre
