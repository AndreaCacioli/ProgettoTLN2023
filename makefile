runRadicioniTrump: format
	python3.9 ./Parte2-Radicioni/Trump/TrumpLM.py

runRadicioniWuPalmer: format
	python3.9 ./Parte2-Radicioni/WSD/WuPalmerTest.py

runRadicioniSemanticDistance: format
	python3.9 ./Parte2-Radicioni/WSD/SimPathTest.py

runRadicioniLeacockChodrow: format
	python3.9 ./Parte2-Radicioni/WSD/LeacockChodrowTest.py

runRadicioniSemCor: format
	python3.9 ./Parte2-Radicioni/WSD/SemCorTest.py

runMazzeiEnglish: format
	python3.9 ./Parte1-Mazzei/EnglishGrammar.py 

runMazzeiKlingon: format
	python3.9 ./Parte1-Mazzei/Klingon.py 

runCaro1: format
	python3.9 ./Parte3-DiCaro/Esercitazione1.py

runCaro2: format
	python3.9 ./Parte3-DiCaro/Esercitazione2.py

runCaro3: format
	python3.9 ./Parte3-DiCaro/Esercitazione3.py

runCaro4: format
	python3.9 ./Parte3-DiCaro/Esercitazione4.py

runCaro5: format
	python3.9 ./Parte3-DiCaro/Esercitazione5.py

runCaro6: format
	python3.9 ./Parte3-DiCaro/Esercitazione6.py

format: 
	clear
	black ./Parte1-Mazzei/*.py ./Parte2-Radicioni/Trump/*.py ./Parte2-Radicioni/WSD/*.py ./Parte3-DiCaro/*.py

