from document import Document
from server import server
import asyncio
import os
from pympler import asizeof


document = Document()

maindiv = document.createElement("div")
maindiv.className = "flex flex-col gap-2 justify-center items-center min-h-full h-full"
maindiv.innerHTML = f"""
<div class="max-w-sm rounded overflow-hidden shadow-lg">
  <img class="w-full" src="/images/image.jpg" alt="Project Alpha">
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2">Project Alpha</div>
    <p id="para1" class="text-gray-700 text-base">
      What is this?
    </p>
  </div>
  <div class="px-6 pt-4 pb-2">
    <span id="btn1" class="inline-block cursor-pointer bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">Read More</span>
  </div>
</div>
"""

document.append(maindiv)

# mem_usage = memory_usage((document, (), {}))
object_size = asizeof.asizeof(document)
print(f"Memory usage: {object_size / 1024} KB")

btn = document.querySelector("#btn1")
p = document.querySelector("#para1")

def tell(self):
  para = self.document.instanceOf(p)
  button = self.document.instanceOf(btn)
  if para.innerHTML == "What is this?":
    para.innerHTML = "This is Project Alpha!"
    button.innerHTML = "Read Less"
  else:
    para.innerHTML = "What is this?"
    button.innerHTML = "Read More"
  return

btn.onClick = tell

port = int(os.environ.get('PORT', 3000))
serve = server(port)

def home():
  return document

serve.route("/", "get", func=home)
serve.route("/doc", "get", func=home)
serve.route("/styles/output.css", "get", file="./styles/output.css")
serve.route("/front.js", "get", file="./front.js")
serve.route("/images/image.jpg", "get", file="./images/image.jpg")

asyncio.run(serve.start())