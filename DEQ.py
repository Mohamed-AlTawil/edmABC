

class DEQ:
    def __init__(self,k):
        self.k=k
    def D1EQ0(self,image,n,i,j):
        sum=0
        for x in range(1-n,n):
            for y in range(1,n):
                sum+=image[i+x,j+y]
        sum=sum+image[i,j+n]
        return sum


    def D1EQ2(self,image,n,i,j):
        sum=0
        for x in range(1,n):
            for y in range(1-n,n):
                sum+=image[i+x,j+y]
        sum=sum+image[i+n,j]
        return sum


    def D1EQ1(self,image,n,i,j):
        sum=0
        for y in range(n-1,1-n,-1):
            for x in range(1-y,n):
                sum+=image[i+x,j+y]
        sum=sum+image[i,j+n]+image[i+n,j]
        return sum


    def D1EQ3(self,image,n,i,j):
        sum=0
        for y in range(1-n,n):
            for x in range(y+1,n):
                sum+=image[i+x,j+y]
        sum=sum+image[i,j-n]+image[i+n,j]
        return sum

    ####################################33
    def D2EQ0(self,image,n,i,j):
        sum=0
        for x in range(1-n,n):
            for y in range(1-n,0):
                sum+=image[i+x,j+y]
        sum=sum+image[i,j-n]
        return sum


    def D2EQ2(self,image,n,i,j):
        sum=0
        for x in range(1-n,0):
            for y in range(1-n,n):
                sum+=image[i+x,j+y]
        sum=sum+image[i-n,j]
        return sum


    def D2EQ1(self,image,n,i,j):
        sum=0
        for y in range(n-2,-n,-1):
            for x in range(-1-y,-n,-1):
                sum+=image[i+x,j+y]
        sum=sum+image[i,j-n]+image[i-n,j]
        return sum


    def D2EQ3(self,image,n,i,j):
        sum=0
        for x in range(1-n,n):
            for y in range(x+1,n):
                sum+=image[i+x,j+y]
        sum=sum+image[i,j+n]+image[i-n,j]
        return sum