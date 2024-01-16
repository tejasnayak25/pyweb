# "!DOCTYPE html"

data = "from document import HTMLElement\n"

tags = ["abbreviation","acronym","address","anchor","applet","area","article","aside","audio","base","basefont","bdi","bdo","bgsound","big","blockquote","body","bold","break","button","caption","canvas","center","cite","code","colgroup","column","comment","data","datalist","dd","define","delete","details","dialog","dir","div","dl","dt","embed","fieldset","figcaption","figure","font","footer","form","frame","frameset","head","header","heading","hgroup","hr","html","Iframes","image","input","ins","isindex","italic","kbd","keygen","label","legend","list","main","mark","marquee","menuitem","meta","meter","nav","nobreak","noembed","noscript","object","optgroup","option","output","p","param","phrase","pre","progress","q","rp","rt","ruby","s","samp","script","section","small","source","spacer","span","strike","strong","style","sub", "sup","summary","svg","table","tbody","td","template","tfoot","th","thead","time","title","tr","track","tt","underline","var","video","wbr","xmp"]

for tag in tags:
    code = f"""
class {tag.capitalize()}(HTMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__("{tag}", *args, **kwargs)
"""
    data += f"\n{code}"

file = open("tags_dict.py", "w")
file.write(data)