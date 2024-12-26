from secand import ImageQ
from math import sqrt
import cv2
import numpy as np
from BeeColony import Bee
import math
import os

#####################

def getMSE(img,imgEdge):
        err = np.sum((img.astype("float") - imgEdge.astype("float")) ** 2)
        err /= float(img.shape[0] * img.shape[1])
        return err

#####################
def getwhite(img):
        count=0
        h = img.shape[0]
        w = img.shape[1]
        for y in range(h):
                for x in range(w):
                        pixel = img[y, x]
                        if pixel >= 200:
                                count+=1
        return count
#####################
def getRMSE(mse):
    return math.sqrt(mse)

#####################
def getPSNR(img,imgEdge):
        return cv2.PSNR(img,imgEdge)

#####################
# def getSNR(img,imgEdge):
#     h = img.shape[0]
#     w = img.shape[1]
#     MN=h*w
#     sum=0
#     sumd=0
#     sumu=0
#     for i in range(0,h):
#         sum=0
#         for j in range(0,w):
#             y=img[i,j]
#             y1=imgEdge[i,j]
#             sub=y-y1
#             sumu=sumu+math.pow(y1,2)
#             sum=sum+math.pow(sub,2)
#         sumd=sumd+sum
#     return (sumu/sumd)


#################################################
def getZeroAndNonzeroImg(img,type="zero",value=199):
        if(type=="zero"):
                zero= np.where(img == 0)
        else:
                zero= np.where(img > value)
        zero1=zero[:][0]
        zero2=zero[:][1]
        merge=np.empty((len(zero1), 2), float)
        merge[:,0]=zero1
        merge[:,1]=zero2
        return merge

