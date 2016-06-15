all: ./data/*.csv MakeMinMaxPlots GetGDD PlotCumGDD OQ2 OQ3 Report

#Question 1
./data/*.csv: download.py cities.txt
	python download.py cities.txt 2012

#Question 2
MakeMinMaxPlots: ./data/*.csv
	python MinMax.py cities.txt 2015

#Question 3
GetGDD: ./data/*.csv
	python GDD_calculate.py cities.txt

#Question 4
PlotCumGDD: GetGDD
	python cumulativeGDDplot.py cities.txt

#Optional Question 2
OQ2: GetGDD
	python GDD_map_Canada.py cities.txt 2015

#Optional Question 3
OQ3: ./data/*.csv
	python GDDTbase.py cities.txt 2015

#Question 6  
Report: report.tex ./plots/
	pdflatex report.tex
	pdflatex report.tex
	pdflatex report.tex

clean:
	rm -rf data
	rm -rf plots
	rm -rf log_download.txt
	rm -rf report.aux
	rm -rf report.log
	rm -rf report.pdf
	rm -rf __pycache__
