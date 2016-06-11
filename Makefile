all: report.pdf

data.csv:

plot.png: data.csv
      python plot.py  data.csv

report.pdf: report.tex plot.png
      pdflatex report.tex
      pdflatex report.tex
     #bibtex report
      pdflatex report.tex

