from collections import defaultdict, deque
import random
import logging
import jieba
import Levenshtein

# https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big
# 比預設的字典（三十萬筆）多了二十萬筆，目測加了很多繁體詞彙
jieba.set_dictionary('app/data/dict.txt.zhtw.trimsize')

class MarkovChat(object):
    chain_length = 2
    #chattiness = 0
    max_words = 25
    MESSAGES_TO_GENERATE = 2
    separator = '\x01'
    stop_word = '\x02'
    ltable = defaultdict(list)
    rtable = defaultdict(list)
    #train_data = 'logs/markov_train.txt'

    def __init__(self, train_data, additional_train_data=None, chattiness=0):
        self.train_data = train_data
        self.chattiness = chattiness
        # stop words will be used in load model, so this line should before _load_model
        self.stop_word_list = self._load_stop_word_list('app/data/stopwords.txt')
        self._load_model(self.train_data)
        logging.info("MarkovChat: load %s", self.train_data)
        if additional_train_data:
            for model in additional_train_data:
                self._load_model(model)
                logging.info("MarkovChat: load %s", model)


    def _load_stop_word_list(self, file_path):
        stop_word_list = [line.strip() for line in open(file_path, 'r').readlines()]
        return stop_word_list


    def _simple_split_message_chinese(self, message):
        words_generator = jieba.cut(message, cut_all=False)
        words = [w for w in words_generator if w not in self.stop_word_list]
        return words


    def _split_message_chinese(self, message):
        words_generator = jieba.cut(message, cut_all=False)
        words = [w for w in words_generator if w not in self.stop_word_list]
        if len(words) > self.chain_length:
            words.append(self.stop_word)
            words = [self.stop_word, self.stop_word] + words
            for i in range(len(words) - self.chain_length):
                list_words = words[i:i + self.chain_length + 1]
                out = []
                # remove stop word
                for s in list_words:
                    if s == self.stop_word:
                        out.append(' ')
                    else:
                        out.append(s)
                yield out

    def _split_message(self, message):
        # split the incoming message into words, i.e. ['what', 'up', 'bro']
        words = message.split()

        # if the message is any shorter, it won't lead anywhere
        if len(words) > self.chain_length:

            # add some stop words onto the message
            # ['what', 'up', 'bro', '\x02']
            words.append(self.stop_word)
            words = [self.stop_word, self.stop_word] + words

            # len(words) == 4, so range(4-2) == range(2) == 0, 1, meaning
            # we return the following slices: [0:3], [1:4]
            # or ['what', 'up', 'bro'], ['up', 'bro', '\x02']
            for i in range(len(words) - self.chain_length):
                yield words[i:i + self.chain_length + 1]

    def _generate_message(self, seed):
        gen_words = deque(seed)

        for _ in range(self.max_words//2):
            lwords = gen_words[0], gen_words[1]
            rwords = gen_words[-2], gen_words[-1]
            lkey = self.separator.join(lwords).lower()
            rkey = self.separator.join(rwords).lower()
            oldlen = len(gen_words)

            if gen_words[0] != self.stop_word and lkey in self.ltable:
                next_word = random.choice(self.ltable[lkey])
                gen_words.appendleft(next_word)

            if gen_words[-1] != self.stop_word and rkey in self.rtable:
                next_word = random.choice(self.rtable[rkey])
                gen_words.append(next_word)

            if oldlen == len(gen_words):
                break

        last_ascii = True
        output = ""
        for word in gen_words:
            if ord(word[0]) < 128 and last_ascii == False:
                output += " "
                output += word
                last_ascii = True
            elif ord(word[0]) >= 128 and last_ascii == True:
                output += " "
                output += word
                last_ascii = False
            elif ord(word[0]) < 128:
                output += word
                last_ascii = True
            elif ord(word[0]) >= 128:
                output += word
                last_ascii = False
        output = " ".join(output.split()).strip(self.stop_word + " ") # remove trailing space
        #return ' '.join(gen_words).strip('\x02 ')
        return output

    def log(self, msg, chattiness=None):
        if not chattiness:
            chattiness = self.chattiness
        # speak only when spoken to, or when the spirit moves me
        #if msg.startswith('!') or 'http://' in msg or not msg.count(' '):
        if msg.startswith('!') or 'http://' in msg or 'https://' in msg:
            return
        if len(msg) < 4:
            logging.warning("input msg too short(len=%s)", len(msg))
            return

        with open(self.train_data, 'a+') as fp:
            fp.write(msg + "\n")

        messages = []
        for words in self._split_message_chinese(msg):
            # if we should say something, generate some messages based on what
            # was just said and select the longest, then add it to the list

            # 生成五次句子，沒有比原本長的就丟掉，然後再選最不相似的
            best_message = msg
            best_similarity = 1.0
            for _ in range(self.MESSAGES_TO_GENERATE):
                generated = self._generate_message(words)
                logging.info("jeiba '%s' => '%s'", " ".join(words), generated)
                if generated in msg:
                    logging.info("skip, just substring")
                    continue
                generated_similarity = Levenshtein.ratio(msg, generated)
                best_similarity = Levenshtein.ratio(msg, best_message)
                if generated_similarity < best_similarity:
                    best_message = generated
                    best_similarity = generated_similarity
                else:
                    logging.info(
                        "predicted msg similarity %s(%s) >= %s(%s), skip",
                        generated, generated_similarity, best_message, best_similarity
                    )
                    continue

            if len(best_message) < 5:
                logging.info("skip, less then 5 char (%s)", best_message)
                continue
            else:
                messages.append((best_message, best_similarity))
                logging.info("append '{}' to candidate".format(best_message))

        self._incremental_train(msg)

        if random.random() >= chattiness:
            pass
        if messages:
            sorted(messages, key=lambda element: element[1], reverse=True)
            return messages[0](0)
        else:
            return ''

    def _incremental_train(self, msg):
        for words in self._split_message_chinese(msg):
            # grab everything but the last word
            lkey = self.separator.join(words[1:]).lower()
            rkey = self.separator.join(words[:-1]).lower()

            # add the last word to the set
            self.ltable[lkey].append(words[0])
            self.rtable[rkey].append(words[-1])

    def random_chat(self):
        key = random.choice(self.rtable.keys())
        words = key.split(self.separator)
        return self._generate_message(words)

    def chat(self, msg):
        msg = msg.lower()
        words = list(self._simple_split_message_chinese(msg))
        logging.info('chat: %s', words)
        if len(words) == 1:
            keys = []
            word = words[0]
            for k, v in self.rtable.items():
                if k.endswith(word):
                    keys.extend(v)
            if keys:
                k = random.choice(keys)
                words.append(k)
        if len(words) == 1:
            keys = []
            word = words[0]
            for k, v in self.ltable.items():
                if k.startswith(word):
                    keys.extend(v)
            if keys:
                k = random.choice(keys)
                words = [k] + words
        if len(words) < 2:
            return ""

        all_msgs = []
        for ctx in zip(words, words[1:]):
            messages = [self._generate_message(ctx) for _ in range(3)]
            all_msgs.extend(messages)

        all_msgs = [m for m in all_msgs if m.lower() not in msg]
        if not all_msgs:
            return ""
        return "(๑•̀ω•́)ノ" + random.choice(all_msgs)

    def _load_model(self, filename):
        try:
            with open(filename, 'r+') as fp:
                lines = fp.readlines()
        except IOError:
            lines = []

        lines = list(set(lines))
        for line in lines:
            self._incremental_train(line)
