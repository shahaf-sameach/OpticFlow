import numpy as np

def dist(mat_a, mat_b):
	distance = (mat_a - mat_b)**2
	distance = np.sum(distance, axis=1)
	distance = np.sqrt(distance)
	return np.mean(distance)

