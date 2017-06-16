import os
import pandas as pd
import matplotlib.pyplot as plt
def collectdata(code):    
    
    report=pd.read_csv('./original data/report.csv',encoding='utf-8')
    profit=pd.read_csv('./original data/profit.csv',encoding='utf-8')
    operation=pd.read_csv('./original data/operation.csv',encoding='utf-8')
    growth=pd.read_csv('./original data/growth.csv',encoding='utf-8')
    debtpaying=pd.read_csv('./original data/debtpaying.csv',encoding='utf-8')
    cashflow=pd.read_csv('./original data/cashflow.csv',encoding='utf-8')
    
        
    
    codeReport=report[report['code']==code]
    codeprofit=profit[profit['code']==code]
    codeoperation=operation[operation['code']==code]
    codegrowth=growth[growth['code']==code]
    codedebt=debtpaying[debtpaying['code']==code]
    codeflow=cashflow[cashflow['code']==code]      
    
    return codeReport,codeprofit,codeoperation,codegrowth,codedebt,codeflow
    
def collectAllData():
    Treport=pd.DataFrame()
    Tprofit=pd.DataFrame()
    Toperation=pd.DataFrame()
    Tgrowth=pd.DataFrame()
    Tdebtpaying=pd.DataFrame()
    Tcashflow=pd.DataFrame()
    for year in range(2004,2017):        
        for quarter in range(1,5):
            report=ts.get_report_data(year,quarter)
            Year=pd.Series([year for i in range(report.shape[0])])
            report.insert(len(report.columns),'year',Year)
            Treport=Treport.append(report,ignore_index=True)           
      
    Treport.to_csv('report.csv',encoding="utf-8")        
    
    for year in range(2004,2017):        
        for quarter in range(1,5):        
            profit=ts.get_profit_data(year,quarter)
            Year=pd.Series([year for i in range(profit.shape[0])])
            profit.insert(len(profit.columns),'year',Year)
            Tprofit=Tprofit.append(profit,ignore_index=True)
    Tprofit.to_csv('profit.csv',encoding="utf-8")
    for year in range(2004,2017):        
        for quarter in range(1,5):        
            operation=ts.get_operation_data(year,quarter)
            Year=pd.Series([year for i in range(operation.shape[0])])
            operation.insert(len(operation.columns),'year',Year)
            Toperation=Toperation.append(operation,ignore_index=True)
    Toperation.to_csv('operation.csv',encoding="utf-8")
    for year in range(2004,2017):        
        for quarter in range(1,5):        
            growth=ts.get_growth_data(year,quarter)
            Year=pd.Series([year for i in range(growth.shape[0])])
            growth.insert(len(growth.columns),'year',Year)
            Tgrowth=Tgrowth.append(growth,ignore_index=True)
    Tgrowth.to_csv('growth.csv',encoding="utf-8")        
    for year in range(2004,2017):        
        for quarter in range(1,5):        
            debtpaying=ts.get_debtpaying_data(year,quarter)
            Year=pd.Series([year for i in range(debtpaying.shape[0])])
            debtpaying.insert(len(debtpaying.columns),'year',Year)
            Tdebtpaying=Tdebtpaying.append(debtpaying,ignore_index=True)
    Tdebtpaying.to_csv('debtpaying.csv',encoding="utf-8")
    for year in range(2004,2017):        
        for quarter in range(1,5):        
            cashflow=ts.get_cashflow_data(year,quarter)
            Year=pd.Series([year for i in range(cashflow.shape[0])])
            cashflow.insert(len(cashflow.columns),'year',Year)
            Tcashflow=Tcashflow.append(cashflow,ignore_index=True)       
    Tcashflow.to_csv('cashflow.csv',encoding="utf-8")
   
