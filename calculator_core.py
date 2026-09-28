import ast, math, operator, re
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}
def _value(n):
 if isinstance(n,ast.Expression): return _value(n.body)
 if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return float(n.value)
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):
  v=_value(n.operand); return v if isinstance(n.op,ast.UAdd) else -v
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.Invert): return _value(n.operand)/100
 if isinstance(n,ast.BinOp) and type(n.op) in OPS:
  left=_value(n.left)
  if isinstance(n.right,ast.UnaryOp) and isinstance(n.right.op,ast.Invert):
   pct=_value(n.right.operand)/100; right=left*pct if isinstance(n.op,(ast.Add,ast.Sub)) else pct
  else: right=_value(n.right)
  return OPS[type(n.op)](left,right)
 raise ValueError('Invalid expression')
def evaluate(expression):
 text=expression.translate(str.maketrans({'×':'*','÷':'/','−':'-'}))
 if not text.strip() or not re.fullmatch(r'[0-9+*/().%\-\s]+',text): raise ValueError('Invalid expression')
 text=re.sub(r'(\([^()]*\)|\d+(?:\.\d*)?)%',r'~(\1)',text)
 try: value=_value(ast.parse(text,mode='eval'))
 except ZeroDivisionError: raise
 except (SyntaxError,OverflowError) as exc: raise ValueError('Invalid expression') from exc
 if not math.isfinite(value): raise ValueError('Result out of range')
 return value
def format_number(value):
 if abs(value)<1e-12: value=0.0
 if value.is_integer() and abs(value)<1e16: return f'{int(value):,}'.replace(',',' ')
 return f'{value:,.10g}'.replace(',',' ')
