import sys
import re
import os
import urllib
from fpdf import FPDF
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui

def main():
    #Get current directory path
    curdirpath=os.getcwd()

    #Get site name
    site=sys.argv[1]

    maindir=sys.argv[2]
    dest=os.path.expanduser('~')+'/'+maindir
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    #Extract comic name and issue no from url
    names=extractnames(site)

    #Create Directory for the comic if it doesn't already exist 
    tdir=dest+"/"+names[0]
    if not os.path.exists(tdir):
        os.makedirs(tdir)

    #The downloaded comic path
    chapterpath=dest+'/'+names[0]
    print('\nComic will be downloaded to: ',chapterpath+'\n')

    #The final name of the comic pdf
    filename=names[0]+'-'+names[1]+'.pdf'

    #Edit url to download all pages of the comic
    editurl=str(site)+"?readType=1"

    print('\nFetching comic...\n')

    fetchcomic(editurl,curdirpath)

    urls=readcontent()

    print('\nDownloading pages, Please wait...\n')
    sz=len(urls)
    if sz>0:
        print('\nNo of pages:',sz,'\n\n')
        createpdf(urls,sz,chapterpath,filename)
        print('\nYour pdf is ready :-D\nEnjoy reading',names[0]+" "+names[1]+" !")
        os.chdir(curdirpath)
    else:
        print("\nSorry :-(, couldn't fetch any pages")
        print("Check the url and try again")

    #os.chdir(curdirpath)
    print()

def extractnames(site):
    arr=site.split("/")
    x=arr.index("Comic")+1
    comicname=arr[x]
    issueno=arr[x+1].split("?")[0]
    return (comicname,issueno)

def fetchcomic(url,curdirpath):
    #Open webdriver & read html source code of webpage
    browser=webdriver.PhantomJS(executable_path=curdirpath+'/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs')
    browser.get(url)
    try:
        element=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,"stSegmentFrame")))
    except Exception:
        browser.save_screenshot('exception.png')
        pass
    finally:
        source_code=browser.page_source
        source_file=open('src.txt','w')
        source_file.write(source_code)
        source_file.flush()
        source_file.close()
        browser.quit()

    exf=Path(curdirpath+'/exception.png')
    if exf.is_file():
        os.remove('exception.png')

def readcontent():
    urls=[]
    with open('src.txt') as srcfile:
        for line in srcfile:
            l,d,r=line.partition('lstImages.push("')
            if d:
                st=r.replace('");','')
                urls.append(st)
        srcfile.close()
    os.remove('src.txt')
    return urls

def createpdf(urls,sz,chapterpath,filename):
    os.chdir(chapterpath)
    i=1
    progress='==>| '
    pdf=FPDF('P','mm','A4')
    x,y,w,h=0,0,200,250
    stat='Completed: '
    for url in urls:
        tfn=str(i)+'.jpg'
        fp=open(tfn,'wb')
        fp.write(urllib.request.urlopen(url).read())
        fp.close()
        pdf.add_page()
        pdf.image(chapterpath+'/'+tfn,x,y,w,h)
        os.remove(tfn)
        #pdf.image(url,x,y,w,h)
        p=str(int(i/sz*100))
        i=i+1
        progress='='+progress
        sys.stdout.write("\r"+stat+progress+p+'%')
        sys.stdout.flush()

    print('\n\nBuilding pdf...\n')
    pdf.output(filename,"F")


