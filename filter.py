#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 00:18:38 2019

@author: sneha
"""

import pandas as pd

df = pd.read_csv("/home/sneha/Documents/Code_for_good/dataset/Anthill games.csv")
df["A"] = df["Area"] + (df["Excess"]*df["Area"])/100
def printknapSack(W, wt, val, n, mval): 
	K = [[0 for w in range(W + 1)] 
			for i in range(n + 1)] 

	for i in range(n + 1): 
		for w in range(W + 1): 
			if i == 0 or w == 0:
				K[i][w] = 0
			elif wt[i - 1] <= w and max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]):
				K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]) 
			else: 
				K[i][w] = K[i - 1][w] 


	res = K[n][W] 
	
	w = W
	ans=set()
	for i in range(n, 0, -1): 
		if res <= 0: 
			continue
		if res == K[i - 1][w]: 
			continue
		elif mval-val[i-1] >=0:
			ans.add(i-1) 
			res = res - val[i - 1] 
			mval=mval-val[i-1]
			w = w - wt[i - 1] 
			#print(mval,w)
	return ans


# Driver program to test above function 
val = []

wt = []
data={"Budget":150000,"Area":1000,"snake":1,"disabled":0}
#print(len(df))
k=0
store=dict()
for (a,b,c,d,e) in zip(df["A"],df["Budget"],df["Snake"],df["Disabled"],df["Product"]):
    if c==data["snake"] and d==data["disabled"]:
        val.append(a)
        wt.append(b)
        #print(a,b,c,d,e)
        store[k]=e
        k=k+1
    
 
        
W = data["Budget"]
mval = data["Area"]

n = len(val) 
res=printknapSack(W, wt, val, n,mval)

    
print(res)



import img2pdf 
from PIL import Image 
import os 
from PyPDF2 import PdfFileMerger  
merger = PdfFileMerger()

y = list(res)
for i in y:
    # storing image path 
    img_path = "/home/sneha/Documents/Code_for_good/images/"+str(i)+".jpg"
    
    # storing pdf path 
    pdf_path = "/home/sneha/Documents/Code_for_good/images/"+str(i)+".pdf"
      
    # opening image 
    image = Image.open(img_path) 
      
    # converting into chunks using img2pdf 
    pdf_bytes = img2pdf.convert(image.filename) 
      
    # opening or creating pdf file 
    file = open(pdf_path, "wb") 
      
    # writing pdf files with chunks 
    file.write(pdf_bytes)
    merger.append(pdf_path)
      
    # closing image file 
    image.close() 
      
    # closing pdf file 
    file.close() 
      
    # output 
    print("Successfully made pdf file"+str(i))
merger.write("/home/sneha/Documents/Code_for_good/images/result.pdf")
merger.close()


