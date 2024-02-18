# Revision of 18 Feb 2024
# The following lines are to enable deletion of a line in a windows command prompt

import random
import time
import string
random.seed(time.time())
from itertools import product
        
                #############################################################
_al='╔'         # Symbols for the Fitch-style proof display                 #
_il='║'         #                                                           #   
_ma='╠'         #                                                           #
_cl='╚'         #                                                           #
_sal='■'        #                                                           #
                ############################################################# 
_im=':'         # Symbols for implication, assumpttion, new argument,       #
_as='!'         # left and right bracket in expressions                     #  
_na='@'         #                                                           # 
_lb='['         #                                                           #
_rb=']'         #                                                           #
                #########################################################################
_sp='$'         # A reserved meaningless symbol                                         #
_eq='='         # Symbol for equality                                                   #                                          
_pr="'"         # Prime - variable suffix                                               #
_pm=5           # Upper bound for number of primes automatically appended to a variable #
_ss=""          # Subscript symbol                                                      #
_f="!"          # Symbol for False                                                      #
_v='?'          # Symbol for disjunction                                                #
                #########################################################################

_par = {                                            # Other parameters
    "name" : "",                                    # Name of the notebook
    "printing" : True,                              # Whether or not output each action to console 
    "new line" : {                                  # New line generator
        "LaTeX" : "\\\\\n",
        "console" : "\n"
        },
    "new paragraph" : {                             # New paragraph generator
        "LaTeX" : "\\\\[7pt]\n",
        "console" : "\n\n"
        }, 
    "mode" : "LaTeX",                             # Mode can be: LaTeX, console
    "notebook cover" : {                            # Prints this when new notebook starts 
        "LaTeX" : "[ADA] Notebook:",  
        "console" : "╔══════════════╗\n║[ADA] Notebook║\n╚══════════════╝\n"
        },                     
    "colon" : ":",                                  # Colons used outside of formal expressions
    "space" : " ",                                  # Spaces used outside of expressions
    "ADA" : "[ADA]",                                # The ADA logo
    "expression title" : "Expression",              # Heading before displaying an expression
    "expressions title" : "Expressions",            # Heading before displaying several expressions
    "action" : "!",                                 # This triggers ADA to react to user input
    "question" : "?",                               # This triggers ADA to answer a question
    "brackets" : ['(',')'],                         # Brackets used outside of expressions
    "comma" : ",",                                  # Commas used outside of expressions
    "period" : "."                                  # Periods used outside of expressions
    }

_notebook=''                                        # Stores the notebook contents
_Exp={}                                             # Stores all expressions written in the notebook
_expNo=0                                            # Counter for expressions
_var=[]                                             # List of used variables
_responseLibrary = {
    "other": {
        "expression error": [
                "You have tried to create an invalid expression!",
                "Alarm, the expression you have tried to create is invalid!"
        ],
    }
}

def pr(*inp):
    print()
    print("--start--")
    print(*inp)
    print("--end--")
    print()

def save():
    f = open(_par["name"].replace(" ","_")+".ada", "w", encoding="UTF-16")
    f.write(_notebook)
    f.close()

def _renameNonContTokens(context=[],expression=''):
# Renames all variables in the expression that are not context variables either in the expression or the provided list of expressions (the context list)      
    expression=N(expression)
    context=context+contextTokens(expression)
    comp=components(expression)
    newExpression=[]
    contTokens=[c.rootToken() for c in context if isToken(c.rootToken())]
    for c in comp:
        tokens=[v for v in reservedTokens(c) if v not in contTokens] #and isToken(c.rootToken())]
        for v in tokens:
            if isInf(v)==False and isEq(v)==False and isArg(v)==False and isToken(v):
                c=c.replaceToken(v,_rewriteToken(v,reservedTokens(c)+contTokens))
        newExpression.append(c)
    return _state(newExpression)
def order(expr):
    if isinstance(expr,str):
        return expr.count(_lb+_rb)
    return -1
def var(var="x"):
    newVar=_rewriteVar(var,_var)
    _var.append(newVar)
    return newVar
def _newLine():
# New line format for the notebook
    return _par["new line"][_par["mode"]]
def _newParagraph():
# New paragraph format for the notebook
    return _par["new paragraph"][_par["mode"]]
def notebook(name='',**parameters):
# Writes the nobook heading, or changes notebook parameters
    global _notebook
    oldname=_par["name"]
    _par["name"]=name
    for p in _par:
        if p in parameters:
            _par[p]=parameters[p]
    if name!='':
        _par["name"]=name
    if oldname!=_par["name"] and len(_notebook)>0:
        _par["name"]=oldname
    if len(_notebook)==0:
        text=_par["notebook cover"][_par["mode"]]+_par["space"]+_par["name"]
        _notebook=_notebook+text
        if _par["printing"]:    
            print(text,end="")
def forest(*inputs):
    note("\\hspace{1cm}".join([exp(i).tokenTree() for i in inputs if isExp(i)]))                        
def note(inp='',*inputs):
    global _expNo
    global _Exp
    if type(inp)==int:
        if len(inputs)==0:
            if str(inp) in list(_Exp.keys()):
                return _Exp[str(inp)]
        else:
            ref=[str(inp)]
            for i in inputs:
                if type(i)==int:
                    ref.append(str(i))
            ref=".".join(ref)
            return _Exp[ref]
    elif type(inp)==argument:
        inp=inp._conclusion
                
    global _notebook
    newLine=_newParagraph()
    if type(inp)==exp:
        if isExp(inp):
            _Exp[str(_expNo)]=inp
            _expNo=_expNo+1
            newLine=newLine+_par["expression title"]+_par["space"]+str(_expNo-1)+_par["colon"]+_newLine()+inp   
            newLine=newLine+"".join([_newLine()+'•'+_par["space"]+f'{i}' for i in inputs]) 
            if _par["printing"]:    
                print(newLine, end="")
            _notebook=_notebook+newLine 
            return inp
    elif type(inp)==list:
        expressions=[e for e in inp if type(e)==exp]
        if len(expressions)>0:
            newLine=""
            for i in range(0,len(expressions)-1):
                _Exp[str(_expNo)]=expressions[i]
                _expNo=_expNo+1
                newLine=newLine+_newLine()+_par["brackets"][0]+str(_expNo-1)+_par["brackets"][1]+_par["space"]+expressions[i]   
            _Exp[str(_expNo)]=expressions[len(expressions)-1]
            _expNo=_expNo+1
            newLine=newLine+_newLine()+_par["brackets"][0]+str(_expNo-1)+_par["brackets"][1]+_par["space"]+expressions[len(expressions)-1]   
        if newLine!="":
            if len(expressions)>1:
                newLine=_newParagraph()+_par["expressions title"]+_par["colon"]+newLine
            else:
                newLine=_newParagraph()+_par["expression title"]+_par["colon"]+newLine
            comments=""
            if len(inputs)>0:
                comments="".join(['•'+_par["space"]+f'{inputs[i]}'+_newLine() for i in range(0,len(inputs)-1)])
                comments=comments+'•'+_par["space"]+f'{inputs[len(inputs)-1]}'
            if comments!="":
                newLine=newLine+_newLine()+comments
            if _par["printing"]:    
                print(newLine, end="")
            _notebook=_notebook+newLine
            return [e for e in inp if type(e)==exp]
    elif type(inp)==str:
        newLine=newLine+str(inp)+_par["space"]+"".join([_newLine()+'•'+_par["space"]+f'{i}' for i in inputs])
        if _par["printing"]:    
            print(newLine, end="")
        _notebook=_notebook+newLine
def isExp(data):
# Determines whether input data is a ADA expression
    if type(data)!=exp and type(data)!=str:
        return False
    counter=0
    for i in range(0,len(data)):
        if data[i]==_lb:
            counter=counter+1
        if data[i]==_rb:
            counter=counter-1
        if counter<0:
            return False
    if counter!=0:
        return False
    return True
def isSVar(data):
# Determines whether input data is a stated variable
    if type(data)!=str and type(data)!=exp:
        return False
    l=len(data)
    if l<3:
        return False
    if data[0]!=_lb:
        return False
    if data[l-1]!=_rb:
        return False
    for i in range(1,l-1):
        if data[i]==_lb or data[i]==_rb:
            return False
    return True 
def isVar(data):
# Determines whether input data is a variable
    if type(data)!=str and type(data)!=exp:
        return False
    if len(data)==0:
        return False
    for char in data:
        if char==_lb or char==_rb:
            return False
    return True 
def isToken(data):
# Determines whether input data is a token
    if data==N or data=="" or isFor(data)==False:
        return False
    if type(data)!=str and type(data)!=exp:
        return False
#    if len(data)==0:
#        return False
    for c in range(0,len(data)):
        if data[c]==_lb and data[c+1]!=_rb:
            return False
    return True 
def isSta(data):
# Determines whether input data is a ADA statement
    if isExp(data)==False:
        return False  
    if len(data)<2:
        return False        
    counter=0
    for i in range(0,len(data)):
        if data[i]==_lb:
            counter=counter+1
        elif data[i]==_rb:
            counter=counter-1
        elif counter==0:
            return False
    return True
def isValue(data):
# Determintes whether input data is a stated expression (value)
    if type(data)!=str and type(data)!=exp:
        return False
    if len(data)<2:
        return False
    d=0
    c=0
    for char in data:
        if char==_lb:
            d=d+1
        elif char==_rb:
            d=d-1
        if d==0:
            c=c+1
        if c==2:
            return False
    if d!=0:
        return False
    return True
            
    
def isFor(data):
# Determines whether input data is a ADA formula
    if isExp(data)==False:
        return False
    elif isSta(data)==True:
        return False
    else:
        return True 

def isInf(formula):
# Determines whether input data is an ADA inference
    if isFor(formula)==False or len(formula)==0:
        return False
    dec=decomposeFor(formula)
    if dec[0][0]==_im and len(dec[1])==2 and dec[2]==False:
        return True
    return False

def isArg(formula):
# Determines whether input data is an ADA inference
    if isFor(formula)==False or len(formula)==0:
        return False
    dec=decomposeFor(formula)
    if len(dec[0])==0:
        return False
    for item in dec[0]:
        if item!=_im and item!=_na and item!=_as:
            return False
    return True
    
def isEq(formula):
# Determines whether input data is an ADA equality
    if isFor(formula)==False or len(formula)==0:
        return False
    dec=decomposeFor(formula)
    if dec[0][0]==_eq and len(dec[1])==2 and dec[2]==False:
        return True
    return False
    
def nonemptyComponents(expression):
# Extracts components of a ADA expression as a list of ADA expressions
    comp = []
    if isExp(expression)==False:
        return comp
    current_comp = []
    depth = 0
    for char in expression:
        if char == _lb:
            if depth > 0:
                current_comp.append(char)
            depth += 1
        elif char == _rb:
            depth -= 1
            if depth > 0:
                current_comp.append(char)
            elif depth == 0 and current_comp:
                comp.append(exp(''.join(current_comp)))
                current_comp = []
        elif depth > 0:
            current_comp.append(char)
    return comp
def components(expression):
# Extracts components of a ADA expression as a list of ADA expressions
    comp = []
    if isExp(expression)==False:
        return comp
    current_comp = []
    depth = 0
    for char in expression:
        if char == _lb:
            if depth > 0:
                current_comp.append(char)
            depth += 1
        elif char == _rb:
            depth -= 1
            if depth > 0:
                current_comp.append(char)
            elif depth == 0:
                comp.append(exp(''.join(current_comp)))
                current_comp = []
        elif depth > 0:
            current_comp.append(char)
    return comp
def distinctComponents(expression):
# Extracts distinct components of a ADA expression as a list of ADA expressions
    comp = []
    if isExp(expression)==False:
        return comp
    current_comp = []
    depth = 0
    for char in expression:
        if char == _lb:
            if depth > 0:
                current_comp.append(char)
            depth += 1
        elif char == _rb:
            depth -= 1
            if depth > 0:
                current_comp.append(char)
            elif depth == 0 and current_comp:
                newComp=exp(''.join(current_comp))
                if newComp not in comp:
                    comp.append(newComp)
                current_comp = []
        elif depth > 0:
            current_comp.append(char)
    return comp

def toExp(inp=''):
    if isSta(inp):
        return exp(inp)
    elif isFor(inp):
        return exp(_lb+inp+_rb)
    elif isinstance(inp, tuple):
        if len(inp)==0:
            return exp(_lb+_rb)
        else:
            return exp(''.join(toExp(item) for item in inp))
    elif isinstance(inp, list):
        #updateinp=[]
        #for i in inp:
        #    if isFor(i):
        #        updateinp.append(i)
        #    elif isinstance(i, tuple) or isinstance(i, #list):
        #        updateinp.append(toExp(i)#)
        if len(inp)==1 and isFor(inp[0]):
            return exp(_lb+inp[0]+_rb) 
        else:
            return exp(_lb+''.join(toExp(item) for item in inp)+_rb)
    return ''

def _state(lis):
    if type(lis)==str or type(lis)==exp:
        lis=[lis]
    if len(lis)==0:
        return N(N)
    else:
        return N(tuple([[i] for i in lis]))

