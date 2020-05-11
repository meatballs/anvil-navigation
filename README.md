# Navigation
A client module for [Anvil Applications](https://anvil.works) that provides dynamic menu construction.

## Introduction
This module builds a menu of link objects in an Anvil application based on a simple dictionary definition.

Rather than manually adding links and their associated click event handlers, the module does that for you!

## Installation
There are two methods to install this module within your own application:

### 1. As a Dependency

  * Create a clone of this application within your own Anvil account using this link:

    [<img src="https://anvil.works/img/forum/copy-app.png" height='40px'>](https://anvil.works/build#clone:2QN4JZNDCSWSXITS=PXZDGQRC56RJGDJ7E5PVWDLM)
  
  * At anvil, open the app in which you'd like to include dynamic navigation and, its settings menu, select 'Dependencies',
    and select your new cloned app in the dropdown.

### 2. By Direct Inclusion

  * In your anvil application, create a new module in the client code section and name it 'navigation'
  * Copy the entire content of `client_code/navigation.py` from this repository into your 'navigation' module
  
 ### Cookiecutter Template
 If you are starting a new application, you can also use this [cookiecutter template](https://github.com/meatballs/anvil-cookiecutter) which will automatically include this module using the direct inclusion method above.

## Usage

You can clone a demonstration of this module in use from:

[<img src="https://anvil.works/img/forum/copy-app.png" height='40px'>](https://anvil.works/build#clone:5V6PL5HAJQNWN6KV=XAX4Z3KVXOVQZKNDUA4X5LE4)

### Forms

In order for a form to act as a target of a menu link, it has to register a name with the navigation module using a decorator 
on its class definition. e.g. Assuming the module is installed as a dependency named 'Navigation':

```python
from ._anvil_designer import HomeTemplate
from anvil import *
from Navigation import navigation


@navigation.register(name="home")
class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
```
if you installed the module by direct inclusion, your import will need to point at the module you created.

### Menu

* In the Main form for your app, add a content panel to the menu on the left hand side and call it 'menu_panel'

* Add a menu definition dict to the code for your Main form and pass the panel and the dict to the menu builder. e.g.

```python
from ._anvil_designer import MainTemplate
from anvil import *
from Navigation import navigation
from HashRouting import routing

menu = [
  {"text": "Home", "target": "home"},
  {"text": "About", "target": "about"},
]


class Main(MainTemplate):
  
  def __init__(self, **properties):
    self.advanced_mode = False
    navigation.build_menu(self.menu_panel, menu)
    self.init_components(**properties)
```
will add 'Home' and 'About' links to the menu which will open registered forms named 'home' and 'about' respectively.

Each item in the dict needs the 'text' and 'target' keys as a minimum. It may also include 'routing' and 'visibility' keys:

 * 'routing' can be either 'classic' or 'hash' to indicate whether clicking the link should use Anvil's `add_component` function or hash routing to open the target form. Classic routing is the default if the key is not present in the menu dict.
 * 'visibility' can be a dict mapping an anvil event to either True or False to indicate whether the link should be made visible when that event is raised.
 
 All other keys in the menu dict are passed to the Link constructor.
 
 For example, to add icons to each of the examples above, a 'Contact' item that uses hash routing and a 'Settings' item that should only be visible when advanced mode is enabled:
 ```python
 from ._anvil_designer import MainTemplate
from anvil import *
from Navigation import navigation
from HashRouting import routing

menu = [
  {"text": "Home", "target": "home", "icon": "fa:home"},
  {"text": "About", "routing": "hash", "target": "about", "icon": "fa:info"},
  {"text": "Contact", "routing": "hash", "target": "contact", "icon": "fa:envelope"},
  {
    "text": "Settings",
    "target": "settings",
    "icon": "fa:gear",
    "visibility": {
      "x-advanced-mode-enabled": True,
      "x-advanced-mode-disabled": False
    }
  }
]


@routing.main_router
class Main(MainTemplate):
  
  def __init__(self, **properties):
    self.advanced_mode = False
    navigation.build_menu(self.menu_panel, menu)
    self.init_components(**properties)
   
  def form_show(self, **event_args):
    self.set_advanced_mode(False)
```
Note - since this example includes hash routing, it also requires a  decorator from the [Hash Routing App](https://github.com/s-cork/HashRouting) on the Main class.

### Startup

In order for the registration to occur, the form classes need to be loaded before the menu is constructed. This can be achieved by using a startup module and importing each of the forms in the code for that module.

e.g. Create a module called 'startup', set it as the startup module and import your Home form before opening the Main form:

```python
from anvil import open_form
from .Main import Main
from . import Home

open_form(Main())
```

### Page Titles
By default, the menu builder will also add a Label to the title slot of your Main form. If you register a form with a title as well as a name, the module will update that label as you navigate around your app. e.g. to add a title to the home page example:
```python
from ._anvil_designer import HomeTemplate
from anvil import *
from Navigation import navigation


@navigation.register(name="home", title="Home")
class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
```

If you want to disable this feature, set the `with_title` argument to `False` when you call `build_menu` in your Main form. e.g.
```python
class Main(MainTemplate):
  
  def __init__(self, **properties):
    self.advanced_mode = False
    navigation.build_menu(self.menu_column_panel, menu, with_title=False)
    self.init_components(**properties)
