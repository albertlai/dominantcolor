#!/usr/bin/env python

import operator
import logging
from sys import maxint
from random import randint

def distance(a, b):
    """ Get the distance between two vectors a and b """
    sum = 0
    if len(a) == len(b):
        for i, a_i in enumerate(a):
            diff = a_i - b[i]
            sum += diff * diff
        return sum
    return 0


def bucketize(means, data, n):
    """ Cluster the data around the means. Vectors are of length n"""
    num_pixels = len(data) / n
    k = len(means) / n
    sums = [0 for i in range(len(means))]
    counts = [0 for i in range(k)]
    logging.debug("Bucketize %d %d" % (num_pixels, k))
    for i in range(num_pixels):
        offset = i * n
        pixel = data[offset : offset + n]
        j_m = 0
        smallest_d = maxint
        # Find the closest mean
        for j in range(k):
            m = j * n
            d = distance(pixel, means[m : m + n])
            if d < smallest_d:
                j_m = j
                smallest_d = d
        counts[j_m] += 1
        m = j_m * n
        # Add the pixel to the running count for that mean's cluster
        sums[m : m + n] = map(operator.add, sums[m : m + n], pixel)
    # Find the new average for all the data points in each cluster
    means = [x / (counts[i / n]) for i, x in enumerate(sums)]
    counts = counts
    return (means, counts)


def kmeans(k, data, n, max, t):
    """ Run k means on some data with vector length n with max value mac 
        and convergence threshold t""" 
    # Initialize the means list randomly
    new_means = [randint(0, max) for i in range(k * n)]
    means = [max * 2 for i in range(len(new_means))]
    safety = 0
    # Run until means converge or we run this too many times
    while distance(means, new_means) > t and safety < 1000:
        means = new_means
        (new_means, counts) = bucketize(means, data, n)
        safety += 1
    return (new_means, counts)
