# How to prepare UnitTests
These test run against an actual FMC device
Required environment variables for most of these tests:

## Required environment test variables
```
FMCIP = ip of the FMC we are testing against
FMCUSER = username of an admin user of the FMC
FMCPASS = password of the FMCUSER
```
## Example 
In most shells: 
```
export FMCIP="192.168.3.22"
export FMCUSER="admin"
export FMCPASS="myadminpassword"
```

# Optional environment test variable
Only define the FMCVERIFY environment variable if you want to IGNORE 
the SSL/TLS certificate validity, typically because your test FMC is 
using a self-signed certificate. Not recommneded for production usage. 
```
FMCVERIFY = "false"
```

