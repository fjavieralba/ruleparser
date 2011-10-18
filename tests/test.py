# coding: utf-8

import ruleparser
import unittest
from nltk import Tree

class TestBasic(unittest.TestCase):

    def setUp(self):
        self.text = [('el', ['DT']), ('perro', ['NN', 'ANIMAL']), ('ladra', ['VB']), ('al', ['DT']), ('gato', ['NN', 'ANIMAL'])]

    def test_simple_tags(self):
        grammar = "ANIMAL : {<ANIMAL>}"
        rp = ruleparser.RuleParser(grammar)

        expected = Tree.parse("(S el/DT (ANIMAL perro/NN/ANIMAL) ladra/VB al/DT (ANIMAL gato/NN/ANIMAL))", parse_leaf=rp.from_string_token_to_tuple)
        result = rp.tag(self.text)
        self.assertEqual(result, expected)

       
    def test_simple_words(self):
        grammar = """
                     PERRO : {"el" "perro"}
                     GATO : {"al" "gato"}
                  """
        rp = ruleparser.RuleParser(grammar)

        expected = Tree.parse("(S (PERRO el/DT  perro/NN/ANIMAL) ladra/VB (GATO al/DT gato/NN/ANIMAL))", parse_leaf=rp.from_string_token_to_tuple)
        result = rp.tag(self.text)
        self.assertEqual(result,expected)
    
    def test_context_left(self):
        grammar = ' PERRO : <DT> {"perro"}'
        rp = ruleparser.RuleParser(grammar)
        expected = Tree.parse("(S el/DT (PERRO perro/NN/ANIMAL) ladra/VB al/DT gato/NN/ANIMAL)", parse_leaf=rp.from_string_token_to_tuple)
        result = rp.tag(self.text)
        self.assertEqual(result,expected)

    def test_context_right(self):
        grammar = 'LADRA : {"ladra"} "al" '
        rp = ruleparser.RuleParser(grammar)
        expected = Tree.parse("(S el/DT perro/NN/ANIMAL (LADRA ladra/VB) al/DT gato/NN/ANIMAL)", parse_leaf=rp.from_string_token_to_tuple)
        result = rp.tag(self.text)
        self.assertEqual(result,expected)

    def test_context_both(self):
        grammar = 'LADRA :"perro" {"ladra"} <DT>'
        rp = ruleparser.RuleParser(grammar)
        expected = Tree.parse("(S el/DT perro/NN/ANIMAL (LADRA ladra/VB) al/DT gato/NN/ANIMAL)", parse_leaf=rp.from_string_token_to_tuple)
        result = rp.tag(self.text)
        self.assertEqual(result,expected)

    def test_operator_interrog_word(self):
        grammar = 'ANIMAL : {"el"? <ANIMAL>}'
        rp = ruleparser.RuleParser(grammar)
        expected = Tree.parse("(S (ANIMAL el/DT perro/NN/ANIMAL) ladra/VB al/DT (ANIMAL gato/NN/ANIMAL))", parse_leaf=rp.from_string_token_to_tuple)

    def test_operator_interrog_tag(self):
        text = [('Spike', ['NN', 'ANIMAL']), ('ladra', ['VB']), ('al', ['DT']), ('gato', ['NN', 'ANIMAL'])]
        grammar = 'ANIMAL : {"el"? <ANIMAL>}'
        rp = ruleparser.RuleParser(grammar)
        expected = Tree.parse("(S (ANIMAL el/DT perro/NN/ANIMAL) ladra/VB al/DT (ANIMAL gato/NN/ANIMAL))", parse_leaf=rp.from_string_token_to_tuple)

    def test_numerals(self):
        text = [('esto', ['DT']),('es', ['VB']),('muy', ['ADV']), ('muy', ['ADV']), ('muy', ['ADV']), ('bonito', ['ADJ'])]
        grammar = 'MUYx3 : {"muy"#3-3}'
        rp = ruleparser.RuleParser(grammar)
        expected = Tree.parse("(S esto/DT es/VB (MUYx3 muy/ADV muy/ADV muy/ADV) bonito/ADJ)", parse_leaf=rp.from_string_token_to_tuple)
        
