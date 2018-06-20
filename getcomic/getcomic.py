import sys
import re
import os
import urllib
import collections
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

class issuefile:
    fname=""
    cname=""
    issue=""
    link=""

    def __init__(self,fname,cname,issue,link):
        self.fname=fname
        self.cname=cname
        self.issue=issue
        self.link=link

def main():
    print('\nTo stop the script press Ctrl+C\n')
    #Get current directory path
    curdirpath=os.getcwd()

    #Get site name
    site=sys.argv[1]

    #Detect link types
    types=detectlinktype(site)

    if types[0]==False and types[1]==False:
        print('\nInvalid Url\n')
        sys.exit()

    #Extract directory name from arguments and make the directory if it doesn't exists
    maindir=sys.argv[2]
    dest=os.path.expanduser('~')+'/'+maindir
    if not os.path.exists(dest):
        os.makedirs(dest)

    #Edit url to download all pages of the comic
    editurl=str(site)+'?readType=1'

    if types[0]==True or types[1]==True:
        if types[2]==False and types[3]==False:
            editurl='http://'+editurl

    #Extract comic name and issue no from url
    names=extractnames(site,types[1])

    #Create Directory for the comic if it doesn't already exists
    tdir=dest+"/"+names[0]
    if not os.path.exists(tdir):
        os.makedirs(tdir)

    #The downloaded comic path
    chapterpath=dest+'/'+names[0]
    print('\nComic will be downloaded to: ',chapterpath+'\n')

    if types[0]==True and types[1]==True:
        print('\nFetching comic...\n')
        done=singlecomic(names[0],names[1],editurl,chapterpath,curdirpath)
        if done:
            print('\nYour pdf is ready :-D\nEnjoy reading',names[0]+" "+names[1]+" !")
    elif types[0]==True and types[1]==False:
        print('\nSearching for issues of '+names[0]+'...\n')
        ilinks=entireseries(names[0],site,chapterpath,curdirpath)
        isz=len(ilinks)
        if isz==0:
            print('\nSorry :-(, couldn\'t find any links to issues of',names[0],'!\n')
        else:
            uod={}
            print('\nNo of issues in '+names[0]+': '+str(isz)+'\n')
            ch=input('Would you like to download the series partially [y/n]? ')
            v1=-1
            v2=-1
            a1=-1
            a2=-1
            an=''
            chs=''
            if ch=='y':
                an=input('Are issues in range annual issues [y/n]? ')
                print()
                if an=='y':
                    a1,a2=[int(x) for x in input('Enter the annual issues range: ').split()]
                    print()
                chs=input('Would you like to download additional issues [y/n]? ')
                if chs=='y':
                    v1,v2=[int(x) for x in input('\nEnter the issue no range you wish to download: ').split()]
                    print()

            for line in ilinks:
                if line.find('/Comic')==0:
                    tarr=line.split('/')
                    x=tarr.index('Comic')+2
                    tis=tarr[x].split('?')[0]
                    iname=names[0]+'-'+tis+'.pdf'
                    iurl='http://readcomiconline.to/'+line+'?readType=1'
                    iobj=issuefile(iname,names[0],tis,iurl)
                    uod[iname]=iobj
            dmap=collections.OrderedDict(sorted(uod.items()))
            done=True

            for di in dmap:
                #print('\nDownloading issue '+dmap[di].issue+' of comic '+names[0]+' ...\n')
                tel=dmap[di].issue.split('-')
                subno=int(tel[-1])
                sub=tel[-2]
                if(an=='y' and subno>=a1 and subno<=a2 and sub=='Annual'):
                    print('\nDownloading issue '+dmap[di].issue+' of comic '+names[0]+' ...\n')
                    done&=singlecomic(dmap[di].cname,dmap[di].issue,dmap[di].link,chapterpath,curdirpath)
                if(chs=='y' and subno>=v1 and subno<=v2 and sub!='Annual'):
                    print('\nDownloading issue '+dmap[di].issue+' of comic '+names[0]+' ...\n')
                    done&=singlecomic(dmap[di].cname,dmap[di].issue,dmap[di].link,chapterpath,curdirpath)
                if ch=='n':
                    print('\nDownloading issue '+dmap[di].issue+' of comic '+names[0]+' ...\n')
                    done&=singlecomic(dmap[di].cname,dmap[di].issue,dmap[di].link,chapterpath,curdirpath)
            if done:
                print('\nPdfs of all issues you want are ready :-D\nEnjoy reading',dmap[di].cname,'!\n')

    #os.chdir(curdirpath)
    print()


