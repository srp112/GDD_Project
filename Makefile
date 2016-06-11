all: report.pdf

#Question 1
data.csv :
      curl -o data.csv ftp://client_climate@ftp.tor.ec.gc.ca/Pub/Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv

#data.csv: curl -o data.csv ftp://client_climate@ftp.tor.ec.gc.ca/Pub/#Get_More_Data_Plus_de_donnees/Station%20Inventory%20EN.csv
     # python download.py

#Question 2
Plotminmax.png : data.csv MinMax.py
      python MinMax.py data.csv

#Question 3

GDDdata.csv : data.csv GDD_calculate.py
      python GDD_calculate.py GDDdata.csv
      
#Question 4
Plot_accumulatedGDD.png : data.csv cumGDDplot.py
      python cumGDDplot.py data.csv

#Question 5
# Github
      
#Question 6
report.pdf : report.tex plot.png
      pdflatex report.tex
      pdflatex report.tex
     #bibtex report

      pdflatex report.tex
#Question 7
# Presentation 

#Question 8 : it has done (workflow)

#Question 9: Create a testsuite 

#Question 10: adequate documentation

#clean:
#   rm -f report.log report.aux report.pdf
#   rm -f data.csv plot.png
