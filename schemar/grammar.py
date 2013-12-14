from pyparsing import Word, oneOf, Optional, QuotedString, alphas, alphanums, printables
from .models import AttributeAlias

#Define Grammars
identifier = Word(alphanums + '_')
def_grammar = oneOf("define def", caseless=True) + identifier
has_one_grammar = identifier + "has one" + identifier + Optional(identifier, None)
has_many_grammar = identifier + "has many" + identifier + Optional(identifier, None)
commit_grammar = "commit" + Word(printables) + Optional(identifier, "mysql")
peek_grammar = "peek" + Optional(identifier, None)
help_grammar = Word("help")
command_grammar = def_grammar | has_one_grammar | has_many_grammar | commit_grammar | peek_grammar | help_grammar

attr_alias = Word(alphas).setParseAction(lambda a: AttributeAlias(a[0]))
attr_literal = QuotedString('"', escChar='\\', multiline=False)
column_def_grammar = identifier + (attr_alias | attr_literal)