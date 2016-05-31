# Python-Fire
[![Build Status](https://travis-ci.org/andela-cnnadi/python-fire.svg?branch=master)](https://travis-ci.org/andela-cnnadi/python-fire) [![Coverage Status](https://coveralls.io/repos/github/andela-cnnadi/python-fire/badge.svg?branch=master)](https://coveralls.io/github/andela-cnnadi/python-fire?branch=master)

Firebase Python Plugin

### Installation

Get started using the PyFire library by installing it:

```
pip install pyfire
```

### Usage

Using the PyFire library is extremely easy. This is a sample books library built with it.
```py
from pyfire import Firebase

firebase = Firebase(FIREBASE_URL)

# Create a Firebase reference
baseref = firebase.ref('base_node')

# Navigate to child nodes
childref = baseref.child('child_node')

# Payload data can be declared using native python data types
payload = {'name': 'Chidiebere Nnadi'}

# The add operation pushes a new node under this node
newnode = childref.add(payload)

# We can get the newnode id using the name key
id = newnode['name']
```

### Methods

#### `__init__(url)`

Creating a new firebase object is simply done using the `Firebase` constructor

```py
firebase = Firebase(FIREBASE_URL)
```

#### `ref(reference)`

Calling the `ref()` method on the firebase object creates and returns a new `FirebaseReference` object.

```py
baseref = firebase.ref(base_ref_name)
```
