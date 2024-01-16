from elem_attrs import attributes
from tags import empty, other

class Style:
  def __init__(self, items = None):
    self.data = ""
    if items is None:
      items = {}
    for key, value in items.items():
      setattr(self, key, value)


  def __str__(self):
    items = vars(self)
    string = ""
    for i, j in items.items():
      if i != "data":
        string += f"{i}:{j};"
    return string
  
class ClassList:
  def __init__(self, elem):
    self.elem = elem

  def replace(self, old, new):
    if old in self.elem.className:
      self.elem.className = self.elem.className.replace(old, new)
    self.elem._changed = True

  def contains(self, item):
    if item in self.elem.className.split():
      return True
    return False
  
  def remove(self, item):
    items = self.elem.className.split()
    if item in items:
      items.remove(item)
      self.elem.className = " ".join(items)
    self.elem._changed = True

class HTMLElement:
  def __init__(self, tag, id = None, className = None, innerHTML= None, children = [], style = None):
    self.tag = tag
    self._id = id
    self._innerHTML = innerHTML
    self.children = list(children)
    self.className = className
    if style:
      self.style = Style(style)
    else:
      self.style = Style()
    self.onClick = None
    self._changed = False

  @property
  def id(self):
    return self._id

  @id.setter
  def id(self, value):
    if value == "document":
        raise Exception("'document' as id for HTML Element is not allowed!")
    self._id = value

  def __setitem__(self, key, value):
    if key == "id" and value == "document":
        raise Exception("'document' as id for HTML Element is not allowed!")

  def __str__(self):
    return self.outerHTML
  
  @property
  def changed(self):
    items = []
    if(self._changed):
      items.append(self)
    for i in self.children:
      if i._changed:
        items.append(i)
      items.append(i.changed)
    
    return items
  
  def resetChanged(self):
    for i in self.children:
      i._changed = False
      i.resetChanged()
  
  @property
  def classList(self):
    return ClassList(self)
    

  def querySelector(self, query:str):
    el = None
    if query.startswith("#"):
      for i in self.children:
        if(i.id == query.split("#")[1]):
          el = i
          break
        el = i.querySelector(query)
        if(el):
          break
          
    return el

  def append(self, *elem):
    for i in elem:
      self.children.append(i)
    self._changed = True

  @property
  def innerHTML(self):
    html = ""
    for i in self.children:
      html += i.outerHTML

    if(html == ""):
        html += self._innerHTML

    return html

  @innerHTML.setter
  def innerHTML(self, html):
    self.children = []
    self._innerHTML = html
    self._changed = True

  @property
  def outerHTML(self):
    attrs = vars(self)
    data = ""
    for i,j in attrs.items():
      if i in attributes.keys():
        data += ((" "+attributes[i]+"=\'" + str(j) + "\'") if j != None and str(j) != "" else f'')
    if self.tag in empty:
      return "<"+self.tag + data + ">"
    else:
      return "<"+self.tag + data + ">" + self.innerHTML + "</" + self.tag + ">"


Element = HTMLElement
class HTMLElement(Element):
    def __setitem__(self, key, value):
        if key == "id":
          if value == "document":
            raise Exception("'document' as id for HTML Element is not allowed!")
        self._changed = True
        Element.__setitem__(self, key, value)

def oneList(items):
  arr = []
  for item in items:
    if type(item) == list:
      arr2 = oneList(item)
      for i in arr2:
        arr.append(i)
    elif type(item) == HTMLElement:
      arr.append(item)
  return arr

def are_all_related(items):
    arr = {}

    for i, j in items.items():
        arr[i] = str(j)
        for k, l in items.items():
              if i != k:
                if not j.querySelector(f"#{l.id}"):
                  arr[k] = str(l)
                else:
                  if k in arr:
                    del arr[k]
              
    return arr

def purify(arr):
  arr = oneList(arr)
  arr2 = {}

  for i in arr:
      if i.id not in arr2:
        arr2[i.id] = i

  if arr2 != dict():
    arr2 = are_all_related(arr2)

  return arr2

class Document:
  def __init__(self, title = "Document"):
    self._innerHTML = ""
    self.children = []
    self._title = title
    self._changed = False

  @property
  def title(self):
    return self._title
  
  @title.setter
  def title(self, value):
    self._changed = True
    self._title = value

  def resetChanged(self):
    self._changed = False
    for i in self.children:
      i._changed = False
      i.resetChanged()

  def append(self, *elem):
    for i in elem:
      self.children.append(i)
    self._changed = True

  def createElement(self, elem):
    return HTMLElement(elem)
  
  @property
  def changed(self):
    items = []
    if(self._changed):
      items = {}
      items["document"] = str(self)
    else:
      for i in self.children:
        if i._changed:
          items.append(i)
        items.append(i.changed)

      items = purify(items)
    
    return items
  
  def querySelector(self, query:str):
    el = None
    if query.startswith("#"):
      for i in self.children:
        if(i.id == query.split("#")[1]):
          el = i
          break
        el = i.querySelector(query)
        if(el):
          break
          
    return el
  
  def __str__(self):
    return self.outerHTML

  @property
  def outerHTML(self):
    file = open("index.html")
    html = file.read()
    html = html.replace("${title}", self.title)
    html = html.replace("${body}", self.innerHTML)
    return html

  @property
  def innerHTML(self):
    html = ""
    for i in self.children:
      html += i.outerHTML
    return html
