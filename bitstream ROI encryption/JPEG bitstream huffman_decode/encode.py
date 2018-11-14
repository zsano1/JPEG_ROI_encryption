import math
import numpy as np
import re
import cv2
zigzag=[
   0,  1,  5,  6, 14, 15, 27, 28,
   2,  4,  7, 13, 16, 26, 29, 42,
   3,  8, 12, 17, 25, 30, 41, 43,
   9, 11, 18, 24, 31, 40, 44, 53,
  10, 19, 23, 32, 39, 45, 52, 54,
  20, 22, 33, 38, 46, 51, 55, 60,
  21, 34, 37, 47, 50, 56, 59, 61,
  35, 36, 48, 49, 57, 58, 62, 63]

code_dc_luminanceby=['00','010','011','100','101','110','1110','11110','111110','1111110','11111110','111111110']
code_dc_chrominanceby=['00','01','10','110','1110','1110','11110','111110','1111110','11111110','111111110','1111111110','11111111110']

AClumby={'00':'1010','01':'00','02':'01','03':'100','04':'1011','05':'11010','06':'1111000','07':'11111000','08':'1111110110','09':'1111111110000010','0A':'1111111110000011','11':'1100','12':'11011','13':'1111001','14':'111110110','15':'11111110110','16':'1111111110000100','17':'1111111110000101','18':'1111111110000110','19':'1111111110000111','1A':'1111111110001000','21':'11100','22':'11111001','23':'1111110111','24':'111111110100','25':'1111111110001001','26':'1111111110001010','27':'1111111110001011','28':'1111111110001100','29':'1111111110001101','2A':'1111111110001110','31':'111010','32':'111110111','33':'111111110101','34':'1111111110001111','35':'1111111110010000','36':'1111111110010001','37':'1111111110010010','38':'1111111110010011','39':'1111111110010100','3A':'1111111110010101','41':'111011','42':'1111111000','43':'1111111110010110','44':'1111111110010111','45':'1111111110011000','46':'1111111110011001','47':'1111111110011010','48':'1111111110011011','49':'1111111110011100','4A':'1111111110011101','51':'1111010','52':'11111110111','53':'1111111110011110','54':'1111111110011111','55':'1111111110100000','56':'1111111110100001','57':'1111111110100010','58':'1111111110100011','59':'1111111110100100','5A':'1111111110100101','61':'1111011','62':'111111110110','63':'1111111110100110','64':'1111111110100111','65':'1111111110101000','66':'1111111110101001','67':'1111111110101010','68':'1111111110101011','69':'1111111110101100','6A':'1111111110101101','71':'11111010','72':'111111110111','73':'1111111110101110','74':'1111111110101111','75':'1111111110110000','76':'1111111110110001','77':'1111111110110010','78':'1111111110110011','79':'1111111110110100','7A':'1111111110110101','81':'111111000','82':'111111111000000','83':'1111111110110110','84':'1111111110110111','85':'1111111110111000','86':'1111111110111001','87':'1111111110111010','88':'1111111110111011','89':'1111111110111100','8A':'1111111110111101','91':'111111001','92':'1111111110111110','93':'1111111110111111','94':'1111111111000000','95':'1111111111000001','96':'1111111111000010','97':'1111111111000011','98':'1111111111000100','99':'1111111111000101','9A':'1111111111000110','A1':'111111010','A2':'1111111111000111','A3':'1111111111001000','A4':'1111111111001001','A5':'1111111111001010','A6':'1111111111001011','A7':'1111111111001100','A8':'1111111111001101','A9':'1111111111001110','AA':'1111111111001111','B1':'1111111001','B2':'1111111111010000','B3':'1111111111010001','B4':'1111111111010010','B5':'1111111111010011','B6':'1111111111010100','B7':'1111111111010101','B8':'1111111111010110','B9':'1111111111010111','BA':'1111111111011000','C1':'1111111010','C2':'1111111111011001','C3':'1111111111011010','C4':'1111111111011011','C5':'1111111111011100','C6':'1111111111011101','C7':'1111111111011110','C8':'1111111111011111','C9':'1111111111100000','CA':'1111111111100001','D1':'11111111000','D2':'1111111111100010','D3':'1111111111100011','D4':'1111111111100100','D5':'1111111111100101','D6':'1111111111100110','D7':'1111111111100111','D8':'1111111111101000','D9':'1111111111101001','DA':'1111111111101010','E1':'1111111111101011','E2':'1111111111101100','E3':'1111111111101101','E4':'1111111111101110','E5':'1111111111101111','E6':'1111111111110000','E7':'1111111111110001','E8':'1111111111110010','E9':'1111111111110011','EA':'1111111111110100','F0':'11111111001','F1':'1111111111110101','F2':'1111111111110110','F3':'1111111111110111','F4':'1111111111111000','F5':'1111111111111001','F6':'1111111111111010','F7':'1111111111111011','F8':'1111111111111100','F9':'1111111111111101','FA':'1111111111111110'}
ACchrby={'00':'00','01':'01','02':'100','03':'1010','04':'11000','05':'11001','06':'111000','07':'1111000','08':'111110100','09':'1111110110','0A':'111111110100','11':'1011',
'12':'111001',
'13':'11110110',
'14':'111110101',
'15':'11111110110',
'16':'111111110101',
'17':'1111111110001000',
'18':'1111111110001001',
'19':'1111111110001010',
'1A':'1111111110001011',
'21':'11010',
'22':'11110111',
'23':'1111110111',
'24':'111111110110',
'25':'111111111000010',
'26':'1111111110001100',
'27':'1111111110001101',
'28':'1111111110001110',
'29':'1111111110001111',
'2A':'1111111110010000',
'31':'11011',
'32':'11111000',
'33':'1111111000',
'34':'111111110111',
'35':'1111111110010001',
'36':'1111111110010010',
'37':'1111111110010011',
'38':'1111111110010100',
'39':'1111111110010101',
'3A':'1111111110010110',
'41':'111010',
'42':'111110110',
'43':'1111111110010111',
'44':'1111111110011000',
'45':'1111111110011001',
'46':'1111111110011010',
'47':'1111111110011011',
'48':'1111111110011100',
'49':'1111111110011101',
'4A':'1111111110011110',
'51':'111011',
'52':'1111111001',
'53':'1111111110011111',
'54':'1111111110100000',
'55':'1111111110100001',
'56':'1111111110100010',
'57':'1111111110100011',
'58':'1111111110100100',
'59':'1111111110100101',
'5A':'1111111110100110',
'61':'1111001',
'62':'11111110111',
'63':'1111111110100111',
'64':'1111111110101000',
'65':'1111111110101001',
'66':'1111111110101010',
'67':'1111111110101011',
'68':'1111111110101100',
'69':'1111111110101101',
'6A':'1111111110101110',
'71':'1111010',
'72':'11111111000',
'73':'1111111110101111',
'74':'1111111110110000',
'75':'1111111110110001',
'76':'1111111110110010',
'77':'1111111110110011',
'78':'1111111110110100',
'79':'1111111110110101',
'7A':'1111111110110110',
'81':'11111001',
'82':'1111111110110111',
'83':'1111111110111000',
'84':'1111111110111001',
'85':'1111111110111010',
'86':'1111111110111011',
'87':'1111111110111100',
'88':'1111111110111101',
'89':'1111111110111110',
'8A':'1111111110111111',
'91':'111110111',
'92':'1111111111000000',
'93':'1111111111000001',
'94':'1111111111000010',
'95':'1111111111000011',
'96':'1111111111000100',
'97':'1111111111000101',
'98':'1111111111000110',
'99':'1111111111000111',
'9A':'1111111111001000',
'A1':'111111000',
'A2':'1111111111001001',
'A3':'1111111111001010',
'A4':'1111111111001011',
'A5':'1111111111001100',
'A6':'1111111111001101',
'A7':'1111111111001110',
'A8':'1111111111001111',
'A9':'1111111111010000',
'AA':'1111111111010001',
'B1':'111111001',
'B2':'1111111111010010',
'B3':'1111111111010011',
'B4':'1111111111010100',
'B5':'1111111111010101',
'B6':'1111111111010110',
'B7':'1111111111010111',
'B8':'1111111111011000',
'B9':'1111111111011001',
'BA':'1111111111011010',
'C1':'111111010',
'C2':'1111111111011011',
'C3':'1111111111011100',
'C4':'1111111111011101',
'C5':'1111111111011110',
'C6':'1111111111011111',
'C7':'1111111111100000',
'C8':'1111111111100001',
'C9':'1111111111100010',
'CA':'1111111111100011',
'D1':'11111111001',
'D2':'1111111111100100',
'D3':'1111111111100101',
'D4':'1111111111100110',
'D5':'1111111111100111',
'D6':'1111111111101000',
'D7':'1111111111101001',
'D8':'1111111111101010',
'D9':'1111111111101011',
'DA':'1111111111101100',
'E1':'11111111100000',
'E2':'1111111111101101',
'E3':'1111111111101110',
'E4':'1111111111101111',
'E5':'1111111111110000',
'E6':'1111111111110001',
'E7':'1111111111110010',
'E8':'1111111111110011',
'E9':'1111111111110100',
'EA':'1111111111110101',
'F0':'1111111010',
'F1':'111111111000011',
'F2':'1111111111110110',
'F3':'1111111111110111',
'F4':'1111111111111000',
'F5':'1111111111111001',
'F6':'1111111111111010',
'F7':'1111111111111011',
'F8':'1111111111111100',
'F9':'1111111111111101',
'FA':'1111111111111110'}

