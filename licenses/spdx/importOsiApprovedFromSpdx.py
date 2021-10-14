#!/usr/bin/env python3

# Copyright (c) 2021, Source Auditor Inc.
# SpdxLicenseIdentifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import json
import requests
from pathlib import Path

def updateSpdxMappingsFile(spdxLicenseId, osiLicenseId):
    """
    Updates the JSON file containing the mappings from the OSI license ID to the SPDX license ID
    """
    spdxMappingsFilePath = Path("importedSpdxFiles.json")
    try:
        spdxMappings = []
        if spdxMappingsFilePath.is_file():
            with spdxMappingsFilePath.open(mode='r') as f:
                spdxMappings = json.load(f)
        identifiers = None
        for idMap in spdxMappings:
            if idMap["id"] == osiLicenseId:
                identifiers = idMap["identifiers"]
                break
        if identifiers == None:
            spdxIdMap = {
                    "id": osiLicenseId,
                    "identifiers": []
                    }
            spdxMappings.append(spdxIdMap)
            identifiers = spdxIdMap["identifiers"]
        found = False
        for spdxId in identifiers:
            if spdxId["identifier"] == spdxLicenseId and spdxId["scheme"] == "SPDX":
                found = True
                break
        if not found:
            identifiers.append({
                            "identifier": spdxLicenseId,
                            "scheme": "SPDX"
                            });
        with spdxMappingsFilePath.open(mode='w+') as f:
            json.dump(spdxMappings, f, indent=4, sort_keys=True)
    except Exception as e:
        print("Error writing SPDX mappings file")
        print(e)
        sys.exit(1)

def createOsiJsonFile(spdxJson, osiLicenseId, outputFilePath):
    osiUrl = "https://opensource.org/licenses/" + osiLicenseId
    spdxUrl = "https://spdx.org/licenses/" + spdxJson["licenseId"]
    osiJson = [{
            "id": osiLicenseId,
            "name": spdxJson["name"],
            "identifiers": [],
            "keywords": ["osi-approved"],
            "links": [
                {
                    "note": "OSI Page",
                    "url": osiUrl
                },
                {
                    "note": "SPDX page",
                    "url": spdxUrl
                }],
            }]
    textCrossRef = None
    if "crossRef" in spdxJson:
        for cross in spdxJson["crossRef"]:
            if cross["match"] == "true" and cross["isValid"] and cross["isLive"] and not cross["isWayBackLink"]:
                if textCrossRef == None or textCrossRef["order"] > cross["order"]:
                    textCrossRef = cross
    if textCrossRef != None:
        osiJson[0]["text"] = [{
                        "media_type": "text/html",
                        "title": "HTML",
                        "url": textCrossRef["url"]
                        }]
    else:
        osiJson[0]["text"] = [{
                        "media_type": "text/html",
                        "title": "HTML",
                        "url": osiUrl
                        }]
    try:
        with outputFilePath.open(mode='w') as f:
            json.dump(osiJson, f, indent=4, sort_keys=True)
    except Exception as e:
        print("Error creating OSI JSON file "+str(outputFilePath))
        print(e)
        sys.exit(1)
        
def createTextFile(spdxJson, osiLicenseId, textFilePath):
    try:
        with textFilePath.open(mode="w") as f:
            f.write(spdxJson["licenseText"])
    except Exception as e:
        print("Error writing text file "+str(textFilePath))
        print(e)
        sys.exit(1)
    
def importFromSpdx(spdxLicenseId, osiLicenseId, osiApproved):
    """
    Fetch the SPDX JSON object for this license ID and copy over any information 
    licenseId - SPDX license ID for the license to be imported
    osiApproved - true if the license is OSI Approved
    
    NOTE: This assumes the script is running in the licenses/spdx directory
    """
    outputFileName = osiLicenseId+".json"
    outputFilePath = Path("..") / "manual" / outputFileName
    textFilePath = Path("..") / ".." / "texts" / "plain" / osiLicenseId
    if outputFilePath.exists():
        print("OSI license ID '"+osiLicenseId+"' already exists")
        sys.exit(1)
    try:
        spdxJson = requests.get("https://spdx.org/licenses/" + spdxLicenseId + ".json").json()
    except Exception as e:
        print("Unable to find SPDX license ID "+spdxLicenseId)
        print(e)
        sys.exit(1)
    createOsiJsonFile(spdxJson, osiLicenseId, outputFilePath)
    createTextFile(spdxJson, osiLicenseId, textFilePath)
    updateSpdxMappingsFile(spdxLicenseId, osiLicenseId)
    # Update the SPDX Mappings file            

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: imporOsiApprovedFromSpdx SPDXLicenseID OSILicenseID")
        sys.exit(2)
    importFromSpdx(sys.argv[1], sys.argv[2], True)
    print("Sucessfully imported "+sys.argv[1]+".  Be sure to review and update as described in the IMPORTING_FROM_SPDX.md")
    sys.exit(0)