def construct(constructor=0,*material):
# Returns the synapsis of expression with expressions

    replacement=[toExp(item) for item in material]
    arrangement={}
    for item in material:
        if type(item)==dict:
            arrangement={**arrangement, **item}
    # for item in material:
    #     replacements.append(toExp(item))
    #     if type(item)==list:
    #         for expr in item:
    #             if type(expr)==exp or type(expr)==str:
    #                 replacements.append(_lb+expr+_rb)
    #     elif type(item)==exp or type(item)==str:
    #         if isFor(item):
    #             replacements.append(_lb+item+_rb)
    #         elif isSta(item):
    #             replacements.append(item)    
    if type(constructor)==list:
        constructor="".join(str(expr) for expr in constructor if isExp(expr))
    elif isExp(constructor)==False:
            return N
    string=constructor
    start = 0
    counter = 0
    skip = 0
    if len(arrangement)>0:
        m=max(arrangement.keys())
    else:
        m=0
    while counter<int(m) or counter-1<len(arrangement)+len(replacement):
        index = string.find(_lb+_rb, start)
        counter = counter+1
        if index == -1:
            if counter in arrangement:
                string = string + N(arrangement[counter])
                start = start + len(arrangement[counter])
                skip = skip +1
            elif counter-1-skip<len(replacement):
                string = string + replacement[counter-1-skip]
                start = start + len(replacement[counter-1-skip])
        else:
            if counter in arrangement:
                string = string[:index]+N(arrangement[counter])+string[index + 2:]
                start = index + len(arrangement[counter])
                skip = skip +1
            elif counter-1-skip<len(replacement):
                string = string[:index]+replacement[counter-1-skip]+string[index + 2:]
                start = index + len(replacement[counter-1-skip])
    return exp(string)
def optimizeStatement(statement):
# Removes duplicate stated components   
    if isSta(statement)==False:
        return NN
    return _state(distinctComponents(statement))

def values(expression):
# Returns the list of stated components in a ADA expression
    if isExp(expression)==False:
        return NN
    return [_state([s]) for s in components(expression)]
    
def contextVars(expression):
# Returns the list of context variables in a ADA expression
    if isExp(expression)==False:
        return []    
    comps=components(expression)
    variables=[]
    for formula in comps:
        if isVar(formula):
            if formula not in variables:
                variables.append(formula)
    return variables

def contextTokens(expression):
# Returns the list of context tokens in an ADA expression
    if isExp(expression)==False:
        return []    
    comps=components(expression)
    tokens=[]
    for formula in comps:
        if isToken(formula) and formula not in tokens and isInf(formula)==False and isEq(formula)==False and isArg(formula)==False:
            tokens.append(formula)
    return tokens

def reservedTokens(expression):     
# Returns the list of all tokens reserved by an ADA expression
    if isExp(expression)==False:
        return []
    expression=exp(expression)
    tokens = []
    for c in expression.cells():
        token=expression.contents(expression.cellSegments([c])[0]).rootToken()
        if isToken(token) and isInf(token)==False and isEq(token)==False and isArg(token)==False:
            tokens.append(token)
    return tokens

def nonContTokens(expression):
    return [t for t in reservedTokens(expression) if t not in contextTokens(expression)]

def reservedVars(expression):     
# Returns the list of all variables reserved by a ADA expression
    if isExp(expression)==False:
        return []
    variables = []
    in_brackets = False
    substring = ''
    for char in expression:
        if char == _lb:
            in_brackets = True
            substring = ''
        elif char == _rb and in_brackets:
            in_brackets = False
            if substring and substring not in variables:
                variables.append(exp(substring))
        elif in_brackets and char not in NN:
            substring += char
    return variables             

def _rewriteVar(oldName,exclude=[]):  
# Renames a variable
    if isVar(oldName)==False:
        oldName='x'
    newName=oldName
    primeCount=0
    for char in reversed(oldName):
        if char == _pr:
            primeCount += 1
        else:
            break
    i=0
    while newName in exclude:
        if primeCount<_pm:
            newName=newName+_pr
            primeCount=primeCount+1
        else:
            newName=oldName+_ss+str(i)
            i=i+1
    return exp(newName)
def _rewriteRootToken(expression,exclude=[]):
# Renames the token
    if expression=="":
        return expression
    primeCount=0
    for char in reversed(expression):
        if char == _pr:
            primeCount += 1
        else:
            break
    i=0
    modifier=""
    if isVar(expression):
        while exp(expression+modifier).rootToken() in exclude:
            if primeCount<_pm:
                modifier=modifier+_pr
                primeCount=primeCount+1
            else:
                primeCount=-1
                modifier=random.choice(string.ascii_letters)
                expression=expression+modifier
        if primeCount!=-1:
            expression=expression+modifier
    else:
        while exp(expression+modifier).rootToken() in exclude:
            modifier=random.choice(string.ascii_letters)
            expression=modifier+expression
            i=i+1
    return exp(expression)
def _rewriteToken(name,exclude=[]):
# Renames the token
    if name=="":
        return name
    primeCount=0
    for char in reversed(name):
        if char == _pr:
            primeCount += 1
        else:
            break
    i=0
    modifier=""
    if isVar(name):
        while name+modifier in exclude:
            if primeCount<_pm:
                modifier=modifier+_pr
                primeCount=primeCount+1
            else:
                primeCount=-1
                modifier=random.choice(string.ascii_letters)
                name=name+modifier
        if primeCount!=-1:
            name=name+modifier
    else:
        while modifier+name in exclude:
            modifier=random.choice(string.ascii_letters)
            name=modifier+name
            i=i+1
    return exp(name)
def rewriteExp(resTokens,expression,contTokensOnly=True):
# Rewrites an expression by renaming its context tokens that are reserved elsewhere
    if contTokensOnly:    
        rewriteTokens=contextTokens(expression)
    else:
        rewriteTokens=reservedTokens(expression)
    expReservedTokens=reservedTokens(expression)
    output=exp(expression)
    for x in rewriteTokens:
        if x in resTokens:
            output=output.replaceToken(x,_rewriteToken(x,resTokens+expReservedTokens))
    return exp(output)

def decomposeFor(formula):  
# Decomposes a formula into concatenation of maximal variables and maximal statements, returned as a variable array, statement array, and boolean value indicating whether the formula starts with a variable or not
    if isFor(formula)==False:
        return [[],[],False]
    statements=[]
    variables=[]
    statBuilder=''
    varBuilder=''
    varFirst=True
    i=0
    while i in range(0,len(formula)):
        if formula[i]==_lb:
            if i==0 and varBuilder=='':
                varFirst=False
            if varBuilder!='':
                variables.append(varBuilder) 
            varBuilder=''
            s=_lb
            d=1
            j=i+1
            while j in range(i+1,len(formula)) and d>0:
                if formula[j]==_lb:
                    d=d+1
                elif formula[j]==_rb:
                    d=d-1
                s=s+formula[j]
                j=j+1
            statBuilder=statBuilder+s
            i=j
        else:
            if statBuilder!='':
                statements.append(statBuilder)
            if formula[i]!=_rb:
                varBuilder=varBuilder+formula[i]
            statBuilder=''
            i=i+1
    if statBuilder!='':
        statements.append(statBuilder)
    if varBuilder!='':
        variables.append(varBuilder)        
    return [variables,statements,varFirst]

def tree(tree='',space=0.5):
# Generates an expression tree using the `forest' package

    if isExp(tree)==False:
        tree=_state(['error: expression expected'])
    trees=[_state([c]) for c in components(tree)]
    output='\\medskip'
    for i in range(0,len(trees)-1):
        output=output+"\\medskip\\begin{forest} baseline=(current bounding box.north) baseline, for tree={grow'=north, draw, rectangle, fill=white}"
        output=output+trees[i]+'\\end{forest}\hspace{'+str(space)+'cm}'
    output=output+"\\begin{forest} baseline=(current bounding box.north) baseline, for tree={grow'=north, draw, rectangle, fill=white}"
    output=output+trees[len(trees)-1]+'\\end{forest}}'    
    return output

def semanticEquivalence(first,second,contextTokens=[]):
    if isExp(first)==False or isExp(second)==False:
        return False
    first=exp(first)
    second=exp(second)
    if first=="" and second!="":
        return False
    if second=="" and first!="":
        return False
    for s in first.cells():
        if s not in second.cells():
            return False
        c=first.contents(first.cellSegments([s])[0]).rootToken()
        d=second.contents(second.cellSegments([s])[0]).rootToken()
        if c in contextTokens and d not in contextTokens:
            return False
        if c in contextTokens and d in contextTokens and c!=d:
            return False
        if (c==N and d!=N) or (c!=N and d==N):
            return False
        if (isInf(c) and isInf(d)==False) or (isInf(c)==False and isInf(d)):
            return False
        elif isInf(c) and isInf(d):
            if c.rootToken()!=d.rootToken():
                return False
        if (isEq(c) and isEq(d)==False) or (isEq(c)==False and isEq(d)):
                return False
        elif isEq(c) and isEq(d):
            if c.rootToken()!=d.rootToken():
                return False
        if (isArg(c) and isArg(d)==False) or (isArg(c)==False and isArg(d)):
                return False
        elif isArg(c) and isArg(d):
            if c.rootToken()!=d.rootToken():
                return False
        for t in second.cells():        
            if t not in first.cells():
                return False
            c=first.contents(first.cellSegments([t])[0]).rootToken()
            d=second.contents(second.cellSegments([t])[0]).rootToken()
            if d in contextTokens and c not in contextTokens:
                return False
            if d in contextTokens and c in contextTokens and c!=d:
                return False
            if (c==N and d!=N) or (c!=N and d==N):
                return False
            if (isInf(c) and isInf(d)==False) or (isInf(c)==False and isInf(d)):
                return False
            elif isInf(c) and isInf(d):
                if c.rootToken()!=d.rootToken():
                    return False
            if (isEq(c) and isEq(d)==False) or (isEq(c)==False and isEq(d)):
                    return False
            elif isEq(c) and isEq(d):
                if c.rootToken()!=d.rootToken():
                    return False
            if (isArg(c) and isArg(d)==False) or (isArg(c)==False and isArg(d)):
                    return False
            elif isArg(c) and isArg(d):
                if c.rootToken()!=d.rootToken():
                    return False
            c=first.contents(first.cellSegments([s])[0]).rootToken()
            d=second.contents(second.cellSegments([t])[0]).rootToken()
            if (isInf(c)==False and isEq(c)==False and isArg(c)==False) and (isInf(d)==False and isEq(d)==False and isArg(c)==False):
                # print(c+d)
                # print(first.scope(first.cellSegments([s])))
                # print(first.cells([first.scope(first.cellSegments([s]))]))
                s_firstScope=first.cells([first.scope(first.cellSegments([s])[0])])
                t_firstScope=first.cells([first.scope(first.cellSegments([t])[0])])
                t_firstContents=first.contents(first.cellSegments([t])[0]).rootToken()
                s_secondScope=second.cells([second.scope(second.cellSegments([s])[0])])
                t_secondScope=second.cells([second.scope(second.cellSegments([t])[0])])
                s_secondContents=second.contents(second.cellSegments([s])[0]).rootToken()
                if s_firstScope==t_firstScope and c==t_firstContents and (s_secondScope!=t_secondScope or d!=s_secondContents):
                    return False
                if s_secondScope==t_secondScope and d==s_secondContents and (s_firstScope!=t_firstScope or c!=t_firstContents):
                    return False  
    return True

def formulateMultuple(statement):
     comps=components(statement)
     if len(comps)==1 and isSta(comps[0]):
         return exp("("+comps[0]+")")
     elif len(comps)==1:
        if len(components(comps[0]))<2:
            return comps[0] 
        else:
            return exp("("+_state([comps[0]])+")")
     else:
         return exp("("+",".join([_state([c]) for c in comps])+")")
     
def formulateTuple(statement):
    comps=components(statement)
    if len(comps)==1 and len(components(comps[0]))==0:
        return exp(str(_state(comps[0])))
    return exp("("+",".join([_state([c]) for c in comps])+")")

def formulateList(statement):
    comps=components(statement)
    #if len(comps)==1:
    #    return exp(comps[0])
    if len(comps)>2:
        l=exp(", ".join([_state([comps[i]]) for i in range(0,len(comps)-1)]))
        return l+", and "+_state([comps[len(comps)-1]])
    elif len(comps)==2:
        return N(comps[0])+" and "+N(comps[1])
    else:
        return exp(", ".join([_state([comps[i]]) for i in range(0,len(comps))]))
 
def formulateTupleList(statement):
    comps=components(statement)
    if len(comps)==1:
        if isFor(comps[0]):
            d=decomposeFor(comps[0])
            valid=True
            for c in d[0]:
                if " " in c:
                    valid=False
            if valid:
                return exp(str(_state(comps[0])))
    return exp("("+", ".join([_state([c]) for c in comps])+")")

def formulateMultupleList(statement):
    comps=components(statement)
    if len(comps)==1 and isSta(comps[0]):
        return exp("("+comps[0]+")")
    elif len(comps)==1:
       if len(components(comps[0]))<2:
           return comps[0] 
       else:
           return exp("("+_state([comps[0]])+")")
    else:
        return exp("("+", ".join([_state([c]) for c in comps])+")")