def get_huffman_tabble():
 data=open("/home/zsa/tinyjpeg/huffnum.txt","r")
 DC0=[]
 DC1=[]
 AC0=[]
 AC1=[]
 line=data.readline()
 while(line):
  if(line.strip('\n')=="DC0"):
   while(line):
    if(line.strip('\n')!="DC1"and line.strip('\n')!="AC0"and line.strip('\n')!="AC1"):
     if(line.split()==["DC0"]):
      line=data.readline()
     else:
      DC0.append(line.split())
      line=data.readline()
    else:
     break

  elif(line.strip('\n')=="DC1"):
   while(line):
    if(line.strip('\n')!="DC0"and line.strip('\n')!="AC0"and line.strip('\n')!="AC1"):
     if(line.split()==["DC1"]):
      line=data.readline()
     else:
      DC1.append(line.split())
      line=data.readline()
    else:
     break
  elif(line.strip('\n')=="AC0"):
   while(line):
    if(line.strip('\n')!="DC1"and line.strip('\n')!="DC0"and line.strip('\n')!="AC1"):
     if(line.split()==["AC0"]):
      line=data.readline()
     else:
      AC0.append(line.split())
      line=data.readline()
    else:
     break
  elif(line.strip('\n')=="AC1"):
   while(line):
    if(line.strip('\n')!="DC1"and line.strip('\n')!="AC0"and line.strip('\n')!="DC0"):
     if(line.split()==["AC1"]):
      line=data.readline()
     else:
      AC1.append(line.split())
      line=data.readline()
    else:
     break
 return DC0,DC1,AC0,AC1
