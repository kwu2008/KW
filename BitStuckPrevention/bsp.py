import sys
import os
import csv

class BSP:

    fileSrcName = 'S-503000-523000.csv'
    fileSrcPath = ''
    fileNormName = 'S-503000-523000-normalized.csv'
    fileNormPath = ''
    fileEmaName = 'S-503000-523000-Ema.csv'
    fileEmaPath = ''
    fileAnaName = 'S-503000-523000-Analysis.csv'
    fileAnaPath = ''
    cvsHeader = ''
    cvsCurrentLine = {}
    lastTimeStamp = -1.0


    def __init__(self):

        print('BSP.__init__')

        cwd = os.path.dirname(os.path.realpath(__file__))

        self.fileSrcPath = os.path.join(cwd, self.fileSrcName)
        self.fileNormPath = os.path.join(cwd, self.fileNormName)
        self.fileEmaPath = os.path.join(cwd, self.fileEmaName)
        self.fileAnaPath = os.path.join(cwd, self.fileAnaName)


    def NormalizeDataAndSave(self):
 
        print('BSP.NormalizeDataAndSave')

        with open(self.fileNormPath, 'w', newline='') as fileNorm:

            with open(self.fileSrcPath, 'r') as fileSrc:
                csvReader = csv.DictReader(fileSrc, delimiter=',')
                lineIdx = -1
                for line in csvReader:

                    lineIdx += 1

                    if lineIdx == 0:

                        print(f'Scr column names are {", ".join(line)}')

                        csvWriter = csv.DictWriter(fileNorm, fieldnames=line)
                        csvWriter.writeheader()

                    self.WriteToNormFile(csvWriter, line)


        print(f'Src file has {lineIdx+1} lines.')
 

    def WriteToNormFile(self, csvWriter, line):

        if self.lastTimeStamp < 0:
            self.lastTimeStamp = float(line['TIME_1900'])
            return

        timeStamp = float(line['TIME_1900'])
        deltaSeconds = (timeStamp - self.lastTimeStamp) * (24 * 60 * 60)
        
        if deltaSeconds >= 1.0:
            csvWriter.writerow(line)
            self.lastTimeStamp = -1.0 
        

    def CalculateEmaAndSave(self):
 
        print('BSP.CalculateEmaAndSave')

        with open(self.fileEmaPath, 'w', newline='') as fileEma:

            with open(self.fileNormPath, 'r') as fileNorm:
                csvReader = csv.DictReader(fileNorm, delimiter=',')
                lineIdx = -1
                for line in csvReader:

                    lineIdx += 1

                    if lineIdx == 0:

                        print(f'Norm column names are {", ".join(line)}')

                        line['EMA'] = '0'

                        print(f'Ema column names are {", ".join(line)}')

                        csvWriter = csv.DictWriter(fileEma, fieldnames=line)

                        csvWriter.writeheader()

                    self.WriteToEmaFile(csvWriter, line)


        print(f'Norm and Ema file has {lineIdx+1} lines.')


    def WriteToEmaFile(self, csvWriter, line):
 
        ema = float(line['RPPV'])
 
        line['EMA'] = str(ema)
        
        csvWriter.writerow(line)



    def AnalyzeBitStuck(self):

        print('BSP.AnalyzeBitStuck')

        with open(self.fileAnaPath, 'w', newline='') as fileAna:

            with open(self.fileEmaPath, 'r') as fileEma:
                csvReader = csv.DictReader(fileEma, delimiter=',')
                lineIdx = -1
                for line in csvReader:

                    lineIdx += 1

                    if lineIdx == 0:

                        print(f'Ema column names are {", ".join(line)}')

                        line['BIT_STUCK'] = '0'

                        print(f'Ana column names are {", ".join(line)}')

                        csvWriter = csv.DictWriter(fileAna, fieldnames=line)

                        csvWriter.writeheader()

                    self.WriteToAnaFile(csvWriter, line)


    def WriteToAnaFile(self, csvWriter, line):
 
        line['BIT_STUCK'] = 'not_implemented'
        
        csvWriter.writerow(line)



def Main():

    print('Main')

    bsp = BSP()

    bsp.NormalizeDataAndSave()

    bsp.CalculateEmaAndSave()
    
    bsp.AnalyzeBitStuck()

 

if __name__ == '__main__':
        Main()


