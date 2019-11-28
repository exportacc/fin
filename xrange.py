def xrange(stop,start,step):
  while start < stop : 
    yield start
    start += step
    
# %timeit xrange 
