#Embedded file name: otp.ai.MagicWordGlobal
from toontown.toonbase import ToonPythonUtil as PythonUtil

class MagicError(Exception):
    pass


def ensureAccess(access, msg = 'Insufficient access'):
    if spellbook.getInvokerAccess() < access:
        raise MagicError(msg)


class Spellbook:

    def __init__(self):
        self.words = {}
        self.currentInvoker = None
        self.currentTarget = None

    def addWord(self, word):
        self.words[word.name.lower()] = word

    def process(self, invoker, target, incantation):
        self.currentInvoker = invoker
        self.currentTarget = target
        word, args = (incantation.split(' ', 1) + [''])[:2]
        try:
            return self.doWord(word, args)
        except MagicError as e:
            return e.message
        except Exception:
            return PythonUtil.describeException(backTrace=1)
        finally:
            self.currentInvoker = None
            self.currentTarget = None

    def doWord(self, wordName, args):
        word = self.words.get(wordName.lower())
        if not word:
            if process == 'ai':
                wname = wordName.lower()
                for key in self.words:
                    if self.words.get(key).access <= self.getInvokerAccess():
                        if wname in key:
                            return 'Did you mean %s' % self.words.get(key).name

            if not word:
                return
        ensureAccess(word.access)
        if self.getTarget() and self.getTarget() != self.getInvoker():
            if self.getInvokerAccess() <= self.getTarget().getAdminAccess():
                raise MagicError('Target must have lower access')
        result = word.run(args)
        if result is not None:
            return str(result)

    def getInvoker(self):
        return self.currentInvoker

    def getTarget(self):
        return self.currentTarget

    def getInvokerAccess(self):
        if not self.currentInvoker:
            return 0
        return self.currentInvoker.getAdminAccess()


spellbook = Spellbook()

class MagicWordCategory:

    def __init__(self, name, defaultAccess = 600):
        self.name = name
        self.defaultAccess = defaultAccess


CATEGORY_UNKNOWN = MagicWordCategory('Unknown')
CATEGORY_USER = MagicWordCategory('Default User', defaultAccess=100)
CATEGORY_VIP = MagicWordCategory('VIP', defaultAccess=250)
CATEGORY_MEDIA = MagicWordCategory('Media', defaultAccess=275)
CATEGORY_COMMUNITY_MANAGER = MagicWordCategory('Community Manager', defaultAccess=300)
CATEGORY_MODERATOR = MagicWordCategory('Moderator', defaultAccess=375)
CATEGORY_CREATIVE = MagicWordCategory('Creative', defaultAccess=390)
CATEGORY_PROGRAMMER = MagicWordCategory('Programmer', defaultAccess=400)
CATEGORY_ADMINISTRATOR = MagicWordCategory('Administrator', defaultAccess=450)
CATEGORY_SYSTEM_ADMINISTRATOR = MagicWordCategory('System Administrator', defaultAccess=500)
CATEGORY_OVERRIDE = MagicWordCategory('OVERRIDE', defaultAccess=900)
MINIMUM_MAGICWORD_ACCESS = CATEGORY_COMMUNITY_MANAGER.defaultAccess

class MagicWord:

    def __init__(self, name, func, types, access, doc):
        self.name = name
        self.func = func
        self.types = types
        self.access = access
        self.doc = doc

    def parseArgs(self, string):
        maxArgs = self.func.func_code.co_argcount
        minArgs = maxArgs - (len(self.func.func_defaults) if self.func.func_defaults else 0)
        args = string.split(None, maxArgs - 1)[:maxArgs]
        if len(args) < minArgs:
            raise MagicError('Magic word %s requires at least %d arguments' % (self.name, minArgs))
        output = []
        for i, (type, arg) in enumerate(zip(self.types, args)):
            try:
                targ = type(arg)
            except (TypeError, ValueError):
                raise MagicError('Argument %d of magic word %s must be %s' % (i, self.name, type.__name__))

            output.append(targ)

        return output

    def run(self, rawArgs):
        args = self.parseArgs(rawArgs)
        return self.func(*args)


class MagicWordDecorator:

    def __init__(self, name = None, types = [str], access = None, category = CATEGORY_UNKNOWN):
        self.name = name
        self.types = types
        self.category = category
        if access is not None:
            self.access = access
        else:
            self.access = self.category.defaultAccess

    def __call__(self, mw):
        name = self.name
        if name is None:
            name = mw.func_name
        word = MagicWord(name, mw, self.types, self.access, mw.__doc__)
        spellbook.addWord(word)
        return mw


magicWord = MagicWordDecorator
