import sys,re

site=sys.argv[1]
print(site,'\n')

'''isbegin=False
httpoc=re.compile('^http://?[A-Za-z0-9]+.[A-Za-z]')
p=re.compile('((hh)?[A-Za-z0-9]+)')
print(p.findall(site))'''

iscomic=False
isissue=False
hashttp=False
#comicex=re.compile('^http://[A-Za-z0-9]+.[A-Za-z]+/Comic')
httpex=re.compile('^http\:\/\/')
httpsex=re.compile('^https\:\/\/')
comicex=re.compile('((https?\:\/\/)?[A-Za-z0-9]+\.[A-Za-z]+/Comic/[A-Za-z0-9\-]+)')
issueex=re.compile('((https?\:\/\/)?[A-Za-z0-9]+\.[A-Za-z]+/Comic/[A-Za-z0-9\-]+/[A-Za-z0-9\-]+\?id=[0-9]+)')
arr=comicex.findall(site)
print(arr)

if (comicex.match(site)):
    iscomic=True
    if(issueex.match(site)):
        isissue=True

if iscomic:
    if isissue:
        print('This is a single comic issue url')
        print(issueex.findall(site))
    else:
        print('This is a series url')
        print(comicex.findall(site))
else:
    print('This url is invalid')

if httpex.match(site):
    print('\nhas http\n')
else:
    if httpsex.match(site):
        print('\nhas https\n')
    else:
        print('\nno http or https\n')





