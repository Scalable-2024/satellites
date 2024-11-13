from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from data_for_satellites import data as ds
# Satellite data as a dictionary
data = ds
# Convert to DataFrame
df = pd.DataFrame.from_dict(data, orient='index')

# Number of clusters
k = 3  # You can change this

# Apply KMeans
kmeans = KMeans(n_clusters=k, random_state=42)
df['cluster'] = kmeans.fit_predict(df)

# Visualize the clustering in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['x'], df['y'], df['z'], c=df['cluster'], cmap='viridis', s=50)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
