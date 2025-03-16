from geopy.geocoders import Nominatim
import json
import os

file_dir = os.path.dirname(os.path.realpath('__file__'))
async def get_addresses():
    with open(os.path.abspath(os.path.realpath(os.path.join(file_dir, "data/addressbook.json"))), 'r') as f:
        return json.load(f)
    
async def save_address(addresses):
    with open(os.path.abspath(os.path.realpath(os.path.join(file_dir, "data/addressbook.json"))), "w") as f:
        json.dump(addresses, f)

geolocator = Nominatim(user_agent="addressbook")
def get_lat_long(address):
    print(address)
    loc = geolocator.geocode(address[len(address)-8:])
    if loc == None:
        loc = geolocator.geocode(address[len(address)-8:])
    if loc != None:
        lat, long = loc.latitude, loc.longitude
    else:
        lat = ""
        long = ""
    
    return lat, long

async def get_address_ID(address):
    addresses = await get_addresses()
    for i in range(len(addresses)):
        if address.lower() == addresses[i]["address"].lower():
            return i
    return -1

async def create_new_address(add, logo):
    address = {}
    address["address"] = add
    address["lat"], address["long"] = get_lat_long(add)
    address["logo"] = logo
    return address

async def update_addressbook(address, logo):
    if (address != "N/A"):
        addresses = await get_addresses()
        address_id = await get_address_ID(address) 
        if address_id == -1:
            addresses.append(await create_new_address(address, logo))
            await save_address(addresses)
            return len(addresses)-1

        else:
            if logo != "":
                addresses[address_id]["logo"] = logo

        return address_id
    return "N/A"
