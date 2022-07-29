import nltk
from random import randint


FIRST_WORDS = ['Is', 'Are', 'Was', 'Were', 'Do', 'Does', 'Did', 'Have', 'Has', 'Had']
PLURAL = ['everyone', 'many', 'any']

# 疑問符を見つける / find question marks
def find_question_marks(pos):
    question_marks = []
    for i in range(len(pos)):
        if pos[i][0] == '?':
            question_marks.append(i)

    return question_marks


# 疑問文を見つける / find question sentences
def find_question_sentences(pos, question_marks):
    question_sentences = []

    for qm in question_marks:
        for i in range(qm-1, -1, -1):
            word = pos[i][0]
            if word in ['.', '?']:
                break
            if word in FIRST_WORDS:
                question_sentences.append((i, qm))

    return question_sentences


# 疑問文の解析 / analyse sentences
def define_sentences(pos, question_sentences):
    defined_sentences = []
    for qs in question_sentences:
        verb_flag = False
        subject, s_lock = '', False
        for i in range(qs[0]+1, qs[1]+1):
            word, tag = pos[i][0], pos[i][1]

            #  you, he, they など一般的なもの
            if tag == 'PRP' and not s_lock:
                if word == 'you':
                    subject = 'I'
                elif word == 'I':
                    subject = 'you'
                else:
                    subject = word.lower()
                s_lock = True 

            # 動詞の確認
            if tag[:2] == 'VB':
                verb_flag = True

            # some people, japanese people
            if tag == 'NNS' or word in PLURAL:
                if verb_flag:
                    break
                subject = 'they'

            # 例外(？) Tom and Jerry など
            # 主語の優先度はandの方が高いとする
            if tag == 'CC':
                if verb_flag:
                    break
                subject, s_lock = 'they', True


        if not subject == '':
            start, end = qs[0], qs[1]
            verb = pos[start][0]

            # TODO:主語によって動詞が変化する場合はここで変換する
            # これ以外にもなんかありそう？
            if subject == 'I':
                if verb == 'Are': verb = 'am'
                elif verb == 'Were': verb = 'was'
                else: pass

            defined_sentences.append((start, end, subject, verb))

    return defined_sentences


# 疑問文に対する答え
def create_answer(subject, verb):
    verb = verb.lower()
    yes = randint(0, 1)
    if yes:
        return f"Yes, {subject} {verb}."
    else:
        if verb == 'am':
            return f"No, {subject}'m not."
        else:
            return f"No, {subject} {verb}n't."


# for purple-task HTML用
def display_question_sentence(pos, defined_sentences):
    result = []
    for ds in defined_sentences:
        start, end = ds[0], ds[1]
        sentence = ''
        sentence += pos[start][0]
        for i in range(start+1, end+1):
            if pos[i][1] != '.':
                sentence += f' {pos[i][0]}'
            else:
                sentence += f'{pos[i][0]}'
        result.append(sentence)
    return result


# for purple-task HTML用
def get_result(text):
    try:
      morph = nltk.word_tokenize(text)
      pos = nltk.pos_tag(morph)
    except:
      nltk.download('punkt')
      nltk.download('averaged_perceptron_tagger')
      morph = nltk.word_tokenize(text)
      pos = nltk.pos_tag(morph)

    question_marks = find_question_marks(pos)
    question_sentences = find_question_sentences(pos, question_marks)
    defined_sentences = define_sentences(pos, question_sentences)
    qs = display_question_sentence(pos, defined_sentences)
    res = [create_answer(ds[2], ds[3]) for ds in defined_sentences]

    result = []
    for i in range(len(res)):
        result.append((qs[i], res[i]))

    return result
