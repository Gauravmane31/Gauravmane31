import json, os, urllib.request, urllib.parse, datetime, collections, html

TOKEN = os.environ['GITHUB_TOKEN']
USER = os.environ.get('GITHUB_USERNAME', 'Gauravmane31')
API = 'https://api.github.com'
HEAD = {'Authorization': f'Bearer {TOKEN}', 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}

def req(url, data=None):
    r = urllib.request.Request(url, data=data, headers=HEAD, method='POST' if data else 'GET')
    with urllib.request.urlopen(r, timeout=30) as x:
        return json.load(x)

def gql(query, variables=None):
    body = json.dumps({'query': query, 'variables': variables or {}}).encode()
    return req('https://api.github.com/graphql', body)

def esc(s): return html.escape(str(s), quote=True)

def rect(x,y,w,h,fill,rx=6,stroke='none'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'

def text(x,y,s,size=14,fill='#C9D1D9',weight='400',anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif" font-size="{size}px" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>'

def make_stats():
    repos=[]; page=1
    while True:
        data=req(f'{API}/users/{USER}/repos?per_page=100&page={page}&type=owner&sort=updated')
        repos += data
        if len(data)<100: break
        page+=1
    stars=sum(r.get('stargazers_count',0) for r in repos)
    forks=sum(r.get('forks_count',0) for r in repos)
    languages=collections.Counter()
    for r in repos:
        if r.get('fork'): continue
        try:
            ld=req(r['languages_url'])
            languages.update(ld)
        except Exception:
            pass
    total_bytes=sum(languages.values()) or 1
    top=languages.most_common(6)
    top_pct=[(k,v/total_bytes*100) for k,v in top]

    query='''query($login:String!,$from:DateTime!,$to:DateTime!){ user(login:$login){ contributionsCollection(from:$from,to:$to){ contributionCalendar{totalContributions} totalCommitContributions totalPullRequestContributions totalIssueContributions totalRepositoryContributions } } }'''
    now=datetime.datetime.now(datetime.timezone.utc); start=now-datetime.timedelta(days=365)
    q=gql(query, {'login':USER,'from':start.isoformat(),'to':now.isoformat()})
    c=q.get('data',{}).get('user',{}).get('contributionsCollection',{})
    total=c.get('contributionCalendar',{}).get('totalContributions',0)
    commits=c.get('totalCommitContributions',0); prs=c.get('totalPullRequestContributions',0); issues=c.get('totalIssueContributions',0)
    width=760; height=250
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" rx="12" fill="#0D1117"/>']
    svg.append(text(28,38, f"Gaurav_Mane's GitHub Stats", 18, '#58A6FF','700'))
    stats=[('Total Stars Earned',stars,'★'),('Total Commits (last year)',commits,'◷'),('Total PRs',prs,'⑂'),('Total Issues',issues,'ⓘ'),('Contributions (last year)',total,'▣')]
    y=70
    for label,val,icon in stats:
        svg.append(text(28,y,icon,15,'#58A6FF','600')); svg.append(text(50,y,label+':',13,'#8B949E','500')); svg.append(text(235,y,str(val),13,'#C9D1D9','700')); y+=30
    svg.append(rect(515,62,205,150,'#0D1117',8,'#21262D'))
    svg.append(text(617,92,'ACTIVITY',12,'#8B949E','700','middle'))
    svg.append(text(617,132,str(total),34,'#58A6FF','700','middle'))
    svg.append(text(617,155,'contributions',12,'#C9D1D9','400','middle'))
    svg.append(text(617,184,f'{commits} commits  •  {prs} PRs',11,'#8B949E','400','middle'))
    svg.append('</svg>')
    open('profile/stats.svg','w',encoding='utf-8').write(''.join(svg))

    # language card
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="250" viewBox="0 0 760 250">','<rect width="100%" height="100%" rx="12" fill="#0D1117"/>']
    svg.append(text(28,38,'Most Used Languages',18,'#58A6FF','700'))
    x=28; barw=704
    palette=['#F1E05A','#E34C26','#3572A5','#00B4AB','#B07219','#563D7C']
    for i,(name,pct) in enumerate(top_pct):
        w=barw*pct/100; svg.append(rect(x,60,w,14,palette[i%len(palette)],0)); x+=w
    y=110
    for i,(name,pct) in enumerate(top_pct):
        col=i%2; row=i//2; xx=35+col*350; yy=y+row*38
        svg.append(f'<circle cx="{xx}" cy="{yy-5}" r="6" fill="{palette[i%len(palette)]}"/>')
        svg.append(text(xx+16,yy,name,13,'#C9D1D9','600')); svg.append(text(xx+190,yy,f'{pct:.2f}%',13,'#8B949E','400'))
    svg.append(text(28,232,'Calculated from language bytes in public non-fork repositories',10,'#6E7681','400'))
    svg.append('</svg>')
    open('profile/top-langs.svg','w',encoding='utf-8').write(''.join(svg))

if __name__=='__main__': make_stats()
