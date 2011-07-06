# coding: utf8

"""
  RuleParser: Tagging Rules Engine
  The engine has the following parts:
    - Rule Sintax: specified on the documentation
    - Parser: implemented in RuleParser.parse_grammar()
    - Engine: implemented in RuleParser.tag()

  IMPORTANT: All input text is a text tree (NLTK style)

"""

#
# TODO:
#  - improve performance using re.compile
#  - exceptions
#  - encoding policy
#  - option to pass regexp flags as parameters to tag method (e.g. re.I)
#

import re
from nltk import Tree
import string
from collections import deque

class RuleParser():
    """ 
    This class implements the Rule Engine.
    """ 
    def __init__(self, grammar_str):
        """ 
        Instantiates a RuleParser Object from a grammar string.
        """
        #parse grammar
        self.rules = self.parse_grammar(grammar_str)

        #common stack
        self.stack = []
        
    
    def parse_grammar(self, grammar_str):
        """
        method that parse a grammar string to obtain an array of consecutive rules
        """
        rules = []
        lines = grammar_str.split('\n')
        for line in lines:
            line = line.strip()
            if line:    
                parts = re.search('([\w\s]+):(.*)', line)
                rule_name = parts.group(1).strip()
                rule_string = parts.group(2).strip()
                rules.append({rule_name : self.from_rule_to_regexp(rule_name, rule_string)})
        return rules

    def tag(self, input_tree):
        """
        Tag an input tree using the rules in parsed grammars.
        """
        #clean input tree:
        input_tree = self.clean(input_tree)
        
        text = self.from_tree_to_text(input_tree)
        #print "INPUT TEXT: "+text
        for rule in self.rules:
            rule_name = rule.keys()[0]
            rule = rule.values()[0]

            matches = re.finditer(rule, text)
            for match in matches:
                match_text = match.group(rule_name)
                #eliminar espacios al principio y al final del matching text,
                #para controlar que cada subarbol <NAME> está bien delimitado
                #en el texto resultante (no se come espacios opcionales):
                match_text = match_text.strip()
                text = string.replace(text, match_text, "<"+rule_name+">")
                #print "TEXT = "+text
                self.stack.append(match_text)

        #print "OUTPUT TEXT : "+text
        output_tree_str = "(S "+self.from_text_to_tree_str(text)+" )"
        #print "OUTPUT TREE STR: "+output_tree_str
        output_tree = Tree.parse(output_tree_str, parse_leaf=self.from_string_token_to_tuple)
        return output_tree
        
        
    def from_rule_to_regexp(self, rule_name, rule_string):
        """
        Translate the whole rule into a regexp
        """
        parts = re.search('([^{]*){([^}]*)}(.*)', rule_string)

        context_left = parts.group(1).strip()
        rule_core = parts.group(2).strip()
        context_right = parts.group(3).strip()

        rule = "%s (?P<%s>%s) %s" % (self.translate(context_left), rule_name, self.translate(rule_core), self.translate(context_right))

        return rule.strip()

    def translate(self, rule_fragment):
        """
        Translate a rule fragment into a regexp
        """
        #constants
        #valid_word = r"[\w&'!\?,\.áéíóúÁÉÍÓÚñÑüÜ\+\-]+"
        #valid_tag = r"[\w&'!\?,\.\+\-]+"
        valid_word = r"[\w\.\?&'!,]+"
        valid_tag = r"[\w]+"
        
        #print "translating rule_fragment = %s" % rule_fragment

        tokens = rule_fragment.split()
        translated_tokens = []
        for token in tokens:
            if token and not token.isspace():
                token = token.strip()
                #print "TOKEN = %s" % token
                #sustituir múltiples espacios por uno sólo:
                token = re.sub('\s+', r'\s', token)

                #sustituir palabras:
                if (re.search(r'"[\?\+\*]$', token)) or ((re.search(r'"#(\d+)\-(\d+)$', token))):
                    token = re.sub('"([^"]*)"', r'(\1/'+valid_tag+r'(/'+valid_tag+r')*\s?)', token)
                else:
                    token = re.sub('"([^"]*)"', r'(\1/'+valid_tag+r'(/'+valid_tag+r')*)', token)
                    
                #sustituir etiquetas:
                if (re.search(r'>[\?\+\*\#]$', token)):
                    token = re.sub('<([^>]*)>', r'(<\1>|('+valid_word+r'(/'+valid_tag+r')*/\1(/'+valid_tag+r')*)\s?)', token)
                else:
                    token = re.sub('<([^>]*)>', r'(<\1>|('+valid_word+r'(/'+valid_tag+r')*/\1(/'+valid_tag+r')*))', token)
                    
                #sustituir operadores #N-N:
                token = re.sub('#(\d+)\-(\d+)', r'{\1,\2}', token)
    
                translated_tokens.append(token)

        translated_fragment = "\s?".join(translated_tokens) 
                
        #hacer opcionales los espacios que siguen a un término opcional:
        #translated_fragment = re.sub('\?\s', r'?\s??', translated_fragment)
        #translated_fragment = re.sub('\{0,(\d+)\}\s', r'{0,\1}\s??', translated_fragment)
        
        #print "translated = %s" % translated_fragment
        
        return translated_fragment

    def from_tree_to_text(self, input_tree):
        """
        Translate a NLTK tree into a tagged text string
        """
        text = ""
        for subtree in input_tree:
            try:
                tree_type = subtree.node
                text += "<%s> " % tree_type
            except:
                word = subtree[0]
                tags = subtree[1]
                tagged_word = word
                for tag in tags:
                    tagged_word += "/%s" % tag
                text += "%s " % tagged_word
        return text.strip()

    def from_text_to_tree_str(self, text):
        """
        Translate from a string tagged text into a NLTK Tree
        """
        tokens = text.split()
        
        #traverse rule list (reversed)
        for rule in reversed(self.rules):
            rule_name = rule.keys()[0]
            rule = rule.values()[0]

            #traverse token list
            i = len(tokens) - 1
            while (i >= 0):
                token = tokens[i]
                match = re.match(r"^<("+rule_name+")>$",token)
                if match: #its a tree
                    tree_name = match.group(1)
                    if tree_name == rule_name:
                        children_str = self.stack.pop()
                        tokens[i] = "(" + tree_name + " " + self.from_text_to_tree_str(children_str)+" )"
                i = i-1
        return " ".join(tokens)    
            

    def from_string_token_to_tuple(self, string_token):
        """
        method that translates a string tagged token into a tuple.
        Example: perro/NN/ANIMAL  ->  ('perro', ['NN', 'ANIMAL'])
        """
        token_match = re.match(r'([^/]*)/(.*)',string_token)
        word = token_match.group(1)
        tags = token_match.group(2).split('/')
        return (word, tags)
        
    def clean (self, tree):
        """
        method that cleans an input tree to avoid forbidden characters in tree words
        """
        return tree
            
