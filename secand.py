
from math import sqrt
import numpy as np
from DEQ import DEQ

class ImageQ:

    def __init__(self,img):
        self.img = img
        self.h = img.shape[0]
        self.w = img.shape[1]

    def gradient(self):

        grad = np.full((self.h,self.w),0, dtype=np.uint8)

        for i in range(4,self.h-4):
          for j in range(4,self.w-4):
            grad[i,j]=max( abs(int(self.img[i-1,j+1])-int(self.img[i+1,j-1])),
                        abs(int(self.img[i-1,j])-int(self.img[i+1,j])),
                        abs(int(self.img[i,j-1])-int(self.img[i,j+1])),
                        abs(int(self.img[i-1,j-1])-int(self.img[i+1,j+1])),
                        abs(int(self.img[i-2,j-1])-int(self.img[i+2,j+1])),
                        abs(int(self.img[i-2,j+1])-int(self.img[i+2,j-1])),
                        abs(int(self.img[i-1,j-2])-int(self.img[i+1,j+2])),
                        abs(int(self.img[i-1,j+2])-int(self.img[i+1,j-2]))
                        )
        return grad
    
    def statistical(self,r):
        deq=DEQ(0)
        ND02=(r-1)*((2*r)-1)+1
        ND13=ND02+1
        D1Q=np.zeros(4,float)
        D2Q=np.zeros(4,float)
        DQn=np.zeros(4,float)
        statistical=np.zeros((self.h,self.w),float)
        for i in range(4,self.h-4):
            for j in range(4,self.w-4):
                D1Q[0]=deq.D1EQ0(self.img,r,i,j)/ND02
                D1Q[1]=deq.D1EQ1(self.img,r,i,j)/ND13
                D1Q[2]=deq.D1EQ2(self.img,r,i,j)/ND02
                D1Q[3]=deq.D1EQ3(self.img,r,i,j)/ND13

                D2Q[0]=deq.D2EQ0(self.img,r,i,j)/ND02
                D2Q[1]=deq.D2EQ1(self.img,r,i,j)/ND13
                D2Q[2]=deq.D2EQ2(self.img,r,i,j)/ND02
                D2Q[3]=deq.D2EQ3(self.img,r,i,j)/ND13

                if(np.max(D1Q)<20):
                    if(np.max(D2Q)<20):
                        statistical[i,j]=0
                        break

                for n in range(0,4):
                    sum=D1Q[n]+D2Q[n]
                    if(sum==0):
                        DQn[n]=0
                    else:
                        sub=abs(D1Q[n]-D2Q[n])
                        sub=sub*2
                        DQn[n]=(sub/sum)
                statistical[i,j]=max(DQn)
        return statistical

    def standrad(self,cornal):
        c=int((cornal-1)/2)
        stand=np.zeros((self.h,self.w),float)
        for i in range (c,self.h-c):
            for j in range (c,self.w-c):
                x=self.sumcornal(i,j,cornal)
                if(x==0):
                    stand[i,j]=0
                else:
                    y=self.sumpowercornal(i,j,cornal,x)
                    stand[i,j] = round(sqrt(y),0)
        
        standmax=np.max(stand)
        for i in range (0,len(stand)):
            for j in range (0,len(stand[0])):
                if(stand[i,j]==0):
                    stand[i,j]=0
                else:
                    stand[i,j]= stand[i,j]/ standmax
        return stand
                
    def sumcornal(self,io,jo,cornal):
        sum=0
        c=int((cornal-1)/2)
        for i in range (io-c,io+c+1):
            for j in range (jo-c,jo+c+1):
                sum=sum+self.img[i,j]
        return sum/((cornal*cornal)-1)

    def sumpowercornal(self,io,jo,cornal,g):
        sum=0
        c=int((cornal-1)/2)
        for i in range (io-c,io+c+1):
            for j in range (jo-c,jo+c+1):
                p=self.img[i,j]-g
                sum=sum + pow(p,2)
        return sum/((cornal*cornal)-1)

    def connect_gradient_statistical(self,grad,statistical,a,b,type="standrad"):  

        # F = np.full((self.h-8,self.w-8),0, dtype=np.uint8)
        F=np.zeros((len(grad),len(grad[0])),float)
        maxI=np.max(grad)
        for i in range(0,len(grad)):
          for j in range(0,len(grad[0])):
            edg1=(a*(grad[i,j]/maxI))
            edg2=(b*statistical[i][j])
            if(type=="standrad"):
                edg=edg1*edg2
                F[i,j]=edg
            else:
                edg=edg1+edg2
                edg=edg
                F[i,j]=edg
        
        return F
