import json
import requests

#Headlines are:
# SYNOPSIS
# DISCUSSION
# AVIATION
# BEACHES
# MARINE

class FxStory():
    def __init__(self):
        self.headline = ""
        self.body = ""

    def serialize(self):
        return {
            'headline': self.headline,
            'body': self.body
        }
    
# this parser is written with FXUS66.kmtr in mind
def fxmtrparse(lines,headlines):

    endMark = "&&"
    
    stories = []
    for head in headlines:
        startMark = "."+head+"..."
        storyLines = []
        foundStartmark = False
        foundEndmark = False
        for line in lines:
            if line.startswith(startMark):
                foundStartmark = True
                storyLines.append(line[len(startMark):].strip())
                continue

            if foundStartmark and line.startswith(endMark):
                foundEndmark = True
                break

            if foundStartmark:
                storyLines.append(line.strip())

        if foundStartmark and foundEndmark:
            story = FxStory()
            story.headline = head
            story.body = " ".join(storyLines).strip()
            stories.append(story)
        
    return stories

r = requests.get('http://tgftp.nws.noaa.gov/data/raw/fx/fxus66.kmtr.afd.mtr.txt')
if r.status_code == 200:

    lines = r.text.split('\n')
    manifest = ["SYNOPSIS","DISCUSSION","BEACHES","AVIATION","MARINE"]

    s = fxmtrparse(lines,manifest)

    for each in s:
        filename = "/home/www/weather/"+each.headline + ".json"
        f = open(filename, 'w')
        f.write(json.dumps(each.serialize()))
        f.close()
