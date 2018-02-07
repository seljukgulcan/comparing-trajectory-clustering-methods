# comparing-trajectory-clustering-methods

This was my pattern recognition course term project. The goal is to compare 4 clustering algorithms (k-medoids, gaussian mixture model, dbscan and hdbscan) on civil flight data. More detail can be found in report.pdf file.

![A snapshot of data](data.png)

Resulting clusters look like this:

![Resulting clusters with one method](result.png)

Trajectory segmentation is applied to reduce the number of sample points and hausdorff distance is used to compare the similarity between trajectories.

![Trajectory Segmentation](segmentation.png)

Code is a mess, I'll try to clean it up when I have time but the pdf report should be enough to get an idea.
