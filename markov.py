import random

def sentence_reader(filename):

    sentence = ''
    for row in open(filename, 'r'):
        words = row.split(' ')
        for word in words:
            if '.' in word:
                sentence = sentence + clean_word(word)
                yield sentence
                sentence = ''
            else:
                sentence = sentence + clean_word(word) + ' '


def clean_word(next_word):

    return next_word.replace('_','').replace('"','').replace('“','').replace('”','').replace(' ','')


def corpus(filename):

    first_words = {}
    last_words = {}
    words = {}

    reader = sentence_reader(filename)
    for line in reader:
        sentence = line.replace('\n','')
        sentence_words = sentence.split(' ')
        if len(sentence_words) == 1:
            continue
        first_word = sentence_words[0]
        if first_word in first_words:
            first_words[first_word] = first_words[first_word] + 1
        else:
            first_words[first_word] = 1

        for index in range(0, len(sentence_words)-1):
            word = sentence_words[index]
            next_word = sentence_words[index + 1]
            ending = 'y' if '.' in next_word else 'n'
            if word in words:
                next_words = words[word]
                if next_word in next_words:
                    next_words[next_word] = next_words[next_word] + 1
                else:
                    next_words[next_word] = 1
            else:
                words[word] = {next_word:1}
            if not next_word in last_words:
                last_words[next_word] = {'y':0,'n':0}
            last_words[next_word][ending] = last_words[next_word][ending] + 1

    return words, first_words, last_words


def pick_first_word(first_words):

    total = 0
    for k,e in first_words.items():
        total = total + e

    index = random.randint(0,total-1)

    running_total = 0
    for k,e in first_words.items():
        if index >= running_total and index <= (running_total + e):
            return k
        running_total = running_total + e


def ending(next_word, last_words):

    total = last_words[next_word]['y'] + last_words[next_word]['n']
    if last_words[next_word]['y'] == 0:
        return False
    if last_words[next_word]['n'] == 0:
        return True
    chance = random.randint(0, total-1)
    return chance < last_words[next_word]['y']


def generate_sentence(words, first_words, last_words):

    first_word = pick_first_word(first_words)

    sentence = first_word

    word = first_word
    while True:
        next_words = words[word]
        next_word = pick_first_word(next_words)
        sentence = sentence + ' ' + next_word
        if ending(next_word, last_words):
            break
        word = next_word

    return sentence

def markov(filename):

    words, first_words, last_words = corpus(filename)

    # print(first_words)
    # print(words)
    # print(last_words)

    for index in range(0,10):
        print(generate_sentence(words, first_words, last_words).strip())



if __name__ == '__main__':
    markov('texts/war-of-the-worlds-hg-wells.txt')
    # markov('texts/one-sentence.txt')
    # markov('texts/one-paragraph.txt')