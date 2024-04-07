"""
In this assignment you should fit a model function of your choice to data 
that you sample from a given function. 

The sampled data is very noisy so you should minimize the mean least squares 
between the model you fit and the data points you sample.  

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You 
must make sure that the fitting function returns at most 5 seconds after the 
allowed running time elapses. If you take an iterative approach and know that 
your iterations may take more than 1-2 seconds break out of any optimization 
loops you have ahead of time.

Note: You are NOT allowed to use any numeric optimization libraries and tools 
for solving this assignment. 

"""

import numpy as np
import time
import random


class Assignment4:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def fit(self, f: callable, a: float, b: float, d:int, maxtime: float) -> callable:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape. 
        
        Parameters
        ----------
        f : callable. 
            A function which returns an approximate (noisy) Y value given X. 
        a: float
            Start of the fitting range
        b: float
            End of the fitting range
        d: int 
            The expected degree of a polynomial matching f
        maxtime : float
            This function returns after at most maxtime seconds. 

        Returns
        -------
        a function:float->float that fits f between a and b
        """


        start = time.time()
        num_smpls = 0
        sections = np.linspace(a, b, 150) # split into sections
        xs = np.zeros(len(sections)) # x values array
        ys = np.zeros(len(sections)) # y values array
        while (time.time() - start) < (maxtime/3): # take samples third of the time
            num_smpls += 1
            for i in range(len(sections) - 1):
                xrndm = random.uniform(sections[i], sections[i] + (b - a) / 150) # take a random sample in the section
                xs[i] += xrndm
                ys[i] += f(xrndm)

        for i in range(len(xs)): # calculates the average
            xs[i] = xs[i] / num_smpls
            ys[i] = ys[i] / num_smpls

        f_list = []
        for i in range(len(xs) - 1): # make a line
            if (xs[i + 1] == xs[i]) : #devisio by 0
                continue
            m = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])
            c = (xs[i + 1] * ys[i] - xs[i] * ys[i + 1]) / (xs[i + 1] - xs[i])
            f_list.append(poly(m, c)) # add the function to the function list

        def g(num): # create the function
            pos = 0
            while xs[pos + 1] < num and pos < len(f_list) - 1:
                pos += 1
            return f_list[pos](num)

        return g



##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment4(unittest.TestCase):

    def test_return(self):
        f = NOISY(0.01)(poly(1,1,1))
        ass4 = Assignment4()
        T = time.time()
        shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        self.assertLessEqual(T, 5)

    # def test_delay(self):
    #     f = DELAYED(7)(NOISY(0.01)(poly(1,1,1)))
    #
    #     ass4 = Assignment4()
    #     T = time.time()
    #     shape = ass4.fit(f=f, a=0, b=1, d=10, maxtime=5)
    #     T = time.time() - T
    #     self.assertGreaterEqual(T, 5)

    def test_err(self):
        f = poly(1,1,1)
        nf = NOISY(1)(f)
        ass4 = Assignment4()
        T = time.time()
        ff = ass4.fit(f=nf, a=0, b=1, d=10, maxtime=5)
        T = time.time() - T
        mse=0
        for x in np.linspace(0,1,1000):            
            self.assertNotEquals(f(x), nf(x))
            mse+= (f(x)-ff(x))**2
        mse = mse/1000
        print(mse)

        
        



if __name__ == "__main__":
    unittest.main()
