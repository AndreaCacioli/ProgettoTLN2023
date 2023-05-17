runRadicioniTrump: format
	python3 ./Parte2-Radicioni/Trump/TrumpLM.py

runRadicioniWuPalmer: format
	python3 ./Parte2-Radicioni/WSD/WuPalmerTest.py

runRadicioniSemanticDistance: format
	python3 ./Parte2-Radicioni/WSD/SimPathTest.py

runRadicioniLeacockChodrow: format
	python3 ./Parte2-Radicioni/WSD/LeacockChodrowTest.py

runMazzeiEnglish: format
	python3 ./Parte1-Mazzei/EnglishGrammar.py 

runMazzeiKlingon: format
	python3 ./Parte1-Mazzei/Klingon.py 

runCaro1: format
	python3 ./Parte3-DiCaro/Esercitazione1.py

format: 
	clear
	black ./Parte1-Mazzei/*.py ./Parte2-Radicioni/Trump/*.py ./Parte2-Radicioni/WSD/*.py ./Parte3-DiCaro/*.py

