#Ryan Jennett
#Short project

#Grab layer from cloud (Pueblo_Apr13_14_2019)
#pick out each feature by session #, make it its own feature class.


#####################################
#Create featureset from online data
#####################################

print ("Starting script to load in data from a feature service.....")
import arcpy
#allow data to overwrite
arcpy.env.overwriteOutput = True


#Get Pueblo_Apr13_14_2019 layer from ArcGISOnline
data_url="https://services1.arcgis.com/KNdRU5cN6ENqCTjk/arcgis/rest/services/Pueblo_Apr13_14_2019/FeatureServer/0/query?where=OBJECTID>0&outFields=*&f=json"

# Set up data paths

arcpy.env.workspace = r"C:\Users\rjennett\Desktop\ShortProject"

data_path = r"C:\Users\rjennett\Desktop\ShortProject\Data\puebloFS.shp"

#Create the feature set variable
puebloFS = arcpy.FeatureSet()

print("Loading the feature service from AGOL into the feature set...........")
#load the json data into the feature set
puebloFS.load(data_url)

#save the feature set data to a feature class in our geodatabase
puebloFS.save(data_path)

#Verify save
if arcpy.Exists(data_path):
    print("Created")
else:
    print("Not created")

#######################################################################################################
#pick out the most recent features, pick out each feature by session #, make it its own feature class.
#######################################################################################################

#create featureclass for each Session by number

#====================Section for functional reference=======================
#This block creates a new feature with only Session 2 values

#create featureclass from selection
# puebloFL = arcpy.MakeFeatureLayer_management(puebloFS, r"C:\Users\rjennett\Desktop\ShortProject\puebloSession2")
# print("make fl")
#
# #select by Session
# query = "Session = 2"
# puebloSEL = arcpy.SelectLayerByAttribute_management(puebloFL, "NEW_SELECTION", query)
# print("selection")
#
# #copy selected features to new layer
# arcpy.CopyFeatures_management (puebloSEL, r"C:\Users\rjennett\Desktop\ShortProject\Data\puebloSession2")
# print("cpy")
#===========================================================================


#create featureclass from selection
puebloFL = arcpy.MakeFeatureLayer_management(puebloFS, r"C:\Users\rjennett\Desktop\ShortProject\Data\puebloSession")
print("Created puebloFL")
print("\n")

#initialize array to hold known values for the field we want to loop through
sessionArr = [2, 3, 4, 5]

#initialize counter
i = 0

for session in sessionArr:
    #create dynamic query to take elements from sessionArr[]
    query = "Session = " + str(sessionArr[i])
    print("Query: " + query)
    #store selection as puebloSEL
    puebloSEL = arcpy.SelectLayerByAttribute_management(puebloFL, "NEW_SELECTION", query)
    #store dynamic file output as outFile to be used in feature copy path
    outFile = "puebloSession" + str(sessionArr[i]) + ".shp"
    print("OutFile: " + outFile)
    # copy selected features to new layer
    arcpy.CopyFeatures_management(puebloSEL, r"C:\Users\rjennett\Desktop\ShortProject\Data\\" + outFile)
    print("Selection copied")
    print("---")
    i += 1
