import tushare as ts
class stockQuation:
    data=0
    
    def __init__(self):
        stockQuation.data=ts.get_k_data('000016',index=True)        
    def MA(self,ma):        
        #MA
        MAdata=stockQuation.data['close'].rolling(window=ma).mean()
        stockQuation.data.insert(len(stockQuation.data.columns),'MA',MAdata)
       # self.showResult('MA')
    def EMA(self,ema):
        #EMA                
        EMA=[]
        for i in range(stockQuation.data['close'].shape[0]):
            if i<ema:
                EMA.append(stockQuation.data['close'][i])
            else:
                EMA.append(2/(ema+1)*stockQuation.data['close'][i]+(ema-1)/(ema+1)\
                           *(EMA[i-1]))
        EMA=pd.Series(EMA)
        if 'EMA' not in list(stockQuation.data.columns):
            stockQuation.data.insert(len(stockQuation.data.columns),'EMA',EMA)         
       # self.showResult('EMA')
        return EMA
    def MACD(self,fast,slow,alpha):
        EMA1=self.EMA(fast)
        EMA2=self.EMA(slow)
        DIF=EMA1-EMA2 
        DEA=[]
        for i in range(stockQuation.data['close'].shape[0]):
            if i==0:
                DEA.append(DIF[i])
            else:
                DEA.append(alpha*DEA[i-1]+(1-alpha)*DIF[i])
        DEA=pd.Series(DEA)
        MACD=(DIF-DEA)*2
        stockQuation.data.insert(len(stockQuation.data.columns),'MACD',MACD)
       # self.showResult('MACD')
        
    def VR(self,N):       
        VR=[]
        for i in range(stockQuation.data['volume'].shape[0]):
            if i<N:
                VR.append(0)
            else:
                AVS=[0 for i in range(N-1)]
                BVS=[0 for i in range(N-1)]
                CVS=[0 for i in range(N-1)]
                for j in range(i-N,i-1,1):
                    if stockQuation.data['volume'][j]<stockQuation.data['volume'][j+1]:
                        AVS[j-(i-N)]=stockQuation.data['volume'][j]
                    elif stockQuation.data['volume'][j]==stockQuation.data['volume'][j+1]:
                        CVS[j-(i-N)]=stockQuation.data['volume'][j]
                    else:
                        BVS[j-(i-N)]=stockQuation.data['volume'][j]
                VR.append((sum(AVS)+1/2*sum(CVS))/(sum(BVS)+1/2*sum(CVS)))
        VR=pd.Series(VR)
        stockQuation.data.insert(len(stockQuation.data.columns),'VR',VR)
       # self.showResult('VR')
    def RSI(self,N):
        RSI=[]
        for i in range(stockQuation.data['EMA'].shape[0]):
            if i<N:
                RSI.append(0)
            else:
                U=[0 for i in range(N)]
                D=[0 for i in range(N)]
                for j in range(i-N+1,i,1):
                    if stockQuation.data['EMA'][j]>stockQuation.data['EMA'][j-1]:
                        U[j-(i-N+1)]=stockQuation.data['EMA'][j]
                    elif stockQuation.data['EMA'][j]<stockQuation.data['EMA'][j-1]:
                        D[j-(i-N+1)]=stockQuation.data['EMA'][j]
                    else:
                        continue
                RSI.append(sum(U)/(sum(U)+sum(D)))
        RSI=pd.Series(RSI)
        stockQuation.data.insert(len(stockQuation.data.columns),'RSI',RSI)
        #self.showResult('RSI')
    def MTM(self,N):
        MTM=[]
        for i in range(stockQuation.data['close'].shape[0]):
            if i<N:
                MTM.append(0)
            else:
                MTM.append(stockQuation.data['close'][i]-stockQuation.data['close'][i-N])
        MTM=pd.Series(MTM)
        stockQuation.data.insert(len(stockQuation.data.columns),'MTM',MTM)
        #self.showResult('MTM')
    def AR(self,N):
        AR=[]
        for i in range(stockQuation.data['open'].shape[0]):
            if i<N:
                AR.append(0)
            else:
                temp1=[stockQuation.data['high'][i]-stockQuation.data['open'][i]\
                       for i in range(i-N,i)]
                temp2=[stockQuation.data['open'][i]-stockQuation.data['low'][i]\
                       for i in range(i-N,i)]
                AR.append(sum(temp1)/sum(temp2)*100)
        AR=pd.Series(AR)
        stockQuation.data.insert(len(stockQuation.data.columns),'AR',AR)
       # self.showResult('AR')
    def BR(self,N):
        BR=[]
        for i in range(stockQuation.data['high'].shape[0]):
            if i<N:
                BR.append(0)
            else:
                temp1=[stockQuation.data['high'][i]-stockQuation.data['close'][i-1]\
                       for i in range(i-N+1,i)]
                temp2=[stockQuation.data['close'][i-1]-stockQuation.data['low'][i]\
                       for i in range(i-N+1,i)]
                BR.append(sum(temp1)/sum(temp2)*100)
        BR=pd.Series(BR)
        stockQuation.data.insert(len(stockQuation.data.columns),'BR',BR)
       # self.showResult('BR')
    def setLabel(self,m):
        tempData=stockQuation.data
        CS=[]     
        for i in range(len(tempData['close'])):   
            if i>len(tempData['close'])-m-1:
                CS.append(0)
            else:
                cs=tempData['close'][i]-tempData['close'][i+m]            
                CS.append(cs)            
        cs=pd.Series(CS)        
        stockQuation.data.insert(len(stockQuation.data.columns),'cs',cs)
    
    def Norm(self):
        ClipData=stockQuation.data.sort_index(ascending=False).head(500)
        ClipData.insert(1,'Code',ClipData['code'])
        clipdata=ClipData.drop('code',axis=1)       
        for i in range(2,len(clipdata.columns)):
            tempData=clipdata.iloc[:,i]
            abstempData=tempData.abs()
            signData=pd.np.sign(tempData)
            minabsData=tempData.min()
            maxabsData=tempData.max()
            FinaltempData=signData*(abstempData-minabsData)/(maxabsData-minabsData)  
            clipdata.iloc[:,i]=FinaltempData
        label=pd.np.sign(clipdata['cs'])*(-1)
        clipdata.insert(len(clipdata.columns),'y',label)
        return clipdata    
        
    def showResult(self,col):
        plt.figure()
        shData=self.data.sort_index(ascending=False).head(500)
        plt.plot(shData[col])
        plt.title(col)
                   
     
test=stockQuation()
test.MA(10)
EMA=test.EMA(10)
test.MACD(10,15,0.5)
test.VR(10)
test.RSI(10)
test.MTM(10)
test.AR(10)
test.BR(10)
test.setLabel(1)
result=test.Norm()
