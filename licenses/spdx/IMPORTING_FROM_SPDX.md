# Importing OSI License Information from SPDX
If an OSI approved license is an [SPDX listed license](https://spdx.org/licenses/) but not in this OSI licenses repository, the `importOsiApprovedFromSpdx.py` can be used to initialize the OSI license data from the SPDX license data.

**PLEASE NOTE:** Since OSI data may differ from SPDX, follow ALL of the steps below to ensure an accurate import of the license data.

## Prerequisites
The `importOsiApprovedFromSpdx.py` utility depends on Python3 and the requirements.txt libraries found in the root of this repository.
## Import Procedure

- Run the command `python importOsiApprovedFromSpdx.py [spdxID]
   [osiID]` where `[spdxID]` is the SPDX listed license ID and the
   `[osiID]` is the ID used by OSI for the license to be imported.
- Review the file `licenses/manual/[osiID].json`
    - Verify the links are live and point to the correct license
    - Compare the name to the name on the OSI license page.  Update if needed.
    - Add any additional metadata available on the OSI website.
- Compare the license text used by SPDX to the license text used by OSI.  If there are any differences, update the file `texts/plain/[osiID]` with the OSI text.  Note: the [SPDX license diff](https://github.com/spdx/spdx-license-diff) browser plugin is a convenient utility for comparing license texts.
- Run the compile.py script to validate the changes
- Create a pull request with the new license data