class exp(str):
# The expression class
    def __init__(self, content=''):
    # Initializes a ADA expression
        super().__init__()
    def __call__(self,*expressions):
    # Returns the synapsis of expressions (does not modify the current expression)
        if len(expressions)==1:
            if type(expressions[0])==int:
                if isVar(self):
                    return self+str(expressions[0])
                elif 0<expressions[0]<len(components(self))+1:
                    return components(self)[expressions[0]-1]
        return construct(self,*expressions)
    def isVar(self):
    # Notes whether the expression is a ADA variable
        note(_par["ADA"]+_par["colon"]+_par["space"]+'It is '+str(isVar(self))+' that "'+ self+'" is a variable.')
    def isCon(self):
    # Notes whether the expression is a ADA constant
        note(_par["ADA"]+_par["colon"]+_par["space"]+'It is '+str(isVar(self.replace(_lb+_rb,'')) and not isVar(self))+' that "'+ self+'" is a constant.')    
    def isExp(self):
    # Notes whether the expression is a valid ADA expression
        note(_par["ADA"]+_par["colon"]+_par["space"]+'It is '+str(isExp(self))+' that "'+ self+'" is an expression.')
    def isSta(self):
    # Notes whether the expression is a ADA statement
        note(_par["ADA"]+_par["colon"]+_par["space"]+'It is '+str(isSta(self))+' that "'+ self+'" is an statement.')
    def isFor(self):
    # Notes whether the expression is a ADA formula
        note(_par["ADA"]+_par["colon"]+_par["space"]+'It is '+str(isFor(self))+' that "'+ self+'" is a formula.')
    def isEquiv(self,expression):
    # Notes whether the expression is a ADA formula
        note(_par["ADA"]+_par["colon"]+_par["space"]+'It is '+str(semanticEquivalence(self,expression))+' that "'+ self+'" and "'+expression+'" are semantically equivalent.')
    def components(self):
    # Returns components of the expression
        comp=components(self)
        #note(_par["ADA"]+_par["colon"]+_par["space"]+'The components of "'+self+'" are: "'+'", "'.join(str(c) for c in comp)+'".')
        return comp
    def compSegments(self):
    # Extracts components of a ADA expression as a list of ADA expressions
        comp = []
        leftRanks=[]
        rightRanks=[]
        if isExp(self)==False:
            return comp
        current_comp = []
        depth = 0
        for i in range(0,len(self)):
            if self[i] == _lb:
                if depth > 0:
                    current_comp.append(self[i])
                else:
                    leftRanks.append(i+1)    
                depth += 1
            elif self[i] == _rb:
                depth -= 1
                if depth > 0:
                    current_comp.append(self[i])
                elif depth == 0:
                    comp.append(exp(''.join(current_comp)))
                    current_comp = []
                    rightRanks.append(len(self)-i)
            elif depth > 0:
                current_comp.append(self[i])
        return [((leftRanks[i],rightRanks[i]),comp[i]) for i in range(0,len(comp))]
    def note(self,*comments):
    # Notes the expression
        note(self,*comments)
        return self
    
    def dual(self):
        dualExpression=""
        for i in range(0,len(self)):
            if self[len(self)-i-1]==_lb:
                dualExpression=dualExpression+_rb
            elif self[len(self)-i-1]==_rb:
                dualExpression=dualExpression+_lb
            else:
                dualExpression=dualExpression+self[len(self)-i-1]
        return exp(dualExpression)
    
    def subExpressions(self):
        subs=[]
        for i in range(0,len(self)):
            for j in range(i+1,len(self)+1):
                if isExp(self[i:j]):
                    subs.append((i,len(self)-j))
        return subs
    def sepTokens(self):
        cells=self.cells()
        revised=self
        checked=[]
        cells=[cells[len(cells)-i-1] for i in range(0,len(cells))]
        for i in range(0,len(cells)):
            if i in checked:
                continue
            revisionNeeded=False
            matching=[]
            cont=revised.contents(revised.cellSegments([cells[i]])[0])
            for j in range(i,len(cells)):
                if j in checked:
                    continue
                if cont.rootToken()==revised.contents(revised.cellSegments([cells[j]])[0]).rootToken():
                    if revised.scope(revised.cellSegments([cells[i]])[0])==revised.scope(revised.cellSegments([cells[j]])[0]):
                        matching.append(j)
                        checked.append(j)
                    elif i!=j:
                        revisionNeeded=True
            if revisionNeeded==False:
                continue
            newCont=_rewriteRootToken(cont,reservedTokens(revised))
            for j in matching:
                segment=revised.cellSegments([cells[j]])[0]
                revised=exp(revised[0:segment[0]]+newCont+revised[len(revised)-segment[1]:len(revised)])
        return exp(revised)  
    def sepVars(self):
        pins=self.pins()
        revised=self
        checked=[]
        pins=[pins[len(pins)-i-1] for i in range(0,len(pins))]
        for i in range(0,len(pins)):
            if i in checked:
                continue
            revisionNeeded=False
            matching=[]
            for j in range(i,len(pins)):
                if j in checked:
                    continue
                if self.contents(self.cellSegments([pins[i]])[0])==self.contents(self.cellSegments([pins[j]])[0]):
                    if self.scope(self.cellSegments([pins[i]])[0])==self.scope(self.cellSegments([pins[j]])[0]):
                        matching.append(j)
                        checked.append(j)
                    elif i!=j:
                        revisionNeeded=True
            if revisionNeeded==False:
                continue
            newvar=_rewriteVar(self.contents(self.cellSegments([pins[i]])[0]),reservedVars(revised))
            for j in matching:
                segment=revised.cellSegments([pins[j]])[0]
                revised=exp(revised[0:segment[0]]+newvar+revised[len(revised)-segment[1]:len(revised)])
        return exp(revised)                             
    def cogsContents(self):
        d=-1
        ats=[]
        reading=''
        for i in range(0,len(self)):
            if self[i]==_lb:
                if d==-1:
                    if reading!="" and i>0:
                        ats.append(exp(reading))
                    reading=_lb
                    d=1
                elif d>-1:
                    reading=reading+_lb
                    d=d+1
            elif self[i]==_rb:
                reading=reading+_rb
                d=d-1
            else:
                if d==0:
                    ats.append(exp(reading))
                    reading=self[i]
                    d=-1
                else:
                    reading=reading+self[i]
        if reading!="":
            ats.append(exp(reading))
        return ats
    def cogs(self):
        d=-1
        ats=[]
        reading=''
        cogLeftIndex=[0]
        cogRightIndex=[]
        for i in range(0,len(self)):
            if self[i]==_lb:
                if d==-1:
                    if reading!="" and i>0:
                        ats.append(exp(reading))
                        cogLeftIndex.append(i)
                        cogRightIndex.append(len(self)-i)
                    reading=_lb
                    d=1
                elif d>-1:
                    reading=reading+_lb
                    d=d+1
            elif self[i]==_rb:
                reading=reading+_rb
                d=d-1
            else:
                if d==0:
                    ats.append(exp(reading))
                    cogRightIndex.append(len(self)-i)
                    cogLeftIndex.append(i)
                    reading=self[i]
                    d=-1
                else:
                    reading=reading+self[i]
        if reading!="":
            cogRightIndex.append(0)
            ats.append(exp(reading))
        return [((cogLeftIndex[i],cogRightIndex[i]),ats[i]) for i in range(0,len(ats))]
        
    def atoms(self):
        d=0
        ats=[]
        reading=''
        for i in range(0,len(self)):
            if self[i]==_lb:
                if d==0:
                    if reading!="" and i>0:
                        ats.append(exp(reading))
                    reading=_lb
                elif d>0:
                    reading=reading+self[i]
                d=d+1
            elif self[i]==_rb:
                if d==1:
                    reading=reading+_rb
                    ats.append(exp(reading))
                    reading=""
                elif d>1:
                    reading=reading+self[i]
                d=d-1
            else:
                reading=reading+self[i]
        if reading!="":
            ats.append(exp(reading))
        return ats
                
    
    def assume(self,statement=''):
    # Produces a valid assumption based on the input and self as the contex   
        if isExp(statement)==False:
            statement=NN
        elif isSta(statement)==False:
            statement=_state([statement])
        #comp=components(statement)
        #for c in comp:
        #    if isToken(c) and c in contextTokens(self):
        #        return exp("[Error]")
        return rewriteExp(nonContTokens(self),statement)

    def replaceToken(self,token,replacement):
        if isToken(token)==False or isToken(replacement)==False:
            return self
        replacement=exp(replacement)
        newExpr=self
        for cell in self.cells():
            segment=newExpr.cellSegments([cell])[0]
            cont=newExpr.contents(segment)
            if newExpr.contents(segment).rootToken()==token:
                comps=components(cont)
                newCont=replacement(*[[c] for c in comps])
                newExpr=exp(newExpr[:segment[0]]+newCont+newExpr[len(newExpr)-segment[1]:])
        return newExpr
    
    def subInToken(self,context,token,replacement,valueSeries=[]):
        if isToken(token)==False:
            return self
        if token in reservedTokens(replacement):
            return False
        replacement=exp(replacement)
        replacement=rewriteExp([c for c in reservedTokens(self) if c not in context],replacement,False)
        newExpr=self
        while token in reservedTokens(newExpr): 
            for cell in newExpr.cells():
                segment=newExpr.cellSegments([cell])[0]
                cont=newExpr.contents(segment)
                if cont.rootToken()==token:
                    # stopped here
                    comps=components(cont)
                    arrangement=[]
                    for i in range(0,len(valueSeries)):
                        if valueSeries[i]-1 in range(0,len(comps)):
                            arrangement.append(comps[valueSeries[i]-1])
                        elif valueSeries[i]==0:
                            arrangement.append(N(N))                   
                    newCont=replacement(*arrangement)
                    newExpr=exp(newExpr[:segment[0]]+newCont+newExpr[len(newExpr)-segment[1]:])
                    break
        return newExpr   
    
    def restate(self,statement='',newVars=''):
    # Produces a valid restatement of the input based on self as the contex
        if isSta(statement)==False:
            statement=NN
        if isSta(newVars)==False:
            newVars=NN
        newVars=[x for x in components(newVars) if isVar(x)]
        statement=N(_state([e for e in components(statement) if e in components(self)]))
        restatement=''
        allowedVars=[x for x in newVars if x not in contextVars(self) and x not in reservedVars(statement)]
        listVarsToReplace=[y for y in reservedVars(statement) if y not in contextVars(self)]
        for i in range(0,len(listVarsToReplace)):
            if i<len(allowedVars):
                statement=statement.replace(_lb+listVarsToReplace[i]+_rb,_lb+allowedVars[i]+_rb)
            else:
                i=len(listVarsToReplace)
        restatement=restatement+statement                    
        return N(restatement)

    def call(self,inp=''):
    # Produces a valid call of a statement based on self as the contex
        if isExp(inp)==False:
            inp=NN
        elif isSta(inp)==False:
            inp=_state([inp])
        # Add a line to the proof
        return rewriteExp(contextVars(self),rewriteExp(reservedVars(self),inp),False)

                
    def identity(self,value=''):
    # Produces a valid identity based on self as the context 
        if isValue(value)==False:
            value=NN
        if components(value)[0] not in components(self):
            value=NN
        return E(value,value)
    
    def proposition(self,assumption='',proof='',statement=''):
    # Produces a valid proposition based on the assumption, the proof, the statement, and on self as the context                 
        if isSta(assumption)==False and assumption!='':
            assumption=NN
        if isSta(proof)==False and proof!='':
            proof=NN
        if isSta(statement)==False and statement!='':
            statement=NN 
        comp=components(assumption)
        for c in comp:
            if c!="":
                return N(I(assumption,N(*{x for x in reservedTokens(statement) if x not in contextTokens(statement) and x in contextTokens(proof) and x not in contextTokens(assumption) and x not in contextTokens(self)})+N(*[y for y in components(statement) if y not in contextTokens(assumption) and y not in contextTokens(self)]))) 
        return exp(N(*{x for x in reservedVars(statement) if x not in contextVars(statement) and x in contextVars(proof) and x not in contextVars(assumption) and x not in contextVars(self)})+statement)

    def apply(self,deduction=0,*inputs, **pars):
    # Produces a valid application of a deduction formula with the specified concretization, based on self as the context           
        logic="restricted"
        if "logic" in pars:
            logic=pars["logic"]
        deduction=exp(deduction)
        if isSta(deduction):
            if len(components(deduction))>0:
                deduction=components(deduction)[0]
        if isInf(deduction)==False:
            return         
        matched=False
        cont=components(self)
        conTokens=[]
        revisedInputs=[]
        for c in cont:
            if isToken(c):
                conTokens.append(c)
        for c in cont:
            if semanticEquivalence(c,deduction,conTokens):
                matched=True
                break
        if matched==False:
            return exp("[Error]")
        dec=decomposeFor(deduction)
        newPremise=[]        
        tokens=contextTokens(dec[1][0])
        premiseComponents=components(dec[1][0])
        freeTokensList=[v for v in tokens if v not in contextTokens(self) and isToken(v)]
        newPremise=[v for v in premiseComponents if v not in contextTokens(self) and isToken(v)==False]
        revisedInputs=[]
        for c in inputs:
            if isSta(c): 
                if len(components(c))==1:                
                    if isToken(c[0])==False:
                        revisedInputs.append(c[0])
            else:                  
                if isToken(c)==False:
                    revisedInputs.append(c)
        inputs=revisedInputs
        
        if len(inputs)<len(freeTokensList):
            newPremise=freeTokensList[len(inputs):]+newPremise
        
        deduction=exp(_state(newPremise)+_im+dec[1][1])
        m=min(len(inputs),len(freeTokensList))
        for i in range(0,m):
            if isExp(inputs[i]):
                k=order(freeTokensList[i])
                if k<order(inputs[i]) and logic!="unrestricted":
                    return exp("[Error]")
                if 0<k:
                    o=order(inputs[i])
                    subs=[i for i in range(1,o+1)]
                    deduction=deduction.subInToken(nonContTokens(self)+reservedTokens(deduction),freeTokensList[i],inputs[i],subs)
                else:
                    deduction=deduction.subInToken(nonContTokens(self)+reservedTokens(deduction),freeTokensList[i],inputs[i])
            elif len(inputs[i])==2:
                oldOrder=order(inputs[i][0])
                revisedOrder=oldOrder
                valids=[]
                for k in inputs[i][1]:
                    if 0<k<order(freeTokensList[i])+1:
                        if k in valids:
                            revisedOrder=revisedOrder-1
                        valids.append(k)
                if len(valids)<oldOrder and logic!="unrestricted":
                    return exp("[Error]")
                if order(freeTokensList[i])<revisedOrder and logic!="unrestricted":
                    return exp("[Error]")
                deduction=deduction.subInToken(nonContTokens(self)+reservedTokens(deduction),freeTokensList[i],inputs[i][0],inputs[i][1]) 
        matched=[]
        dec=decomposeFor(deduction)
        premise=components(dec[1][0])
        for c in range(0,len(premise)):
            #if premise[c]!="":
            expr=exp(self+N(premise[c]))
            compCells=expr.componentCells()
            cell1=compCells[len(compCells)-1]
            for i in range(0,len(compCells)-1):
                if expr.doMatch(cell1,compCells[i]):
                    matched.append(c)
                    break       
        essentialPremise=[]
        for c in premise:
            if c!=N:
                essentialPremise.append(c)    
        if len(matched)==len(essentialPremise):
            return rewriteExp(nonContTokens(self),decomposeFor(deduction)[1][1])
        else:
            #p("".join(N(c) for c in premise if c not in matched)+_im+decomposeFor(deduction)[1][1])
            return N("".join(N(premise[c]) for c in range(0,len(premise)) if c not in matched)+_im+decomposeFor(deduction)[1][1])

    def uniqueVars(self,expression=''):
    # Return the list of reserved variables in the expression that do not occur in self unless in a subexpression that matches with the statement of the given expression
        if isExp(expression)==False:
            return []
        return [v for v in reservedVars(expression) if v not in reservedVars(self.replace(_state([expression]),''))]

    def localVars(self,start=0,end=0):
    # returns the list of local variables in a stated expression at the marked location
        if start<0 or start>end or end>len(self):
            return []
        if isSta(self[start:end])==False:
            return []
        #if isValue(self[start:end])==False:
        #    return []
        localVars=reservedVars(self[start:end])
        leftPos=start
        rightPos=end
        while leftPos>0:
            d=0
            i=leftPos
            while d<1 and i>0:
                i=i-1
                if self[i]==_lb:
                    d=d+1
                if self[i]==_rb:
                    d=d-1
            for v in contextVars(self[i+d:leftPos]):
                if v in localVars:
                    localVars.remove(v)
            leftPos=i
        while rightPos<len(self)-1: 
            d=0
            j=rightPos
            while d<1 and j<len(self):
                if self[j]==_rb:
                    d=d+1
                if self[j]==_lb:
                    d=d-1
                j=j+1
            for v in contextVars(self[rightPos:j-d]):
                if v in localVars:
                    localVars.remove(v)
            rightPos=j   
        return localVars
    def relativeLeftComponents(self,start=0,end=0):
    # returns the list of components before the marked location
        if start<0 or start>end or end>len(self):
            return []
        relComp=[]
        leftPos=start
        # rightPos=end
        while leftPos>0:
            d=0
            i=leftPos
            while d<1 and i>0:
                i=i-1
                if self[i]==_lb:
                    d=d+1
                if self[i]==_rb:
                    d=d-1
            for c in components(self[i+d:leftPos]):
                relComp.append(c)
            leftPos=i
        return relComp
    def relativeComponents(self,start=0,end=0):
    # returns the list of components before the marked location
        if start<0 or start>end or end>len(self):
            return []
        relComp=[]
        leftPos=start
        rightPos=end
        while leftPos>0:
            d=0
            i=leftPos
            while d<1 and i>0:
                i=i-1
                if self[i]==_lb:
                    d=d+1
                if self[i]==_rb:
                    d=d-1
            for c in components(self[i+d:leftPos]):
                relComp.append(c)
            leftPos=i
        while rightPos<len(self)-1: 
            d=0
            j=rightPos
            while d<1 and j<len(self):
                if self[j]==_rb:
                    d=d+1
                if self[j]==_lb:
                    d=d-1
                j=j+1
            for c in components(self[rightPos:j-d]):
                relComp.append(c)
            rightPos=j 
        return relComp
    def relativeContextTokens(self,start=0,end=0):
    # returns the list of surrounding context variables for a stated expression at the marked location
        if start<0 or start>end or end>len(self):
            return []
        if isSta(self[start:end])==False:
            return []
        if isValue(self[start:end])==False:
            return []
        relContTokens=[]
        leftPos=start
        rightPos=end
        while leftPos>0:
            d=0
            i=leftPos
            while d<1 and i>0:
                i=i-1
                if self[i]==_lb:
                    d=d+1
                if self[i]==_rb:
                    d=d-1
            for v in contextTokens(self[i+d:leftPos]):
                relContTokens.append(v)
            leftPos=i
        while rightPos<len(self)-1: 
            d=0
            j=rightPos
            while d<1 and j<len(self):
                if self[j]==_rb:
                    d=d+1
                if self[j]==_lb:
                    d=d-1
                j=j+1
            for v in contextVars(self[rightPos:j-d]):
                relContTokens.append(v)
            rightPos=j 
        return relContTokens
    def relativeContextVars(self,start=0,end=0):
    # returns the list of surrounding context variables for a stated expression at the marked location
        if start<0 or start>end or end>len(self):
            return []
        if isSta(self[start:end])==False:
            return []
        if isValue(self[start:end])==False:
            return []
        relContVars=[]
        leftPos=start
        rightPos=end
        while leftPos>0:
            d=0
            i=leftPos
            while d<1 and i>0:
                i=i-1
                if self[i]==_lb:
                    d=d+1
                if self[i]==_rb:
                    d=d-1
            for v in contextVars(self[i+d:leftPos]):
                relContVars.append(v)
            leftPos=i
        while rightPos<len(self)-1: 
            d=0
            j=rightPos
            while d<1 and j<len(self):
                if self[j]==_rb:
                    d=d+1
                if self[j]==_lb:
                    d=d-1
                j=j+1
            for v in contextVars(self[rightPos:j-d]):
                relContVars.append(v)
            rightPos=j 
        return relContVars
    def isSegment(self,segment=(-1,-1)):
    # Checks whether the input is a segment in self
        if type(segment)!=tuple and type(segment)!=list:
            return False
        if len(segment)!=2:
            return False
        if type(segment[0])!=int:
            return False
        if type(segment[1])!=int:
            return False
        if segment[0]<0 or segment[0]+segment[1]>len(self) or segment[1]<0:
            return False
        return True         
    def isCellSegment(self,segment=[-1,-1]):
    # Checks whether the input is a cog in self 
        if self.isSegment(segment)==False:
            return False
        if segment[0]==0 and segment[1]!=0:
            return False
        if segment[0]!=0 and segment[1]==0:
            return False
        if segment[0]==0 and segment[1]==0:
            return True
        else:
            return isValue(self[segment[0]-1:len(self)-segment[1]+1])
    def isPinSegment(self,pin=[-1,-1]):
    # Checks whether the input is a pin in self
        if self.isCellSegment(pin)==False:
            return False
        return isVar(self[pin[0]:len(self)-pin[1]])
    def contents(self,*segment):
    # Returns contents of a segment in self
        if len(segment)==0:
            return N
        if type(segment[0])==list or type(segment[0])==tuple:
            segment=segment[0]
        if self.isSegment(segment)==False:
            return N
        if isExp(self[segment[0]:len(self)-segment[1]]):
            return exp(self[segment[0]:len(self)-segment[1]])
        else:
            return self[segment[0]:len(self)-segment[1]]
    def cellContents(self,cell):
    # Returns contents of a segment in self
        return self.contents(self.cellSegments([cell])[0]).rootToken()
    def cellSegments(self,cells=[]):
    # Returns the list of all cogs, with an optional input of cells, in which case cogs of the cells are returned
        if cells==[]:
            cellSegments=[]
            for i in range(0,len(self)):
                if self.cellSegment(i)!=[-1,-1]:
                    cellSegments.append(self.cellSegment(i))
            return cellSegments
        elif type(cells)==list:
            cellSegments=[]
            for cell in cells:
                if type(cell)!=list and type(cell)!=tuple:
                    continue
                if len(cell)!=2:
                    continue
                if type(cell[0])!=int:
                    continue
                if type(cell[1])!=int:
                    continue
                if cell[0]<0:
                    continue
                if cell[1]<0:
                    continue
                c=0
                start=0
                if cell[0]>0:
                    for i in range(0,len(self)):
                        if self[i]==_lb:
                            c=c+1
                        if c==cell[0]:
                            start=i+1
                            break
                    if cell[0]>c:
                        continue
                else:
                    start=0
                c=0
                end=0
                if cell[1]>0:
                    for i in range(0,len(self[::-1])):
                        if self[::-1][i]==_rb:
                            c=c+1
                        if c==cell[1]:
                            end=i+1
                            break
                    if cell[1]>c:
                        continue
                else:
                    end=0
                if self.isCellSegment([start,end]):
                    cellSegments.append([start,end])
            return cellSegments
        else:
            return []
    def componentCells(self):
        cells = []
        if isExp(self)==False:
            return cells
        current_cell = []
        oBracketCount = 0
        cBracketCount = self.count(_rb)
        depth = 0
        for char in self:
            if char == _lb:
                oBracketCount = oBracketCount+1
                if depth==0:
                    current_cell.append(oBracketCount)
                depth += 1
            elif char == _rb:
                cBracketCount = cBracketCount-1
                depth -= 1
                if depth == 0:
                    current_cell.append(cBracketCount+1)    
                    cells.append(current_cell)
                    current_cell = []
        return cells
    def cells(self,cellSegments=[]):
        if type(cellSegments)==list and len(cellSegments)==0:
            cellSegments=self.cellSegments()
        elif type(cellSegments)!=list:
            return []
        cells=[]
        for segment in cellSegments:
            if self.isCellSegment(segment)==False:
                continue
            cellStart=0
            cellEnd=0
            if segment[0]==0 and segment[1]==0:
                cells.append((cellStart,cellEnd))
            else:
                for i in range(0,segment[0]):
                    if self[i]==_lb:
                        cellStart=cellStart+1
                for i in range(0,segment[1]):
                    if self[::-1][i]==_rb:
                        cellEnd=cellEnd+1
                cells.append((cellStart,cellEnd))
        return cells
    def pins(self):
    # Returns the list of all pins
        return [self.cells([s])[0] for s in self.cellSegments() if self.isPinSegment(s)]
    def scope(self,cellSegment=[-1,-1]):
    # returns the segment of the scope of a cell segment  
        if self.isCellSegment(cellSegment)==False:
            return [-1,-1]
        rootToken=self.contents(cellSegment).rootToken()
        if rootToken==N:
            return [0,0]
        if isInf(rootToken)==True:
            return [0,0]
        if isEq(rootToken)==True:
            return [0,0]
        if isArg(rootToken)==True:
            return [0,0]
        leftPos=cellSegment[0]-1
        rightPos=cellSegment[1]-1
        l=cellSegment[0]-1
        r=cellSegment[1]-1
        firstTime=True
        while leftPos>0 or rightPos>0:
            d=0
            i=leftPos
            while d<1 and i>0 and leftPos>0:
                i=i-1
                if self[i]==_lb:
                    d=d+1
                if self[i]==_rb:
                    d=d-1
            e=0
            j=rightPos
            while e<1 and j>0 and rightPos>0:
                j=j-1
                if self[::-1][j]==_rb:
                    e=e+1
                if self[::-1][j]==_lb:
                    e=e-1
            if firstTime==True or (rootToken in contextTokens(self[i+d:leftPos])):
                l=i+d
                if r!=0:
                    r=j+e
            if firstTime==True or (rootToken in contextTokens(self[len(self)-rightPos:len(self)-(j+e)])):
                r=j+e
                if l!=0:
                    l=i+d
            leftPos=i 
            rightPos=j
            firstTime=False
        #print('Remark: The scope of the stated variable '+self[start:end]+' at position ['+str(start)+', '+str(end)+'] in the expression "'+self+'" is: "'+self[l:r]+'" at position ['+str(l)+', '+str(r)+'].')
        #print(str([l,r])+str(start)+','+str(end))
        return [l,r]
    def findPos(self, string='', n=1):
    # Returns the position of nth occurence of a string s in self
        if type(n)!=int:
            return -1
        elif n<0:
            return -1
        find = self.find(string)
        if find>-1:
            i=1
            while find != -1 and i != n:
                find = self.find(string, find + 1)
                i = i+1
        return find
       
    def substitute(self,inp=['',''],value='',positions=[],RHS=True):
    # Produces a valid substitution of the RHS (or LHS if RHS is False) of the equation formula in the statement, in the specified positions, based on self as the context     
        if positions==[]:
            k=value.count(inp[0])
            for i in range(0,k):
                positions.append(k)
        equation=E(inp[0],inp[1])
        if equation not in components(self):
            equation=E(inp[1],inp[0])
        if equation not in components(self):
            return exp("[Error]")
        if isFor(equation)==False:
            if isSta(equation)==True:
                equation=components(equation)[0]                
            else:
                equation=E(NN,NN)
        if isSta(value)==False:
            value=N(value)
        if isEq(equation)==False:
            return N(N)
        elif components(value)[0] not in components(self):
            return exp("[Error]")
        elif type(positions)!=list:
            return value
        pr(equation, value)
        positions=[p for p in positions if exp(value).findPos(inp[0], p)!=-1]
        resTokens=[]
        for p in positions:
            for v in reservedTokens(inp[0]):
                if v not in contextTokens(self) and v in exp(value).relativeContextTokens(exp(value).findPos(inp[0], p),exp(value).findPos(inp[0], p)+len(inp[0])):                  
                    continue
                resTokens=[v for v in exp(value).relativeContextTokens(exp(value).findPos(inp[0], p),exp(value).findPos(inp[0], p)+len(inp[0])) if v not in contextTokens(self)]
            value=exp(value[:exp(value).findPos(inp[0], p)]+rewriteExp(resTokens,inp[1],False)+value[exp(value).findPos(inp[0], p)+len(inp[0]):])
        return value
    def cellSegment(self,start=-1):
    # Returns the cell segment that starts at start
        if type(start)!=int:
            return [-1,-1]
        elif start==0:
            return [0,0]
        elif start<0 or start>len(self)-1:
            return [-1,-1]
        if self[start-1]==_lb:
            d=1
            j=start-1
            last=j
            while d>0 and j<len(self)-1:
                j=j+1
                old_d=d
                if self[j]==_lb:
                    d=d+1
                elif self[j]==_rb:
                    d=d-1
                if d==1 or (old_d==1 and d==2):
                    last=j
            return [start,len(self)-(last+1)]          
        else:
            return [-1,-1]
    def subComponentToken(self,i=-1):
        if type(i)!=int:
            return N
        elif i<-1 or i>len(self)-1:
            return N
        expression=self
        if expression[i]==_lb:
            d=1
            j=i
            token=''
            while d>0 and j<len(expression)-1:
                j=j+1
                old_d=d
                if expression[j]==_lb:
                    d=d+1
                elif expression[j]==_rb:
                    d=d-1
                if d==1 or (old_d==1 and d==2):
                    token=token+expression[j]
            return exp(token)
        elif i==-1:
            i=0
            d=0
            j=i
            token=''
            while j<len(expression):
                old_d=d
                if expression[j]==_lb:
                    d=d+1
                elif expression[j]==_rb:
                    d=d-1
                if d==0 or (old_d==0 and d==1):
                    token=token+expression[j]
                j=j+1
            return exp(token)            
        else:
            return N        
    def rootToken(self):
        i=0
        d=0
        j=i
        token=''
        while j<len(self):
            old_d=d
            if self[j]==_lb:
                d=d+1
            elif self[j]==_rb:
                d=d-1
            if d==0 or (old_d==0 and d==1):
                token=token+self[j]
            j=j+1
        return exp(token)    

    def doMatch(self,cell1,cell2):
        exp1=self.contents(self.cellSegments([cell1])[0])
        exp2=self.contents(self.cellSegments([cell2])[0])
        if semanticEquivalence(exp1,exp2)==False:
            return False
        cells=self.cells()
        for p in cells:
            for q in cells:
                if p[0]+1>cell1[0] and p[1]+1>cell1[1]:
                    if (q[0]==cell1[0] and q[1]==cell1[1]) or (q[0]<cell1[0] and q[1]>cell1[1])  or (q[0]>cell1[0] and q[1]<cell1[1]):
                        if self.contents(self.cellSegments([p])[0]).rootToken()==self.contents(self.cellSegments([q])[0]) and self.scope(self.cellSegments([p])[0])==self.scope(self.cellSegments([q])[0]):
                            cor_p=[p[0]-cell1[0]+cell2[0],p[1]-cell1[1]+cell2[1]]
                            if self.contents(self.cellSegments([p])[0]).rootToken()!=self.contents(self.cellSegments([cor_p])[0]).rootToken() or self.scope(self.cellSegments([p])[0])!=self.scope(self.cellSegments([cor_p])[0]):   
                                return False
                if p[0]+1>cell2[0] and p[1]+1>cell2[1]:
                    if (q[0]==cell2[0] and q[1]==cell2[1]) or (q[0]<cell2[0] and q[1]>cell2[1])  or (q[0]>cell2[0] and q[1]<cell2[1]):
                        if self.contents(self.cellSegments([p])[0]).rootToken()==self.contents(self.cellSegments([q])[0]) and self.scope(self.cellSegments([p])[0])==self.scope(self.cellSegments([q])[0]):
                            cor_p=[p[0]-cell2[0]+cell1[0],p[1]-cell2[1]+cell1[1]]
                            if self.contents(self.cellSegments([p])[0]).rootToken()!=self.contents(self.cellSegments([cor_p])[0]).rootToken() or self.scope(self.cellSegments([p])[0])!=self.scope(self.cellSegments([cor_p])[0]):   
                                return False

        return True
    def tree(self,caption,sibling=2,level=2,formulaColor='white',statementColor='white'):
    # Generates an expression tree, currently only in the tikzpicture format
    
        output='\\begin{tikzpicture}[baseline=(current bounding box.north), sibling distance='+str(sibling)+'cm, level distance='+str(level)+'cm, every node/.style = { shape=rectangle, draw=black, align=center, fill=white, font=\\ttfamily}] \\node '
        if isFor(self.subComponentToken(-1)):
            color=formulaColor
        else:
            color=statementColor
        output=output+'[fill='+color+']'+'{'+self.subComponentToken(-1)+'}'
        for i in range(0,len(self)):
            if self[i]==_lb:
                if isFor(self.subComponentToken(i)):
                    color=formulaColor
                else:
                    color=statementColor
                output=output+'child { node'+'[fill='+color+']'+ '{'+self.subComponentToken(i)+'}'
            if self[i]==_rb:
                output=output+'}'
        output=output+';\\end{tikzpicture}'
        return output

    def cell(self, show=''):
        if show=='compact':
            if isSta(self)==False:
                self=_state([self])
            output="\\smallskip $$\scalebox{0.8}{"
            text=''
            for i in range(0,len(self)):
                if self[i]==_lb:
                    #if i>0 and self[i-1]==_rb:
                    #    output=output+", 
                    if _im in self.subComponentToken(i):
                        output=output+'\\texttt{'+text+'}\\colorbox{gray!60}{\\minibox[frame]{'
                    elif len(self.subComponentToken(i))==0:
                            output=output+'\\texttt{'+text+'}{{'
                    elif isVar(self.subComponentToken(i)):
                        output=output+'\\texttt{'+text+'}\\colorbox{white}{{'
                    else: 
                        output=output+'\\texttt{'+text+'}\\colorbox{gray!30}{\\minibox[frame]{'
                    text=''
                elif self[i]==_rb:
                    output=output+'\\texttt{'+text+'}}}'
                    text=''
                    if i+1<len(self):
                        if self[i+1]==_lb:
                            output=output+'\\hspace{0.5mm}'
                elif self[i]==_im:
                    output=output+'\\texttt{'+text+'}\\vspace{2mm}\\\\'
                    text=''
                elif self[i]==_as:
                    output=output+'\\texttt{'+text+'}\\vspace{2mm}\\\\ \\textbf{Assuming:}'
                    text=''
                else:
                    text=text+self[i]
            output=output+'\\texttt{'+text+'}}$$\\smallskip'
            return output
        else:
            if isSta(self)==False:
                self=_state([self])
            output="\\smallskip\\setlength{\\ULdepth}{8pt} $$"
            text=''
            for i in range(0,len(self)):
                if self[i]==_lb:
                    #if i>0 and self[i-1]==_rb:
                    #    output=output+", 
                    if _im in self.subComponentToken(i):
                        output=output+'\\texttt{'+text+'}\\colorbox{gray!30}{\\minibox[frame]{'
                    elif len(self.subComponentToken(i))==0:
                            output=output+'\\texttt{'+text+'}{\\colorbox{white}{}{'
                    elif isVar(self.subComponentToken(i)):
                        output=output+'\\texttt{'+text+'}{\\colorbox{white}{'
                    else: 
                        output=output+'\\texttt{'+text+'}{\\minibox[frame]{'
                    text=''
                elif self[i]==_rb:
                    output=output+'\\texttt{'+text+'}}}'
                    text=''
                    if i+1<len(self):
                        if self[i+1]==_lb:
                            output=output+'\\hspace{1mm}'
                elif self[i]==_im:
                    if self[i+1]!=_im and self[i+1]!=_as and self[i-1]!=_lb and self[i-2:i]!=_lb+_im:
                        output=output+'\\texttt{'+text+'}\\vspace{2mm}\\\\'
                        text=''
                elif self[i]==_as:
                    if self[i+1]!=_im and self[i+1]!=_as:
                        if self[i-2:i]!=_lb+_im:
                            output=output+'\\texttt{'+text+'}\\vspace{2mm}\\\\ \\textbf{Assume: }'
                        else:
                            output=output+'\\texttt{'+text+'}\\textbf{Assume: }'
                else:
                    text=text+self[i]
            output=output+'$$'
            return output     
    def tokenTree(self, show=''):
    # Generates an expression tree using the `forest' package
        if show=='':  
            output="\\medskip\\scalebox{0.8}{\\begin{forest} baseline=(current bounding box.north) baseline, for tree={grow'=north, draw, rectangle, fill=white} ["
            output=output+'{\\text{'+self.subComponentToken(-1)+'}}'
            for i in range(0,len(self)):
                if self[i]==_lb:
                    output=output+'[{'+'\\text{'+self.subComponentToken(i)+'}}'
                if self[i]==_rb:
                    output=output+']'
            output=output+']\\end{forest}}'
            return output
        elif show=='cogs':
            output="\\medskip\\scalebox{0.9}{\\begin{forest} baseline=(current bounding box.north) baseline, for tree={grow'=north, draw, rectangle, fill=white} ["
            output=output+'{\\text{\\fbox{'+str(0)+'}\\,'+self.subComponentToken(-1)+'\\,\\fbox{'+str(len(self))+'}}}' 
            for i in range(0,len(self)):
                if self[i]==_lb:
                    output=output+'[{'+'\\text{\\fbox{'+str(i+1)+'}\\,'+self.subComponentToken(i)+'\\,\\fbox{'+str(self.cog(i+1)[1])+'}}}' 
                if self[i]==_rb:
                    output=output+']'
            output=output+']\\end{forest}}'
            return output            
        elif show=='ranks':
            output="\\medskip\\scalebox{0.9}{\\begin{forest} baseline=(current bounding box.north) baseline, for tree={grow'=north, draw, rectangle, fill=white} ["
            output=output+'{\\text{\\fbox{'+str(0)+'}\\,'+self.subComponentToken(-1)+'\\,\\fbox{'+str(0)+'}}}' 
            for i in range(0,len(self)):
                if self[i]==_lb:
                    output=output+'[{'+'\\text{\\fbox{'+str(self.cells([[i+1,self.cellSegment(i+1)[1]]])[0][0])+'}\\,'+self.subComponentToken(i)+'\\,\\fbox{'+str(self.cells([[i+1,self.cellSegment(i+1)[1]]])[0][1])+'}}}' 
                if self[i]==_rb:
                    output=output+']'
            output=output+']\\end{forest}}'
            return output           
    def cellTree(self):
        output="$$\\medskip\\scalebox{0.9}{\\begin{forest} baseline=(current bounding box.north) baseline, for tree={grow'=north, draw, rectangle, fill=white} ["
        output=output+'{\\text{\\fbox{'+str(0)+'}\\,\\fbox{'+str(0)+'}}}' 
        for i in range(0,len(self)):
            if self[i]==_lb:
                output=output+'[{'+'\\text{\\fbox{'+str(self.cells([[i+1,self.cellSegment(i+1)[1]]])[0][0])+'}\\,\\fbox{'+str(self.cells([[i+1,self.cellSegment(i+1)[1]]])[0][1])+'}}}' 
            if self[i]==_rb:
                output=output+']'
        output=output+']\\end{forest}}$$'
        return output            
    
    def scopeTree(self,variable='x'):
    # Generates an expression tree using the `forest' package, coloring in the nodes for the n-th occurence of the variable and its scope
        output="\\medskip\\scalebox{0.9}{\\medskip\\begin{forest} baseline=(current bounding box.north) baseline, for tree={grow'=north, draw, rectangle, fill=white} ["
        n=1
        starts=[]
        scopes=[]
        scopeStarts=[]
        while self.findPos(_state([variable]),n)>-1:
            starts.append(self.findPos(_state([variable]),n))
            scopes.append(self.scope([starts[n-1]+1,len(self)-(starts[n-1]+1+len(variable))]))
            scopeStarts.append(scopes[n-1][0])
            n=n+1
        if [0,0] in scopes:
            output=output+'{\\textbf{'+self.subComponentToken(-1)+'}}, fill=black!20' 
        else:
            output=output+'{\\text{'+self.subComponentToken(-1)+'}}'
        for i in range(0,len(self)):
            if self[i]==_lb:
                if i in starts or (i+1 in scopeStarts and i+1!=0):
                    output=output+'[{'+'\\textbf{'+self.subComponentToken(i)+'}}, fill=black!20'                   
                else:
                    output=output+'[{'+'\\text{'+self.subComponentToken(i)+'}}'
            if self[i]==_rb:
                output=output+']'
        output=output+']\\end{forest}}'
        return output
    
    def matchTree(self,cell=[0,0]):
    # Generates an expression tree using the `forest' package, coloring in the nodes for the n-th occurence of the variable and its scope
        output="\\medskip\\scalebox{0.9}{\\medskip\\begin{forest} baseline=(current bounding box.north) baseline, for tree={grow'=north, draw, rectangle, fill=white} ["
        matchingSegments=[]
        matchingSegmentLeftIndicies=[]
        cellSegment=self.cellSegments([cell])[0]
        for matchingCell in self.cells():
            if self.doMatch(cell,matchingCell):
                matchingSegments.append(self.cellSegments([matchingCell])[0])
                matchingSegmentLeftIndicies.append(self.cellSegments([matchingCell])[0][0])
        if [0,0] in matchingSegments or [0,0]==cellSegment:
            output=output+'{\\textbf{'+self.subComponentToken(-1)+'}}, fill=black!20' 
        else:
            output=output+'{\\text{'+self.subComponentToken(-1)+'}}'
        for i in range(0,len(self)):
            if self[i]==_lb:
                if i+1 in matchingSegmentLeftIndicies:
                    output=output+'[{'+'\\textbf{'+self.subComponentToken(i)+'}}, fill=black!20'                   
                else:
                    output=output+'[{'+'\\text{'+self.subComponentToken(i)+'}}'
            if self[i]==_rb:
                output=output+']'
        output=output+']\\end{forest}}'
        return output
    
    def plotCells(self):
        cells=self.cells()
        n=len(cells)
        
        tikz_code = "\\begin{tikzpicture}[scale=0.3]"

        # Rotate the grid by 90 degrees
        tikz_code += "\\begin{scope}[rotate=45]\n"
        
        # Draw the grid with the specified step size
        tikz_code += "\\draw[gray] (0,0) grid ("+str(n)+","+str(n)+");"
        
        # Plot the dots
        for x, y in cells:
            tikz_code += "\\draw[thick, fill=gray, fill opacity=0.4] ("+str(n)+","+str(n)+") rectangle ("+str(x)+","+str(y)+");"
        
        for x, y in cells:    
            tikz_code += "\\draw[fill=white] ("+str(x)+","+str(y)+") circle (5pt);"
        tikz_code += "\\draw[fill=white] (0,0) circle (5pt);"
            
        for cellA in cells:
            save=[0,0]
            for cellB in cells:
                if cellA[0]+1>cellB[0] and cellA[1]+1>cellB[1]:
                    if cellB[0]+1>save[0] and cellB[1]+1>save[1]:
                        save=cellB
            tikz_code += "\\draw[thick] ("+str(cellA[0])+","+str(cellA[1])+") -- ("+str(save[0])+","+str(save[1])+");"
        
        # End the rotated scope
        tikz_code += "\\end{scope}"
        
        tikz_code += "\\end{tikzpicture}"
        return tikz_code   
    
    def decompound(expr):
        if len(expr)==0:
            return expr
        if isSta(expr) and len(components(expr))>1:
            return exp(", ".join(_state([c]) for c in components(expr)))
        elif isSta(expr) and len(components(expr))==1:
            return expr
        compDec=decomposeFor(expr)
        reduction=""
        naturalSeparators=[" ",":", ";", ".", ",", "!", "?"]
        if compDec[2]:
            for i in range(0,len(compDec[0])-1):
                if compDec[0][i][-1] in naturalSeparators and compDec[0][i+1][0] in naturalSeparators:
                    reduction=reduction+compDec[0][i]+formulateList(compDec[1][i])
                else:
                    reduction=reduction+compDec[0][i]+formulateTuple(compDec[1][i])
            reduction=reduction+compDec[0][len(compDec[0])-1]          
            if len(compDec[1])==len(compDec[0]):
                if compDec[0][len(compDec[0])-1][-1] in naturalSeparators:
                    reduction=reduction+formulateList(compDec[1][len(compDec[0])-1])
                else:
                    reduction=reduction+formulateTuple(compDec[1][len(compDec[0])-1])                        
        else:
            if len(compDec[0])>0:
                if compDec[0][0][0] in naturalSeparators:
                    reduction=formulateTupleList(compDec[1][0])
                else:
                    reduction=formulateTuple(compDec[1][0])
            else:
                reduction=formulateTuple(compDec[1][0])  
            for i in range(1,len(compDec[1])-1):
                if compDec[0][i-1][-1] in naturalSeparators and compDec[0][i][0] in naturalSeparators:
                    reduction=reduction+compDec[0][i-1]+formulateTupleList(compDec[1][i])
                else:
                    reduction=reduction+compDec[0][i-1]+formulateTuple(compDec[1][i])
            if len(compDec[1])==len(compDec[0]) and len(compDec[1])>1:
                if compDec[0][len(compDec[1])-2][-1] in naturalSeparators and compDec[0][len(compDec[1])-1][0] in naturalSeparators:
                    reduction=reduction+compDec[0][len(compDec[1])-2]+formulateTupleList(compDec[1][len(compDec[1])-1])
                else:
                    reduction=reduction+compDec[0][len(compDec[1])-2]+formulateTuple(compDec[1][len(compDec[1])-1])
                reduction=reduction+compDec[0][len(compDec[0])-1]
            elif len(compDec[1])==len(compDec[0]) and len(compDec[1])==1:
                if compDec[0][0][0] in naturalSeparators:
                    reduction=reduction+compDec[0][0]
                else:
                    reduction=reduction+compDec[0][0]
            elif len(compDec[1])>len(compDec[0]) and len(compDec[1])>1:
                if compDec[0][len(compDec[1])-2][-1] in naturalSeparators:
                    reduction=reduction+compDec[0][len(compDec[1])-2]+formulateTupleList(compDec[1][len(compDec[1])-1])
                else:
                    reduction=reduction+compDec[0][len(compDec[1])-2]+formulateTuple(compDec[1][len(compDec[1])-1])            
        return exp(reduction)
    
    def reservedVars(self):
        print('Remark: Reserved variables of "'+self+'" are: "'+'", "'.join(str(c) for c in reservedVars(self))+'".')
        return reservedVars(self)
    def natural(self, logic="", instruction=""):
        if instruction=="original":
            return self
        if instruction=="cell":
            return self.cell()
        expr=self
        newexpr=expr
        refreshed=True
        while refreshed==True:
            refreshed=False
            for cell in newexpr.cells():
                if refreshed==True:
                    break
                if cell==(0,0):
                    continue
                seg=newexpr.cellSegments([cell])[0]
                #print(expr)
                #print(seg)
                component=newexpr.contents(seg)
                if isToken(component) and _lb in component:
                    component=exp(component.replace(NN,"*"))
                    newexpr=exp(newexpr[:seg[0]]+component+newexpr[len(newexpr)-seg[1]:])
                    refreshed=True
                    break
        refreshed=True
        while refreshed==True:
            refreshed=False
            for cell in newexpr.cells():
                if refreshed==True:
                    break
                seg=newexpr.cellSegments([cell])[0]
                #print(expr)
                #print(seg)
                component=newexpr.contents(seg)                   
                if isInf(component):
                    dec=decomposeFor(component)
                    if logic!="propositional":
                        varl=[]
                        stal=[]
                        for comp in components(dec[1][0]):
                            if isToken(comp): 
                                if comp not in varl:
                                    varl.append(comp)
                            else:
                                stal.append(comp)
                        varr=[]
                        star=[]
                        for comp in components(dec[1][1]):
                            if isToken(comp): 
                                if comp not in varr:
                                    varr.append(comp)
                            else:
                                star.append(comp)
                        if len(varl)>0:
                            if len(stal)>0:
                                if len(varr)+len(star)>1:
                                    component="for "+_state(varl)+", given "+_state(stal)+", conclusions "+_state(varr+star)+" hold"
                                else:
                                    component="for "+_state(varl)+", given "+_state(stal)+", conclusion "+_state(varr+star)+" holds"                            
                            else:
                                if len(varr)+len(star)>1:
                                    component="for "+_state(varl)+", "+_state(varr+star)+" hold"
                                else:
                                    component="for "+_state(varl)+", "+_state(varr+star)+" holds"                                                            
                        else:
                            if len(stal)>0:
                                if len(varr)+len(star)>1:
                                    component="( "+_state(stal)+" => "+_state(varr+star)+" )"
                                else:
                                    component="( "+_state(stal)+" => "+_state(varr+star)+" )"                                                        
                            else:
                                if len(varr)+len(star)>1:
                                    component=_state(varr+star)+" hold"
                                else:
                                    component=_state(varr+star)+" holds"                                                                                        
                        newexpr=exp(newexpr[:seg[0]]+component+newexpr[len(newexpr)-seg[1]:])
                        refreshed=True
                        break
                    else:
                        dec=decomposeFor(component)
                        newexpr=exp(newexpr[:seg[0]]+"( "+dec[1][0]+" => "+dec[1][1]+" )"+newexpr[len(newexpr)-seg[1]:])
        refreshed=True
        while refreshed==True:
            refreshed=False
            for cell in newexpr.cells():
                if refreshed==True:
                    break
                if cell==(0,0):
                    continue
                seg=newexpr.cellSegments([cell])[0]
                #print(expr)
                #print(seg)
                component=newexpr.contents(seg)
                if isSta(component):
                    com=components(component)
                    component="("+",".join(com)+")"
                    newexpr=exp(newexpr[:seg[0]]+component+newexpr[len(newexpr)-seg[1]:])
                    refreshed=True
                    break
        expr=newexpr                            
        for cell in expr.cells():
            seg=newexpr.cellSegments([cell])[0]
            component=newexpr.contents(seg)
            component=exp(component)
            reduction=component.decompound()
            newexpr=exp(newexpr[:seg[0]]+reduction+newexpr[len(newexpr)-seg[1]:])             
        newexpr=newexpr.replace(_lb+_rb,"*")
        newexpr=newexpr.replace(_lb,"")
        newexpr=newexpr.replace(_rb,"")
        return str(newexpr)                         
                                         ##############################
