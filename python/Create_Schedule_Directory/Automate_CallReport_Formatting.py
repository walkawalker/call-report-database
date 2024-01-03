# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from pathlib import Path

def format_callreports(p,fp):
    years = [2001]# + x for x in range(0,19)]
    quarters = ['03_31']#,'Source_6.30', 'Source_9.30', 'Source_12.31']#, 'Source_3.31','Source_6.30', 'Source_9.30', 'Source_12.31']
    for y in years:
        yeardf = pd.DataFrame()
        yearflag = 0
        for q in quarters:
            ct=0
            plist = list(p.glob(f'**\\{y}\\{q}\\*'))
            if not plist:
                print(f'the following folder didnt exist/has nothing {y}:{q}')
                continue
            for pl in plist:
                if ct == 0:
                    dfinitial = pd.read_csv(pl, sep='\t', on_bad_lines='warn',engine="python") 
                    dfinitial.drop(dfinitial.columns[-1],axis=1,inplace=True)
                    #columndescrip = pd.DataFrame(dfinitial.columns)
                    #dfinitial.drop(0,inplace=True)
                    dfinitial['IDRSSD'] = dfinitial['IDRSSD'].astype(int)
                    #dfinitial = createdatecol(q, y, dfinitial)
                    ct += 1
                    continue
                else: 
                    dftomerge = pd.read_csv(pl, sep='\t', on_bad_lines='warn', engine="python")
                    dftomerge.drop(dftomerge.columns[-1],axis=1,inplace=True)
                    #columndescriptomerge = dftomerge.iloc[0]
                    dftomerge.drop(0,inplace=True)
                print(str(pl))
                dftomerge['IDRSSD'] = pd.to_numeric(dftomerge['IDRSSD'], errors = 'coerce').dropna()
                #dftomerge = createdatecol(q, y, dftomerge)
                dfinitial = pd.merge(dfinitial, dftomerge, on=['IDRSSD'], how='left', suffixes=('', '_y'))
                dfinitial.drop(dfinitial.filter(regex='_y$').columns, axis=1, inplace=True)
            #    columndescrip = pd.concat([columndescrip, columndescriptomerge])
            #    columndescrip.drop(['IDRSSD'], axis=0, inplace=True)
            #columndescrip.drop(list(columndescrip.filter(regex = 'TEXT',axis=0).index),axis = 0, inplace = True)
            #columndescrip.to_csv(f'{fp}\\{y}\\{y}_ColumnDescription_{q}.csv')
            if yearflag==0:
                yeardf = dfinitial
                yearflag+=1
            else:
                yeardf = pd.concat([yeardf, dfinitial], axis=0, ignore_index=True)
                print(len(yeardf))        
        yeardf.drop(list(yeardf.filter(regex = 'TEXT').columns),axis = 1, inplace = True)
        #colnotnumeric = ['RCON9224','RCON9999','IDRSSD','FDIC Certificate Number','OCC Charter Number','OTS Docket Number','Primary ABA Routing Number','Financial Institution Name','Financial Institution Address','Financial Institution City','Financial Institution State','Financial Institution Zip Code','Financial Institution Filing Type','Last Date/Time Submission Updated On','RCONFT03','RCONFT06',	'RCONFT07', 'RCONFT09','RCONFT11', 'RCONFT13','RCONFT16','RCONFT17']
        #colnumeric = []
        #for col in yeardf.columns:
        #    if col not in colnotnumeric:
        #        colnumeric.append(col)
        #yeardf[colnumeric] = yeardf[colnumeric].apply(pd.to_numeric, errors='coerce', axis=1)
        #yeardf.to_excel(f'{fp}\\{y}\\{y}_CallReports_{q}.xlsx',index=False)
        yeardf.to_excel(f'{fp}\\{y}_CallReports_{q}.xlsx',index=False)
#def createdatecol(q, y, df):
#    for i in range(len(df)):
#        if q == 'Source_3.31':
#            df['Reporting_Period_End_Date'] = pd.Series([f'{y}0331' for x in range(len(df.index))])
#        elif q == 'Source_6.30':
#            df['Reporting_Period_End_Date'] = pd.Series([f'{y}0630' for x in range(len(df.index))])
#        elif q == 'Source_9.30':
#            df['Reporting_Period_End_Date'] = pd.Series([f'{y}0930' for x in range(len(df.index))])
#        elif q == 'Source_12.31':
#            df['Reporting_Period_End_Date'] = pd.Series([f'{y}1231' for x in range(len(df.index))])

if __name__ == "__main__":
    p = Path('C:\\Users\\whill\\call-report-database\\Bulk_Files')
    fp = 'C:\\Users\\whill\\call-report-database\\Bulk_Files'
    format_callreports(p, fp)