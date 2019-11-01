import pandas as pd
import numpy as np
import matplotlib
import glob
import re
import os
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches


# Function create the XML file
def pdToXml(name, coordinates, size, img_folder):

    xml = ['<annotation>']
    xml.append("    <folder>{}</folder>".format(img_folder))
    xml.append("    <filename>{}</filename>".format(name))
    xml.append("    <source>")
    xml.append("        <database>Unknown</database>")
    xml.append("    </source>")
    xml.append("    <size>")
    xml.append("        <width>{}</width>".format(size["width"]))
    xml.append("        <height>{}</height>".format(size["height"]))
    xml.append("        <depth>3</depth>".format())
    xml.append("    </size>")
    xml.append("    <segmented>0</segmented>")

    for field in coordinates:
        xmin, ymin = max(0,field[0]), max(0,field[1])
        xmax = min(size["width"], field[0]+field[2])
        ymax = min(size["height"], field[1]+field[3])

        xml.append("    <object>")
        xml.append("        <name>Face</name>")
        xml.append("        <pose>Unspecified</pose>")
        xml.append("        <truncated>0</truncated>")
        xml.append("        <difficult>0</difficult>")
        xml.append("        <bndbox>")
        xml.append("            <xmin>{}</xmin>".format(int(xmin)))
        xml.append("            <ymin>{}</ymin>".format(int(ymin)))
        xml.append("            <xmax>{}</xmax>".format(int(xmax)))
        xml.append("            <ymax>{}</ymax>".format(int(ymax)))
        xml.append("        </bndbox>")
        xml.append("    </object>")
    xml.append('</annotation>')
    
    return '\n'.join(xml)

# Function to transform the coordinates of the oval to a rectangle
def transformCoordinates(OrgCoordinates, MaxWidth, MaxHeight):
    # Get the values of the oval
    (AxisMax, AxisMin, Angle, X, Y, _) = list(map(float, OrgCoordinates.split()))

    # 
    Width = 2 * max(abs(AxisMax * math.cos(Angle)), abs(AxisMin * math.sin(Angle)))
    Height = 2 * max(abs(AxisMax * math.sin(Angle)), abs(AxisMin * math.cos(Angle)))

    # Coordinates X and Y
    X = X - Width/2
    Y = Y - Height/2

    # Check that the coordinates do not 
    # pass the limits of the images
    if X < 0:
        X = 1

    if Y < 0:
        Y = 1

    if X + Width > MaxWidth:
        Width = MaxWidth - X - 1 

    if Y + Height > MaxHeight:
        Height = MaxHeight - Y - 1

    # return the final coordinates
    return [X, Y, Width, Height]



# Return a list with all the lines of a file
def generateArray(file):
    
    # Open the file
    with open(file, "r") as f:
        # Read file and make it an array
        contentArray = f.read().split('\n')
        
    # Array to store the dictionary of all images
    infoList = []

    iI = 0  # Index
    # Move across the content array of this file
    while(iI < len(contentArray)):
        # Check if the current value is a name of an image
        if(re.match('(\d)*_(\d)*_(\d)*_big_img_(\d)*', contentArray[iI])): 

            try:
                lbDict = dict() # Temporal dictionary
                annotations = [] # Temporal array to store the annotations

                # Store the image name
                lbDict["name"] = "{}.jpg".format(contentArray[iI])

                # matplotlib: To manage images
                img = mpimg.imread(os.path.join("dataset", lbDict["name"]))
                # fig,ax = plt.subplots(1)
                # ax.imshow(img) 

                # Height, width, ...
                (MaxHeight, MaxWidth, _) = img.shape

                # Dictionary as an attr
                lbDict["size"] = {
                    "height": MaxHeight,
                    "width": MaxWidth,
                }

                iI += 1 # Move the index
                iJ = 0  # New sub-index to get the annotations
                iN = int(contentArray[iI])

                # Loop to move accross the annotations
                while(iJ < iN):
                    iI += 1
                    iJ += 1

                    # Transforme the ellipse coordinates to a rectangle coordinates
                    Recta = transformCoordinates(contentArray[iI], MaxWidth, MaxHeight)
                    annotations.append(Recta)

                    # To create the red rectangle 
                    # rect = patches.Rectangle(
                    #         (rec[0],rec[1]),rec[2],rec[3],
                    #         linewidth = 1,
                    #         edgecolor = 'r',
                    #         facecolor = 'none')
                    # ax.add_patch(rect)
                
                # plt.show()

                # Add the annotations to the dictionary
                lbDict["annotations"] = annotations

                # Append the dictionary to the array
                infoList.append(lbDict)


            # Catch any array
            except:
                print("{} not found...", format(contentArray[iI]))

        # Increment the index
        iI += 1

    # Return the array with dictionaries 
    return infoList


# Load the path/name of all the images
images = glob.glob('./dataset/*.jpg')
# Delete the initial path
images = list(map((lambda x: x[10:]), images))
# Make the result a pandas Series
images = pd.Series(images)

# Load the path/name of all the images
labels = glob.glob('./labels/*ellipseList.txt')
# Make the result a pandas Series
labels = pd.Series(labels)

# Generate an array of arrays with the dictionaries
allImagesDir = [generateArray(f) for f in labels]

# Array flattened with all the directories
flArray = np.hstack(allImagesDir)

# Array that store the names from the array with dictionaries
arrNames = list(map((lambda x: x["name"]), flArray))

# Filter the images of the datasets
result = images.isin(arrNames)
images = images[~result]

# Delete the unused images
for im in images:
    os.remove(os.path.abspath('./dataset/' + str(im)))


# Loop to move accross the array with the dictionaries
for imag in flArray:
    # Get the XML
    xml = pdToXml(imag['name'], imag['annotations'], imag['size'], "dataset")

    # Make the path to the .xml file
    nombre = imag['name'][:-4] + ".xml"
    path = os.path.abspath("dataset") + "\\" + nombre

    # Write the file
    with open(path, 'w') as fp:
        fp.write(xml)


print("Dataset cleaned")




