all: pdf convert upload

pdf:
	pdflatex gtd.tex

convert:
	python convert.py

upload:
	python upload.py

clean:
	rm *.pdf
	rm *.log
	rm *.aux
	rm -r files