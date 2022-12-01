import sys
import numpy as np
import random
from numpy.linalg import norm
import syllables
import gensim.downloader as api
import re

def main(topic):
    print("Starting Cleaning...")
    haiku = open('bfbarry.txt', 'r', encoding = 'UTF-8')
    haiku2 = open('poetrnn.txt', 'r', encoding = 'UTF-8')
    haiku3 = open('all_haiku.txt', 'r', encoding = 'UTF-8')

    lines = [re.sub(' +', ' ', line.rstrip()) for line in haiku]
    lines2 = [line.rstrip() for line in haiku2]
    lines3 = [re.sub(r'[^\w\d\s\']+', '', re.sub(' +', ' ', line.rstrip())) for line in haiku3]

    haiku.close()
    haiku2.close()
    haiku3.close()
    print("...Finished Cleaning")

    bank = createBank(lines, lines2)
    
    if topic == "randn":
        new_haiku = generateRand(bank)
    else:
        generate(topic, bank)

    outer(new_haiku)

    return 0

def cleaner(dataset):
    cleaned = []
    return cleaned

def createBank(dataset, dataset2):
    print("Starting Banking...")
    wordBank = {}
    for line in dataset:
        for w in line.split():
            word = w.lower()
            if word not in wordBank:
                wordBank[word] = syllables.estimate(word)
    for line in dataset2:
        for w in line.split():
            word = w.lower()
            if word not in wordBank:
                wordBank[word] = syllables.estimate(word)

    cashout = open('word_syllable.txt', 'w', encoding = 'UTF-8')
    for word in wordBank:
        cashout.write(str(wordBank[word]) + ' | ' + word + "\n")
    cashout.close()
    
    print("...Finished Banking")
    return wordBank

def generate(topic, bank):
    print("Starting Generation...")

    print("Loading Word2Vec...")
    wv = api.load('word2vec-google-news-300')
    print("...Finished Loading")
    vec_top = wv[topic]
    line1 = 5
    line2 = 7
    line3 = 5
    result = []

    while (line1 != 0):
        rank = []
        for word in bank:
            if word == topic or word in result:
                pass
            elif bank[word] <= line1:
                try:
                    vec_word = wv[word]
                    rank.append((word, similarity(vec_top, vec_word), bank[word]))
                except:
                    pass
        topNext = max(rank, key = lambda x: x[1])
        # print(topNext)

        result.append(topNext[0])
        line1 -= topNext[2]

    while (line2 != 0):
        rank = []
        for word in bank:
            if word == topic or word in result:
                pass
            elif bank[word] <= line2:
                try:
                    vec_word = wv[word]
                    rank.append((word, similarity(vec_top, vec_word), bank[word]))
                except:
                    pass
        topNext = max(rank, key = lambda x: x[1])
        # print(topNext)

        result.append(topNext[0])
        line2 -= topNext[2]

    while (line3 != 0):
        rank = []
        for word in bank:
            if word == topic or word in result:
                pass
            elif bank[word] <= line3:
                try:
                    vec_word = wv[word]
                    rank.append((word, similarity(vec_top, vec_word), bank[word]))
                except:
                    pass
        topNext = max(rank, key = lambda x: x[1])
        # print(topNext)

        result.append(topNext[0])
        line3 -= topNext[2]

    print(result)
        
    return 0

def similarity(vec1, vec2):
    return (np.dot(vec1, vec2)) / (norm(vec1) * norm(vec2))

def generateRand(bank):
    print("Starting Generation...")

    print("Loading Word2Vec...")
    wv = api.load('word2vec-google-news-300')
    print("...Finished Loading")
    
    temp = []
    count = 1000

    while (count > 0):
        topic = random.choice(list(bank.keys()))
        # print(topic)
        try:
            vec_top = wv[topic]
            # print(topic, test)
            line1 = 5
            line2 = 7
            line3 = 5
            result = []
            history = {}

            while (line1 != 0):
                rank = []
                for word in bank:
                    if word == topic or word in result:
                        pass
                    elif bank[word] <= line1:
                        try:
                            vec_word = wv[word]
                            score = similarity(vec_top, vec_word)
                            history[word] = score
                            rank.append((word, score, bank[word]))
                        except:
                            pass
                # print(rank)
                topNext = max(rank, key = lambda x: x[1])

                result.append(topNext[0])
                line1 -= topNext[2]
                if (line1 == 0):
                    result.append('/')

            while (line2 != 0):
                rank = []
                for word in history:
                    if word in result:
                        pass
                    elif bank[word] <= line2:
                        try:
                            rank.append((word, history[word], bank[word]))
                        except:
                            pass
                topNext = max(rank, key = lambda x: x[1])

                result.append(topNext[0])
                line2 -= topNext[2]
                if (line2 == 0):
                    result.append('/')

            while (line3 != 0):
                rank = []
                for word in history:
                    if word in result:
                        pass
                    elif bank[word] <= line3:
                        try:
                            rank.append((word, history[word], bank[word]))
                        except:
                            pass
                topNext = max(rank, key = lambda x: x[1])

                result.append(topNext[0])
                line3 -= topNext[2]

            temp.append(result)
            count-= 1
            # print(result, count)
        except:
            pass

    # print(temp)
    return temp

def outer(haiku):
    new_file = open('output.txt', 'w', encoding = 'UTF-8')

    for h in haiku:
        new_file.write('5, 7, 5 | ' + ' '.join(h) + "\n")

    new_file.close()

    return 0


if __name__ == "__main__":
    main(sys.argv[1])