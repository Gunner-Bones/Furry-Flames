import discord, asyncio, sys, os, urllib.request, json, math, random
from discord.ext import commands


Client = discord.Client()
bot_prefix= "??"
client = commands.Bot(command_prefix=bot_prefix)

s = None
try: s = open("pass.txt","r")
except: sys.exit("[Error] pass.txt needed for Secret")
sl = []
for l in s: sl.append(l.replace("\n",""))
SECRET = sl[0]

# https://discordapp.com/oauth2/authorize?client_id=495787867524825109&scope=bot


DEMONSLIST = []
DLPOINTS = []
#DLRCOUNT = []

CHAR_SUCCESS = "✅"
CHAR_FAILED = "❌"


NOBOT = False

def memberadmin(member):
    for r in member.roles:
       if r.permissions.administrator: return True
    return False

def getrole(s,rn):
    try:
        rid = int(rn)
        return discord.utils.find(lambda r: str(rid) in str(r.id), s.roles)
    except: return discord.utils.find(lambda r: rn.lower() in r.name.lower(), s.roles)

def getmember(s,mn):
    if str(mn).startswith("<@"):
        mid = mn.replace("<@",""); mid = mid.replace(">","")
        return discord.utils.find(lambda m: str(mid) in str(m.id), s.members)
    try:
        mid = int(mn)
        return discord.utils.find(lambda m: str(mid) in str(m.id), s.members)
    except: return discord.utils.find(lambda m: mn.lower() in m.name.lower(), s.members)

def getchannel(s,mn):
    if str(mn).startswith("<#"):
        mid = mn.replace("<#",""); mid = mid.replace(">","")
        return discord.utils.find(lambda m: str(mid) in str(m.id), s.channels)
    try:
        mid = int(mn)
        return discord.utils.find(lambda m: str(mid) in str(m.id), s.channels)
    except: return discord.utils.find(lambda m: mn.lower() in m.name.lower(), s.channels)

def getguild(sid):
    for guild in client.guilds:
        if str(guild.id) == str(sid): return guild
    return None

def paramquotationlist(p):
    params = []
    while True:
        try:
            p1 = p.index("\""); p = p[:p1] + p[p1 + 1:]
            p2 = p.index("\""); p = p[:p2] + p[p2 + 1:]
            params.append(p[p1:p2])
        except ValueError:
            if params == []: return None
            return params

def paramnumberlist(p):
    params = []; i = -1; nf = False; iq = False; tempparam = [""]
    while True:
        try:
            i += 1
            tp = int(p[i])
            if not iq:
                nf = True
                tempparam[0] += str(tp)
        except ValueError:
            if p[i] == " " and iq: iq = False
            if p[i] == "\"" and not iq: iq = True
            if p[i] == " " and nf:
                params.append(int(tempparam[0]))
                tempparam[0] = ""
                nf = False
        except IndexError:
            if nf:
                params.append(int(tempparam[0]))
                tempparam[0] = ""
            if params == []: return None
            return params

def paramlistlist(p,i):
    params = paramquotationlist(p)
    if params is None: return None
    if len(params) == 0: return None
    params = params[i]; params = params.split(",")
    for n in params:
        if str(n).startswith(" "): params[params.index(n)] = n[1:]
        if n[len(n) - 1] == " ": params[params.index(n)] = n[:len(n) - 1]
    return params

def datasettings(file,method,line="",newvalue="",newkey=""):
    """
    :param file: (str).txt
    :param method: (str) get,change,remove,add
    :param line: (str)
    :param newvalue: (str)
    :param newkey: (str)
    """
    s = None
    try: s = open(file,"r")
    except: return None
    sl = []
    for l in s: sl.append(l.replace("\n",""))
    for nl in sl:
        if str(nl).startswith(line):
            if method == "get": s.close(); return str(nl).replace(line + "=","")
            elif method == "change": sl[sl.index(nl)] = line + "=" + newvalue; break
            elif method == "remove": sl[sl.index(nl)] = None; break
    if method == "add": sl.append(newkey + "=" + newvalue)
    if method == "get": return None
    s.close()
    s = open(file,"w")
    s.truncate()
    slt = ""
    for nl in sl:
        if nl is not None:
            slt += nl + "\n"
    s.write(slt); s.close(); return None

