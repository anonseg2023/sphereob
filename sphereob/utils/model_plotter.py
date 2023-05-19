
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt


#define Matplotlib figure and axis
fig, ax = plt.subplots()

#create simple line plot

#add rectangle to plot
#ax.add_patch(Rectangle((0, 0), 1, 1))


#                          depth    thick
ax.add_patch(Rectangle((0, 0), 1, 1, color="black"))
ax.add_patch(Rectangle((0, 0.8), 1, 0.2, color="grey"))
#ax.add_patch(plt.Circle((0.5, 0.5), 0.1, color='grey'))
ax.add_patch(Rectangle((0.3, 0.3), .4, 0.05,angle=360, color="grey"))
plt.axis('off')

#display
plt.show()