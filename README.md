# Python-Fire
[![Build Status](https://travis-ci.org/andela-cnnadi/python-fire.svg?branch=master)](https://travis-ci.org/andela-cnnadi/python-fire) [![Coverage Status](https://coveralls.io/repos/github/andela-cnnadi/python-fire/badge.svg?branch=master)](https://coveralls.io/github/andela-cnnadi/python-fire?branch=master)

Easy to use Firebase Python Plugin. Built as a wrapper around the Firebase REST HTTP API. Syntax is reminiscent of the simple syntax available in Javascript. Inspired by the [python-firebase](https://github.com/ozgur/python-firebase) library by [ozgur](https://github.com/ozgur).

## Installation

Get started using the PyFire library by installing it:

```
pip install pyfire
```

## Usage

Using the PyFire library is extremely easy. This is a sample books library built with it.

```py
from pyfire import Firebase

firebase = Firebase(YOUR_FIREBASE_URL)

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
```

### `Firebase` Methods

#### `__init__(url)`

Creating a new `Firebase` object is simply done using the `Firebase` constructor.

```py
firebase = Firebase(FIREBASE_URL)
```

#### `ref(reference)`

Calling the `ref()` method on the firebase object creates and returns a new `FirebaseReference` object. We can use this object to manipulate that reference.

```py
ref = firebase.ref(ref_name)
```

### `FirebaseReference` Methods

#### `get()`

This method returns all the content in that ref. An error is thrown if there are issues with permissions or any other HTTP error.

```py
results = ref.get()
```

#### `push(payload)`

This method creates new data under this ref. A random id is generated as the key and the `payload` is set as the value. The id is stored in the `name` key of the returned dictionary.

```py
record = ref.push(payload)
id = record['name']
```

#### `set(payload)`

This method sets the value of the ref to `payload`. If there was data in this ref before, it replaces it with `payload`. If this ref does not exists, it is created and then stored against the payload.

```py
ref.set(payload)
```

#### `update(payload)`

This method updates the keys in the ref with data specified in the payload. If we had payload with data `{'name': 'Egor'}`, it will replace the `name` key in the ref with the value `Egor`. This is the same things as doing `ref.child(name).set('Egor')`.

```py
ref.set(payload)
```

#### `delete()`

This method deletes the ref.

```py
ref.delete()
```

## TODO

Some of the pending functionality that needs to be implemented include:

- Authentication
- Streaming API
- Priority
- Server Values