def getACDC():
 DC0,DC1,AC0,AC1=get_huffman_tabble()
 i=0
 code_dc_luminance=code_dc_luminanceby
 code_dc_chrominance=code_dc_chrominanceby
 AClum={}
 ACchr={}
 for i in range(len(DC0)):
   code_dc_luminance[int(DC0[i][0])]=(str(bin(int(DC0[i][2]))[2:]).zfill(int(DC0[i][1])))
 for i in range(len(AC0)):
   a=str(hex(int(AC0[i][0]))[2:].upper()).zfill(2)
   AClum[a]=str(bin(int(AC0[i][2]))[2:]).zfill(int(AC0[i][1]))
 for i in range(len(DC1)):
   code_dc_chrominance[int(DC1[i][0])]=(str(bin(int(DC1[i][2]))[2:]).zfill(int(DC1[i][1])))
 for i in range(len(AC1)):
   a=str(hex(int(AC1[i][0]))[2:]).zfill(2)
   ACchr[a]=str(bin(int(AC1[i][2]))[2:].upper()).zfill(int(AC1[i][1]))
 return code_dc_luminance,code_dc_chrominance,AClum,ACchr


def size(value):
 if (value!=0):
  return int(math.log(abs(value),2))+1
 else:
  return 0
def binaryval(val):
 if(val>0):
   size=int(math.log(abs(val),2))+1
   return str(bin(val)[2:]).zfill(size)
 if(val==0):
   return ""
 else:
   size=int(math.log(abs(val),2))+1
   a=val+2**(size)-1

   return str(bin(a)[2:]).zfill(size)
