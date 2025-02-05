"""
PyTest e' la libreria che gestisce i test in python.
Si puo' eseguire come uno script, e scannerizza tutto il progetto in cerca di package che iniziano con "test".
Se trova uno di questi package, esegue tutti i file che iniziano con "test" al suo interno.
I test si possono quindi dividere in diversi package in base alle parti dell'agente che si vogliono testare singolarmente
e fanno al loro interno degli assert per controllare che tutto vada come ci si aspetta.
"""

def test_prova() -> None:
    assert 1 == 1