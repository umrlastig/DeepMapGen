import math
from skimage import color, io, data_dir, filters, morphology, measure
import matplotlib.pyplot as plt
import os
import numpy as np
import networkx as nx

file = os.path.join(data_dir, 'D:\Donnees\planignv2_1.jpg') 
map = io.imread(file)

# convert map from RGB to luminance
map_gray = color.rgb2gray(map)

# binarize the gray image
# threshold = 100
yen = filters.threshold_yen(map_gray)
binary_yen = map_gray > yen

# morphological closing the very thin artifacts
map_closed = morphology.closing(binary_yen, morphology.square(1))

# label the connected components with 8-connectivity (or 2-connectivity in skimage)
map_labeled = measure.label(map_closed, background=1, connectivity=2)

# then, compute the properties of each component
regions = measure.regionprops(map_labeled)
pruned_regions = []
total_height = 0
total_width = 0
for props in regions:
    bbox = props.bbox
    # compute the ratio of black pixels in the bounding box of the given region
    nb_black = 0
    nb_pixels = 0
    for i in range(bbox[0],bbox[2]):
        for j in range(bbox[1],bbox[3]):
            nb_pixels += 1
            if(map_closed[i,j]==0):
                nb_black += 1
    ratio = nb_black / nb_pixels
    if(ratio < 0.25):
        continue
    width = bbox[3]-bbox[1]
    height = bbox[2]-bbox[0]
    total_height += height
    total_width += width
    pruned_regions.append(props)

mean_height = total_height/len(pruned_regions)
mean_width = total_width/len(pruned_regions)
print('means:')
print(mean_height)
print(mean_width)
textboxes = []
for props in pruned_regions:
    bbox = props.bbox
    # compute the size of the region, to remove the ones that are too large (and cannot be a character) and too small
    width = bbox[3]-bbox[1]
    height = bbox[2]-bbox[0]
    if (max(width,height) < 0.5 * min(mean_height,mean_width)):
        continue
    if (max(width,height) > 4.0 * max(mean_height,mean_width)):
        continue
    # print(width)
    # print(height)
    textboxes.append(props)

# now write the image with the text boxes
nrows, ncols = map_gray.shape
output = np.zeros((nrows,ncols))
for props in textboxes:
    bbox = props.bbox
    for i in range(bbox[0],bbox[2]):
        for j in range(bbox[1],bbox[3]):
            output[i,j] = 1

# now we need to cluster the text boxes, using a graph
G=nx.Graph()
# first create a node for each textbox
G.add_nodes_from([1,len(textboxes)])
for i in range (1,len(textboxes)):
    for j in range (i+1,len(textboxes)):
        # check if there should be an edge between nodes i and j
        # there are two conditions to meet
        # first, textboxes should be neighbours in the x-axis
        textbox1 = textboxes[i]
        bbox1 = textbox1.bbox
        width1 = bbox1[3]-bbox1[1]
        x1, y1 = textbox1.centroid
        textbox2 = textboxes[j]
        bbox2 = textbox2.bbox
        width2 = bbox2[3]-bbox2[1]
        x2, y2 = textbox2.centroid
        if(abs(x1 - x2) >= 1.5 * max(width1,width2)):
            continue
        # then, the second condition guarantees that the two textboxes have similar heights
        height1 = bbox1[2]-bbox1[0]
        height2 = bbox2[2]-bbox2[0]
        if(max(height1,height2)/min(height1,height2) < 2):
            # create an edge in the graph between nodes i and j
            G.add_edge(i,j)

print(G.number_of_edges())
        
# then create the connected components in the graph, and filter them
final_strings=[]
for component in nx.connected_components(G):
    # first we have to compute the height and width of the graph
    xmin = ncols
    ymin = nrows
    xmax = 0
    ymax = 0
    total_height = 0
    total_width = 0
    for node in component:
        # get the textbox that correspond to this node
        textbox = textboxes[node-1]
        bbox = textbox.bbox
        if(bbox[0] < ymin):
            ymin = bbox[0]
        if(bbox[1] < xmin):
            xmin = bbox[1]
        if(bbox[2] > ymax):
            ymax = bbox[2]
        if(bbox[3] > xmax):
            xmax = bbox[3]
        # increment the total heights and widths with the node values to compute the mean for all nodes
        total_height += bbox[2] - bbox[0]
        total_width += bbox[3] - bbox[1]
    
    component_height = ymax-ymin
    component_width = xmax-xmin
    # now compute the means of height and width for the nodes in the component
    mean_height = total_height / len(component)
    mean_width = total_width / len(component)

    # then compares the component height and width the means of its nodes
    if((component_height > 0.5*mean_height) and (component_width > 1.5*mean_width)):
        final_strings.append(component)

# now write the image with the final strings
nrows, ncols = map_gray.shape
output_strings = np.zeros((nrows,ncols))
for string in final_strings:
    for node in string:
        textbox = textboxes[node]
        bbox = textbox.bbox
        for i in range(bbox[0],bbox[2]):
            for j in range(bbox[1],bbox[3]):
                output_strings[i,j] = 1

# result visualization
fig, axes = plt.subplots(1, 6, figsize=(8, 4))
ax = axes.ravel()

ax[0].imshow(map)
ax[0].set_title("Original")
ax[1].imshow(binary_yen, cmap=plt.cm.gray)
ax[1].set_title("Thresholded")
ax[2].imshow(map_closed, cmap=plt.cm.gray)
ax[2].set_title("Closing")
ax[3].imshow(map_labeled, cmap='nipy_spectral')
ax[3].set_title("Labeled")
ax[4].imshow(output, cmap=plt.cm.gray)
ax[4].set_title("Textboxes")
ax[5].imshow(output_strings, cmap=plt.cm.gray)
ax[5].set_title("Strings")

fig.tight_layout()
plt.show()
