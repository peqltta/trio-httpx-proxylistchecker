import httpx
import trio
proxies = []
proxfile = 'proxies.txt'
file2 = 'working.txt'
async def checkproxy(proxy):
    async with httpx.AsyncClient(proxies='http://'+proxy) as client:
        try:
            response = await client.get('https://google.com')
            print(proxy+' - alive')
            writeline(file2, proxy)
        except httpx.HTTPError as exc:
            print(proxy+' - dead')
            
async def spawntask(proxies):
    async with trio.open_nursery() as nursery:
        for proxy in proxies:
            nursery.start_soon(checkproxy, proxy)

def readfile(file):
    f = open(file,'r')
    for line in f:
        proxies.append(line.strip())

def writeline(file2, line):
    f = open(file2,'a')
    f.write("%s\n" % line)
readfile(proxfile)
while len(proxies) > 0:
    print('Next Batch')
    trio.run(spawntask, proxies[:100])
    del proxies[:100]


