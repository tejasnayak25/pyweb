from document import Document
from server import server
import asyncio
import time
import copy, os

document = Document()

maindiv = document.createElement("div")
maindiv.className = "flex flex-col gap-2 justify-between min-h-full h-full"

div = document.createElement("div")
div.id = "Div1"
div.className = "w-full relative z-20"

div3 = document.createElement("div")
div3.id = "Div3"
div3.className = "bg-black relative z-20 flex justify-between mx-2"

imagediv = document.createElement("div")
imagediv.id = "Divimg"
imagediv.className = "w-full -mt-12 relative z-10"

p = document.createElement("p")
p.id = "Hi"
p.innerHTML = "Bye"
p.className = "para w-full block"

span = document.createElement("span")
span.id = "Span1"
span.innerHTML = "Project Alpha"
span.className = "w-full p-12 pb-0 lg:text-4xl text-2xl text-center lemon-regular block"
# span.style.color = "black"

div.append(p)

# div.innerHTML = "Hi"
p.append(span)

img = document.createElement("img")
img.src = "https://wallpapercave.com/wp/Q423sdL.jpg"
img.style.width = "100%"
img.id = "Image1"
img.className = "rendering-auto"

imagediv.append(img)

button = document.createElement("button")
button.innerHTML = "Click Me!"
# button.style.width = "100%"
button.id = "button"
button.style.color = "white"
button.className = "btn btn-info m-3"

inp = document.createElement("input")
inp.type = "text"
inp.id = "Input1"
inp.value = ""
inp.placeholder = "Enter text"
inp.className = "input input-info m-3 lg:w-11/12 w-8/12"

cross = document.createElement("button")
cross.innerHTML = "X"
cross.id = "cross"
cross.className = "btn btn-primary"

div2 = document.createElement("div")
div2.id = "div-hidden"
div2.className = "hidden"
p2 = document.createElement("p")
p2.innerHTML = ""
p2.id = "p-data"
div2.append(p2, cross)

def tell(self):
  p = self.document.querySelector(f"#{p2.id}")
  inpu = self.document.querySelector(f"#{inp.id}")
  div = self.document.querySelector(f"#{div2.id}")
  doc = self.document
  p.innerHTML = inpu.value
  div.classList.replace("hidden", "block")
  doc.title = inpu.value

def hide(self):
  p = self.document.querySelector(f"#{p2.id}")
  div = self.document.querySelector(f"#{div2.id}")
  p.innerHTML = ""
  div.classList.replace("block", "hidden")
  

button.onClick = tell
cross.onClick = hide

div3.append(inp, button)

maindiv.append(div, imagediv, div3, div2)
document.append(maindiv)


serve = server(os.environ['PORT'])
def home():
  return document
serve.route("/", "get", func=home)
serve.route("/doc", "get", func=home)
serve.route("/styles/output.css", "get", file="./styles/output.css")
serve.route("/front.js", "get", file="./front.js")
asyncio.run(serve.start())
