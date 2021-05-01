import sys
import os
import csv

class BitStuckDetect:

    fileSrcName = 'S-503000-523000.csv'
    fileSrcPath = ''
    fileNormName = 'S-503000-523000-normalized.csv'
    fileNormPath = ''
    fileEmaName = 'S-503000-523000-Ema.csv'
    fileEmaPath = ''
    fileAnaName = 'S-503000-523000-Analysis.csv'
    fileAnaPath = ''
    lastTimeStamp = -1.0
    normRppvList = []

    emaCoeff = 0.1  # 10%

    ema = -10001.0
    emaDroppingTimeThreshold = 60.0  # in seconds
    emaDroppingStartTimeStamp = -1.0
    emaRisingStartTimeStamp = -1.0
    bitStuck = False

    seriesRPPV = []
    seriesEMA = []
    seriesTIME1900 = []
    seriesTime = []
    seriesBITSTUCKDETECT = []


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
            self.normRppvList = []
            self.normRppvList.append(float(line['RPPV']))
            return

        timeStamp = float(line['TIME_1900'])
        deltaSeconds = (timeStamp - self.lastTimeStamp) * (24 * 60 * 60)

        self.normRppvList.append(float(line['RPPV']))
        
        if deltaSeconds >= 1.0:
            line['RPPV'] = str(int(sum(self.normRppvList)/len(self.normRppvList)))
            line['CMPP'] = str(round(float(line['CMPP']), 2))
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
 
        rppv = float(line['RPPV'])

        if self.ema < 0:
            self.ema = rppv
        else:
            emaNow = rppv * self.emaCoeff + ( 1.0 - self.emaCoeff) * self.ema
            self.ema = emaNow

        line['EMA'] = str(int(self.ema))
        
        csvWriter.writerow(line)



    def AnalyzeBitStuck(self):

        print('BSP.AnalyzeBitStuck')

        self.ema = -10001.0
        self.emaDroppingStartTimeStamp = -1.0
        self.emaRisingStartTimeStamp = -1.0
        self.bitStuck = False

        with open(self.fileAnaPath, 'w', newline='') as fileAna:

            with open(self.fileEmaPath, 'r') as fileEma:
                csvReader = csv.DictReader(fileEma, delimiter=',')
                lineIdx = -1
                for line in csvReader:

                    lineIdx += 1

                    if lineIdx == 0:

                        print(f'Ema column names are {", ".join(line)}')

                        line['BIT_STUCK_DETECT'] = '0'

                        print(f'Ana column names are {", ".join(line)}')

                        csvWriter = csv.DictWriter(fileAna, fieldnames=line)

                        csvWriter.writeheader()

                    self.WriteToAnaFile(csvWriter, line)

        if self.bitStuck:
            print('Bit Stuck detected!!!')


    def WriteToAnaFile(self, csvWriter, line):
 
        emaNow = float(line['EMA'])
        timeNow = float(line['TIME_1900'])

        if self.ema < -10000.0:
            line['BIT_STUCK_DETECT'] = 'Start'
            self.ema = emaNow
            csvWriter.writerow(line)
            return

        if emaNow < self.ema:
            if self.emaDroppingStartTimeStamp < 0:
                self.emaDroppingStartTimeStamp = timeNow

            self.emaRisingStartTimeStamp = -1.0

            emaDroppingLastingSeconds = (timeNow - self.emaDroppingStartTimeStamp) * (24*60*60)

            if emaDroppingLastingSeconds >= self.emaDroppingTimeThreshold:
                self.bitStuck = True
                line['BIT_STUCK_DETECT'] = 'BitStuck'
            else:
                line['BIT_STUCK_DETECT'] = 'EmaDropping(' + str(round(emaDroppingLastingSeconds,3)) +')'
        else:
            if self.emaRisingStartTimeStamp < 0:
                self.emaRisingStartTimeStamp = timeNow

            self.emaDroppingStartTimeStamp = -1.0

            emaRisingLastingSeconds = (timeNow - self.emaRisingStartTimeStamp) * (24*60*60)

            line['BIT_STUCK_DETECT'] = 'EmaRising(' + str(round(emaRisingLastingSeconds,3)) +')'

        self.ema = emaNow
        csvWriter.writerow(line)


    def CreateDataSeries(self):

        print('BSP.CreateDataSeries')

        self.seriesRPPV = []
        self.seriesEMA = []
        self.seriesTIME1900 = []
        self.seriesBITSTUCKDETECT = []
        self.seriesTime = []

        with open(self.fileAnaPath, 'r') as fileAna:
            csvReader = csv.DictReader(fileAna, delimiter=',')
            lineIdx = -1
            for line in csvReader:

                lineIdx += 1

                self.seriesRPPV.append( float(line['RPPV']) ) 
                self.seriesEMA.append( float(line['EMA']) ) 
                self.seriesTIME1900.append( float(line['TIME_1900']) ) 

                txt = line['BIT_STUCK_DETECT']

                if 'BitStuck' in txt:
                    self.seriesBITSTUCKDETECT.append( -1.0 )
                elif 'EmaRising' in txt:
                    self.seriesBITSTUCKDETECT.append( 1.0 )
                else:
                    self.seriesBITSTUCKDETECT.append( 0.0 )
 
        for i in range(len(self.seriesTIME1900)):
            seconds = (self.seriesTIME1900[i] - self.seriesTIME1900[0] ) * (24*60*60)
            self.seriesTime.append(seconds)


    def Analyze(self):

        print('BSP.Analyze')

        self.NormalizeDataAndSave()

        self.CalculateEmaAndSave()
        
        self.AnalyzeBitStuck()

        self.CreateDataSeries()
       


def Main():

    print('Main')

    bsp = BitStuckDetect()

    bsp.Analyze()

 

if __name__ == '__main__':
        Main()


