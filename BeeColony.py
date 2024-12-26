
from math import pi, sin,sqrt,cos
from pickle import TRUE
import random
import numpy as np

class Bee :
    def __init__(self,img,nonzero,F):
        self.img = img
        self.h = F.shape[0]
        self.w = F.shape[1]
        self.SN=300#int(4*sqrt(len(nonzero)))
        self.D=2 
        self.countlimit = 75 #int(self.SN/4)
        self.Limit= np.zeros(self.SN)
        self.valuefitness= np.zeros(self.SN)
        self.last=np.zeros((self.h,self.w),np.uint8)
        self.max=np.max(img)
        self.median=np.quantile(F, .87) #.87
        self.F=F
        self.imgnonzero=nonzero
        self.fit=self.median * self.max 
        print(self.median)

    def Initialization_population(self):
        chbee=np.zeros((self.SN, self.D))
        osbee=np.zeros((self.SN, self.D))

        for i in range (0,self.SN):
            for  j in range (0,self.D):
                    chbee[i,j]=self.ch(500)
                    osbee[i,j]=self.OS(chbee[i,j])

        GS=self.generate_source(chbee,osbee)
        return GS
    
    def Initialization_population_without(self):
        list=np.zeros((self.SN, self.D))

        for i in range (0,self.SN):
            for  j in range (0,self.D):
                list[i,j]=random.randint(0,self.h-1)
        return list
    
    def worker_bee(self,gs):

        # gs and V is index of value in image
        V=self.new_generate_source(gs)# old value 
        for i in range(0,self.SN):
            check = self.fitness(int(V[i,0]),int(V[i,1]),int(gs[i,0]),int(gs[i,1]),i)#check between old and new value
            if(check==False):
                    self.Limit[i]+=1
            else: 
                    self.Limit[i]=0
                    gs[i]= V[i] # set new value
        return gs

    def Onlooker_bee(self,gs):
        Pro=self.probability(gs)
        k=random.randint(0,self.SN-1)
        newpoint=0
        if(np.max(Pro)>0):
            rend1=random.random()
            result = np.where(Pro >= rend1)
            newpoint=result[0][0]
        else: 
            while True:
                # print("probability null")
                newpoint=random.randint(0,self.SN-1)
                if newpoint != k:
                    break

        newV=self.new_one_generate_source(gs[newpoint],gs[k])

        check = self.fitness(int(newV[0]),int(newV[1]),int(gs[newpoint,0]),int(gs[newpoint,1]),newpoint)
        if(check==False):
                self.Limit[newpoint]+=1
        else: 
                self.Limit[newpoint]=0
                gs[newpoint]= newV
        return gs

    # def removeLowfitness(self,gs,ite):
    #     # print("fitness:",np.max(self.valuefitness))
    #     # fit=np.empty(self.SN, float)
    #     # for i in range(0,self.SN):
    #     #     fit[i]=self.img[int(gs[i,0]),int(gs[i,1])] * self.F[int(gs[i,0]),int(gs[i,1])]
    #     sum = np.sum(self.valuefitness)
    #     # maxgs=np.max(fit)
    #     avg=sum/self.SN
    #     # print("avg:",avg)
    #     # if(avg>75): # من اجل عدم حذف قيم كثيرة
    #     #     avg=75
    #     # if(ite%100==0):
    #     #     print(avg)
    #     for i in range(0,self.SN):
    #         if(self.valuefitness[i]<avg):
    #             self.Limit[i]=self.countlimit
        

    def Scout_bee(self,gs):
      
        avg=self.valuefitness.mean()
