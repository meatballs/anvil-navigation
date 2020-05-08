#    Anvil Navigatio
#    Copyright 2020 Owen Campbell
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.

#   You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
from anvil import Label, Link, get_open_form, set_url_hash

__version__ = "0.1.0"

# A dict mapping a form's name to a further dict with the form's class and title
_forms = {}

# A list of all navigation links
_links = []

# A dict mapping an event name to list of dicts.
# Each of those dicts has keys "link" and "visible" with values of a link instance and boolean respectively.
# The boolean is used to set the 'visible' property of the link when the event is raised.
_visibility = {}

_title_label = Label()


class register:
    """A decorator to register a form in the _forms dict."""

    def __init__(self, name, title=None):
        self.name = name
        self.title = title

    def __call__(self, cls):
        _forms[self.name] = {"class": cls, "title": self.title}
        return cls


def get_form(name):
    """Create an instance of a registered form."""
    return _forms[name]["class"]()


def _open_tagged_form(form_name):
    """Use classic routing to open a registered form"""
    form = get_form(form_name)
    _title_label.text = _forms[form_name]["title"]
    get_open_form().content_panel.clear()
    get_open_form().content_panel.add_component(form)


def _default_link_click(**event_args):
    """A handler for navigation link click events
  
  * Clears the role of all links registered in this module
  * Set the calling link's role to 'selected'
  * Calls the relevant action for classic or hash routing
  """
    for l in _links:
        l.role = ""
    link = event_args["sender"]
    link.role = "selected"
    actions = {"classic": _open_tagged_form, "hash": set_url_hash}
    actions[link.tag.routing](link.tag.target)


def _visibility_event_handler(**event_args):
    """A handler for all registered visibility events"""
    items = _visibility[event_args["event_name"]]
    for item in items:
        item["link"].visible = item["visible"]


def _register_visibility(container, link, visibility):
    """Register the visibility events and set the handler on the container"""
    for event, visible in visibility.items():
        if event not in _visibility:
            _visibility[event] = []
            container.set_event_handler(event, _visibility_event_handler)
        _visibility[event].append({"link": link, "visible": bool(visible)})


def build_menu(container, items, with_title=True):
    """Add links to the container and set their initial visibility"""
    if with_title:
        container.parent.add_component(_title_label, slot="title")
    for item in items:
        link = navigation_link(**item)
        _links.append(link)
        visibility = link.tag.visibility
        if visibility is None:
            link.visible = True
        else:
            link.visible = False
            _register_visibility(container, link, visibility)
        container.add_component(link)


def navigation_link(
    routing="classic", target=None, on_click=None, visibility=None, **kwargs
):
    """Create a link instance
  
  Parameters
  ----------
  routing
    Either 'classic' or 'hash'
  target
    Either the name of a registered form for classic routing or
    a url_hash for hash routing
  on_click
    event handler to call when clicked
  visibility
    a dict mapping the names of events to either True or False
  kwargs
    will be passed the Link constructor
  """
    if routing not in ("classic", "hash"):
        raise ValueError(
            "A navigation link's routing must either be 'classic' or 'hash'"
        )
    link = Link(**kwargs)
    link.tag.routing = routing
    link.tag.target = target
    link.tag.visibility = visibility
    if on_click is None:
        link.set_event_handler("click", _default_link_click)
    else:
        link.set_event_handler("click", on_click)
    return link
