# Navigation
A client module for [Anvil Applications](https://anvil.works) that provides dynamic menu construction.

## Introduction
This module builds a menu of link objects in an Anvil application based on a simple dictionary definition.

Rather than manually adding links and their associated click event handlers, the module does that for you!

## Installation
There are two methods to install this module within your own application:

* As a dependency

  * Create a clone of this application within your own Anvil account using this link:

    [<img src="https://anvil.works/img/forum/copy-app.png" height='40px'>](https://anvil.works/build#clone:2QN4JZNDCSWSXITS=PXZDGQRC56RJGDJ7E5PVWDLM)
  
  * At anvil, open the app in which you'd like to include dynamic navigation and, its settings menu, select 'Dependencies',
    and select your new cloned app in the dropdown.

* By direct inclusion

  * In your anvil application, create a new module in the client code section and name it 'navigation'
  * Copy the entire content of `client_code/navigation.py` from this repository into your 'navigation' module
  
 ### Cookiecutter Template
 If you are starting a new application, you can also use the [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template
 at https://github.com/meatballs/anvil-cookiecutter which includes this module by default.
