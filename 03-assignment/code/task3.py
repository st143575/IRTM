import numpy as np
import matplotlib.pyplot as plt

#data
precision_list = np.array([1.0, 0.5, 0.33, 0.5, 0.4, 0.33, 0.43, 0.5])
precision2_list = precision_list.copy()
recall_list = np.array([0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.6, 0.8])
i=recall_list.shape[0]-2

# interpolation...
while i>=0:
    if precision_list[i+1]>precision_list[i]:
        precision_list[i]=precision_list[i+1]
    i=i-1

# plotting...
fig, ax = plt.subplots()
for i in range(recall_list.shape[0]-1):
    ax.plot((recall_list[i],recall_list[i]),(precision_list[i],precision_list[i+1]),'k-',label='',color='red') #vertical
    ax.plot((recall_list[i],recall_list[i+1]),(precision_list[i+1],precision_list[i+1]),'k-',label='',color='red') #horizontal

ax.plot(recall_list, precision2_list,'k--',color='blue')

plt.axis([0, 0.9, 0, 1.0])

plt.xlabel('Recall')
plt.ylabel('Precision')

plt.savefig('Assignment3/img/fig.jpg')
