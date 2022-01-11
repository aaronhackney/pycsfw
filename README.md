# Cisco Secure Firewall SDK
This python library is intended to abstract the complexities of interacting with the Cisco Secure Firewall Management Center via API.

# Requirements
This library was developed and tested under python 3.10 and Cisco Secure Firewall Management Center Management center 7.1. Prior versions may work, but YMMV.

# Installation
1. (Optional) Create a python virtual environment. The below commands will create the venv in the existing directory `~/envs/` and activate it as the current python interpreter.
```
python3 -m venv ~/envs/pycsfw && source ~/envs/pycsfw/bin/activate
```

2. Clone or download/unzip the repo and install the module
```
git clone git@github.com:aaronhackney/pycsfw.git
cd pycsfw
pip install -r requirements.txt
pip install -e .
```

You can verify that the package is installed with `pip list | grep pycsfw`
```
$ pip list | grep pycsfw
pycsfw             0.1.0     /Users/aahackne/Projects/test/pycsfw
```

# Usage
The sample and tests packages have a few examples that should give one a good idea of how to use this client.  
   
## 1. Instantiate the client and get a token
```
from pycsfw import CSFWClient

csfw_client = CSFWClient('192.168.1.30', "admin", "mypassword", verify=False)
```

## 2. Get the domain UUID
The domain UUIDs that your user has access to are stored in `csfw_client.token["DOMAINS"]` and a domain UUID is
required for most API calls.

To set the domain UUID for the client instance, use the `get_domain_uuid` method.  

In this example, I have a domain called "Customer A" that I want to work on. 
The CSFW Manager will call this "Global/Customer A" (Customer A domain is a subset of the Global Domain).
```
csfw_client.get_domain_uuid("Global/Customer A")
```

If you need to identify the domain name at runtime, you can enumerate all domains from the firewall manager using 
`csfw_client.get_fmc_domain_list()`
```
domains = csfw_client.get_fmc_domain_list()
```

## 3. Use one of the methods to get information from the management center. See sample/get_interfaces.py
```
zone_list = csfw_client.get_security_zones_list()
```
## 4. The data is represented using pydantic dataclass objects (see models.py)  
If you want to use the objects like regular dictionaries for logging, printing, etc, 
you can treat the objects like a dictionary using pydantic's built in .dict() method
```
print(my_iface.dict())
print(my_iface.dict(exclude_unset=True))
```

You can also impoort a dictionary with keys corresponding to the pydantic dataclass models
In this example, I have a dict representing a network object that we map onto the NetworkObjectModel dataclass.
See models.py for all of the gory details of the dataclass definitions
```
my_net_obj = NetworkObjectModel(
    **{
        "name": "unittest-network-2",
        "value": "192.168.2.0/24",
        "overridable": False,
        "description": "Test Network obj 2",
    }
)






