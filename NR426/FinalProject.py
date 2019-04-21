# Ryan Jennett
# Final project 5: identifying parcels whose owners do not live there
# Using BoulderCoParcelsforLongmont and LongmontBndBuf

import arcpy
from arcpy import env

# env.workspace = r"N:\MyFiles\NR426Py\FinalProject\GIS211ProjectData.gdb"
env.workspace = r"C:\Users\rjennett\Desktop\NR426FinalProject\FinalProject\GIS211ProjectData.gdb"
env.overwriteOutput = True

# Reference data
longmontBuffer = "Longmont_Bnd_buf"
parcels = "BoulderCoParcelsforLongmont"


# Clip the data
parcelsClip = "parcelsClip"
arcpy.Clip_analysis(parcels, longmontBuffer, parcelsClip)
print("Clip complete")

# Create field for new address
arcpy.AddField_management(parcelsClip, "trueAddress", "TEXT")
print("TrueAddress field added")

# Create and calculate new STREETNO field to create usable data of int type
# (given STREETNO field is float)

arcpy.AddField_management(parcelsClip, "intStreetno", "SHORT")
print("intStreetno field added")

with arcpy.da.UpdateCursor(parcelsClip, ("intStreetno", "STREETNO")) as cursor:
    for row in cursor:
        row[0] = row[1]
        cursor.updateRow(row)

print("intStreetno calculated")

# Calculate the new address field

with arcpy.da.UpdateCursor(parcelsClip, ("trueAddress", "STREETNO", "STREETNAME", "STREETSUF")) as cursor:
    for row in cursor:
        row[0] = str(row[1]) + " " + str(row[2]) + " " + str(row[3])
        cursor.updateRow(row)

print("trueAddress calculated")

# Test mailing address against new address field
# Use cursor, field calculator or SQL

# Method:
# check MAIL_ADDR1 and MAIL_ADDR2 against STREETNO and STREETNAME
# done in order will return unique values

# Create lists from fields to use in comparison

# Populate a list from the STREETNAME field
lsSTREETNAME = [row[0] for row in arcpy.da.SearchCursor(parcelsClip, 'STREETNAME')]
print(lsSTREETNAME)

# Populate a list from the MAIL_ADDR1 field
lsMAIL_ADDR1 = [row[0] for row in arcpy.da.SearchCursor(parcelsClip, 'MAIL_ADDR1')]
print(lsMAIL_ADDR1)

print(set(lsSTREETNAME) & set(lsMAIL_ADDR1))

for item in lsMAIL_ADDR1:
    lsSplit = item.split( )
    MAIL_ADDRstreet = lsSplit[1]
print(MAIL_ADDRstreet)

# query = "MAIL_ADDR1 LIKE '%STREETNAME%' OR MAIL_ADDR2 LIKE '%STREETNAME%'"
#
# arcpy.SelectLayerByAttribute_management(parcelsClip, "NEW_SELECTION", query)
#
# print("Selection made")

#Create a layer from the selection of non matching addresses
# arcpy.MakeFeatureLayer_management(parcelsClip, "verifyLyr", query)
# print("verifyLyr created")

