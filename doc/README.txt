RULE PARSER
===========


SINTAXIS
========

	NOMBRE_REGLA : contexto { REGLA } contexto

	REGLA está formada por una secuencia de tokens. Los tokens pueden ser de dos tipos:
 
Etiquetas:  <NP>
Palabras:  "perro"
	A las etiquetas y palabras se les pueden aplicar los siguientes operadores: 
Operadores "+", "*" y "?": {“no”? <VB>* <POSITIVO>+}
Cuantificadores finitos (rango) :  {“no” <VB>#1-3 <POSITIVO>}
	El contexto también está formado por tokens: 
Tokens de contexto a derecha e izquierda:  “el” { <NP> } <VP>

	Dentro de cada token (de etiqueta o de palabra) se puede utilizar cualquier expresión regular (excepto el operador finito con llaves {0,4})

Ejemplos de reglas:

4 Tokens genéricos:  4_TOKENS : { <.*>#4-4 }

Extraer emails: EMAIL : { "[\w\d\.]+@[\w\d\.]+\.\w+" }

Snippets: 
	
	NP : {<DT>? <NN>+}
	ME_GUSTA : "me gusta" { <NP> } 