#codeReport,codeprofit,codeoperation,codegrowth,codedebt,codeflow=collectdata(600519)
#plot some figures
from fnmatch import fnmatch, fnmatchcase
def savePrices(code):
    min_max_scalar=preprocessing.MinMaxScaler() 
    prices=ts.get_k_data(str(code).zfill(6),start='2004-01-01',end='2016-12-30',autype='qfq')
    pricesNo=ts.get_k_data(str(code).zfill(6),start='2004-01-01',end='2016-12-30',autype=None)
    prices['close']=min_max_scalar.fit_transform(prices['close'])  
    pricesNo['close']=min_max_scalar.fit_transform(pricesNo['close'])
    prices['volume']=min_max_scalar.fit_transform(prices['volume'])
    p=[]   
    pNo=[]
    v=[]
    for year in range(2004,2017):
        ind=[i for i in range(prices.index.shape[0])\
             if fnmatch((prices.loc[i])['date'],str(year)+'*')]
        inde=pd.Series(ind)
        p.append((prices.loc[inde])['close'].mean())
        v.append((prices.loc[inde])['volume'].mean())
        pNo.append((pricesNo.loc[inde])['close'].mean())
    price=pd.Series(p)
    priceNo=pd.Series(pNo)
    volume=pd.Series(v)
    isExists=os.path.exists('C:\\Users\\70613\\'+str(code).zfill(6)+'\\')
    if not isExists:
        os.mkdir('./intermediate data'+str(code).zfill(6)+'/')
    volume.to_csv('./intermediate data'+str(code).zfill(6)+'/vol.csv',encoding='utf-8',index=False)
    prices.to_csv('./intermediate data'+str(code).zfill(6)+'/prices.csv',encoding='utf-8')
    pricesNo.to_csv('./intermediate data'+str(code).zfill(6)+'/pricesNo.csv',encoding='utf-8')
    price.to_csv('./intermediate data'+str(code).zfill(6)+'/extraP.csv',encoding='utf-8',index=False)  
    priceNo.to_csv('./intermediate data'+str(code).zfill(6)+'/extraPNo.csv',encoding='utf-8',index=False) 
from sklearn import preprocessing