def alldatakeys(file) -> list:
    s = None
    try: s = open(file,"r")
    except: return []
    sl = []
    for l in s: sl.append(l.replace("\n", ""))
    for nl in sl:
        nla = str(nl).split("=")
        sl[sl.index(nl)] = nla[0]
    s.close()
    for nl in sl:
        if nl == "": sl.remove(nl)
    return sl

SCDIR = datasettings(file="scv.txt",method="get",line="PDD")

def linkedplayer(uid):
    uid = str(uid)
    if alldatakeys(SCDIR) != []:
        for lp in alldatakeys(SCDIR):
            if lp == uid: return datasettings(file=SCDIR,method="get",line=lp)
    return None

def strtolist(s):
    if str(s) == "[]" or str(s) == "['']": return []
    st = str(s).replace("[",""); st = st.replace("]",""); st = st.replace("'",""); st = st.split(",")
    for t in st:
        if t.startswith(" "): st[st.index(t)] = t[1:]
    return st

def pls(id):
    url = "https://pointercrate.com/api/v1/players/" + str(id)
    rq = urllib.request.Request(url)
    try: rt = str(urllib.request.urlopen(rq).read())
    except: return None
    rt = rt[2:len(rt) - 1]; rt = rt.replace("\\n",""); rt = rt.replace("  ","")
    rj = json.loads(rt)
    return rj['data']

def prd(pn):
    url = "https://pointercrate.com/api/v1/records?player=" + str(pn)
    rq = urllib.request.Request(url)
    try: rt = str(urllib.request.urlopen(rq).read())
    except: return None
    rt = rt[2:len(rt) - 1]; rt = rt.replace("\\n", ""); rt = rt.replace("  ", "")
    rj = json.loads(rt)
    return rj

def drd(dn):
    dn = dn.replace(" ","%20")
    url = "https://pointercrate.com/api/v1/records?demon=" + str(dn)
    rq = urllib.request.Request(url)
    try: rt = str(urllib.request.urlopen(rq).read())
    except: return None
    rt = rt[2:len(rt) - 1]; rt = rt.replace("\\n", ""); rt = rt.replace("  ", "")
    print(rt)
    rj = json.loads(rt)
    return rj


def drcount(drd):
    c = 0
    tc = 0
    for d in drd:
        if d['progress'] == 100: c += 1
        tc += 1
    return [c,tc]

def drctext(dlrd):
    return "[" + dlrd['position'] + "] **" + dlrd['name'] + "**: " + str(dlrd['count'][0]) + " completion records *(" + str(dlrd['count'][1]) + " total records)*"

def lpr(data):
    # requires data from prd(), difference between this and lp is this counts non-100 records
    # this is unused since pointercrate doesn't do that by default
    s = 0
    for d in data:
        if d['demon']['position'] <= 100:
            dp = int(d['progress'])
            dpos = int(d['demon']['position'])
            v = (dp / ((dp / 5) + ((-dp / 5) + 1) * math.exp(-0.008 * dpos)))
            print(str(v) + " " + str(dpos) + " " + str(dp))
            s += v
    return s

def lp(data):
    # requires data from pls()
    s = 0
    for d in data['beaten']:
        if int(d['position']) <= 100:
            s += (100 / ((100/5) + ((-100/5) + 1) * math.exp(-0.008*int(d['position']))))
    for d in data['verified']:
        if int(d['position']) <= 100:
            s += (100 / ((100/5) + ((-100/5) + 1) * math.exp(-0.008*int(d['position']))))
    return s

def dget(value):
    try:
        value = int(value)
        url = "https://pointercrate.com/api/v1/demons?position=" + str(value)
    except: url = "https://pointercrate.com/api/v1/demons?name=" + value
    rq = urllib.request.Request(url)
    try: rt = str(urllib.request.urlopen(rq).read())
    except: return None
    rt = rt[2:len(rt) - 1]; rt = rt.replace("\\n", ""); rt = rt.replace("  ", "")
    rj = json.loads(rt)
    return rj[0]


def simadd(id,new):
    pdata = pls(id)
    if pdata is not None:
        ndemon = dget(new)
        if ndemon is not None:
            olp = lp(pdata)
            pdata['beaten'].append(ndemon)
            nlp = lp(pdata)
            return nlp - olp
    return None

