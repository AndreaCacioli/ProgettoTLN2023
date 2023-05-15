runRadicioniTrump: format
	python3 ./Parte2-Radicioni/TrumpLM.py

runRadicioniWSD: format
	python3 ./Parte2-Radicioni/WordSenseDisambiguation.py

runMazzeiEnglish: format
	python3 ./Parte1-Mazzei/EnglishGrammar.py 

runMazzeiKlingon: format
	python3 ./Parte1-Mazzei/Klingon.py 

format: 
	clear
	black ./Parte1-Mazzei/*.py ./Parte2-Radicioni/*.py

