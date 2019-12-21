import bottle


@bottle.get('/static/<filename>')
def getmain(filename):
    return bottle.static_file(filename, root='html')


imageFileNames = os.listdir('photos')
counter = 0


@bottle.get('/image')
def getimage():
    return bottle.static_file(imageFileNames[counter], root='photos')


with open('labels.json') as f:
   labels = json.load(f)


@bottle.post('/')
def postmain():
    labels.append(bottle.request.body.read())
    with open('labels.json', 'w') as f:
        json.dump(labels, f)
    counter += 1
