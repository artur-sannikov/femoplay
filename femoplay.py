"""
FemoPlay
A simple game engine for didatic purpose.

Use: python femoplay.py stories/test.story
"""

from collections import namedtuple
import sys

class Answer:
    """Answer plain data structure
    type: str, like 'jmp' or 'scorejmp'
    args: list, the arguments for the type
    keynum: int, the keyboard number for answer selecting
    text: str, the prompt of the answer
    """

    def __init__(self, type, args, keynum, text):
        self.type = type
        self.args = args
        self.keynum = keynum
        self.text = text

class Question:
    """Question plain data structure
    qui: str, question identifier
    title: str, one line title
    text: str, multiline description
    answers: list of Answer
    """

    def __init__(self, qid, title, text, answers):
        self.qid = qid
        self.title = title
        self.text = text
        self.answers = answers

# the special answer for game ending
ANSWER_QUIT = Answer('jmp',["LOSE"], 0, 'Quit the game')

def readfile(fname):
    """
    Get the content of the text file with filename fname as string

    Parameters:
    ===========
    fname: str, the filename

    Returns:
    ========
    content: str, the content of the entire file
    """
    txt = ""
    with open(fname, 'r') as f:
        txt = f.read()
    return txt

def parsequestions(txt):
    """
    Parse the content of a story and create the Question and Answer data
    structure.

    The content of a story must be structured.
    The first two characters of a line can be used as marker:
        'Q:' means to start a Question definition
        'A:' means to start a Answer definition

    Question.
    Q:qid:title
    ... multiline description ...
    A:1:Answer Text:jmp 01
    <Others answers, 9 max>

    When a new Question starts the following lines are the description.
    The description ends when an Answer is defined. At least one.
    The question id must be unique in the story.

    Answer:
    A:keynum:text:cmd arg1 arg2 ...

    keynum must be a digit from 1 to 9. All keynum must be unique for each
    question. The command and the argument are just saved in the answer, not
    checked.

    TODO:
    =====
    * Error managment
    * Check if question id duplicated
    * Check unique keynum in question
    * Check the cmd and args?

    Parameters:
    ===========
    txt: the content of a single story file

    Returns:
    ========
    qtable: dict, {"question_id": Question, ...}
            'START', 'LOSE', 'WIN' keys are guaranteed
    """

    # Parser build as finite state machine

    # STATES
    ERROR = -1
    BEGIN = 0
    NEW_QUESTION = 1
    TEXT_QUESTION = 2
    ANSWER = 3
    SKIP = 4

    qtable = {
            "START": Question("START",
                              "No game to play",
                              "Please, configure the START question",
                              []),
            "LOSE": Question("LOSE",
                              "Game Over!",
                              "I'm sorry, you lose!",
                              []),
            "WIN": Question("WIN",
                              "Mission Completed Successfully",
                              "Bye bye",
                              []),
    }

    state = BEGIN
    # for each line
    for line in txt.split('\n'): #\n is the end of a line

        if state == BEGIN:
            if line.startswith('Q:'):
                state = NEW_QUESTION

        if state == TEXT_QUESTION:
            if line.startswith('Q:'):
                state = NEW_QUESTION
            elif line.startswith('A:'):
                state = ANSWER
            else:
                # q create on NEW_QUESTION
                q.text += line + '\n'

        if state == ANSWER:
            if line.startswith('Q:'):
                state = NEW_QUESTION
            elif len(line) == 0:
                state = SKIP
            else:
                # parse the anwer
                s = line.split(':')
                kn = int(s[1]) #FIXME add check
                if kn <= 0 or kn > 9:
                    state = ERROR
                txt = s[2]
                cmd = s[3]
                scmd = cmd.split(' ')
                t = scmd[0]
                ans = Answer(t, scmd[1:], kn, txt)
                q.answers.append(ans)

        if state == SKIP:
            if line.startswith('Q:'):
                state = NEW_QUESTION
            elif line.startswith('A:'):
                state = ANSWER

        # on row states
        if state == ERROR:
            #FIXME manage error
            print("ERROR")
            break

        if state == NEW_QUESTION:
            s = line.split(':')
            qid = s[1]
            title = s[2]
            q = Question(qid, title, "", [])
            qtable[qid] = q
            state = TEXT_QUESTION
            continue

    return qtable

def say(question, score):
    """
    Print the question and the score

    Parameters:
    ===========
    question: Question
    score: int

    Returns:
    =========
    void
    """
    print("") # blank line
    print("********************%s*********************"%question.title)
    print("Score: ",score)
    print(question.text)

def ask(question, score):
    """
    Print the question and get the answer.

    TODO:
    * Repeat the question if no answer matching

    Parameters:
    ===========
    question: Question
    score: int

    Returns:
    =========
    answer: Answer
    """

    say(question, score)
    print("") # blank line
    print("Possible answers:")
    for ans in question.answers:
        print("[%i] %s"%(ans.keynum, ans.text))

    print("[%i] %s"%(ANSWER_QUIT.keynum, ANSWER_QUIT.text))

    d = input("Your answer: ")
    i = 0
    try:
        i = int(d)
    except:
        pass

    for ans in question.answers:
        if ans.keynum == i:
            return ans

    return ANSWER_QUIT

def answer_exe(ans, score):
    """
    Run the specific code for the type of the answer and update the score
    if necessary.

    TODO:
    * error handling

    Parameters:
    ===========
    ans: Answer
    score: int

    Returns:
    ===========
    qid: str, the next question id to ask
    score: the value of updated score
    """

    if ans.type == 'jmp':
        return ans.args[0], score
    elif ans.type == 'scorejmp':
        #FIXME check integer
        s = int(ans.args[1])
        return ans.args[0], score + s

    return "", score


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Use: python %s file.story"%sys.argv[0])
        exit(1)

    fname = sys.argv[1]

    storytxt = readfile(fname)
    questions = parsequestions(storytxt)

    score = 1
    qid = "START"

    while qid not in ["LOSE", "WIN"]:

        ques = questions[qid]
        answ = ask(ques, score)
        qid, score = answer_exe(answ, score)

        if score <= 0:
            qid = "LOSE"

    ques = questions[qid]
    say(ques, score)