def dl():
    global DEMONSLIST
    url1 = "https://pointercrate.com/api/v1/demons?limit=100"
    url2 = "https://pointercrate.com/api/v1/demons?position__gt=101"
    rq1 = urllib.request.Request(url1); rq2 = urllib.request.Request(url2)
    try: rt1 = str(urllib.request.urlopen(rq1).read()); rt2 = str(urllib.request.urlopen(rq2).read())
    except:
        print("Could not access Demons List")
        return
    rt1 = rt1[2:len(rt1) - 3]; rt2 = rt2[2:len(rt2) - 3 ]
    rt1 = rt1.replace("\\n",""); rt2 = rt2.replace("\\n","")
    rt1 = rt1.replace("  ",""); rt2 = rt2.replace("  ","")
    rj1 = json.loads(rt1); rj2 = json.loads(rt2)
    DEMONSLIST = []
    for d1 in rj1: DEMONSLIST.append(d1)
    for d2 in rj2: DEMONSLIST.append(d2)
    global DLPOINTS
    #global DLRCOUNT
    for d in DEMONSLIST:
        dp = (100 / ((100/5) + ((-100/5) + 1) * math.exp(-0.008*int(d['position']))))
        DLPOINTS.append({'name':d['name'],'position':d['position'],'points':dp})
        #DLRCOUNT.append({'name':d['name'],'position':d['position'],'count':drcount(drd(d['name']))})
    print("Demons List Data ready!")

def rm():
    for guild in client.guilds:
        if str(guild.id) == "162862229065039872":
            c = random.randint(0,len(guild.members))
            for p in guild.members:
                if c == 0:
                    if p.bot: c += 1
                    else: return p.name
                c -= 1


@client.event
async def on_ready():
    print("Bot Ready!")
    print("Name: " + client.user.name + ", ID: " + str(client.user.id))
    sl = ""
    for guild in client.guilds: sl += guild.name + ", "
    print("Connected Servers: " + sl[:len(sl) - 2])
    dl()
    await client.change_presence(activity=discord.Game(name=rm()))


