import string
import json

from string import punctuation
class oops(Exception):
    pass


def spell(s):
    copy = s
    #synonyms = syno(check)
    with open('english3.txt') as fh:
        l= []
        for line in fh:
            line = line.rstrip()
            l.append(line)
        #print(l)
    
    l2 = []
    s = s.replace('-', ' ')
    s = s.replace('/', ' ') 
    #print(type(line))
    s = ''.join(ch for ch in s if ch not in (punctuation or '1234567890'))
    #print(line)
    l2.append(s)
    #print(l2)
    #s = file.read()
    for i in range(len(l2)):
        l2[i] = l2[i].split()
    
    errors = []
    for i in l2:
        for w in i:
            w = w.lower()
            if w not in l:
                errors.append(w)

    print(errors)




    suggs = similar(errors, l)

    synonyms = syno(copy)

    return suggs





    #syno('sample.txt', 'english3.txt')
    #return similar(errors, l)

def similar(l, ind):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    err = dict()
    for word in l:
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        #print(splits)
        deletes = [a + b[1:] for a, b in splits if b]
        #print(deletes)
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        #print(transposes)
        replaces   = [a + c + b[1:] for a, b in splits for c in letters if b]
        #print(replaces)
        inserts    = [a + c + b     for a, b in splits for c in letters]
        #print(inserts)
        
        
        plus = []
        for x in splits:
            plus.append(x[0])
            plus.append(x[1])

        #all = set(deletes + transposes + replaces + inserts + plus)
        all = set(deletes + transposes + replaces + inserts)
        #print(all)
        for i in all:
            if i in ind:
                if word not in err.keys():
                    err[word] = [i]
                else:
                    err[word].append(i)
   
        #print('functioning' in all)
    print(err)
    return err


def syno(s):
    out = dict()
    l2 = ''
    s = s.rstrip()
    s = s.lower()
    s = s.replace('-', ' ')
    s = s.replace('/', ' ')
    s = ''.join(ch for ch in s if ch not in ('!"#$%&\'()*+,-/:;<=>?@[\\]^_`{|}~' or '1234567890'))
    #print(s)
    l2 += (s) + ' '
    l2 = l2.split('.')
    for i in range(len(l2)):
        l2[i] = l2[i].split()

        #print(l2)
    toomuch = []
    for i in l2:
        for w in i:
            if i.count(w) >=3 and w not in toomuch:
                toomuch.append(w)
                #print('suggest something else for: ' + w)


    with open('en_thesaurus.json') as fh:
        s = fh.read()
        x = json.loads(s)
        #print(x)
    
    for w in toomuch:
        sugs = []
        for i in x:
            if i['word'].lower() == w:
                sugs.append(i['synonyms'])
                
                
        if w not in out.keys():
            out[w] = sugs
        else:
            out[w].append(sugs)

            #if i['word'].lower() == w:
               # sugs.append(i['synonyms'])

        #print('for ' + w + ' suggest: ' + str(sugs))
    
    print(out)
    return out


#syno('sample.txt', 'english3.txt')


#spell('sample.txt')

spell("First sentence. Second sentnce with much space before period and one spelling error   \n  " + '\n' + "      . THIRD SENTENCE ALL-CAPS WITH A HYPHEN. Fourth sentence thankless uses the word thankless three or more times thankless thankless also no period at end. Thankful, Thankful, Thankful.")
