import argparse
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from data_for_satellites import data as ds

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="KMeans Clustering for Satellite Data")
parser.add_argument('--clusters', type=int, default=3,
                    help='Number of clusters for KMeans')
args = parser.parse_args()

# Satellite data as a dictionary
data = ds

# Convert to DataFrame
df = pd.DataFrame.from_dict(data, orient='index')

# Apply KMeans
kmeans = KMeans(n_clusters=args.clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df)

# Visualize the clustering in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['x'], df['y'], df['z'], c=df['cluster'], cmap='viridis', s=50)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title(f'KMeans Clustering with {args.clusters} Clusters')
plt.show()