@client.event
async def on_message(message):
    if str(message.content).startswith("??"): await client.change_presence(activity=discord.Game(name=rm()))
    if str(message.content).startswith("??calc "):
        global DEMONSLIST
        # ??calc <new demons>
        cdm = str(message.content).replace("??calc ",""); cdd = paramlistlist(cdm,0)
        if cdd is None:
            await message.add_reaction(CHAR_FAILED)
            await message.channel.send("**Error**: Invalid command")
        else:
            cdp = linkedplayer(str(message.author.id))
            if cdp is None:
                await message.add_reaction(CHAR_FAILED)
                await message.channel.send("**Error**: You are not linked to a Pointercrate Player!")
            else:
                cdpl = pls(cdp)
                if cdpl is None:
                    await message.add_reaction(CHAR_FAILED)
                    await message.channel.send("**Error**: You are linked to an invalid Pointercrate Player!")
                else:
                    ctv = False
                    try: ct = cdpl['beaten']
                    except: ctv = True
                    if ctv:
                        await message.add_reaction(CHAR_FAILED)
                        await message.channel.send("**Error**: You have not beaten any List Demons!")
                    else:
                        global DLPOINTS
                        cddn = ""; cddtp = 0; cdde = None; cddet = 0; cddf = []
                        for d in cdd:
                            dn = False
                            try: dnt = int(d)
                            except: dn = True
                            dpf = False
                            for dp in DLPOINTS:
                                if not dn:
                                    if str(dp['position']) == str(d):
                                        if dp['name'].lower() in cddf:
                                            dpf = True
                                        else:
                                            dppb = False
                                            for pb in cdpl['beaten']:
                                                if pb['name'] == dp['name']: dppb = True
                                            for pb in cdpl['verified']:
                                                if pb['name'] == dp['name']: dppb = True
                                            if not dppb:
                                                cddn += dp['name'] + ", "
                                                cddtp += int(dp['points'])
                                                dpf = True; cddf.append(dp['name'].lower())
                                            if dppb: dpf = True
                                else:
                                    if str(dp['name']).lower() == str(d).lower():
                                        if dp['name'].lower() in cddf:
                                            dpf = True
                                        else:
                                            dppb = False
                                            for pb in cdpl['beaten']:
                                                if pb['name'] == dp['name']: dppb = True
                                            for pb in cdpl['verified']:
                                                if pb['name'] == dp['name']: dppb = True
                                            if not dppb:
                                                cddn += dp['name'] + ", "
                                                cddtp += int(dp['points'])
                                                dpf = True; cddf.append(dp['name'].lower())
                                            if dppb: dpf = True
                            if not dpf:
                                cdde = d
                                break
                        if cdde is not None:
                            if cddet == 0:
                                await message.add_reaction(CHAR_FAILED)
                                await message.channel.send("**Error**: Invalid demon \'" + str(cdde) + "\'")
                        else:
                            if cddtp == 0:
                                await message.add_reaction(CHAR_SUCCESS)
                                await message.channel.send("**" + message.author.name + "**: This combination of Demons "
                                                                                        "does not yield any points!")
                            else:
                                cddpp = int(lp(cdpl) + cddtp)
                                cddn = cddn[:len(cddn) - 2]
                                await message.add_reaction(CHAR_SUCCESS)
                                await message.channel.send("**" + message.author.name + "**: Beating **" + cddn +
                                                           "** will give you *" + str(cddtp) + "* points! (New Total: *"
                                                           + str(cddpp) + "*)")
    """
    #DEPRICATED COMMAND
    if str(message.content).startswith("??stats "):
        # ??stats <player id>
        psm = str(message.content).replace("??stats ","")
        psp = None
        try: psp = int(psm)
        except:
            await message.add_reaction(CHAR_FAILED)
            await message.channel.send("**Error**: Invalid player ID")
        else:
            psps = lp(pls(psp))
            if psps is None:
                await message.add_reaction(CHAR_FAILED)
                await message.channel.send("**Error**: Invalid player ID")
            else:
                pspn = pls(psp)['name']
                await message.add_reaction(CHAR_SUCCESS)
                await message.channel.send("**" + pspn + "**: " + str(psps))
    """
    if str(message.content).startswith("??suggest "):
        # ??suggest <points> [optional range]
        spm = str(message.content).replace("??suggest ",""); spm = spm.split(" ")
        if len(spm) > 2 or len(spm) == 0:
            await message.add_reaction(CHAR_FAILED)
            await message.channel.send("**Error**: Invalid command")
        else:
            cdp = linkedplayer(str(message.author.id))
            if cdp is None:
                await message.add_reaction(CHAR_FAILED)
                await message.channel.send("**Error**: You are not linked to a Pointercrate Player!")
            else:
                sppld = pls(cdp)
                if sppld is None:
                    await message.add_reaction(CHAR_FAILED)
                    await message.channel.send("**Error**: You are linked to an invalid Pointercrate Player!")
                else:
                    ctv = False
                    try: ct = sppld['beaten']
                    except: ctv = True
                    if ctv:
                        await message.add_reaction(CHAR_FAILED)
                        await message.channel.send("**Error**: You have not beaten any List Demons!")
                    else:
                        spp = None; spv = False
                        try: spp = int(spm[0])
                        except: spv = True
                        if spv:
                            await message.add_reaction(CHAR_FAILED)
                            await message.channel.send("**Error**: Invalid points number")
                        else:
                            if spp <= 0:
                                await message.add_reaction(CHAR_FAILED)
                                await message.channel.send("**Error**: Invalid points number")
                            else:
                                spr = 5; sprv = True
                                if len(spm) == 3:
                                    sprt = None
                                    try: sprt = int(spm[2])
                                    except:
                                        await message.add_reaction(CHAR_FAILED)
                                        await message.channel.send("**Error**: Invalid range")
                                        sprv = False
                                    if sprv:
                                        if sprt < 1 or sprt > 500:
                                            await message.add_reaction(CHAR_FAILED)
                                            await message.channel.send("**Error**: Invalid range")
                                            sprv = False
                                        if sprv: spr = sprt
                                if sprv:
                                    spgp = 0
                                    spgd = []
                                    rvt = 0
                                    md = random.randint(0, 1)
                                    while spgp < spp and rvt < 100:
                                        rv = random.randint(1,100)
                                        for d in DLPOINTS:
                                            if d['position'] == rv and not any(pd['name'] == d['name'] for pd in
                                                                               sppld['beaten']) and d['name'] not in spgd:
                                                if md == 1 and spp > 30:
                                                    if d['points'] < (spp / 3):
                                                        tva = spgp + d['points']
                                                        if tva - spp < spr:
                                                            spgp += d['points']
                                                            spgd.append(d['name'])
                                                else:
                                                    tva = spgp + d['points']
                                                    if tva - spp < spr:
                                                        spgp += d['points']
                                                        spgd.append(d['name'])
                                        rvt += 1
                                    if spgp == 0 or len(spgd) == 0:
                                        await message.add_reaction(CHAR_FAILED)
                                        await message.channel.send("**Error**: Could not find any demons that fit these"
                                                                          " requirements")
                                    else:
                                        spgdm = ""
                                        for d in spgd: spgdm += "**" + d + "**, "
                                        spgdm = spgdm[:len(spgdm) - 2]
                                        await message.add_reaction(CHAR_SUCCESS)
                                        await message.channel.send("**" + sppld['name'] + "**: Beating " + spgdm +
                                                                          " will give you *" + str(spgp) + "* list points")
    if str(message.content).startswith("??startdrlw "):
        # ??startdrlw <channel name>
        if not memberadmin(message.author):
            await message.add_reaction(CHAR_FAILED)
            await message.channel.send("**Error**: You are not an Administrator!")
        else:
            swlm = str(message.content).replace("??startdrlw",""); swlp = paramquotationlist(swlm)
            if len(swlp) != 1:
                await message.add_reaction(CHAR_FAILED)
                await message.channel.send("**Error**: Invalid command")
            else:
                swlc = getchannel(message.guild,swlp[0])
                if swlc is None:
                    await message.add_reaction(CHAR_FAILED)
                    await message.channel.send("**Error**: Invalid channel")
                else:
                    if datasettings(file="sclw.txt",method="get",line=str(message.guild.id)) is not None:
                        await message.add_reaction(CHAR_FAILED)
                        await message.channel.send("**Error**: Demon Racing leaderboard already set up!")
                    else:
                        datasettings(file="sclw.txt",method="add",newkey=str(message.guild.id),newvalue=str(swlc.id))
                        await message.add_reaction(CHAR_SUCCESS)
                        await message.channel.send("**" + message.author.name + "**: Demon Racing leaderboard set up in "
                                                                                "channel *" + swlc.name + "*")
    """
    if str(message.content).startswith("??recordcount "):
        # ??recordcount <demon name>
        rcm = str(message.content).replace("??recordcount ","")
        dlrf = False
        global DLRCOUNT
        for d in DLRCOUNT:
            if d['name'].lower() == rcm.lower():
                await message.add_reaction(CHAR_SUCCESS)
                await message.channel.send(drctext(d))
                dlrf = True
        if not dlrf:
            await message.add_reaction(CHAR_FAILED)
            await message.channel.send(destination=message.channel,
                                      content="**Error**: Could not find demon")
    if str(message.content).startswith("??recordnumberequals "):
        # ??recordnumberequals <completion record count>
        rnm = str(message.content).replace("??recordnumberequals ", "")
        rnf = True
        try: rnm = int(rnm)
        except:
            await message.add_reaction(CHAR_FAILED)
            await message.channel.send(destination=message.channel,
                                      content="**Error**: Invalid number")
            rnf = False
        if rnf:
            rnc = []
            for d in DLRCOUNT:
                if d['count'][0] == rnm: rnc.append(d)
            if len(rnc) == 0:
                await message.add_reaction(CHAR_FAILED)
                await message.channel.send(destination=message.channel,
                                          content="**Error**: No demons found with those parameters")
            else:
                rnct = ""
                for r in rnc: rnct += drctext(r) + "\n"
                await message.add_reaction(CHAR_SUCCESS)
                await message.channel.send(rnct)
    if str(message.content).startswith("??recordnumbermin "):
        # ??recordnumbermin <completion record count>
        rnm = str(message.content).replace("??recordnumbermin ", "")
        rnf = True
        try:
            rnm = int(rnm)
        except:
            await message.add_reaction(CHAR_FAILED)
            await message.channel.send(destination=message.channel,
                                      content="**Error**: Invalid number")
            rnf = False
        if rnf:
            rnc = []
            for d in DLRCOUNT:
                if d['count'][0] >= rnm: rnc.append(d)
            if len(rnc) == 0:
                await message.add_reaction(CHAR_FAILED)
                await message.channel.send(destination=message.channel,
                                          content="**Error**: No demons found with those parameters")
            else:
                rnct = ""
                for r in rnc: rnct += drctext(r) + "\n"
                await message.add_reaction(CHAR_SUCCESS)
                await message.channel.send(rnct)
    """

if not NOBOT:
    client.run(SECRET)