def plotPapr(code):
    min_max_scalar=preprocessing.MinMaxScaler()  
    volume=pd.read_csv('./intermediate data/'+str(code).zfill(6)+'/vol.csv',encoding='utf-8',\
                       header=None,skip_blank_lines=False)
    price=pd.read_csv('./intermediate data/'+str(code).zfill(6)+'/extraP.csv',\
                      encoding='utf-8',header=None,skip_blank_lines=False)
    priceNo=pd.read_csv('./intermediate data/'+str(code).zfill(6)+'/extraPNo.csv',\
                        encoding='utf-8',header=None,skip_blank_lines=False)
    industry=pd.read_csv('./original data/indusClassified.csv',encoding='utf-8')
    codeReport,codeprofit,codeoperation,codegrowth,codedebt,codeflow=\
                collectdata(code)
    
    code_profit_ratio=min_max_scalar.fit_transform(codeprofit['net_profits'])   
    extra=[4*i-1 for i in range(1,int(code_profit_ratio.shape[0]/4+1))]
    extra_netprofit_Data=code_profit_ratio[extra]
    eps=min_max_scalar.fit_transform(codeprofit['eps'])
    extra_eps_Data=eps[extra]    
    business_income=min_max_scalar.fit_transform(codeprofit['business_income'])
    extra_business_income=business_income[extra]
    bips=min_max_scalar.fit_transform(codeprofit['bips'])
    extra_bips=bips[extra]
    corr={}
    interm_corr={}
    priInd=list(pd.notnull(price).any(1).nonzero()[0])
    proInd=[i for i in range(len(extra))]
    coInd=list(set(priInd).intersection(set(proInd)))
    
    corr['code']=str(code).zfill(6)
    if len(industry[industry['code']==code])!=0:
        corr['c_name']=industry[industry['code']==code]['c_name'].iloc[0]
        corr['name']=industry[industry['code']==code]['name'].iloc[0]
    else:
        corr['c_name']=' '
        corr['name']=' '
    corr['volVp']=(price.dropna(axis=0,how='any')[0]).corr(volume.dropna(axis=0,how='any')[0])
    corr['nprtVp']=(price[0][coInd]).corr(pd.Series(extra_netprofit_Data).iloc[coInd])
    corr['epsVp']=(priceNo[0][coInd]).corr(pd.Series(extra_eps_Data).iloc[coInd])
    corr['busincomeVp']=(price[0][coInd]).corr(pd.Series(extra_business_income).iloc[coInd])
    corr['bipsVp']=(priceNo[0][coInd]).corr(pd.Series(extra_bips).iloc[coInd])    
    
    interm_corr['price']=price[0][coInd]
    interm_corr['priceNo']=priceNo[0][coInd]
    interm_corr['netprofit']=pd.Series(extra_netprofit_Data).iloc[coInd]
    interm_corr['eps']=pd.Series(extra_eps_Data).iloc[coInd]
    interm_corr['busincome']=pd.Series(extra_business_income).iloc[coInd]
    interm_corr['bips']=pd.Series(extra_bips).iloc[coInd]
    interm_corr['code']=str(code).zfill(6)
    if len(industry[industry['code']==code])!=0:
        interm_corr['c_name']=industry[industry['code']==code]['c_name'].iloc[0]
        interm_corr['name']=industry[industry['code']==code]['name'].iloc[0]
    else:
        interm_corr['c_name']=' '
        interm_corr['name']=' '
    
    x=pd.np.arange(2004,2004+len(extra),1) 
    '''  
    figure=plt.figure()
    ax1=figure.add_subplot(111)
    ax1.plot(x,volume.iloc[:len(extra)],'k-',label='volume')
    ax1.plot(x,extra_netprofit_Data,'r-',label='netprofit')
    ax1.plot(x,extra_business_income,'g-',label='business_income')
    ax1.plot(x,price.iloc[:len(extra)],'m--',label='price')
    plt.legend(loc='upper left')
    fig=plt.figure()
    ax2=fig.add_subplot(111)
    ax2.plot(x,extra_eps_Data,'b-',label='eps')    
    ax2.plot(x,extra_bips,'y-',label='bips')
    ax2.plot(x,priceNo.iloc[:len(extra)],'m--',label='priceNo')
    plt.legend(loc='upper left')    
    plt.show()
    '''
    print(corr)
    return corr,interm_corr
#prices=ts.get_h_data(str(600519),start='2004-01-01',end='2016-12-30')
#prices.to_csv(str(600519)+'prices.csv',encoding='utf-8')
def findValidCode():
    profit=pd.read_csv('./original data/profit.csv',encoding='utf-8')
    ValidCode=[]
    erroryear=[]
    erroryearIn=[]
    errornan=[]
    codeList=list(set(profit['code']))
    for code in codeList:
       codeprofit=profit[profit['code']==code]
       year=list(set(codeprofit['year']))
       T=0
       anchor=0
       if max(year)-min(year)+1!=len(year):
           T=1
           erroryear.append(code)
           continue
       for y in year:           
           if list(codeprofit['year']).count(y)!=4:
               anchor=1
       if anchor==1:
           T=1
           erroryearIn.append(code)
           continue
       temp=codeprofit.dropna(axis=0,how='any')
       if temp.shape[0]!=codeprofit.shape[0]:
           T=1
           errornan.append(code)
           continue
       if T==0:
           ValidCode.append(code)       
    return ValidCode,erroryear,erroryearIn,errornan

validCode,erroryear,erroryearIn,errornan=findValidCode()
result1=[]
result2=[]
for i in range(len(validCode)):
    #savePrices(validCode[i])    
    result1.append(plotPapr(validCode[i])[0])
    result2.append(plotPapr(validCode[i])[1])
    print(i)

#savePrices(10) 
result1=pd.DataFrame(result1)   
result2=pd.DataFrame(result2)

#temp=pd.read_csv('C:\\Users\\70613\\70613\\result.csv',encoding='utf-8')
#result=pd.DataFrame(result1).append(temp,ignore_index=True)
result1.to_csv('./final result/result.csv',encoding='utf-8')
result2.to_csv('./final result/mid-result.csv',encoding='utf-8')
plotPapr(833)