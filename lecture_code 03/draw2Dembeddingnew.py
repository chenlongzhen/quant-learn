import tushare as ts
import pandas as pd

def getStockVar(stockId,start,end,ktype='D'):
    '''
    get stock close - open
    :param stockId: 
    :param start: 
    :param end: 
    :param ktype: 
    :return:
     pd.series
    '''
    data = ts.get_hist_data(stockId)
    assert  len(data) > 100
    openData = data['open']
    closeData = data['close']
    var = closeData - openData
    return var



def getDiff(stockList):
    '''
    get var DataFrame
    :param stockList: 
    :return:
     date - stoclid , DataFrame
    '''
    seriesList = []
    colNames = []
    for sid in stockList:
        print("getting {}".format(sid))
        try:
            var = getStockVar(sid, '2016-10-01','2017-10-01')
            #print(var)
            seriesList.append(var)
            colNames.append(sid)
        except:
            print("getting {} failed. pass.".format(sid))
    df = pd.concat(seriesList, axis=1)
    df.columns = colNames
    return df

stockAllId=ts.get_stock_basics().index
varData = getDiff(stockAllId)
varData = varData.fillna(varData.mean())
names = varData.columns

# save it
varData.to_csv("../data/all_var.csv")
#names = varData.columns
#varData = pd.read_csv("../data/all_var.csv")
#names = varData.columns

from sklearn import covariance, cluster
x = varData/varData.std(axis=0)
print("data finished")

edge_model = covariance.GraphLassoCV()
edge_model.fit(x)
centers, labels = cluster.affinity_propagation(edge_model.covariance_)
n_labels = labels.max()

for i in range(n_labels + 1):
    print('Cluster %i: %s' % ((i + 1), ', '.join(names[labels == i])))

print("cluster finished")


# #############################################################################
# Find a low-dimension embedding for visualization: find the best position of
# the nodes (the stocks) on a 2D plane

# We use a dense eigen_solver to achieve reproducibility (arpack is
# initiated with random vectors that we don't control). In addition, we
# use a large number of neighbors to capture the large-scale structure.
from sklearn import cluster, covariance, manifold
node_position_model = manifold.LocallyLinearEmbedding(
    n_components=2, eigen_solver='dense', n_neighbors=6)

embedding = node_position_model.fit_transform(x.T).T
print("embedding finished")


#print embedding



# #############################################################################
# Visualization
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
plt.figure(1, facecolor='w', figsize=(10, 8))
plt.clf()
ax = plt.axes([0., 0., 1., 1.])
plt.axis('off')

# Display a graph of the partial correlations
partial_correlations = edge_model.precision_.copy()
d = 1 / np.sqrt(np.diag(partial_correlations))
partial_correlations *= d
partial_correlations *= d[:, np.newaxis]
non_zero = (np.abs(np.triu(partial_correlations, k=1)) > 0.02)

# Plot the nodes using the coordinates of our embedding
plt.scatter(embedding[0], embedding[1], s=100 * d ** 2, c=labels,
            cmap=plt.cm.spectral)

# Plot the edges
start_idx, end_idx = np.where(non_zero)
# a sequence of (*line0*, *line1*, *line2*), where::
#            linen = (x0, y0), (x1, y1), ... (xm, ym)
segments = [[embedding[:, start], embedding[:, stop]]
            for start, stop in zip(start_idx, end_idx)]
values = np.abs(partial_correlations[non_zero])
lc = LineCollection(segments,
                    zorder=0, cmap=plt.cm.hot_r,
                    norm=plt.Normalize(0, .7 * values.max()))
lc.set_array(values)
lc.set_linewidths(15 * values)
ax.add_collection(lc)

# Add a label to each node. The challenge here is that we want to
# position the labels to avoid overlap with other labels
for index, (name, label, (x, y)) in enumerate(
        zip(names, labels, embedding.T)):

    dx = x - embedding[0]
    dx[index] = 1
    dy = y - embedding[1]
    dy[index] = 1
    this_dx = dx[np.argmin(np.abs(dy))]
    this_dy = dy[np.argmin(np.abs(dx))]
    if this_dx > 0:
        horizontalalignment = 'left'
        x = x + .002
    else:
        horizontalalignment = 'right'
        x = x - .002
    if this_dy > 0:
        verticalalignment = 'bottom'
        y = y + .002
    else:
        verticalalignment = 'top'
        y = y - .002
    plt.text(x, y, name, size=10,
             horizontalalignment=horizontalalignment,
             verticalalignment=verticalalignment,
             bbox=dict(facecolor='w',
                       edgecolor=plt.cm.spectral(label / float(n_labels)),
                       alpha=.6))

plt.xlim(embedding[0].min() - .15 * embedding[0].ptp(),
         embedding[0].max() + .10 * embedding[0].ptp(),)
plt.ylim(embedding[1].min() - .03 * embedding[1].ptp(),
         embedding[1].max() + .03 * embedding[1].ptp())

plt.show()
plt.savefig('../data/test.png')