def entireseries(name,murl,chapterpath,curdirpath):
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    browser=webdriver.Chrome(chrome_options=options)

    browser.get(murl)
    try:
        element=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,"stSegmentFrame")))
    except Exception:
        browser.save_screenshot('exception.png')
        pass
    finally:
        source_code=browser.page_source
        source_file=open('series.txt','w')
        source_file.write(source_code)
        source_file.flush()
        source_file.close()
        browser.quit()

    exf=Path(curdirpath+'/exception.png')
    if exf.is_file():
        os.remove('exception.png')

    return getissuelinks()


def getissuelinks():
    #print('\nissue links\n')
    si=-1
    di=-1
    arr=[]

    with open('series.txt') as series:
        for line in series:
            if line.find('Issue Name')!=-1 and si==-1:
                si=line.find('Issue Name')

            if line.find('Comments')!=-1 and di==-1:
                di=line.find('Comments')

            if si!=-1:
                l,d,r=line.partition('href')
                if d:
                    p=re.compile('"([^"]*)"')
                    #print(p.findall(r))
                    arr.append(p.findall(r)[0])

            if si!=-1 and di!=-1:
                series.close()
                break

    os.remove('series.txt')
    #print(arr)
    return arr


def singlecomic(name,issue,url,chapterpath,curdirpath):
    filename=name+'-'+issue+'.pdf'
    fpath=Path(chapterpath+'/'+filename)
    done=False
    if fpath.is_file():
        print('\nThe file '+filename+' already exists.\n')
        done=True
    else:
        fetchcomic(url,curdirpath)

        urls=readcontent()

        print('\nDownloading pages, Please wait...\n')
        sz=len(urls)
        if sz>0:
            print('\nNo of pages:',sz,'\n\n')
            createpdf(urls,sz,chapterpath,filename)
            done=True
            #print('\nYour pdf is ready :-D\nEnjoy reading',name+" "+issue+" !")
            os.chdir(curdirpath)
        else:
            print("\nSorry :-(, couldn't fetch any pages")
            print("Check the url and try again")

    return done

def detectlinktype(site):
    isseries=False
    isissue=False
    hashttp=False
    hashttps=False
    #comicex=re.compile('^http://[A-Za-z0-9]+.[A-Za-z]+/Comic')
    httpex=re.compile('^http\:\/\/')
    httpsex=re.compile('^https\:\/\/')
    comicex=re.compile('((https?\:\/\/)?[A-Za-z0-9]+\.[A-Za-z]+/Comic/[A-Za-z0-9\-]+)')
    issueex=re.compile('((https?\:\/\/)?[A-Za-z0-9]+\.[A-Za-z]+/Comic/[A-Za-z0-9\-]+/[A-Za-z0-9\-]+\?id=[0-9]+)')

    if comicex.match(site):
        isseries=True
        if issueex.match(site):
            isissue=True

    if httpex.match(site):
        hashttp=True
    elif httpsex.match(site):
        hashttps=True

    return (isseries,isissue,hashttp,hashttps)


def extractnames(site,isissue):
    arr=site.split("/")
    x=arr.index("Comic")+1
    comicname=arr[x]
    issueno=""
    if isissue:
        issueno=arr[x+1].split("?")[0]
    return (comicname,issueno)

def fetchcomic(url,curdirpath):
    #Open webdriver & read html source code of webpage
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    browser=webdriver.Chrome(chrome_options=options)
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

