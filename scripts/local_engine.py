"""Windows adapter around the pinned upstream huashu-art-motion engine."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, pathlib, shutil, subprocess, sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
ENCODER_WAIT = '\n        ff.stdin.close(); ff.wait()\n'
ENCODER_CHECK = (ENCODER_WAIT +
    '        if ff.returncode != 0: raise SystemExit(f"FFmpeg failed with exit code {ff.returncode}")\n'
    '        if not Path(vid).is_file() or Path(vid).stat().st_size == 0: raise SystemExit("FFmpeg produced no video output")\n')

def tools():
    home=pathlib.Path.home()
    explicit_ff=os.environ.get('COOPER_FFMPEG')
    ff=explicit_ff if explicit_ff and pathlib.Path(explicit_ff).is_file() else shutil.which('ffmpeg')
    if not ff:
        candidate=home/'.workbuddy/skills/lemo-opuscar-workbuddy/bin/ffmpeg.exe'
        if candidate.is_file(): ff=str(candidate)
    browser=os.environ.get('COOPER_BROWSER')
    if not browser:
        for candidate in [pathlib.Path('C:/Program Files/Google/Chrome/Application/chrome.exe'),pathlib.Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')]:
            if candidate.is_file(): browser=str(candidate); break
    return {'python':sys.executable,'ffmpeg':ff,'browser':browser,'modules':{x:bool(importlib.util.find_spec(x)) for x in ['playwright','PIL','numpy']}}

def environment():
    discovered=tools()
    if not discovered['ffmpeg'] or not discovered['browser']: raise RuntimeError('Missing FFmpeg or browser: '+json.dumps(discovered))
    env=os.environ.copy()
    env['PYTHONUTF8']='1'
    env['PYTHONIOENCODING']='utf-8'
    env['COOPER_BROWSER']=discovered['browser']
    env['PATH']=str(pathlib.Path(discovered['ffmpeg']).parent)+os.pathsep+env.get('PATH','')
    return env

def init(project):
    target=project/'production'
    if target.exists(): raise RuntimeError('Refusing to overwrite existing production directory')
    upstream_render=SKILL/'upstream/scripts/engine/render.py'
    if upstream_render.read_text(encoding='utf-8').count(ENCODER_WAIT)!=1:
        raise RuntimeError('Unsupported upstream renderer: encoder status check could not be installed')
    project.mkdir(parents=True,exist_ok=True)
    shutil.copytree(SKILL/'upstream/scripts',target,ignore=shutil.ignore_patterns('__pycache__'))
    for page in ('index.html', 'clip.html'):
        html_path=target/'engine'/page
        html=html_path.read_text(encoding='utf-8')
        html_path.write_text(html.replace('<head>','<head><link rel="icon" href="data:,">',1),encoding='utf-8')
    changes=[]
    for script in target.rglob('*.py'):
        text=script.read_text(encoding='utf-8')
        old=text
        # Supply a dedicated headless browser executable; no user profile is used.
        text=text.replace('.chromium.launch(args=', '.chromium.launch(executable_path=__import__("os").environ.get("COOPER_BROWSER") or None, args=')
        text=text.replace("'--enable-gpu-rasterization', '--ignore-gpu-blocklist'", "'--disable-accelerated-2d-canvas'")
        if script == target/'engine/render.py': text=text.replace(ENCODER_WAIT,ENCODER_CHECK,1)
        if text!=old:
            script.write_text(text,encoding='utf-8')
            changes.append({'path':str(script.relative_to(project)),'before':hashlib.sha256(old.encode()).hexdigest(),'after':hashlib.sha256(text.encode()).hexdigest()})
    receipt={'adapterVersion':'0.1.2','upstream':'8a0d7d72ca65fcce6f8ba82c4a6c8dfe35b8422c','patches':changes}
    (project/'engine-adapter.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'engine':str(target/'engine'),'patches':len(changes)},ensure_ascii=False))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('action',choices=['doctor','init','lint','render','qa','deliver'])
    ap.add_argument('--project',type=pathlib.Path)
    ap.add_argument('--out',type=pathlib.Path)
    ap.add_argument('--audio',type=pathlib.Path)
    ap.add_argument('--fps',type=int,default=30)
    ap.add_argument('--stills')
    ap.add_argument('--spec',type=pathlib.Path)
    args,extra=ap.parse_known_args()
    if args.spec and args.action != 'render': ap.error('--spec is only valid with render')
    if args.action=='doctor': print(json.dumps(tools(),ensure_ascii=False,indent=2)); return
    if not args.project: ap.error('--project required')
    project=args.project.resolve()
    if args.action=='init': init(project); return
    production=project/'production'
    command=[sys.executable,'-X','utf8']
    if args.action=='lint': command += [str(production/'storyboard_lint.py'),str(project/'镜头表.md')]
    elif args.action=='render':
        if not args.out: ap.error('--out required')
        command += [str(production/'engine/render.py'),'--out',str(args.out.resolve()),'--fps',str(args.fps)]
        if args.audio: command += ['--audio',str(args.audio.resolve())]
        if args.stills: command += ['--stills',args.stills]
        if args.spec: command += ['--spec',str(args.spec.resolve())]
    elif args.action=='qa': command += [str(production/'qa.py'),'--project',str(production/'engine'),'--out',str(project/'qa'),'--fps',str(args.fps)]
    elif args.action=='deliver':
        if not args.out: ap.error('--out requires input MP4')
        command += [str(production/'deliver.py'),str(args.out.resolve()),'--root',str(project),'--project',str(production/'engine'),'--qa',str(project/'qa'),'--out',str(project/'output')]
    command += extra
    print(json.dumps({'command':command},ensure_ascii=False),flush=True)
    raise SystemExit(subprocess.call(command,env=environment(),cwd=project))

if __name__=='__main__': main()
