from flask import Flask, request, Response, send_from_directory
import os
import random
from os import path
from flask_cors import CORS
from wand.image import Image
import fontforge
import psMat
import sys
from collections import deque

CAP_CHARS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
DOWN_CHARS = set('gjpqy')
UP_CHARS = set('bdfhiklt')
MID_CHARS = set('acemnorsuvwxz')
SPECIAL_CHARS = set('i')
SPECIAL_Y_TRANS = {
    'j': 0.2,
    'u': 0.1,
    '-': -1.5,
    '\'': -0.9,
    '`': -0.9,
}
SPECIAL_Y_SCALE = {
    'i': 0.75,
    '\'': 0.4,
    '`': 0.4,
    '-': 0.6
}

app = Flask(__name__)
CORS(app)

SPECIAL_CHARS = set('gjpqy')

def normalizeGlyph(g, letter):
    bb = g.boundingBox() #compact box that contains the letter
    dy = bb[3]-bb[1]     # xmin,ymin,xmax,ymax
    newScale = 800/(dy)
    transforms = deque()
    #shifting
    if letter in SPECIAL_Y_TRANS:
        transforms.append(psMat.translate(-bb[0], -bb[1] - SPECIAL_Y_TRANS[letter] * (bb[3] - bb[1])))
    elif letter in DOWN_CHARS:
        #print('DOWN CASE: ', letter)
        #print(bb)
        transforms.append(psMat.translate(-bb[0], -bb[1] - 0.35 * (bb[3] - bb[1]))) # 0,0 35% of its height
    else:
        transforms.append(psMat.translate(-bb[0], -bb[1]))

    # if letter in SPECIAL_CHARS:
    #     print('i: ', letter)
    #     print(bb)
    #     transforms.append(psMat.translate(300, 0) )
    # scaling
    if dy > 800:
        transforms.append(psMat.scale(newScale))
    if letter in MID_CHARS and letter not in SPECIAL_Y_SCALE:
        transforms.append(psMat.scale(0.5))
    elif letter in SPECIAL_Y_SCALE:
        transforms.append(psMat.scale(SPECIAL_Y_SCALE[letter]))

    #composing
    while len(transforms) > 1:
        el1 = transforms.popleft()
        el2 = transforms.popleft()
        transforms.appendleft(psMat.compose(el1, el2))
    g.transform(transforms[0])
    print('POST: ', letter)
    bb2 = g.boundingBox()
    g.width = bb2[2]
    g.simplify()
    # g.round()
    # g.cluster(0, 100)
    print(g.boundingBox(), g.width)
    
    return g

@app.route('/svg', methods=['POST'])
def handle_svg():
    with open('test.svg', 'wb') as f:
        f.write(request.data)
    print('Data', request.data)
    return request.data

@app.route('/svg2font', methods=['POST'])
def svg2font():
    font_id = random.randint(0, 10**10)
    dname = f'fontdata-{font_id}'
    os.mkdir(dname)
    data = request.json
    print('Got data: ', data)
    for cname, svg in data.items():
        bin_img = bytes(svg, encoding='utf8')
        with Image(blob=bin_img) as img:
            img.trim()
            img.save(filename=path.join(dname, f'letter_{cname}.svg'))

    font = fontforge.font()
    for ltr in data.keys():
        glyph = font.createMappedChar(ltr)
        glyph.importOutlines(path.join(dname, f'letter_{ltr}.svg'))
        try:
            normalizeGlyph(glyph, ltr)
        except Exception as err:
            print('Caught error: ', err)
    font.generate(path.join(dname, 'testfont.ttf'))
    # os.rmdir(dname)
    return {
        'fontId': font_id
    }

@app.route('/font/<string:font_id>.ttf', methods=['GET'])
def getFont(font_id):
    dname = f'fontdata-{font_id}'
    # with open(path.join(dname, 'testfont.ttf'), 'rb') as f:
    #     data = f.read()
    # return Response(data, mimetype='application/octet-stream')
    return send_from_directory(dname, 'testfont.ttf')
