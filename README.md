# pycsfw - Cisco Secure Firewall Client
This library is intended to abstract the complexities of interacting with the Cisco Secure Firewall Management Center via API.

# Requirements
This library was developed and tested under python 3.10 and Cisco Secure Firewall Management Center Management center 7.1. Prior versions may work, but YMMV.

# Installation
1. git clone git@github.com:aaronhackney/pycsfw.git
2. cd pycsfw
3. pip install -r requirements.txt
4. pip install -e . (The period is required!)

You can verify that the package is installed with `pip list | grep pycsfw`
```
$ pip list | grep pycsfw
pycsfw             0.1.0     /Users/aahackne/Projects/test/pycsfw
```

# Useage
The sample and tests packages have a few examples that should give one a good idea of how to use this client.  
   
## 1. Instantiate the Client and get a token
```
from pycsfw import CSFWClient
csfw_client = CSFWClient('192.168.1.30', "admin", "mypassword", verify=False)
csfw_client.get_auth_token()
```

## 2. Get the domain UUID
The domain UUIDs that your token has access to are stored in `csfw_client.token["DOMAINS"]` and is required for almost
every call you will make.  

To get the domain UUID for the domain you are wanting to make API calls against, use the `get_domain_uuid` method.  

In this example, I have a domain called "Customer A" that I want to work on. 
The CSFW Manager will call this "Global/Customer A" (Customer A domain is a subset of the Global Domain).
```
domain_uuid = csfw_client.get_domain_uuid("Global/Customer A")

## 3. Use one of the methods to get information from the management center. See sample/get_interfaces.py
```
zone_list = csfw_client.get_security_zones_list(domain_uuid)

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