# 
        for i in range(0,self.SN):
            if(self.Limit[i]>=self.countlimit or self.valuefitness[i]<avg ):
                    self.bestSol(gs,gs[i],i)
                    chbee0=self.ch(100)
                    chbee1=self.ch(100)
                    osbee0=self.OS(chbee0)
                    osbee1=self.OS(chbee1)
                    gs[i]= self.one_generate_source(chbee0,chbee1,osbee0,osbee1)
                    self.Limit[i]=0
        return gs


    def ch(self,K):
        xmin=0
        xmax=self.w-1 # -1 لان المصفوفة تبدء من الصفر الى w-1
        chsmal=np.zeros(K,float)
        chsmal[0] = random.random()
        for k in range(1,K):
            chsmal[k]=sin(pi*chsmal[k-1])
        return int(xmin+chsmal[K-1]*(xmax-xmin))

    def OS(self,x):
        xmin=0
        xmax=self.w-1
        return xmin+xmax-x
    
    def generate_source(self,ch,os):
        GS=np.empty((self.SN, 2), float) #XIJ
        merge=np.concatenate((ch, os), axis=0) # دمج عناصر المصفوفتين
        merge=np.unique(merge, axis=0) # حذف السطور المكررة

        value=np.zeros(len(merge))
        # حصول على قيم من مصفوفة الصورة حسب الاحداثيات الموجودة ضمن مصفوفة XOX 
        for i in range(0,len(value)):
           value[i]=self.img[
                int(merge[i][0]),
            int(merge[i][1])
            ]
        indexmaxValue=np.zeros(self.SN)
        maxvalue=np.zeros(0) #XIJ2
        getmax = True

        # الحصول على اعلى قيم بعدد SNمن مصفوفة XIJ
        while(getmax):
            MAX=np.where(value == max(value))
            maxvalue=np.concatenate([maxvalue,np.array(MAX[0])])
            if(len(maxvalue)<self.SN-1):
                value=np.delete(value, np.where(value == max(value)))
            if(len(maxvalue)>self.SN-1):
                indexmaxValue = maxvalue[:self.SN]
                getmax=False
            if(len(maxvalue)==self.SN-1):
                getmax=False
                indexmaxValue = maxvalue[:self.SN]

        # حصول على احداثيات بدائية للنحل
        
        for i in range(0,len(indexmaxValue)):
            GS[i]= merge[int(indexmaxValue[i])]
        # print(GS)

        return GS

    def one_generate_source(self,ch0,ch1,os0,os1):

        vlauech=self.img[int(ch0), int(ch1)]
        vlaueos=self.img[int(os0), int(os1)]
        if(vlauech>vlaueos):
            return [ch0,ch1]
        return [os0,os1]

    

    def new_generate_source(self,GS,):
        D=2
        V=np.zeros((len(GS), D), float)
        for i in range(0,len(GS)):
            check=5
            while(check>0):
                rand = random.uniform(-1, 1)
                k=random.randint(0,self.SN-1)
                for j in range(0,D):
                    V[i,j]=abs(GS[i,j]+(rand*(GS[i,j]- GS[k,j])))
                    V[i,j]= int(V[i,j])
                    if(V[i,j]>=self.F.shape[j]):
                        V[i,j]= int(V[i,j]*0.5)
                if(V[i] in GS ):
                    check-=1
                else:
                    break
            if(check==0):
                k=random.randint(0,len(self.imgnonzero)-1)
                V[i]=self.imgnonzero[k]
        return V

    def new_one_generate_source(self,gs,kgs):

        value=np.zeros(2)
        check=5
        while(check>0):
            rand = random.uniform(-1, 1)
            for j in range(0,2):
                value[j]=abs(gs[j]+(rand*(gs[j]- kgs[j])))
                value[j]=int(value[j])
                if(value[j]>=self.F.shape[j]):
                    value[j]=int( value[j]*0.5)
            if value in gs:
                check-=1
            else:
                break
        return value

    def fitness(self,vi,vj,gsi,gsj,i):
        fitv=self.img[vi,vj] * self.F[vi,vj]
        fitgs=self.img[gsi,gsj] * self.F[gsi,gsj]
        if(fitv<fitgs):
            self.valuefitness[i]=fitgs
            return False
        self.valuefitness[i]=fitv
        return True
    
    def fitnessnew(self,vi,vj,gsi,gsj,i):
        fitv=self.img[vi,vj]
        fitgs=self.img[gsi,gsj]
        if(fitv<fitgs):
            self.valuefitness[i]=fitgs
            return False
        self.valuefitness[i]=fitv
        return True

    def probability(self,gs):
        p=np.zeros(len(gs),float)
        fit = self.getvalue(gs)
        sumfit=np.sum(fit)
        if(sumfit==0):
            sumfit=1
        # print(sumfit)
        for i in range(len(gs)):
            pp=fit[i]/(sumfit)
            if(i==0):
                p[i]=pp
            else:
                p[i]=p[i-1]+pp
        return p

    def getvalue(self,gs):
        value=np.zeros(len(gs))
        for i in range(len(gs)):
           value[i]=self.img[int(gs[i,0]),int(gs[i,1])]
        return value
    
    def finish(self,gs):
        for i in range(0,len(gs)):
            if(self.valuefitness[i]>=self.fit):#self.fit 
                self.last[int(gs[i,0]),int(gs[i,1])]= self.img[int(gs[i,0]),int(gs[i,1])]
            
    def bestSol(self,gs,ongs,i):
       
        if(self.valuefitness[i]>=self.fit):
            self.last[int(ongs[0]),int(ongs[1])]= self.img[int(ongs[0]),int(ongs[1])]
            