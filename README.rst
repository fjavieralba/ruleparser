RULE PARSER
===========

  Tagging Rules Engine written in Python.

  The engine has the following parts:
    
    * Rule Syntax: specified on the documentation
    * Rule Parser: implemented in RuleParser.parse_grammar()
    * Tagging Engine: implemented in RuleParser.tag()

  IMPORTANT: All input text is a text tree (NLTK style) with a modification: each token can have one or more tags.
  EVERY token must be tagged, at least with the empty string ``''``


SYNTAX
========

Rule structure
--------------
::

	RULE_NAME : context { RULE } context

``RULE`` is a sequence of tokens. There can be two types of tokens:
 
  * Tags:  ``<NP>``
  * Words: ``"dog"``

Operators
---------

The following operators can be applied to both tags and words:

  * Operators: ``+``, ``*`` and ``?``::
        
        {“not”? <VB>* <POSITIVE>+}

  * Finite quantifiers (ranges)::
  
        {“not” <VB>#1-3 <POSITIVE>}
	
Context
--------

Context is also a sequence of tokens.
 
Example: Context tokens on both left and right::

  “the” { <NP> } <VP>

Inside each token (tag or word) any regular expression can be used (except the 
finite quantifier within curly brackets, e.g: {0,4})

Examples of rules:

  * 4 generic tokens::
      
      4_TOKENS : { <.*>#4-4 }

  * Extract emails::
      
      EMAIL : { "[\w\d\.]+@[\w\d\.]+\.\w+" }

  * Snippets:: 

      NP : {<DT>? <NN>+}
      I_LIKE : "i like" { <NP> } 