i=1
print(binaryval(-70))
record=0
def count0(unit):
 global i,record
 count_0=0
 lj=0
 while(unit[i]=='0'):
   if((lj<15)and(i<63)): 
    count_0+=1
    i+=1
    lj+=1
    record=i
   else:
    if((lj>=15)and(i<63)):
     i+=1
     lj+=1
    else:
     i=63
     return '00'
     break
 if(lj!=0):
   i=record
 lj=15
 return str(hex(count_0)[2:])+str(hex(size(int(unit[i])))[2:])



def readdata(filename):
 data=open(filename,"r")
 line=data.readline()
 i=0
 a=[]
 while line:
   a.append(line.split())
   line=data.readline()
   i+=1
 data.close()
 return a
x2=0
y2=0
def dataunitCrCb(a,mod):
 global x2,y2
 unit=[]
 for i in range(8):
  for j in range(8):
    unit.append(a[x2][y2])
    y2+=1
  x2+=1
  y2=y2-8
 return unit
x=0
y=0
def dataunit(a,mod):
 global x,y
 unit=[]
 if(mod=="1"):
  for i in range(8):
   for j in range(8):
     unit.append(a[x][y])
     y+=1
   x+=1
   y=y-8
 if(mod=="2"):
  for i in range(16):
   for j in range(8):
     unit.append(a[x][y])
     y+=1
   x+=1
   y=y-8
 if(mod=="3"):
  for i in range(8):
   for j in range(16):
     unit.append(a[x][y])
     y+=1
   x+=1
   y=y-16
 if(mod=="4"):
  for i in range(16):
   for j in range(16):
     unit.append(a[x][y])
     y+=1
   x+=1
   y=y-16
 return unit
xx=0
yy=0
def get8_8(unit,mod):
  block=[]
  global xx,yy
  if(mod=="1"):
    block=unit
  if(mod=="2"):
   block=unit
  if(mod=="3"):
   for i in range(8):
    for j in range(8):
     block.append(unit[xx+yy])
     yy+=1
    xx+=8
   yy=0
   xx=8
   for i in range(8):
    for j in range(8):
     block.append(unit[xx+yy])
     yy+=1
    xx+=8
   yy=0
   xx=0
  if(mod=="4"):
   for i in range(8):
    for j in range(8):
     block.append(unit[xx+yy])
     yy+=1
    xx+=8
   yy=0
   xx=8
   for i in range(8):
    for j in range(8):
     block.append(unit[xx+yy])
     yy+=1
    xx+=8
   yy=0
   xx=128
   for i in range(8):
    for j in range(8):
     block.append(unit[xx+yy])
     yy+=1
    xx+=8
   yy=0
   xx=128+8
   for i in range(8):
    for j in range(8):
     block.append(unit[xx+yy])
     yy+=1
    xx+=8
   yy=0
   xx=0
  return block
modfile=open("/home/zsa/tinyjpeg/mod.txt","r")
filename="/home/zsa/tinyjpeg/Y.txt"
dataY=readdata(filename)
filename="/home/zsa/tinyjpeg/Cb.txt"
dataCb=readdata(filename)
filename="/home/zsa/tinyjpeg/Cr.txt"
dataCr=readdata(filename)
mod=modfile.read()

get_huffman_tabble()
code_dc_luminance,code_dc_chrominance,AClum,ACchr=getACDC()
print(code_dc_chrominance)
print(ACchr)
print(code_dc_luminance)
print(AClum)
for key in AClumby.keys():
  if key not in AClum:
    AClum[key]=AClumby[key]
for key in ACchrby.keys():
  if key not in ACchr:
    ACchr[key]=ACchrby[key]