class TestAdvanced(unittest.TestCase):

    def setUp(self):
        self.text = [('Real_Madrid',['NN','NE', 'Equipo_Futbol']), ('y',['CONJ']), ('F.C._Barcelona',['NN','NE','Equipo_Futbol']), ('disputan',['VB']), ('hoy',['ADV']), ('la',['DT']), ('final',['NN']), ('de',['PP']), ('la',['DT']), ('Copa_del_Rey',['NN','NE','Evento'])]

    def test_cascaded_rules(self):
        grammar = """
                  NP : {<DT>? <NN>+}
	          VP : {<VB> <ADV>}
                  """

        rp = ruleparser.RuleParser(grammar)
        expected = Tree.parse("(S (NP Real_Madrid/NN/NE/Equipo_Futbol) y/CONJ (NP F.C._Barcelona/NN/NE/Equipo_Futbol) (VP disputan/VB hoy/ADV) (NP la/DT final/NN) de/PP (NP la/DT Copa_del_Rey/NN/NE/Evento))", parse_leaf=rp.from_string_token_to_tuple)
        result = rp.tag(self.text)
        self.assertEqual(result,expected)

    def test_cascaded_rules_2(self):
        grammar = """
                  EQUIPOS : {<Equipo_Futbol> <CONJ> <Equipo_Futbol>}
                  PARTIDO : {<EQUIPOS> <VB>}
                  """
        rp = ruleparser.RuleParser(grammar)
        expected = Tree.parse("(S (PARTIDO (EQUIPOS Real_Madrid/NN/NE/Equipo_Futbol y/CONJ F.C._Barcelona/NN/NE/Equipo_Futbol) disputan/VB) hoy/ADV la/DT final/NN de/PP la/DT Copa_del_Rey/NN/NE/Evento)", parse_leaf=rp.from_string_token_to_tuple)
        result = rp.tag(self.text)
        self.assertEqual(result,expected)

    def test_context_rules(self):
         self.text = [('He',['VB']), ('estudiado',['VB']), ('en',['ADV']), ('la',['DT']), ('Universidad',['NN']), ('Complutense',['NN']), ('y',['CONJ']), ('he',['VB']), ('trabajado',['VB']), ('en',['ADV']), ('Yahoo!',['NN']), ('durante',['ADV']), ('2',['NN']), ('años',['NN'])]
         grammar = """
                      EMPRESA : "trabajado" "en" {<NN>+}
                      UNIVERSIDAD : "estudiado" "en" <DT>? {<NN>+}
                      TECNOLOGIA : "trabajado" "con" {<.*>}
                   """
         rp = ruleparser.RuleParser(grammar)
         expected = Tree.parse("(S He/VB estudiado/VB en/ADV la/DT (UNIVERSIDAD Universidad/NN Complutense/NN) y/CONJ he/VB trabajado/VB en/ADV (EMPRESA Yahoo!/NN) durante/ADV 2/NN años/NN)", parse_leaf=rp.from_string_token_to_tuple)
         result = rp.tag(self.text)
         self.assertEqual(result,expected)

    def test_repetitive_rules(self):
         self.text = [('He',['VB']), ('estudiado',['VB']), ('en',['ADV']), ('la',['DT']), ('Universidad',['NN']), ('Complutense',['NN']), ('y',['CONJ']), ('he',['VB']), ('trabajado',['VB']), ('en',['ADV']), ('Yahoo!',['NN']), ('durante',['ADV']), ('2',['NN']), ('años',['NN'])]
         grammar = """
                      UNIVERSIDAD : {"universidad"}
                      UNIVERSIDAD : {"complutense"}
                      UNIVERSIDAD : {<UNIVERSIDAD> <UNIVERSIDAD>}
                   """
         rp = ruleparser.RuleParser(grammar)
         expected = Tree.parse("(S He/VB estudiado/VB en/ADV la/DT (UNIVERSIDAD (UNIVERSIDAD Universidad/NN) (UNIVERSIDAD Complutense/NN)) y/CONJ he/VB trabajado/VB en/ADV Yahoo!/NN durante/ADV 2/NN años/NN)", parse_leaf=rp.from_string_token_to_tuple)
         result = rp.tag(self.text)
         self.assertEqual(result,expected)

if __name__ == '__main__':
    unittest.main()
