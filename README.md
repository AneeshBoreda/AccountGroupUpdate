# Prisma Cloud alert csv export with tags and account group names 

Version: *1.0*
Author: *Aneesh Boreda*

### Summary
This script will add specified users to specified account groups based on a csv file.

### Requirements and Dependencies

1. Python 3.7 or newer

2. OpenSSL 1.0.2 or newer

(if using on Mac OS, additional items may be nessessary.)

3. Pip

```sudo easy_install pip```

4. Requests (Python library)

```sudo pip install requests```

5. YAML (Python library)

```sudo pip install pyyaml```

### Configuration

1. Navigate to *alert_tags_acctgrp/config/configs.yml*

2. Fill out your Prisma Cloud access key, secret, and customer name - if you are the only customer in your account then leave this blank.

3. API base - only need to adjust this if you are on a different stack (app=api, app2=api2, app3=api3, etc.)
  
### Input Data

The file sample_input.csv is provided showing the necessary formatting.
The data should be placed in input.csv in two columns. The left column should contain Account IDs, while the right column should contain the group that each account must be added to.

### Run

```
python runner.py input.csv

```
