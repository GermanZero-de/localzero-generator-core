#!/usr/bin/env python
# coding: utf-8

from generatorcore.generator import Result
import json

class Gtest:
    
    gen:dict = None  # Generator dictionary
    xls:dict = None  # Excel dictionary
    eps:float = 0.001 # max rel accuracy for test to pass
    p_sector_gen = None
    
    # read excel-dictionary
    def set_excel(self, excel_path):
        with open(excel_path, 'r') as fp:
            self.xls = json.load(fp)
        fp.close()
        
    # set Generator dictionary
    def set_dict(self, gen):
        self.gen = gen
    
    def check(self, sector:str, filter: int):
        # compare data
        # parameters: 
        #             sector: Sector to be checked (i.e. 'b18') 
        #             filter: printout filter
        #             == 1 non existing row and column values
        #             == 2 values not determined (None)
        #             == 4 values that differ by more than 1%
        #             == 8 values correct
        #             or combinations (i.e. 2+4 = 6)
        gen = self.gen
        xls = self.xls       
        eps = self.eps
        
        #counter
        vne = vn = vnc = vcc = vnz = 0
        
        if gen is None or xls is None:
            print('dictionaries to compare missing')
            return
        
        sector_xls = self.xls[sector]
        sector_gen = self.gen[sector]
        self.p_sector_gen = sector_gen

        #rows
        for row in sector_xls:
            if len(row) < 1:
                continue

            if row not in sector_gen:
                vne += 1
                if filter & 1 != 0:
                    print('row "' + row + '" does not exist\n')
                continue

            #columns
            for col in sector_xls[row]:
                if type(sector_gen[row]) != dict:
                    continue
                if col not in sector_gen[row]:
                    vne += 1
                    if filter & 1 != 0:
                        print('column "' + col + '" does not exist (' + row + ')')
                    continue

                # exclude string values
                if not isinstance(sector_xls[row][col], str) and not isinstance(sector_gen[row][col], str):

                    # print None - values
                    if sector_gen[row][col] is None:
                        vn += 1
                        if filter & 2 != 0:
                            print('%-50s: %15.2f is None' % (row + '.' + col, sector_xls[row][col]))

                    # treat 0 or non 0 values different
                    elif sector_xls[row][col] != 0:
                        #if type(sector_gen[row][col]) is not float:
                            #continue
                        rerr = abs((sector_gen[row][col] - sector_xls[row][col]) / sector_xls[row][col])
                        if rerr > eps:
                            vnc += 1
                            if filter & 4 != 0:
                                print('%-50s: %15.2f %15.2f Excel' % (row + '.' + col, sector_gen[row][col], sector_xls[row][col]))
                        else:
                            vcc += 1
                            if filter & 8 != 0:
                                print('%-50s: %15.2f %15.2f Correct' % (row + '.' + col, sector_gen[row][col], sector_xls[row][col]))

        for row in sector_gen:
            if row not in sector_xls:
                vnz += 1
                if filter & 16 != 0:
                    print('%-50s: row not in Excel' % (row))
            else:
                for col in sector_gen[row]:
                    if sector_gen[row][col] is not None:
                        if col not in sector_xls[row]:
                            vnz += 1
                            if filter & 16 != 0:
                                print('%-50s: %15.2f column not in Excel' % (row + '.' + col, sector_gen[row][col]))

        # Statistics
        print('columns or rows not declared: ' + str(vne))
        print('values not calculated: ' + str(vn))
        print('values wrong: ' + str(vnc))
        print('values not in Excel: ' + str(vnz))
        print('values correct: ' + str(vcc))
        print('sum: ' + str(vne + vn + vnc + vnz + vcc))

