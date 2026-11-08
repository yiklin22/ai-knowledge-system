"""Interactive knowledge-graph view: one self-contained HTML file (no network), coloured by mastery."""
import json
from pathlib import Path

from .index import edges
from .parse import Page

HTML = """<!doctype html><meta charset=utf-8><title>Knowledge graph</title>
<style>body{margin:0;font:13px system-ui;background:#0f1115;color:#ddd}canvas{display:block}
#tip{position:fixed;top:10px;left:10px;max-width:340px;background:#1b1e26;border:1px solid #333;padding:10px;border-radius:6px}
#leg{position:fixed;bottom:10px;left:10px;color:#999}</style>
<canvas id=c></canvas><div id=tip>Hover a node. Drag to move. Arrows = prerequisite order.</div>
<div id=leg>● unseen &nbsp;<span style=color:#e8a33d>● learning</span> &nbsp;<span style=color:#4cc38a>● mastered</span> &nbsp; ring = concept, square = other types</div>
<script>
const D=__DATA__,c=document.getElementById('c'),x=c.getContext('2d'),tip=document.getElementById('tip');
let W,H;function rs(){W=c.width=innerWidth;H=c.height=innerHeight}rs();onresize=rs;
const N=D.nodes,idx={};N.forEach((n,i)=>{idx[n.id]=i;n.x=W/2+Math.random()*200-100;n.y=H/2+Math.random()*200-100;n.vx=n.vy=0});
const E=D.edges.filter(e=>!e.derived&&idx[e.from]!==undefined&&idx[e.to]!==undefined);
const col=n=>n.level>=3?'#4cc38a':n.level>0?'#e8a33d':'#6b7280';
function step(){for(const a of N){for(const b of N){if(a===b)continue;let dx=a.x-b.x,dy=a.y-b.y,d=dx*dx+dy*dy+.1;if(d<40000){const f=900/d;a.vx+=dx*f;a.vy+=dy*f}}
 a.vx+=(W/2-a.x)*.002;a.vy+=(H/2-a.y)*.002}
 for(const e of E){const a=N[idx[e.from]],b=N[idx[e.to]],dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1,f=(d-90)*.01;a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f}
 for(const n of N){if(n===drag)continue;n.vx*=.8;n.vy*=.8;n.x+=n.vx;n.y+=n.vy}}
function draw(){x.clearRect(0,0,W,H);
 for(const e of E){const a=N[idx[e.from]],b=N[idx[e.to]],pre=e.rel==='prerequisite_for';x.strokeStyle=pre?'#5b7bd5':'#2d3340';x.lineWidth=pre?1.2:.7;x.beginPath();x.moveTo(a.x,a.y);x.lineTo(b.x,b.y);x.stroke();
  if(pre){const t=Math.atan2(b.y-a.y,b.x-a.x),px=b.x-Math.cos(t)*9,py=b.y-Math.sin(t)*9;x.fillStyle='#5b7bd5';x.beginPath();x.moveTo(px,py);x.lineTo(px-6*Math.cos(t-.4),py-6*Math.sin(t-.4));x.lineTo(px-6*Math.cos(t+.4),py-6*Math.sin(t+.4));x.fill()}}
 for(const n of N){x.fillStyle=col(n);x.beginPath();if(n.type==='concept')x.arc(n.x,n.y,6,0,7);else x.rect(n.x-5,n.y-5,10,10);x.fill();
  if(n===hover){x.strokeStyle='#fff';x.stroke()}x.fillStyle='#aaa';x.fillText(n.title.slice(0,26),n.x+9,n.y+4)}}
let drag=null,hover=null;
const at=(mx,my)=>N.find(n=>Math.hypot(n.x-mx,n.y-my)<9);
c.onmousemove=e=>{if(drag){drag.x=e.offsetX;drag.y=e.offsetY;return}hover=at(e.offsetX,e.offsetY)||null;
 tip.innerHTML=hover?`<b>${hover.title}</b><br>${hover.type} · ${hover.status} · mastery ${hover.level}/5<br>${hover.summary}<br><code>./kb tutor ${hover.slug}</code>`:'Hover a node. Drag to move. Arrows = prerequisite order.'};
c.onmousedown=e=>{drag=at(e.offsetX,e.offsetY)||null};onmouseup=()=>drag=null;
(function loop(){step();draw();requestAnimationFrame(loop)})();
</script>"""


def write(pages: list[Page], mastery: dict[str, int], out: Path):
    nodes = [{"id": p.id, "slug": p.stem, "type": p.fm["type"], "title": p.fm["title"], "summary": p.fm["summary"],
              "status": p.fm["status"], "level": mastery.get(p.id, 0)} for p in pages]
    data = json.dumps({"nodes": nodes, "edges": edges(pages)}).replace("</", "<\\/")
    out.parent.mkdir(exist_ok=True)
    out.write_text(HTML.replace("__DATA__", data), encoding="utf-8")
