from flask import Flask, request, Response, send_from_directory
import os
import random
from os import path
from flask_cors import CORS
from wand.image import Image
import fontforge
import psMat


app = Flask(__name__)
CORS(app)

SPECIAL_CHARS = set('gjpqy')

def normalizeGlyph(g, letter):
    bb = g.boundingBox()
    dy = bb[3]-bb[1]
    newScale = 800/(dy)
    transforms = []
    if letter in SPECIAL_CHARS:
        print('SPECIAL CASE: ', letter)
        print(bb)
        transforms.append(psMat.translate(-bb[0], -bb[1] - 0.5 * (bb[3] - bb[1])))
    else:
        transforms.append(psMat.translate(-bb[0], -bb[1]))

    if dy > 800:
        transforms.append(psMat.scale(newScale))
    if len(transforms) > 1:
        g.transform(psMat.compose(*transforms))
    else:
        g.transform(transforms[0])
    print(g.boundingBox())
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
    return send_from_directory(dname, 'testfont.ttf', as_attachment=True)
