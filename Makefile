all: report.pdf

data.csv:
      curl ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv

plot.png: data.csv
      python plot.py  data.csv

report.pdf: report.tex plot.png
      pdflatex report.tex
      pdflatex report.tex
     #bibtex report
      pdflatex report.tex