result=""
resu=""
if(mod=="1"):
 for ii in range(len(dataY)/8-1):
   for jj in range(len(dataY[0])/8):
     x=ii*8
     y=jj*8
     unit=dataunit(dataY,mod)
     blocknY=get8_8(unit,mod)
     x-=8
     unit=dataunit(dataCr,mod)
     blocknCr=get8_8(unit,mod)
     x-=8
     unit=dataunit(dataCb,mod)
     blocknCb=get8_8(unit,mod)
     blockY=[]
     blockCr=[]
     blockCb=[]
     for ind in range(64):
        blockY.append("0")
        blockCb.append("0")
        blockCr.append("0")
     for index in range(64):
       blockY[zigzag[index]]=blocknY[index]
       blockCr[zigzag[index]]=blocknCr[index]
       blockCb[zigzag[index]]=blocknCb[index]

     if(ii==0 and jj==0):
        tempY1=int(blockY[0])
        tempCr=int(blockCr[0])
        tempCb=int(blockCb[0])
     else:
        blockY[0]=str(int(blockY[0])-tempY1)
        blockCr[0]=str(int(blockCr[0])-tempCr)
        blockCb[0]=str(int(blockCb[0])-tempCb)
        tempY1=int(blockY[0])+tempY1
        tempCr=int(blockCr[0])+tempCr
        tempCb=int(blockCb[0])+tempCb
     result+=code_dc_luminance[size(int(blockY[0]))]
     result+=binaryval(int(blockY[0]))
     while(i<64):
      result+=AClum[count0(blockY).upper()]+binaryval(int(blockY[i]))
      i+=1
     i=1
     result+=code_dc_chrominance[size(int(blockCb[0]))]
     result+=binaryval(int(blockCb[0]))
     while(i<64):
      result+=ACchr[count0(blockCb).upper()]+binaryval(int(blockCb[i]))
      i+=1
     i=1
     result+=code_dc_chrominance[size(int(blockCr[0]))]
     result+=binaryval(int(blockCr[0]))
     while(i<64):
      result+=ACchr[count0(blockCr).upper()]+binaryval(int(blockCr[i]))
      i+=1
     i=1
if(mod=="3"):
 for ii in range(1):
   for jj in range(1):
     x=ii*16
     y=jj*8
     x2=ii*8
     y2=jj*8
     unit=dataunit(dataY,mod)
     blocknY=get8_8(unit,mod)
     x-=8
     unit=dataunitCrCb(dataCr,mod)
     blocknCr=get8_8(unit,"1")
     x2-=8
     unit=dataunitCrCb(dataCb,mod)
     blocknCb=get8_8(unit,"1")
     blockY1=[]
     blockY2=[]
     blockCr=[]
     blockCb=[]
     for ind in range(64):
        blockY1.append("0")
        blockY2.append("0")
        blockCb.append("0")
        blockCr.append("0")
     for index in range(64):
       blockY1[zigzag[index]]=blocknY[index]
       blockY2[zigzag[index]]=blocknY[index+64]
       blockCr[zigzag[index]]=blocknCr[index]
       blockCb[zigzag[index]]=blocknCb[index]
     if(ii==0 and jj==0):
        tempY1=int(blockY1[0])
        tempY2=int(blockY2[0])
        tempCr=int(blockCr[0])
        tempCb=int(blockCb[0])
        blockY2[0]=str(int(blockY2[0])-tempY1)
     else:
        tempY1=int(blockY1[0])
        blockY1[0]=str(tempY1-tempY2)
        tempY2=int(blockY2[0])
        blockY2[0]=str(tempY2-tempY1)
        blockCr[0]=str(int(blockCr[0])-tempCr)
        blockCb[0]=str(int(blockCb[0])-tempCb)
        tempCr=int(blockCr[0])+tempCr
        tempCb=int(blockCb[0])+tempCb
     result+=code_dc_luminance[size(int(blockY1[0]))]
     result+=binaryval(int(blockY1[0]))
     while(i<64):
      result+=AClum[count0(blockY1).upper()]+binaryval(int(blockY1[i]))
      i+=1
     i=1

     result+=code_dc_luminance[size(int(blockY2[0]))]
     result+=binaryval(int(blockY2[0]))
     while(i<64):
      result+=AClum[count0(blockY2).upper()]+binaryval(int(blockY2[i]))
      i+=1
     i=1
     
     result+=code_dc_chrominance[size(int(blockCb[0]))]
     result+=binaryval(int(blockCb[0]))
     while(i<64):
      result+=ACchr[count0(blockCb).upper()]+binaryval(int(blockCb[i]))
      i+=1
     i=1
     result+=code_dc_chrominance[size(int(blockCr[0]))]
     result+=binaryval(int(blockCr[0]))
     while(i<64):
      result+=ACchr[count0(blockCr).upper()]+binaryval(int(blockCr[i]))
      i+=1
     i=1
