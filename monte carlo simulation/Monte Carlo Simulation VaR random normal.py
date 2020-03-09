#!/usr/bin/env python
# coding: utf-8

# In[97]:


import pandas as pd
from pandas_datareader import data
from scipy.stats import norm 
import numpy as np


# In[113]:


class VaR():
    '''
    Data format must be DataFrame
    '''
    import pandas as pd
    import numpy as np
    from math import sqrt
    
    def __init__(self,datas):
        self.datas = datas
    
    def DailyReturn(self):
        return self.datas.diff()/self.datas.shift(1)
    
    def Log_Return(self):
        return np.log(self.datas/self.datas.shift(1))
    
    def cholesky(self,A):
        """Performs a Cholesky decomposition of A, which must 
        be a symmetric and positive definite matrix. The function
        returns the lower variant triangular matrix, L."""
        n = len(A)

        # Create zero matrix for L
        L = [[0.0] * n for i in range(n)]

        # Perform the Cholesky decomposition
        for i in range(n):
            for k in range(i+1):
                tmp_sum = sum(L[i][j] * L[k][j] for j in range(k))

                if (i == k): # Diagonal elements
                    L[i][k] = np.sqrt(A[i][i] - tmp_sum)
                else:
                    L[i][k] = (1.0 / L[k][k] * (A[i][k] - tmp_sum))
        return np.asarray(L).reshape(n,n)
    
class Monte(VaR):
    '''
    不用特意定義 __init__ 系統會繼承
    '''
    def correlation(self,num):
        '''
        '''
        return np.asarray((num).corr())
    
    def returns(self,mu,sd,delta_t,random):
        a = (mu - (sd**2) /2 )* delta_t
        b = sd * np.sqrt(delta_t) * random
        return (np.exp( a + b) - 1)


# In[99]:


tickers = ['2330.tw', '2882.tw', '2317.tw']
start_date = '2010-01-01'
end_date = '2012-12-31'
number = 5000

t2330 = data.DataReader(tickers[0],'yahoo', start_date, end_date)['Close']
t2882 = data.DataReader(tickers[1],'yahoo', start_date, end_date)['Close']
t2317 = data.DataReader(tickers[2],'yahoo', start_date, end_date)['Close']

df = pd.concat([t2330,t2882,t2317],axis=1)
df.columns =['2330.tw', '2882.tw', '2317.tw']


# In[114]:


method = Monte(df)
r = method.Log_Return()
mu = r.mean()
std = r.std()


# In[107]:


random_normal = np.random.normal(size=number*3).reshape(-1,3)


# In[117]:


corr = method.correlation(r)

cholesky_l = method.cholesky(corr)

corr_random = [ cholesky_l @ random_normal[num,:].T for num in range(len(random_normal))] 


# In[119]:


random_num = pd.DataFrame({
  '2330' : np.asarray(corr_random)[:,0] ,
  '2882' : np.asarray(corr_random)[:,1] ,
  '2317' : np.asarray(corr_random)[:,2] 
})


# In[120]:


mu2330 = np.asarray(mu)[0]
mu2882 = np.asarray(mu)[1]
mu2317 = np.asarray(mu)[2]

std2330 = np.asarray(std)[0]
std2882 = np.asarray(std)[1]
std2317 = np.asarray(std)[2]


# In[124]:


delta_t = 1/250
df = pd.DataFrame({
    '2330' : method.returns(mu2330,std2330,delta_t,random_num['2330']),
    '2882' : method.returns(mu2882,std2882,delta_t,random_num['2882']),
    '2317' : method.returns(mu2317,std2317,delta_t,random_num['2317'])
})


# In[122]:


df['portfolio'] = (df * (0.1527828,0.1858858,0.6613314)).sum(axis=1)

ff = pd.DataFrame()
for i in df.columns :
    ff[i] = np.asarray(df[i].sort_values(ascending=True)) 

var_data =ff * (42000 , 51100 , 181800 , 274900)

var_data


# In[123]:


var_data.quantile(0.025)

