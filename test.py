import requests

BASE = "http://127.0.0.1:5000/"

# Test data for strips
strips_data = [
    {"strip_id": 1, "title": "Batman: Year One", "author": "Frank Miller", "publicationYear": 1987, "genre": "Superhero", "url": "/images/batman_year_one.jpg"},
    {"strip_id": 2, "title": "Watchmen", "author": "Alan Moore", "publicationYear": 1986, "genre": "Superhero", "url": "/images/watchmen.jpg"},
    {"strip_id": 3, "title": "The Sandman", "author": "Neil Gaiman", "publicationYear": 1989, "genre": "Fantasy", "url": "/images/sandman.jpg"},
    {"strip_id": 4, "title": "Maus", "author": "Art Spiegelman", "publicationYear": 1980, "genre": "Historical", "url": "/images/maus.jpg"},
    {"strip_id": 5, "title": "Spider-Man: Blue", "author": "Jeph Loeb", "publicationYear": 2002, "genre": "Superhero", "url": "/images/spiderman_blue.jpg"},
    {"strip_id": 6, "title": "Spider-Man: The New Avenger", "author": "J. Michael Straczynski", "publicationYear": 2004, "genre": "Superhero", "url": "/images/spiderman_new_avenger.jpg"},
]

# Test data for users
users_data = [
    {"firstName": "Mats", "lastName": "Claerhout", "city": "Kortrijk", "email": "mats.claerhout@gmail.com"},
    {"firstName": "Piet", "lastName": "Pietersen", "city": "Rotterdam", "email": "piet.pietersen@email.com"},
    {"firstName": "Klaas", "lastName": "Klaassen", "city": "Utrecht", "email": "klaas.klaassen@email.com"},
    {"firstName": "Jits", "lastName": "Bulcaen", "city": "Harelbeke", "email": "jits.bulcaen@witblad.be"},
]

# Test data for collections
collections_data = [
    {"userId": 1, "stripId": 1, "status": "Owned"},
    {"userId": 1, "stripId": 2, "status": "Want to Read"},
    {"userId": 2, "stripId": 3, "status": "Owned"},
    {"userId": 2, "stripId": 4, "status": "Reading"},
    {"userId": 3, "stripId": 5, "status": "Owned"},
    {"userId": 3, "stripId": 1, "status": "Want to Read"},
]

# Test PUT: Adding strips to the database
print("Testing PUT (Create Strips):")
for i in range(len(strips_data)):
    response = requests.put(BASE + f"strips/{i + 1}", json=strips_data[i])
    print(f"PUT Response for Strip {i + 1}: {response.json()}")

input("Press Enter to continue...\n")

# Test PUT: Adding users to the database
print("Testing PUT (Create Users):")
for i in range(len(users_data)):
    response = requests.put(BASE + f"users/{i + 1}", json=users_data[i])
    print(f"PUT Response for User {i + 1}: {response.json()}")

input("Press Enter to continue...\n")

# Test PUT: Adding collections to the database
print("Testing PUT (Create Collections):")
for i in range(len(collections_data)):
    response = requests.put(BASE + f"collections/{i + 1}", json=collections_data[i])
    print(f"PUT Response for Collection {i + 1}: {response.json()}")

input("Press Enter to continue...\n")

# Test GET all strips (Retrieve all)
print("Testing GET All Strips (Retrieve all):")
response = requests.get(BASE + "strips/")  # Get all strips
if response.status_code == 200:
    print("GET All Strips Response:", response.json())
else:
    print(f"GET All Strips Error: {response.status_code}, {response.text}")

input("Press Enter to continue...\n")

# Test PATCH: Update a strip (partial update)
print("Testing PATCH (Update Strip):")
patch_data = {"title": "Updated Batman: Year One", "author": "Frank Miller"}  # Update title and author
response = requests.patch(BASE + "strips/1", json=patch_data)  # Patch strip with ID 1
if response.status_code == 200:
    print("PATCH Response for Strip 1:", response.json())
else:
    print(f"PATCH Error: {response.status_code}, {response.text}")

input("Press Enter to continue...\n")

# Test DELETE: Delete a strip
print("Testing DELETE (Delete Strip):")
response = requests.delete(BASE + "strips/1")  # Delete strip with ID 1
if response.status_code == 204:
    print("DELETE Response: Strip 1 deleted successfully.")
else:
    print(f"DELETE Error: {response.status_code}, {response.text}")

input("Press Enter to continue...\n")

# Test GET after DELETE: Try to fetch deleted strip
print("Testing GET after DELETE (Retrieve):")
response = requests.get(BASE + "strips/1")  # Attempt to get deleted strip
if response.status_code == 404:
    print("GET after DELETE Response: Strip not found.")
else:
    print(f"GET after DELETE Error: {response.status_code}, {response.text}")

# Test PUT strip with ID 1 again in the database
response = requests.put(BASE + "strips/1", json=strips_data[0])
print(f"PUT Response for Strip 1 again: {response.json()}")
