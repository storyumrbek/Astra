import json, os, re, tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
from calculator_core import evaluate, format_number
BG='#101114'; PANEL='#17191e'; KEY='#292b30'; FUNC='#55585f'; ORANGE='#ff9f0a'; WHITE='#f5f5f7'; MUTED='#9699a2'
def history_path():
 p=Path(os.getenv('APPDATA') or os.getenv('XDG_DATA_HOME') or Path.home()/'.local'/'share')/'iPhoneCalculator'; p.mkdir(parents=True,exist_ok=True); return p/'history.json'
class Calculator:
 def __init__(self,root):
  self.root=root; self.expr=''; self.done=False; self.history=self.read_history(); root.title('Calculator'); root.geometry('880x690'); root.minsize(720,610); root.configure(bg=BG)
  outer=tk.Frame(root,bg=BG); outer.pack(fill='both',expand=True,padx=28,pady=22); head=tk.Frame(outer,bg=BG); head.pack(fill='x',pady=(0,18))
  tk.Label(head,text='CALCULATOR',bg=BG,fg=MUTED,font=('Segoe UI',9,'bold')).pack(anchor='w'); tk.Label(head,text='Calculator',bg=BG,fg=WHITE,font=('Segoe UI',20,'bold')).pack(side='left')
  tk.Button(head,text='◷  History',command=self.toggle_history,bg=PANEL,fg=WHITE,relief='flat',bd=0,padx=16,pady=9).pack(side='right')
  body=tk.Frame(outer,bg=BG); body.pack(fill='both',expand=True); self.card=tk.Frame(body,bg=PANEL,highlightthickness=1,highlightbackground='#282a30'); self.card.pack(side='left',fill='both',expand=True)
  self.hp=tk.Frame(body,bg=PANEL,width=260); self.hp.pack_propagate(False); area=tk.Frame(self.card,bg=PANEL); area.pack(fill='both',expand=True,padx=24,pady=24)
  display=tk.Frame(area,bg='#0b0c0f',height=150); display.pack(fill='x',pady=(0,10)); display.pack_propagate(False)
  self.expl=tk.Label(display,text='',bg='#0b0c0f',fg=MUTED,anchor='e',font=('Segoe UI',13)); self.expl.pack(fill='x',padx=18,pady=(18,0)); self.out=tk.Label(display,text='0',bg='#0b0c0f',fg=WHITE,anchor='e',font=('Segoe UI',36,'bold')); self.out.pack(fill='x',padx=18)
  row=tk.Frame(area,bg=PANEL); row.pack(fill='x',pady=(0,8)); self.hint=tk.Label(row,text='',bg=PANEL,fg=MUTED,font=('Segoe UI',9)); self.hint.pack(side='left'); tk.Button(row,text='⌫',command=lambda:self.press('⌫'),bg=PANEL,fg=MUTED,relief='flat',bd=0,font=('Segoe UI',13)).pack(side='right')
  grid=tk.Frame(area,bg=PANEL); grid.pack(fill='both',expand=True)
  for c in range(4): grid.grid_columnconfigure(c,weight=1,uniform='c')
  for r in range(5): grid.grid_rowconfigure(r,weight=1,uniform='r')
  for r,items in enumerate([('AC','±','%','÷'),('7','8','9','×'),('4','5','6','−'),('1','2','3','+'),('(','0',')','=')]):
   for c,label in enumerate(items):
    color=FUNC if label in ('AC','±','%','(',')') else ORANGE if label in ('÷','×','−','+','=') else KEY
    tk.Button(grid,text=label,command=lambda x=label:self.press(x),bg=color,fg=WHITE,activebackground='#ffb340' if color==ORANGE else '#3a3d44',relief='flat',bd=0,font=('Segoe UI',18,'bold'),cursor='hand2').grid(row=r,column=c,sticky='nsew',padx=5,pady=5,ipady=5)
  tk.Label(area,text='Enter = result · Backspace = erase · Esc = clear · Ctrl+C = copy',bg=PANEL,fg='#71747c',font=('Segoe UI',9)).pack(fill='x',pady=(10,0)); self.build_history(); root.bind('<Key>',self.key); root.bind('<Control-c>',lambda e:self.copy()); self.refresh()
 def read_history(self):
  try:
   h=json.loads(history_path().read_text(encoding='utf-8')); return h if isinstance(h,list) else []
  except (OSError,json.JSONDecodeError): return []
 def save_history(self):
  try: history_path().write_text(json.dumps(self.history[:100],ensure_ascii=False,indent=2),encoding='utf-8')
  except OSError: pass
 def build_history(self):
  top=tk.Frame(self.hp,bg=PANEL); top.pack(fill='x',padx=14,pady=16); tk.Label(top,text='History',bg=PANEL,fg=WHITE,font=('Segoe UI',14,'bold')).pack(side='left'); tk.Button(top,text='Clear',command=self.clear_history,bg=PANEL,fg=MUTED,relief='flat',bd=0).pack(side='right'); self.hist=tk.Frame(self.hp,bg=PANEL); self.hist.pack(fill='both',expand=True,padx=12); self.render_history()
 def render_history(self):
  for w in self.hist.winfo_children(): w.destroy()
  if not self.history: tk.Label(self.hist,text='Calculations appear here',bg=PANEL,fg=MUTED).pack(pady=30); return
  for item in self.history[:30]:
   box=tk.Frame(self.hist,bg=PANEL,highlightthickness=1,highlightbackground='#303239'); box.pack(fill='x',pady=4); tk.Label(box,text=item['expression'],bg=PANEL,fg=MUTED,anchor='e',wraplength=210).pack(fill='x',padx=9,pady=(7,0)); tk.Button(box,text=item['result'],command=lambda x=item['result']:self.load(x),bg=PANEL,fg=WHITE,activeforeground=ORANGE,relief='flat',bd=0,anchor='e',font=('Segoe UI',13,'bold')).pack(fill='x',padx=9,pady=(0,7))
 def toggle_history(self):
  if self.hp.winfo_manager(): self.hp.pack_forget()
  else: self.hp.pack(side='right',fill='y',padx=(14,0)); self.render_history()
 def key(self,e):
  if e.char and e.char in '0123456789.+-*/()%': self.press({'*':'×','/':'÷','-':'−'}.get(e.char,e.char)); return 'break'
  if e.keysym in ('Return','KP_Enter'): self.press('='); return 'break'
  if e.keysym=='BackSpace': self.press('⌫'); return 'break'
  if e.keysym=='Escape': self.press('AC'); return 'break'
 def press(self,k):
  if k=='AC': self.expr=''; self.done=False
  elif k=='⌫': self.expr=self.expr[:-1]; self.done=False
  elif k=='=': self.calculate(); return
  elif k=='±':
   m=re.search(r'(\d+(?:\.\d*)?)$',self.expr)
   if not m: self.expr='−('+self.expr+')' if self.expr else '−'
   else:
    i=m.start(); unary=i>0 and self.expr[i-1]=='−' and (i==1 or self.expr[i-2] in '+−×÷('); self.expr=self.expr[:i-1]+self.expr[i:] if unary else self.expr[:i]+'−'+self.expr[i:]
   self.done=False
  elif k in '+−×÷':
   if self.done: self.done=False
   if self.expr and self.expr[-1] in '+−×÷': self.expr=self.expr[:-1]+k
   elif self.expr: self.expr+=k
  elif k=='.':
   if self.done: self.expr=''; self.done=False
   if '.' not in re.split(r'[+−×÷()]',self.expr)[-1]: self.expr+=('0' if not self.expr or self.expr[-1]=='%' else '')+'.'
  elif k=='%':
   if self.expr and (self.expr[-1].isdigit() or self.expr[-1]==')'): self.expr+='%' 
  elif k=='(':
   if self.done: self.expr=''; self.done=False
   if self.expr and (self.expr[-1].isdigit() or self.expr[-1]==')'): self.expr+='×'
   self.expr+='('
  elif k==')':
   if self.expr.count('(')>self.expr.count(')') and self.expr[-1] not in '+−×÷.(': self.expr+=')'
  elif k.isdigit():
   if self.done: self.expr=''; self.done=False
   if self.expr.endswith(')') or self.expr.endswith('%'): self.expr+='×'
   self.expr+=k
  self.refresh()
 def calculate(self):
  try: value=evaluate(self.expr)
  except (ValueError,ZeroDivisionError): self.out.configure(text='Error',fg='#ff6b63'); self.hint.configure(text='Check expression'); return
  result=format_number(value); self.history.insert(0,{'expression':self.expr,'result':result,'time':datetime.now().isoformat(timespec='seconds')}); self.history=self.history[:100]; self.save_history(); self.expr=str(int(value)) if value.is_integer() else str(value); self.done=True; self.expl.configure(text=self.expr+' ='); self.out.configure(text=result,fg=WHITE); self.hint.configure(text='Saved to history'); self.render_history()
 def refresh(self):
  self.expl.configure(text=self.expr)
  if not self.expr: self.out.configure(text='0',fg=WHITE); self.hint.configure(text=''); return
  try: self.out.configure(text=format_number(evaluate(self.expr)),fg=WHITE); self.hint.configure(text='Preview')
  except (ValueError,ZeroDivisionError): self.out.configure(text='',fg=WHITE); self.hint.configure(text='')
 def load(self,value): self.expr=value.replace(' ',''); self.done=True; self.refresh()
 def clear_history(self):
  if self.history and messagebox.askyesno('Clear history','Delete all saved calculations?'): self.history=[]; self.save_history(); self.render_history()
 def copy(self):
  try: value=format_number(evaluate(self.expr))
  except (ValueError,ZeroDivisionError): value=self.out.cget('text')
  if value and value!='Error': self.root.clipboard_clear(); self.root.clipboard_append(value); self.hint.configure(text='Copied')
if __name__=='__main__':
 root=tk.Tk(); Calculator(root); root.mainloop()
