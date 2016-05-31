from pyfire import Firebase

firebase = Firebase('https://apitest-72809.firebaseio.com/')

# Create a Firebase reference
ref = firebase.ref('books')

# Get the contents of the reference
books = ref.get()

# Payload data can be declared using native python data types
payload = {'name': 'Harry Potter and the Prisoner of Azkaban', 'pages': 780}

# The add operation pushes a new node under this node
book = ref.add(payload)

# We can get the new node id using the name key
id = book['name']

# We can navigate to child nodes
bookref = ref.child(id)

# We can update specific records in this ref
bookref.update({'pages': 600})

# We can also just outright replace the content
bookref.set({'name': 'Harry Potter and the Order of the Phoenix', 'pages': 980})

# We can obviously simulate an update with a set
bookref.child('pages').set(790)

# We can delete the book once we're done
bookref.delete()
