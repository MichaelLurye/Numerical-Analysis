"""
In this assignment you should fit a model function of your choice to data 
that you sample from a contour of given shape. Then you should calculate
the area of that shape. 

The sampled data is very noisy so you should minimize the mean least squares 
between the model you fit and the data points you sample.  

During the testing of this assignment running time will be constrained. You
receive the maximal running time as an argument for the fitting method. You 
must make sure that the fitting function returns at most 5 seconds after the 
allowed running time elapses. If you know that your iterations may take more 
than 1-2 seconds break out of any optimization loops you have ahead of time.

Note: You are allowed to use any numeric optimization libraries and tools you want
for solving this assignment. 
Note: !!!Despite previous note, using reflection to check for the parameters 
of the sampled function is considered cheating!!! You are only allowed to 
get (x,y) points from the given shape by calling sample(). 
"""

import numpy as np
import time
import random
import scipy
from shapely.geometry import Polygon
from sklearn.cluster import KMeans
from functionUtils import AbstractShape


class MyShape(AbstractShape):
    def __init__(self, area,contour):
        self.area1 = area
        self.contour1 = contour
    def area(self):
        return self.area1
    def contour(self,n):
        return self.contour1[:n]





class Assignment5:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before 
        solving the assignment for specific functions. 
        """

        pass

    def area(self, contour: callable, maxerr=0.001)->np.float32:

        """
        Compute the area of the shape with the given contour. 

        Parameters
        ----------
        contour : callable
            Same as AbstractShape.contour 
        maxerr : TYPE, optional
            The target error of the area computation. The default is 0.001.

        Returns
        -------
        The area of the shape.

        """
        points = contour(500) # take 500 samples
        n = len(points)
        area = 0.0
        for i in range(n): #shoelace algorithem
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[i][1] * points[j][0]
        area = abs(area) / 2.0
        return np.float32(area)

    def fit_shape(self, sample: callable, maxtime: float) -> AbstractShape:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape.

        Parameters
        ----------
        sample : callable.
            An iterable which returns a data point that is near the shape contour.
        maxtime : float
            This function returns after at most maxtime seconds.

        Returns
        -------
        An object extending AbstractShape.
        """

        # replace these lines with your solution
        start = time.time()
        points = []
        points.append(sample()) # take first sample if there is no time
        while time.time()-start < maxtime / 7: # sample 1/7 of the given time
            points.append(sample())

        K = 12
        kmeans = KMeans(n_clusters=K) # classifie the points into 12 clusters
        kmeans.fit(points)
        centers = kmeans.cluster_centers_
        centers_avg = np.mean(points, axis=0)
        angles = np.arctan2(centers[:, 1] - centers_avg[1], centers[:, 0] - centers_avg[0]) # sort the centers
        sorted_indices = np.argsort(angles)
        centers = centers[sorted_indices]

        distances = scipy.spatial.distance.cdist(centers, centers, 'euclidean') # determine the optimal order
        from scipy.optimize import linear_sum_assignment
        _, tsp_order = linear_sum_assignment(distances)
        optimal_order = np.concatenate((tsp_order, [tsp_order[0]]))
        optimal_centroids = centers[optimal_order]

        polygon = Polygon(optimal_centroids) # create a Polygon object
        return MyShape(polygon.area,points.sort())


##########################################################################


import unittest
from sampleFunctions import *
from tqdm import tqdm


class TestAssignment5(unittest.TestCase):

    def test_return(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=5)
        T = time.time() - T
        self.assertTrue(isinstance(shape, AbstractShape))
        self.assertLessEqual(T, 5)

    # def test_delay(self):
    #     circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
    #
    #     def sample():
    #         time.sleep(7)
    #         return circ()
    #
    #     ass5 = Assignment5()
    #     T = time.time()
    #     shape = ass5.fit_shape(sample=sample, maxtime=5)
    #     T = time.time() - T
    #     self.assertTrue(isinstance(shape, AbstractShape))
    #     self.assertGreaterEqual(T, 5)

    def test_circle_area(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=30)
        T = time.time() - T
        a = shape.area()
        self.assertLess(abs(a - np.pi), 0.01)
        self.assertLessEqual(T, 32)

    def test_bezier_fit(self):
        circ = noisy_circle(cx=1, cy=1, radius=1, noise=0.1)
        ass5 = Assignment5()
        T = time.time()
        shape = ass5.fit_shape(sample=circ, maxtime=30)
        T = time.time() - T
        a = shape.area()
        self.assertLess(abs(a - np.pi), 0.01)
        self.assertLessEqual(T, 32)


if __name__ == "__main__":
    unittest.main()
