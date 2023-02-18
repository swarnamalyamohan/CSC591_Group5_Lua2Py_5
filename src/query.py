import math

def has(col):
    '''
    A query that returns contents of a column. If `col` is a `NUM` with
    unsorted contents, then sort before return the contents.
    Called by (e.g.) the `mid` and `div` functions.
    '''
    if not col['isSym'] and not col['ok']:
        col['has'].sort()
    col['ok'] = True
    return col['has']

def mid(col):
    '''
    A query that  returns a `cols`'s central tendency  
    (mode for `SYM`s and median for `NUM`s). Called by (e.g.) the `stats` function.
    '''
    if col['isSym']:
        return col['mode']
    else:
        return per(has(col),0.5)

def div(col):
    '''
    A query that returns a `col`'s deviation from central tendency    
    (entropy for `SYM`s and standard deviation for `NUM`s)..
    '''
    if (col['isSym']):
        e = 0
        for n in col['has']:
            e = e-n/col['n']*math.log(n/col['n'],2)
            return e
    else:
        return (per(has(col),0.9) - per(has(col),0.1))/2.58
    
def stats(data,fun=None,cols=None,nPlaces=None):
    '''
    A query that returns `mid` or `div` of `cols` (defaults to `data.cols.y`)
    '''
    cols = cols if cols else data['cols']['y']
    tmp = kap(cols, lambda k, col: (rnd((fun or mid)(col), nPlaces), col['txt']))
    tmp["N"] = len(data.rows)
    return tmp, list(map(mid, cols))

def norm(num,n):
    '''
    A query that normalizes `n` 0..1. Called by (e.g.) the `dist` function.
    '''
    if(n=='?'):
        return n
    else:
        return (n-num['lo'])/(num['hi']-num['lo'] + 1/math.inf)
    
def value(has,nB=None,nR=None,sGoal=None):
    '''
    -- A query that returns the score a distribution of symbols inside a SYM.
    '''    
    sGoal = sGoal if sGoal!=None else True
    nB = nB if nB !=None else 1
    nR = nR if nR !=None else 1
