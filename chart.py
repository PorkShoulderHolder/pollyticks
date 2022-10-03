
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
df = pd.read_csv("county_income.csv", sep=',')

income = df[df.LineCode == 3]
population = df[df.LineCode == 2]


results = pd.read_json("election_results.json")
density = pd.read_csv("Population-Density-By-County.csv")

merged = pd.merge(results, income, left_on='fips', right_on='GeoFips')
merged["income_per_capita"] = pd.to_numeric(merged['2019'], errors='coerce')

population["population"] = pd.to_numeric(population['2019'], errors='coerce')
merged = pd.merge(merged, population, left_on='fips', right_on='GeoFips')

merged = pd.merge(merged, density, left_on='fips', right_on='GCT_STUB.target-geo-id2')

sns.set(style = "darkgrid")

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')


ax.set_xlabel("population density")
ax.set_ylabel("income per capita")
ax.set_zlabel("biden support")

ax.scatter(merged.population, merged.income_per_capita, merged.biden_support)

plt.show()
import plotly.express as px
df = pd.DataFrame()
axes = [ 'income_per_capita', 'biden_support', 'Density per square mile of land area']
for i, c in enumerate(axes):
    df[c] = merged[c]
print(df)
fig = px.scatter_3d(df, x=axes[0], y=axes[1], z = axes[2])
fig.update_traces(marker_size=1)
fig.show()
