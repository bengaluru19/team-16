#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 03:55:17 2019

@author: sneha
"""

import img2pdf 
from PIL import Image 
import os 
from PyPDF2 import PdfFileMerger  
merger = PdfFileMerger()

y = [0,1,2,3]
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

    