N=exp('')                                # ADA Tokens               #
NN=exp('')('')                        #                            #
E=exp(NN+_eq+NN)              #                            #
I=exp(NN+_im+NN)              #                            #
                                        ##############################

class argument():
    def __init__(self,cont=[],**pars):
        global _Exp
        global _expNo
        self._stat=exp(_na+_lb+_rb)
        self._logic="unrestricted" # options: propositional, predicate, unrestricted
        self._lines=[]
        self._conclusion=NN
        self._pos=2
        self._theme="basic" #"narrative", "theory", "basic", "fitch", "language"
        self._dialect="original" #"cell", "natural"
        self._fitch=''
        self._natural=''
        self._prefix=''
        self._name=''
        self._maxDigits=3
        self._lineLabel='L:'
        self._space=' '
        self._startArgument='(new argument started)'
        self._endArgument='(argument complete)'
        self._given='If ('
        self._weGet=') then: '
        self._newLine="\n"
        self._endProof='This argument proves the following.'+self._newLine
        self._assumptionPhrases=[' Assume: ',' Suppose we have: ', ' Let us assume: ', ' Let us suppose: ', ' We assume: ', ' We suppose: ']
        self._conclusionPhrases=[' Therefore, ',' So, ',' Then: ', ' We thus obtain: ',' This gives us: ', ' We then get the following: ',' Hence: ']
        self._substitutionPhrases=[' By substitution, ',' So, by substitution, ',' Substitution gives: ', ' By substitution, we thus obtain: ',' Substitution gives: ', ' By substitution, we then get the following: ',' Hence, by substitution: ']
        self._argumentPhrases=['Consider the following argument.','We argue as follows.','Let us argue as follows.', 'Let us consider the following argument.','Here is an argument.', 'Let us look into the following.','Let us indulge in the following.']
        self._closeArgumentPhrases=['Let us now step out from the argument.','Stepping out from the argument.','We step out from the argument.', 'We now return to the encompassing argument.']
        self._endProofPhrases=['This completes the proof.','The proof is now complete.','The proof is complete.', 'This ends the proof.']
        self._context=[]
        self._proved=N(N)
        self._lineNo=0
        self._lineNoPrefix=""
        self._parentlineNoPrefix=-1
        self._parentPos=-1
        self._parentPrinting="basic"
        self._label=""
        if "name" in pars:
            self._name=pars["name"]
        if "theme" in pars:
            if pars["theme"] in ["narrative","fitch","theory","basic","language"]:
                self._theme=pars["theme"]
        if isinstance(cont,argument):
            if "name" in pars:
                self._name=cont._name+" - "+pars["name"]
            self._theme=cont._theme
            self._dialect=cont._dialect
            self._context=cont._context+cont._stat.relativeComponents(cont._pos,cont._pos)
            if cont._theme=="fitch":
                self._prefix=cont._prefix+_il
            else:
                self._prefix=_par["space"]
            self._parentLineNoPrefix=cont._lineNoPrefix
            self._parentPos=cont._pos
            self._parentPrinting=cont._theme
            self._lineNoPrefix=cont._lineNoPrefix+str(cont._lineNo)+"."
            _Exp[cont._lineNoPrefix+str(cont._lineNo)]=self
            if _notebook[len(_notebook)-1:]=="\n":
                fitchNewLine=self._space+self._prefix+_al+self._space+"Argument"+self._no(self._name)+_par["period"]
                naturalNewLine=_newParagraph()+"Argument"+self._no(self._name,True)+_par["period"]
                theoryNewLine=_newParagraph()+"Theory"+self._no(self._name)+_par["period"]
                basicNewLine=_newParagraph()+"Deductive Argument"+self._no(self._name)
            else:
                if cont._theme=="fitch":
                    fitchNewLine=_newLine()+self._space+self._prefix+_al+self._space+"Argument"+self._no(self._name)+_par["period"]
                else:
                    fitchNewLine=_newParagraph()+self._space+self._prefix+_al+self._space+"Argument"+self._no(self._name)+_par["period"]                    
                naturalNewLine=_newParagraph()+"Argument"+self._no(self._name, True)+_par["period"]
                theoryNewLine=_newParagraph()+"Theory"+self._no(self._name)+_par["period"]           
                basicNewLine=_newParagraph()+"Deductive Argument"+self._no(self._name)+_par["period"]
            cont._lineNo=cont._lineNo+1
            cont._lines.append("")
            self._logic=cont._logic
        else:
            self._lineNoPrefix=str(_expNo)+"."
            if _notebook[len(_notebook)-1:]=="\n":
                fitchNewLine=self._space+self._prefix+_al+self._space+"Argument"+self._no(self._name)+_par["period"]
                naturalNewLine="Argument"+self._no(self._name)+_par["period"]
                theoryNewLine="Theory"+self._no(self._name)+_par["period"]        
                basicNewLine="Deductive Argument"+self._no(self._name)+_par["period"]
            else:
                fitchNewLine=_newParagraph()+self._space+self._prefix+_al+self._space+"Argument"+self._no(self._name)+_par["period"]
                naturalNewLine=_newParagraph()+"Argument"+self._no(self._name)+_par["period"]
                theoryNewLine=_newParagraph()+"Theory"+self._no(self._name)+_par["period"]  
                basicNewLine=_newParagraph()+"Deductive Argument"+self._no(self._name)+_par["period"]
                _Exp[self._lineNoPrefix+str(self._lineNo)]=self
            _expNo=_expNo+1
        if "dialect" in pars:
            self._dialect=pars["dialect"]
        if "theme" in pars:
            self._theme=pars["theme"]
        if "logic" in pars:
            self._logic=pars["logic"]
        elif self._logic=="":
            self._logic="predicate"
        self._addLine(fitchNewLine,naturalNewLine,theoryNewLine,basicNewLine)
        self._lines.append(NN)

    def _no(self,name="",brackets=False):
        if name!="":
            name=": "+name
            if name[len(name)-1]==".":
                name=name[:len(name)-1]
        number=self._lineNoPrefix+str(self._lineNo)+name
        if brackets:
            number="("+number+")"
        return self._space+number
    def __call__(self,inp=-1):
        if type(inp)==int:
            if inp>0 and inp<len(self._lines):
                return self._lines[inp]
            else:
                return self._stat
        elif type(inp)==str:
            self._label=inp
        elif type(inp)==argument:
            cont=inp._context+inp._stat.relativeComponents(inp._pos,inp._pos)
            for c in cont:
                if c not in self._context:
                    self._context.append(c)
    def _assumptionPhrase(self):
        return self._assumptionPhrases[random.randint(0, len(self._assumptionPhrases) - 1)]
    def _conclusionPhrase(self):
        return self._conclusionPhrases[random.randint(0, len(self._conclusionPhrases) - 1)]
    def _substitutionPhrase(self):
        return self._substitutionPhrases[random.randint(0, len(self._substitutionPhrases) - 1)]
    def _argumentPhrase(self):
        return self._argumentPhrases[random.randint(0, len(self._argumentPhrases) - 1)]
    def _closeArgumentPhrase(self):
        return self._closeArgumentPhrases[random.randint(0, len(self._closeArgumentPhrases) - 1)]
    def _endProofPhrase(self):
        return self._endProofPhrases[random.randint(0, len(self._endProofPhrases) - 1)]
    def _addLine(self, fitchLine="", naturalLine="", theoryLine="",basicLine="",languageLine=""):
        global _notebook
        if self._theme=="fitch":
            _notebook=_notebook+fitchLine
            print(fitchLine, end="", flush=True)
        elif self._theme=="narrative":
            _notebook=_notebook+naturalLine
            print(naturalLine, end="", flush=True)
        elif self._theme=="theory":
            _notebook=_notebook+theoryLine
            print(theoryLine, end="", flush=True)
        elif self._theme=="basic":
            _notebook=_notebook+basicLine
            print(basicLine, end="", flush=True)
        elif self._theme=="language":
            _notebook=_notebook+languageLine
            print(languageLine, end="", flush=True)
        self._lineNo=self._lineNo+1
    def proof(self,theme="fitch"):
        # Stopped here
        global _notebook
        pos=0
        readingLine=False
        line=""
        depth=0
        lineStartDepth=0
        argumentDepth=0
        lineType=''
        for pos in range(0,len(self._stat)):
            if self._stat[pos:pos+1]==_lb:
                if readingLine:
                    line=line+self._stat[pos:pos+1]
                depth=depth+1
            elif self._stat[pos:pos+1]==_im:
                if readingLine and lineStartDepth==depth:
                    if line!="":
                        lineNatural=exp(line).natural(self._logic,self._dialect)
                        fitchPrefix=self._space
                        for k in range(0,depth-1):
                            fitchPrefix=fitchPrefix+_il
                        if lineType=='conclusion':
                            fitchNewLine=fitchPrefix+_il+self._space+lineNatural+_newLine()
                            naturalNewLine=self._conclusionPhrase()+lineNatural+_par["period"]
                        elif lineType=='assumption':
                            fitchNewLine=fitchPrefix+_ma+self._space+lineNatural+_newLine()
                            naturalNewLine=self._assumptionPhrase()+lineNatural+_par["period"]
                        if theme=="fitch":
                            _notebook=_notebook+fitchNewLine
                            print(fitchNewLine, end="")
                        elif theme=="narrative":
                            _notebook=_notebook+naturalNewLine
                            print(naturalNewLine, end="")
                    line=""
                    lineType='conclusion'
                    lineStartDepth=depth
                elif readingLine and lineStartDepth<depth:
                    line=line+self._stat[pos:pos+1]
                else:
                    readingLine=True
                    lineType='conclusion'
                    lineStartDepth=depth                    
            elif self._stat[pos:pos+1]==_as:
                if readingLine and lineStartDepth==depth:
                    if line!="":
                        lineNatural=exp(line).natural(self._logic,self._dialect)
                        fitchPrefix=self._space
                        for k in range(0,depth-1):
                            fitchPrefix=fitchPrefix+_il
                        if lineType=='conclusion':
                            fitchNewLine=fitchPrefix+_il+self._space+lineNatural+_newLine()
                            naturalNewLine=self._conclusionPhrase()+lineNatural+_par["period"]
                        elif lineType=='assumption':
                            fitchNewLine=fitchPrefix+_ma+self._space+lineNatural+_newLine()
                            naturalNewLine=self._assumptionPhrase()+lineNatural+_par["period"]
                        if theme=="fitch":
                            _notebook=_notebook+fitchNewLine
                            print(fitchNewLine, end="")
                        elif theme=="narrative":
                            _notebook=_notebook+naturalNewLine
                            print(naturalNewLine, end="")
                    line=""
                    lineType='assumption'
                    lineStartDepth=depth
                elif readingLine and lineStartDepth<depth:
                    line=line+self._stat[pos:pos+1]
                else:
                    readingLine=True
                    lineType='assumption'
                    lineStartDepth=depth   
            elif self._stat[pos:pos+1]==_na:
                if readingLine and lineStartDepth==depth:
                    readingLine=False
                    if line!="":
                        lineNatural=exp(line).natural(self._logic,self._dialect)
                        fitchPrefix=self._space
                        for k in range(0,depth-1):
                            fitchPrefix=fitchPrefix+_il
                        if lineType=='conclusion':
                            fitchNewLine=fitchPrefix+_il+self._space+lineNatural+_newLine()
                            naturalNewLine=self._conclusionPhrase()+lineNatural+_par["period"]
                        elif lineType=='assumption':
                            fitchNewLine=fitchPrefix+_ma+self._space+lineNatural+_newLine()
                            naturalNewLine=self._assumptionPhrase()+lineNatural+_par["period"]
                        if theme=="fitch":
                            _notebook=_notebook+fitchNewLine
                            print(fitchNewLine, end="")
                        elif theme=="narrative":
                            _notebook=_notebook+naturalNewLine
                            print(naturalNewLine, end="")
                    line=""
                    readingLine=False
                    argumentDepth=argumentDepth+1
                    fitchPrefix=self._space
                    for k in range(0,depth):
                        fitchPrefix=fitchPrefix+_il
                    fitchNewLine=""
                    naturalNewLine=_newParagraph()+self._argumentPhrase()
                    if theme=="fitch":
                        _notebook=_notebook+fitchNewLine
                        print(fitchNewLine, end="")
                    elif theme=="narrative":
                        _notebook=_notebook+naturalNewLine
                        print(naturalNewLine, end="")

                elif readingLine and lineStartDepth<depth:
                    line=line+self._stat[pos:pos+1]
                else:
                    argumentDepth=argumentDepth+1
                    fitchPrefix=self._space
                    for k in range(0,depth-1):
                        fitchPrefix=fitchPrefix+_il
                    if argumentDepth==1:
                        fitchNewLine=_newLine()+"Proof."+_newLine()
                        naturalNewLine=_newParagraph()+"Proof."
                    else:
                        fitchNewLine=""
                        naturalNewLine=_newParagraph()+self._argumentPhrase()
                    if theme=="fitch":
                        _notebook=_notebook+fitchNewLine
                        print(fitchNewLine, end="")
                    elif theme=="narrative":
                        _notebook=_notebook+naturalNewLine
                        print(naturalNewLine, end="")
            elif self._stat[pos:pos+1]==_rb:
                if readingLine and lineStartDepth<depth:
                    line=line+self._stat[pos:pos+1]
                else:
                    readingLine=False
                    if line!="":
                        lineNatural=exp(line).natural(self._logic,self._dialect)
                        fitchPrefix=self._space
                        for k in range(0,depth-1):
                            fitchPrefix=fitchPrefix+_il
                        if lineType=='conclusion':
                            fitchNewLine=fitchPrefix+_il+self._space+lineNatural+_newLine()
                            naturalNewLine=self._conclusionPhrase()+lineNatural+_par["period"]
                        elif lineType=='assumption':
                            fitchNewLine=fitchPrefix+_ma+self._space+lineNatural+_newLine()
                            naturalNewLine=self._assumptionPhrase()+lineNatural+_par["period"]
                        if theme=="fitch":
                            _notebook=_notebook+fitchNewLine
                            print(fitchNewLine, end="")
                        elif theme=="narrative":
                            _notebook=_notebook+naturalNewLine
                            print(naturalNewLine, end="")
                    line=""
                    if argumentDepth==depth:
                        argumentDepth=argumentDepth-1
                        fitchPrefix=self._space
                        for k in range(0,depth-1):
                            fitchPrefix=fitchPrefix+_il
                        if argumentDepth==0:
                            fitchNewLine=fitchPrefix+_cl+self._space+"QED"
                            naturalNewLine=_newParagraph()+self._endProofPhrase()
                        else:
                            fitchNewLine=""
                            naturalNewLine=_newParagraph()+self._closeArgumentPhrase()
                        if theme=="fitch":
                            _notebook=_notebook+fitchNewLine
                            print(fitchNewLine, end="")
                        elif theme=="narrative":
                            _notebook=_notebook+naturalNewLine
                            print(naturalNewLine, end="")
                        
                depth=depth-1
            else:
                if readingLine and lineStartDepth<depth:
                    line=line+self._stat[pos:pos+1]
    def conclude(self,input1="",*input2,**input3):
        if input1=="":
            return self.end()
        if isinstance(input1,argument):
            ret = self._use(input1,**input3)
            return ret
        if isinstance(input1,list):
            ret = self.restate(*[i for i in input1],**input3)
            return ret 
        if isSta(input1):
            c=components(input1)
            if len(c)==1:
                input1=c[0]   
        if isEq(input1):
            if len(input2)==0:
                R = self.synEquality(input1)
                if R!=None:
                    return R
            else:
                c=components(input1)
                ret = self.sub([c[0],c[1]],input2[0],*[i for i in input2 if type(i)==int],**input3)
                return ret
        if isInf(input1):
            ret = self._apply(input1,*input2,**input3)
            return ret
    def synEquality(self,equality):
        cont=self._context+self._stat.relativeComponents(self._pos,self._pos)
        contTokens=contextTokens(_state(cont))
        comp=components(equality)
        if semanticEquivalence(comp[0],comp[1],contTokens):
            equality=N(equality)
            equalityNatural=equality.natural(self._logic,self._dialect)
            self._lines.append(equality)
            self._stat=exp(self._stat[:self._pos]+_im+equality+self._stat[self._pos:])
            self._pos=self._pos+len(equality)+len(_im)
            fitchNewLine=_newLine()+self._space+self._prefix+_il+self._space+equalityNatural+self._no()
            naturalNewLine=self._conclusionPhrase()+equalityNatural+self._no("",True)+_par["period"]
            theoryNewLine=_newParagraph()+"Theorem"+self._no()+_par["period"]+self._label+_newLine()+_par["space"]+equalityNatural+_par["period"]
            basicNewLine=_newParagraph()+"Conclusion"+self._no()+_par["period"]+self._label+_newLine()+_par["space"]+equalityNatural+_par["period"]
            _Exp[self._lineNoPrefix+str(self._lineNo)]=equality
            self._addLine(fitchNewLine,naturalNewLine,theoryNewLine,basicNewLine)           
            return equality                        
    def restate(self,*inputs,**pars):
        name=""
        if "name" in pars:
            name=pars["name"]  
        cont=self._context+self._stat.relativeComponents(self._pos,self._pos)
        conTokens=[]
        revisedInputs=[]
        for c in cont:
            if isToken(c):
                conTokens.append(c)
        inputs=[i for i in components(N(inputs)) if isToken(i)==False]
        for inp in inputs:
            #if isToken(inp) and inp in conTokens:
            #    revisedInputs.append(inp)
            #else:
            for c in cont:
                if semanticEquivalence(c,inp,conTokens):
                    revisedInputs.append(inp)
                    break
        restatement=_state(revisedInputs)
        restatementNatural=restatement.natural(self._logic,self._dialect)
        self._lines.append(restatement)
        self._stat=exp(self._stat[:self._pos]+_im+restatement+self._stat[self._pos:])
        self._pos=self._pos+len(restatement)+len(_im)
        fitchNewLine=_newLine()+self._space+self._prefix+_il+self._space+restatementNatural+self._no(name)
        naturalNewLine=self._conclusionPhrase()+restatementNatural+self._no(name,True)+_par["period"]
        theoryNewLine=_newParagraph()+"Theorem"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+restatementNatural+_par["period"]
        basicNewLine=_newParagraph()+"Conclusion"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+restatementNatural+_par["period"]
        _Exp[self._lineNoPrefix+str(self._lineNo)]=restatement
        self._addLine(fitchNewLine,naturalNewLine,theoryNewLine,basicNewLine)           
        return restatement        
    def assume(self,*assumptions,**pars):
        name=""
        if "name" in pars:
            name=pars["name"]                         
        assumption="".join([N(a) for a in assumptions])
        if self._pos==len(self._stat):
            return False
        if self._logic=="propositional":
            cont=reservedTokens(assumption)
            for c in cont:
                if c not in self._context:
                    self._context.append(c)
        assumption=_state(self._context+self._stat.relativeComponents(self._pos,self._pos)).assume(assumption)
        if self._logic!="propositional":
            assumption=_renameNonContTokens(self._context+self._stat.relativeLeftComponents(self._pos,self._pos),assumption)
        assumptionNatural=assumption.natural(self._logic,self._dialect)
        self._lines.append(assumption)
        self._stat=exp(self._stat[:self._pos]+_as+assumption+self._stat[self._pos:])
        self._pos=self._pos+len(assumption)+len(_as)
        fitchNewLine=_newLine()+self._space+self._prefix+_ma+self._space+assumptionNatural+self._no(name)
        naturalNewLine=self._assumptionPhrase()+assumptionNatural+self._no(name,True)+_par["period"]
        basicNewLine=_newParagraph()+"Assumption"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+assumptionNatural+_par["period"]
        languageNewLine=_newParagraph()+"Formulator"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+assumptionNatural+_par["period"]
        comp=components(assumption)
        notation=False
        axiom=False
        for c in comp:
            if isToken(c):
                notation=True
            else:
                axiom=True
        if notation and axiom:
            theoryNewLine=_newParagraph()+"Formulator and Axiom"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+assumptionNatural+_par["period"]            
        elif notation:
            theoryNewLine=_newParagraph()+"Formulator"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+assumptionNatural+_par["period"]
        elif axiom:
            theoryNewLine=_newParagraph()+"Axiom"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+assumptionNatural+_par["period"]
        _Exp[self._lineNoPrefix+str(self._lineNo)]=assumption
        self._addLine(fitchNewLine,naturalNewLine,theoryNewLine,basicNewLine,languageNewLine)
        if isSta(assumption) and len(comp)==1:
            if isToken(comp[0]):
                return comp[0]
        return assumption
    def _use(self,arg='',**pars):
        if self._theme=="language":
            return N(N)
        name=""
        if "name" in pars:
            name=pars["name"]       
        global _notebook
        if type(arg)!=argument:
            return False
        if arg._parentLineNoPrefix!=self._lineNoPrefix:
            return False
        #for c in arg._context:
        #    if c not in self._context+self._stat.relativeComponents(self._pos,self._pos):
        #        return False
        conclusion=arg._conclusion
        if self._logic!="propositional":              
            conclusion=rewriteExp([var for var in reservedVars(self._stat) if var not in contextVars(self._stat.relativeLeftComponents(arg._parentPos,arg._parentPos))],conclusion)
            conclusion=rewriteExp([var for var in contextVars(_state(self._stat.relativeLeftComponents(self._pos,self._pos))) if var not in contextVars(_state(self._stat.relativeLeftComponents(arg._parentPos,arg._parentPos)))],conclusion,False)
            conclusion=_renameNonContTokens(self._context+self._stat.relativeComponents(self._pos,self._pos),conclusion)
        else:
            for c in arg._context:
                if c not in self._context:
                    self._context.append(c)
        self._lines.append(conclusion)
        argForm=components(_renameNonContTokens(self._context+self._stat.relativeComponents(self._pos,self._pos),arg._stat))[0]
        self._stat=exp(self._stat[:arg._parentPos]+argForm+self._stat[arg._parentPos:self._pos]+_im+conclusion+self._stat[self._pos:])
        self._pos=self._pos+len(conclusion)+len(_im)+len(argForm)
        conclusionNatural=conclusion.natural(self._logic,self._dialect)
        fitchNewLine=_newLine()+self._space+self._prefix+_il+self._space+conclusionNatural+self._no(name)
        if _notebook[len(_notebook)-1:]=="\n":
            theoryNewLine="Theorem"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+conclusionNatural+_par["period"]
            basicNewLine="Conclusion"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+conclusionNatural+_par["period"]
            naturalNewLine=self._conclusionPhrase()[1:]+conclusionNatural+self._no(name,True)+_par["period"]
        else:    
            theoryNewLine=_newParagraph()+"Theorem"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+conclusionNatural+_par["period"]
            basicNewLine=_newParagraph()+"Conclusion"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+conclusionNatural+_par["period"]
            naturalNewLine=self._conclusionPhrase()+conclusionNatural+self._no(name,True)+_par["period"]
        _Exp[self._lineNoPrefix+str(self._lineNo)]=conclusion  
        self._addLine(fitchNewLine,naturalNewLine,theoryNewLine,basicNewLine)
        return conclusion 
    def _apply(self,deduction='',*inputs,**pars):
        if self._theme=="language":
            return N(N)
        name=""
        if "name" in pars:
            name=pars["name"]  
        if self._pos==len(self._stat):
            return False
        application=_state(self._context+self._stat.relativeComponents(self._pos,self._pos)).apply(deduction,*inputs, logic=self._logic)
        #if self._logic!="propositional":
            #application=_renameNonContTokens(self._context+self._stat.relativeComponents(self._pos,self._pos),application)        
        applicationNatural=application.natural(self._logic,self._dialect)
        self._lines.append(application)
        self._stat=exp(self._stat[:self._pos]+_im+application+self._stat[self._pos:])
        self._pos=self._pos+len(application)+len(_as)
        fitchNewLine=_newLine()+self._space+self._prefix+_il+self._space+applicationNatural+self._no(name)
        naturalNewLine=self._conclusionPhrase()+applicationNatural+self._no(name,True)+_par["period"]
        theoryNewLine=_newParagraph()+"Theorem"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+applicationNatural+_par["period"]
        basicNewLine=_newParagraph()+"Conclusion"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+applicationNatural+_par["period"]
        _Exp[self._lineNoPrefix+str(self._lineNo)]=application
        self._addLine(fitchNewLine,naturalNewLine,theoryNewLine,basicNewLine)           
        return application
    def sub(self,inp,where,*places,**pars):
        if self._theme=="language":
            return N(N)
        name=""
        if "name" in pars:
            name=pars["name"]  
        if self._pos==len(self._stat):
            return False
        substitution=_state(self._context+self._stat.relativeComponents(self._pos,self._pos)).substitute(inp,where,[x for x in places])
        if self._logic!="propositional":
            substitution=_renameNonContTokens(self._context+self._stat.relativeComponents(self._pos,self._pos),substitution)        
        substitutionNatural=substitution.natural(self._logic,self._dialect)
        self._lines.append(substitution)
        self._stat=exp(self._stat[:self._pos]+_im+substitution+self._stat[self._pos:])
        self._pos=self._pos+len(substitution)+len(_as)
        fitchNewLine=_newLine()+self._space+self._prefix+_il+self._space+substitutionNatural+self._no(name)
        naturalNewLine=self._substitutionPhrase()+substitutionNatural+self._no(name,True)+_par["period"]
        theoryNewLine=_newParagraph()+"Theorem"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+substitutionNatural+_par["period"]
        basicNewLine=_newParagraph()+"Conclusion"+self._no(name)+_par["period"]+self._label+_newLine()+_par["space"]+substitutionNatural+_par["period"]
        _Exp[self._lineNoPrefix+str(self._lineNo)]=substitution
        self._addLine(fitchNewLine,naturalNewLine,theoryNewLine,basicNewLine)           
        return substitution 
    def end(self,*conclusions):
        if self._theme=="language":
            return N(N)
        if self._pos==len(self._stat):
            return N
        d=0
        i=self._pos
        assStartPos=[]
        assEndPos=[]
        conStartPos=[]
        conEndPos=[]
        last=''
        while d<1 and i>0:
            i=i-1
            if self._stat[i]==_lb:
                d=d+1
            if self._stat[i]==_rb:
                d=d-1
            if self._stat[i]==_as and d==0:
                if last=='conclusion':
                    assStartPos.append(i)
                    assEndPos.append(conStartPos[len(conStartPos)-1])
                elif last=='':
                    assStartPos.append(i)
                    assEndPos.append(self._pos)
                else:
                    assStartPos[len(assStartPos)-1]=i              
                last='assumption'
            if (self._stat[i]==_im or self._stat[i]==_na) and d==0:
                if last=='assumption':
                    conStartPos.append(i)
                    conEndPos.append(assStartPos[len(assStartPos)-1])
                elif last=='':
                    conStartPos.append(i)
                    conEndPos.append(self._pos)
                elif len(conStartPos)==1:
                    conStartPos.append(i)
                    conEndPos.append(conStartPos[0])
                else:
                    conStartPos[len(conStartPos)-1]=i              
                last='conclusion'
        assList=[]
        for i in range(0,len(assStartPos)):
            assList=assList+components(self._stat[assStartPos[i]:assEndPos[i]])
        assumption=_state(assList)
        conList=[]
        for i in range(1,len(conStartPos)):
            if self._stat[conStartPos[i]-1]!=_na:
                conList=conList+components(self._stat[conStartPos[i]:conEndPos[i]])
        proof=_state(conList)
        if len(conStartPos)<1:
            statement=NN
        else:
            statement=_state(components(self._stat[conStartPos[0]:conEndPos[0]]))
        for cons in conclusions:
            for con in components(cons):
                if con in components(proof):
                    statement=statement+_state([con])
        proposition=_state(self._context+self._stat.relativeComponents(i,i)).proposition(assumption,proof,statement)
        propositionNatural=proposition.natural(self._logic,self._dialect)
        prop=components(proposition)[0]
        if isInf(prop):
            dec=decomposeFor(components(proposition)[0])
            propositionConclusionNatural=exp(dec[1][1]).natural(self._logic,self._dialect)
        else:
            propositionConclusionNatural=prop.natural(self._logic,self._dialect)
        self._lines.append(NN)
        self._lines.append(proposition)
        if self._pos<len(self._stat)-1:
            fitchNewLine=_newLine()+self._space+self._prefix+_cl+self._space+self._endArgument+self._newLine+self._space+self._prefix+self._space+propositionNatural
            naturalNewLine=" Subargument complete. It proves the following: "+propositionNatural+self._no("",True)+_par["period"]+_newParagraph()
            self._prefix=self._prefix[0:len(self._prefix)-1]
            self._stat=exp(self._stat[:self._pos+1]+_im+proposition+self._stat[self._pos+1:])
            self._pos=self._pos+1+len(_im)+len(proposition)
            self._addLine(fitchNewLine,naturalNewLine,"")               
        else:
            fitchNewLine=_newLine()+self._space+self._prefix+_cl+self._space+propositionConclusionNatural+self._no()
            naturalNewLine=_newParagraph()+"Argument complete. It proves that under the stated assumptions, we have the following: "+propositionConclusionNatural+self._no("",True)+_par["period"]
            theoryNewLine=_newParagraph()+"Theory complete."
            basicNewLine=_newParagraph()+"Deductive argument complete. It proves that under the stated assumptions, we have the following: "+propositionConclusionNatural+self._no("",True)+_par["period"]
            self._conclusion=proposition
            _Exp[self._lineNoPrefix+str(self._lineNo)]=proposition
            self._pos=self._pos+1
            self._addLine(fitchNewLine,naturalNewLine,theoryNewLine,basicNewLine)    
            self._lineNo=self._lineNo+1
        return proposition
