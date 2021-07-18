import itertools
from os import stat
from collections import Counter
from itertools import chain
from nltk.probability import entropy

from numpy.lib.arraysetops import isin

class VocabEntry(object):
    def __init__(self):
        self.word2id = dict()
        self.unk_id = 3
        self.word2id['<pad>'] = 0
        self.word2id['<s>'] = 1
        self.word2id['</s>'] = 2
        self.word2id['<unk>'] = 3

        self.id2word_ = {v: k for k,v in self.word2id.items()}
    
    def __getitem__(self, word):
        return self.word2id.get(word, self.unk_id)
    
    def __contains__(self, word):
        return word in self.word2id
    
    def __setitem__(self, key, value):
        raise ValueError('vocabulary is readonly')

    def __len__(self):
        return len(self.word2id)
    
    def __repr__(self):
        return 'Vocabulary[size = %d]' % len(self)

    def id2word(self, idx):
        return self.id2word[idx]

    def add(self, word):
        if word not in self:
            wid = self.word2id[word] = len(self) 
            self.id2word_[wid] = word
            return wid
        else:
            return self[word]
    
    def is_unk(self, word):
        return word not in self
    
    def merge(self, other):
        for word in other.word2id:
            self.add(word)
    
    @staticmethod
    def from_corpus(corpus, size, freq_cutoff = 0):
        vocab_entry = VocabEntry()
        word_freq = Counter(chain(*corpus))
        non_singletons = [w for w in word_freq if word_freq[w] > 1]
        singletons = [w for w in word_freq if word_freq[w] == 1]
        print('number of word types: %d, number of word types w/ frequency > 1: %d' % (len(word_freq), len(non_singletons)))
        print('number of singletons: %d' % len(singletons))

        total_appearance_count = 0
        top_k_words = sorted(word_freq.keys(), reverse = True, key = word_freq.get)[:size]
        words_not_included = []
        for word in top_k_words:
            total_appearance_count += word_freq[word]
            if len(vocab_entry) < size:
                if word_freq[word] >= freq_cutoff:
                    vocab_entry.add(word)
                else:
                    words_not_included.append(word)
        print('number of words not included: %s' % len(words_not_included))
        appearance_count = 0
        for word in words_not_included:
            appearance_count += word_freq[word]
        print('total token count: ', total_appearance_count)
        print('unk token count: ', appearance_count)
        return vocab_entry

class Vocab(object):
    def __init__(self, **kwargs):
        self.entries = []
        for key, item in kwargs.items():
            assert isinstance(item, VocabEntry)
            self.__setattr__(key, item)

            self.entries.append(key)
    
    def __repr__(self):
        return 'Vocab(%s)' % (', '.join('%s %swords' % (entry, getattr(self, entry)) for entry in self.entries))