if(mod=="2"):
 for ii in range(len(dataY)/16-1):
   for jj in range(len(dataY[0])/16):
     x=ii*8
     y=jj*16
     x2=ii*8
     y2=jj*8
     unit=dataunit(dataY,mod)
     blocknY=get8_8(unit,mod)
     x-=16
     unit=dataunitCrCb(dataCr,mod)
     blocknCr=get8_8(unit,"1")
     x2-=8
     unit=dataunitCrCb(dataCb,mod)
     blocknCb=get8_8(unit,"1")
     blockY1=[]
     blockY2=[]
     blockCr=[]
     blockCb=[]
     for ind in range(64):
        blockY1.append("0")
        blockY2.append("0")
        blockCb.append("0")
        blockCr.append("0")
     for index in range(64):
       blockY1[zigzag[index]]=blocknY[index]
       blockY2[zigzag[index]]=blocknY[index+64]
       blockCr[zigzag[index]]=blocknCr[index]
       blockCb[zigzag[index]]=blocknCb[index]
     if(ii==0 and jj==0):
        tempY1=int(blockY1[0])
        tempY2=int(blockY2[0])
        tempCr=int(blockCr[0])
        tempCb=int(blockCb[0])
        blockY2[0]=str(int(blockY2[0])-tempY1)
     else:
        tempY1=int(blockY1[0])
        blockY1[0]=str(tempY1-tempY2)
        tempY2=int(blockY2[0])
        blockY2[0]=str(tempY2-tempY1)
        blockCr[0]=str(int(blockCr[0])-tempCr)
        blockCb[0]=str(int(blockCb[0])-tempCb)
        tempCr=int(blockCr[0])+tempCr
        tempCb=int(blockCb[0])+tempCb
     result+=code_dc_luminance[size(int(blockY1[0]))]
     result+=binaryval(int(blockY1[0]))
     while(i<64):
      result+=AClum[count0(blockY1).upper()]+binaryval(int(blockY1[i]))
      i+=1
     i=1

     result+=code_dc_luminance[size(int(blockY2[0]))]
     result+=binaryval(int(blockY2[0]))
     while(i<64):
      result+=AClum[count0(blockY2).upper()]+binaryval(int(blockY2[i]))
      i+=1
     i=1
     
     result+=code_dc_chrominance[size(int(blockCb[0]))]
     result+=binaryval(int(blockCb[0]))
     while(i<64):
      result+=ACchr[count0(blockCb).upper()]+binaryval(int(blockCb[i]))
      i+=1
     i=1
     result+=code_dc_chrominance[size(int(blockCr[0]))]
     result+=binaryval(int(blockCr[0]))
     while(i<64):
      result+=ACchr[count0(blockCr).upper()]+binaryval(int(blockCr[i]))
      i+=1
     i=1