for countItration in range(25,31):
        countItrationStr=str(countItration)
        print(countItrationStr+' -----> ')

        newfile="new"
        # Folder path containing the images 
        folder_path = "D:\\thiese\\thiese\\thesis\\code\\work\\ourMethod\\"+newfile

        # Get the names of all files in the folder
        file_names = os.listdir(folder_path)

        # Filter out non-image files
        image_names = [file_name for file_name in file_names if file_name.endswith((".jpg", ".png"))]
        csv=np.array([["name","h","w","k",
                "MSEABC","RMSEABC","PSNRABC","whiteABC",
                "MSEcanny","RMSEcanny","PSNRcanny","whitecanny",
                "MSEsobel","RMSEsobel","PSNRsobel","whitesobel",
                "MSEprewitt","RMSEprewitt","PSNRprewitt","whiteprewitt",
                "whiteImage"
                ]])
        # Print the image names
        for image_name in image_names:

                
                nameimg=image_name

                print(nameimg)
                img1 = cv2.imread('D:\\thiese\\thiese\\thesis\\code\\work\\ourMethod\\'+newfile+'\\'+nameimg)#mammography.png / #
                img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

                h = img.shape[0]
                w = img.shape[1]
                whiteimg=getwhite(img)

                image=ImageQ(img)

                P=image.gradient()
                E=image.statistical(4)
                F=image.connect_gradient_statistical(P,E,0.5,1,type="statistical") # type="statistical" /// type="standrad"
                nonzero=getZeroAndNonzeroImg(img,type="nonzero")
                k=int(10*sqrt(len(nonzero)))
                b=Bee(img,nonzero,F)
                GS=b.Initialization_population()
                for i in range(0,k):
                        GS=b.worker_bee(GS)
                        GS=b.Onlooker_bee(GS)
                        # b.removeLowfitness(GS,i)
                        GS=b.Scout_bee(GS)

                b.finish(GS)
                cv2.imwrite('D:\\thiese\\thiese\\thesis\\code\\work\\ourMethod\\new\\edge'+countItrationStr+'\\ABC_'+nameimg, b.last)
                print('finish')
                imgMyEdg = b.last
                
                msemy=getMSE(img,imgMyEdg)
                RMSEmy=getRMSE(msemy)
                PSNREmy=getPSNR(img,imgMyEdg)#(RMSEmy)
                # SNRmy=getSNR(img,imgMyEdg)
                whitemy=getwhite(imgMyEdg)
        ########################Canny operator
                t_lower = 100  # Lower Threshold ####200
                t_upper = 250  # Upper threshold
                aperture_size = 5  # Aperture size

                # Applying the Canny Edge filter
                # with Custom Aperture Size
                edgeCanny = cv2.Canny(img, t_lower, t_upper, 
                                apertureSize=aperture_size)
                cv2.imwrite('D:\\thiese\\thiese\\thesis\\code\\work\\ourMethod\\new\\edge'+countItrationStr+'\\canny'+nameimg, edgeCanny)
                msecanny=getMSE(img,edgeCanny)
                whitecanny=getwhite(edgeCanny)
                RMSEcanny=getRMSE(msecanny)
                PSNREcanny=getPSNR(img,edgeCanny)#(RMSEcanny)
                # SNRcanny=getSNR(img,edgeCanny)
        ########################Sobel operator
                sobel_x = cv2.Sobel(img,cv2.CV_8U, 1, 0, ksize=3)
                sobel_y = cv2.Sobel(img, cv2.CV_8U, 0, 1, ksize=3)

                # Convert the output to absolute values
                sobel_x = cv2.convertScaleAbs(sobel_x)
                sobel_y = cv2.convertScaleAbs(sobel_y)

                # Combine the x and y gradients
                sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
                cv2.imwrite('D:\\thiese\\thiese\\thesis\\code\\work\\ourMethod\\new\\edge'+countItrationStr+'\\sobel'+nameimg, sobel_combined)
                msesobel=getMSE(img,sobel_combined)
                whitesobel=getwhite(sobel_combined)
                # SNRsobel=getSNR(img,sobel_combined)
                RMSEsobel=getRMSE(msesobel)
                PSNREsobel=getPSNR(img,sobel_combined)#(RMSEsobel)
        ##################Prewitt operator
                kernel_x = np.array([[-1, 0, 1],
                                [-1, 0, 1],
                                [-1, 0, 1]])

                kernel_y = np.array([[-1, -1, -1],
                                [0, 0, 0],
                                [1, 1, 1]])

                prewitt_x = cv2.filter2D(img, -1, kernel_x)
                prewitt_y = cv2.filter2D(img, -1, kernel_y)

                # Combine the x and y gradients
                prewitt_combined = cv2.addWeighted(prewitt_x, 0.5, prewitt_y, 0.5, 0)
                cv2.imwrite('D:\\thiese\\thiese\\thesis\\code\\work\\ourMethod\\new\\edge'+countItrationStr+'\\prewitt'+nameimg, prewitt_combined)

                mseprewitt=getMSE(img,prewitt_combined)
                whiteprewitt=getwhite(prewitt_combined)
                # SNRprewitt=getSNR(img,prewitt_combined)
                RMSEprewitt=getRMSE(mseprewitt)
                PSNREprewitt=getPSNR(img,prewitt_combined)#(RMSEprewitt)
        ###################


                csv1=np.array([
                [
                        nameimg,str(h),str(w),str(k),
                        str(msemy),str(RMSEmy),str(PSNREmy),str(whitemy),
                        str(msecanny),str(RMSEcanny),str(PSNREcanny),str(whitecanny),
                        str(msesobel),str(RMSEsobel),str(PSNREsobel),str(whitesobel),
                        str(mseprewitt),str(RMSEprewitt),str(PSNREprewitt),str(whiteprewitt),
                        str(whiteimg)
                ]
                ])
        
                csv=np.vstack((csv,csv1))
        np.savetxt('new\\edge'+countItrationStr+'\\dataofnewTest'+newfile+'.csv', csv, delimiter=',' ,fmt='%s') # DataWithStandrad
        cv2.waitKey(0)	
        cv2.destroyAllWindows()

