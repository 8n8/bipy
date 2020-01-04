import bottle
import json
import os


@bottle.get('/')
def getmain():
    return bottle.static_file('index.html', root='.')


def remove_done(imfs, labels):
    return list(set(imfs) - set(labels.keys()))


with open('labels.json') as f:
   labels = json.load(f)

imageFileNames = remove_done(os.listdir('photos'), labels)
counter = 0


@bottle.get('/image')
def getimage():
    global counter
    if counter == len(imageFileNames):
        print("\nALL DONE!\n")
        return
    return bottle.static_file(imageFileNames[counter], root='photos')


@bottle.post('/')
def postmain():
    global counter
    if counter == len(imageFileNames):
        print("\nALL DONE!\n")
        return
    choices = json.loads(str(bottle.request.body.read().decode()))
    print(choices)
    labels[imageFileNames[counter]] = choices
    with open('labels.json', 'w') as f:
        json.dump(labels, f)
    counter += 1
    print(counter)


bottle.run(host='localhost', port=3000, debug=True, server='paste')