if(mod=="4"):
 for ii in range(len(dataY)/16-1):
   for jj in range(len(dataY[0])/16):
     x=ii*16
     y=jj*16
     x2=ii*8
     y2=jj*8
     unit=dataunit(dataY,mod)
     blocknY=get8_8(unit,mod)
     x-=16
     unit=dataunitCrCb(dataCr,mod)
     blocknCr=get8_8(unit,"1")
     x2-=8
     unit=dataunitCrCb(dataCb,mod)
     blocknCb=get8_8(unit,"1")
     blockY1=[]
     blockY2=[]
     blockY3=[]
     blockY4=[]
     blockCr=[]
     blockCb=[]
     for ind in range(64):
        blockY1.append("0")
        blockY2.append("0")
        blockY3.append("0")
        blockY4.append("0")
        blockCb.append("0")
        blockCr.append("0")

     for index in range(64):
       blockY1[zigzag[index]]=blocknY[index]
       blockY2[zigzag[index]]=blocknY[index+64]
       blockY3[zigzag[index]]=blocknY[index+128]
       blockY4[zigzag[index]]=blocknY[index+192]
       blockCr[zigzag[index]]=blocknCr[index]
       blockCb[zigzag[index]]=blocknCb[index]
     if(ii==0 and jj==0):
        tempY1=int(blockY1[0])
        tempY2=int(blockY2[0])
        tempY3=int(blockY3[0])
        tempY4=int(blockY4[0])
        tempCr=int(blockCr[0])
        tempCb=int(blockCb[0])
        blockY2[0]=str(int(blockY2[0])-tempY1)
        blockY3[0]=str(tempY3-tempY2)
        blockY4[0]=str(tempY4-tempY3)
     else:
        tempY1=int(blockY1[0])
        blockY1[0]=str(tempY1-tempY4)
        tempY2=int(blockY2[0])
        tempY3=int(blockY3[0])
        tempY4=int(blockY4[0])
        blockY2[0]=str(tempY2-tempY1)
        blockY3[0]=str(tempY3-tempY2)
        blockY4[0]=str(tempY4-tempY3)
        blockCr[0]=str(int(blockCr[0])-tempCr)
        blockCb[0]=str(int(blockCb[0])-tempCb)
        tempCr=int(blockCr[0])+tempCr
        tempCb=int(blockCb[0])+tempCb
     result+=code_dc_luminance[size(int(blockY1[0]))]
     result+=binaryval(int(blockY1[0]))
     while(i<64):
      result+=AClum[count0(blockY1).upper()]+binaryval(int(blockY1[i]))
      i+=1
     i=1

     result+=code_dc_luminance[size(int(blockY2[0]))]
     result+=binaryval(int(blockY2[0]))
     while(i<64):
      result+=AClum[count0(blockY2).upper()]+binaryval(int(blockY2[i]))
      i+=1
     i=1
     result+=code_dc_luminance[size(int(blockY3[0]))]
     result+=binaryval(int(blockY3[0]))
     while(i<64):
      result+=AClum[count0(blockY3).upper()]+binaryval(int(blockY3[i]))
      i+=1
     i=1
     result+=code_dc_luminance[size(int(blockY4[0]))]
     result+=binaryval(int(blockY4[0]))
     while(i<64):
      result+=AClum[count0(blockY4).upper()]+binaryval(int(blockY4[i]))
      i+=1
     i=1
     result+=code_dc_chrominance[size(int(blockCb[0]))]
     result+=binaryval(int(blockCb[0]))
     while(i<64):
      result+=ACchr[count0(blockCb).upper()]+binaryval(int(blockCb[i]))
      i+=1
     i=1
     result+=code_dc_chrominance[size(int(blockCr[0]))]
     result+=binaryval(int(blockCr[0]))
     while(i<64):
      result+=ACchr[count0(blockCr).upper()]+binaryval(int(blockCr[i]))
      i+=1
     i=1


m=0
while(m<len(result)-7):
  res=str(hex(8*int(result[m])+4*int(result[m+1])+2*int(result[m+2])+int(result[m+3]))[2:])+str(hex(8*int(result[m+4])+4*int(result[m+5])+2*int(result[m+6])+int(result[m+7]))[2:])+" "
  if str(hex(8*int(result[m])+4*int(result[m+1])+2*int(result[m+2])+int(result[m+3]))[2:])+str(hex(8*int(result[m+4])+4*int(result[m+5])+2*int(result[m+6])+int(result[m+7]))[2:])=='ff':
     resu=resu+res+"00 "
  else:
     resu=resu+res
  m+=8
print(resu)
data=open("/home/zsa/tinyjpeg/res.txt","w")
data.write(resu)









