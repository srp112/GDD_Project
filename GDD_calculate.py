import csv
import os
import argparse as arg

parser = arg.ArgumentParser(description='Accept input and calculate GDD.')
parser.add_argument('csv', metavar='CSV File Name', type=str, help='Complete File Path of Cities File (Required!).')
parser.add_argument('tbase', metavar='Base Temperature', type=float, nargs='?', default=10, help='Base Temperature (default: 10).')
parser.add_argument('tupper', metavar='Upper Temperature', type=float, nargs='?', default=30, help='Upper Temperature (default: 30).')

args = parser.parse_args()
with open(args.csv, 'r') as cf:
    while True:
        line = cf.readline()  
        if line:  
            #pass    # do something here  
            print(line)
            line=line.strip('\n')
            with open('data/'+line+'.csv', 'r') as f:
                with open('data/tmp_'+line+'.csv', 'w') as newfile:
                    writer = csv.writer(newfile, lineterminator='\n')
                    for row in csv.reader(f):
                        if row[0] == 'Year':
                            writer.writerow(row+['GDD'])
                        else:
                            #How to handle missing info in csv file should be discussed
                            if row[3]=='' or row[4]=='':
                                GDD = 0
                            #Use GDD = 0 for missing info here
                            else:
                                upper = min(float(row[3]), args.tupper)
                                lower = float(row[4])
                                GDD = ((upper + lower) / 2) - args.tbase
                                if GDD < 0:
                                    GDD = 0
                            #Round to 2 digit floating number
                            writer.writerow(row+['%.2f' % (GDD)])
            #os.remove('data/'+line+'.csv')
            os.rename('data/tmp_'+line+'.csv', 'data/'+line+'.csv')
        else:  
            break
