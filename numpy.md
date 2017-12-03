If you’re multiplying a 3x2 matrix by a 2x1 matrix…
* The two inner numbers must match (columns of first = 2, rows of second =2)
* The matrix produced will have dimensions equal to the outer numbers (rows of the first = 3, columns of the second = 1); you get a 3x1 matrix!

Types of indexing:
* Basic list indexing - (start, stop, step)
* Matrix indexing - (rows, columns)
* You can use basic indexing within your row and/or column indexing, e.g., (start:stop:step, start:stop:step)

np.linspace - (start, stop, number of values)
np.arange - (start, stop, step/spacing between values)
