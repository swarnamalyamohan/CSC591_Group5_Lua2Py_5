import math

def COL(n,s):
    '''
    Create a 'NUM' or a 'SYM' Column
    names are a little language that    
    e.g. makes `NUM`s if name starts in upper case; or
    e.g. makes goals if the name ends with
    the maximize (`+`) or minimize (`-`) or klass (`!`) symbol.
    '''
    if ord(s[0]) >= 65 and ord(s[0]) <= 90:
        col = NUM(n,s)
    else:
        col = SYM(n,s)
    
    col.isIgnored = 'X' in col['txt'][-1]
    col.isKlass = '!' in col['txt'][-1]
    col.isGoal = any(x in col['txt'][-1] for x in ['!', '+', '-'])

    return col

def NUM(n,s):
    '''
    Create a 'NUM' to summarize a stream of numbers
    '''
    return {

        'at' : n if n!=None else 0,
        'txt' : s if s!=None else 0,
        'n' : 0,
        'hi' : -math.inf,
        'lo' : math.inf,
        'ok' : True,
        'has' : {},
        'w' : -1 if (s or "").endswith('-') else 1

    }
    

def SYM(n=None,s=None):
    '''
    Create a `SYM` to summarize a stream of symbols.
    '''
    return {

        'at' : n if n!=None else 0,
        'txt' : s if s!=None else 0,
        'n' : 0,
        'mode' : None,
        'most' : 0,
        'isSym' : True,
        'has' : {},
    }

def COLS(ss):
    '''
    Create a set of `NUM`s or `SYM`s columns.
    Once created, all cols are stored in `all`
    while the non-skipped cols are also stored as
    either `cols.x` independent input variables or
    `cols.y` dependent goal variables.
    '''
    cols={}
    cols['names'] = ss
    cols['all'] = []
    cols['x'] = []
    cols['y'] = []
    for n,s in enumerate(ss):
        col = cols['all'].append(COL(n,s))
        if not col.isIgnored:
            if col.isKlass:
                cols.klass = col
            if col.isGoal:
                cols['y'].append(col)
            else:
                cols['x'].append(col)
    return cols

def RANGE(at,txt,lo,hi=None):
    '''
    Create a RANGE  that tracks the y dependent values seen in 
    the range `lo` to `hi` some independent variable in column number `at` whose name is `txt`. 
    Note that the way this is used (in the `bins` function, below)
    for  symbolic columns, `lo` is always the same as `hi`.
    '''
    return {
        'at' : at,
        'txt' : txt,
        'lo' : lo,
        'hi' : lo if hi is None else hi,
        'y' : SYM() 
    }


def row(data,t):
    '''
    Update `data` with  row `t`. If `data.cols`
    does not exist, the use `t` to create `data.cols`.
    Otherwise, add `t` to `data.rows` and update the summaries in `data.cols`.
    To avoid updating skipped columns, we only iterate
    over `cols.x` and `cols.y`.
    '''
    if data['cols']:
        data['rows'].append(t)
        for cols in [data['cols']['x'],data['cols']['y']]:
            for col in cols:
                add(col, t[col['at']])

    else:
        data['cols'] = COLS(t)

    return data

def add(col,x,n=None):
    '''
    Update one COL with `x` (values from one cells of one row).
    Used  by (e.g.) the `row` and `adds` function.
    `SYM`s just increment a symbol counts.
    `NUM`s store `x` in a finite sized cache. When it
    fills to more than `the.Max`, then at probability 
    `the.Max/col.n` replace any existing item
    (selected at random). If anything is added, the list
    may not longer be sorted so set `col.ok=false`.
    '''
    if (x!='?'):
        n = n or 1
        col['n'] = col['n'] + n
        if col['isSym']:
            col['has']['x'] = n + (col['has']['x'] if col['has']['x'] else 0)
            if(col['has']['x'] > col['most']):
                col['most'], col['mode'] = col['has']['x'],x
        else:
            col['lo'] = min(x,col['lo'])
            col['hi'] = max(x,col['hi'])
            all = len(col['has'])
            pos = (all < the['Max'] and all+1) or (rand() < the['Max']/col['n'] and rint(1,all))
            if pos:
                col['has']['pos'] = x
                col['ok'] = False

def adds(col,t):
    '''
    Update a COL with multiple items from `t`. This is useful when `col` is being
    used outside of some DATA.
    '''
    for x in t:
        add(col,x)
    return col

def extend(range,n,s):
    '''
    Update a RANGE to cover `x` and `y`
    '''
    range['lo'] = min(n,range['lo'])
    range['hi'] = max(n,range['hi'])
    add(range['y'],s)

