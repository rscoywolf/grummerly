from string import punctuation
from flask import Flask, render_template, request
import string
import json

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/result", methods=['POST', 'GET'])
def result():
    inp = request.form.to_dict()
    text = inp['text']
    s = spell(text)
    return render_template("index.html", text=text, suggs=s)


if __name__ == '__main__':
    app.run(debug=True, port=5001)


def spell(s):
    copy = s
    with open('english3.txt') as fh:
        l = []
        for line in fh:
            line = line.rstrip()
            l.append(line)

    with open('58000.txt') as f:
        fifty = []
        for line in f:
            line = line.rstrip()
            fifty.append(line)

    # master = set(l + fifty)

    l2 = []
    s = s.replace('-', ' ')
    s = s.replace('/', ' ')
    s = ''.join(ch for ch in s if ch not in (punctuation or '1234567890'))
    l2.append(s)
    for i in range(len(l2)):
        l2[i] = l2[i].split()

    errors = []
    for i in l2:
        for w in i:
            w = w.lower()
            if w not in l:
                errors.append(w)

    suggs = similar(errors, l, fifty)

    synonyms = syno(copy)

    return (suggs, synonyms)


def similar(l, ind, fifty):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    err = dict()
    for word in l:
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in splits for c in letters if b]
        inserts = [a + c + b for a, b in splits for c in letters]

        plus = []
        for x in splits:
            plus.append(x[0])
            plus.append(x[1])

        all = set(deletes + transposes + replaces + inserts)
        for i in all:
            if i in fifty:
                if word not in err.keys():
                    err[word] = [i]
                else:
                    err[word].append(i)

        if err == {}:
            for i in all:
                if i in ind:
                    if word not in err.keys():
                        err[word] = [i]
                    else:
                        err[word].append(i)
        if err == {}:
            err[word] = ['unknown word!']

    # print(err)
    return err


def syno(s):
    out = dict()
    l2 = ''
    s = s.rstrip()
    s = s.lower()
    s = s.replace('-', ' ')
    s = s.replace('/', ' ')
    s = ''.join(ch for ch in s if ch not in (
        '!"#$%&\'()*+,-/:;<=>?@[\\]^_`{|}~' or '1234567890'))
    l2 += (s) + ' '
    l2 = l2.split('.')
    for i in range(len(l2)):
        l2[i] = l2[i].split()

    toomuch = []
    for i in l2:
        for w in i:
            if i.count(w) >= 3 and w not in toomuch:
                toomuch.append(w)

    with open('en_thesaurus.json') as fh:
        s = fh.read()
        x = json.loads(s)

    for w in toomuch:
        sugs = []
        for i in x:
            if i['word'].lower() == w:
                sugs.append(i['synonyms'][:7])
        sugs2 = []
        for l in sugs:
            sugs2 += l
        sugs2 = set(sugs2)

        if w not in out.keys():
            out[w] = sugs2
        else:
            out[w].append(sugs2)

    return out
