---
title: From Python NLTK to AST to Code.
layout: post_page
---
   
First this.  
   
      "A butterfly alights apon a key. SyntaxError"
      -ReadEvalPrrint

Yes, I may be the greatest poet you have ever read. You are welcome. But let's get back to business. I want more python code being generated. And I do not want your butterflies and their nasty `SyntaxErrors`. Let's take the formal grammer a bit farther and make the AST tree and not the raw text code. What for you ask? Well to tell the truth, I want to do `if`, `for` and possibly `while` loops and builting that from strings sounds painful. But we could build it in pure python logic! [Enter Stage Right] The AST.



    import nltk
    print nltk.__version__
    from nltk.parse import generate
    from nltk import CFG
    
    grammar = CFG.fromstring("""Module -> "Module([" E "])"
    E -> E ", " E | "If(" Compare ", [" E "], [" E "])" | "Print(None, [" S "], True)" 
    Compare -> "Compare(left=" S ", ops=[" cmp ",], comparators=[" S "])"
    cmp -> "Gt()" | "Lt()"
    S -> S ", " S | "BinOp(" S ", " O ", " S ")"| "Num(" N ")" | Name 
    O -> "Add()" | "Sub()" 
    Name -> "Name(" id ", Load())"
    id -> "'a'" | "'b'"
    N -> 1
    """)
    
    
    print(repr(grammar.productions()).replace(',', ',\n'))

Out

    3.0b1
    [Module -> 'Module([' E '])',
     E -> E ',
     ' E,
     E -> 'If(' Compare ',
     [' E '],
     [' E '])',
     E -> 'Print(None,
     [' S '],
     True)',
     Compare -> 'Compare(left=' S ',
     ops=[' cmp ',
    ],
     comparators=[' S '])',
     cmp -> 'Gt()',
     cmp -> 'Lt()',
     S -> S ',
     ' S,
     S -> 'BinOp(' S ',
     ' O ',
     ' S ')',
     S -> 'Num(' N ')',
     S -> Name,
     O -> 'Add()',
     O -> 'Sub()',
     Name -> 'Name(' id ',
     Load())',
     id -> "'a'",
     id -> "'b'",
     N -> 1]
     
Now generate AST instances and run them! 

    import sys
    from ast import *
    for s in generate.generate(grammar, depth=7, n=5):
        code = ''.join(s)
        print code
        new_ast = eval(code)
        fix_missing_locations(new_ast) # Because this is all new code
        a = 1
        b = 2
        exec(compile(new_ast, filename="<ast>", mode="exec"))
        
Out
    
    Module([Print(None, [Name('a', Load())], True), Print(None, [Name('a', Load())], True)])
    1
    1
    Module([Print(None, [Name('a', Load())], True), Print(None, [Name('b', Load())], True)])
    1
    2
    Module([Print(None, [Name('b', Load())], True), Print(None, [Name('a', Load())], True)])
    2
    1
    Module([Print(None, [Name('b', Load())], True), Print(None, [Name('b', Load())], True)])
    2
    2
    Module([If(Compare(left=Name('a', Load()), ops=[Gt(),], comparators=[Name('a', Load())]), [Print(None, [Name('a', Load())], True)], [Print(None, [Name('a', Load())], True)])])
    1
    
A lot of "stuff" is happening right now. Buuuuuut it's kind of a pain to read this. I want code again. Real python code. A bit of research shows what we have a few options of various levels of upkeep. 
[unparse](https://pypi.python.org/pypi/UnParse) and 
[codegen.py](https://github.com/andreif/codegen/blob/master/codegen.py) look intersting. Let's try unparse first. 

    import unparse
    
    print new_ast
    unparse.Unparser(new_ast, sys.stdout)

Out
    <_ast.Module object at 0x3414290>
    
    if (a > a):
        print a
    else:
        print a
    Out[27]:
    <unparse.Unparser instance at 0x23a1680>
    
Hmph! Works.

    for s in generate.generate(grammar, depth=7, n=10):
        code = ''.join(s)
        new_ast = eval(code)
        fix_missing_locations(new_ast) # Because this is all new code
        a = 1
        b = 2
        print "=" * 10
        print "Code:",
        unparse.Unparser(new_ast, sys.stdout)
        print "\n\n"
        print "Output:"
        exec(compile(new_ast, filename="<ast>", mode="exec"))
        
Out

    ---snip somewhere in the middle---
    ==========
    Code:
    if (b > a):
        print a
    else:
        print b 
    
    
    Output:
    1
    ==========
    Code:
    if (b > a):
        print b
    else:
        print a 
    
    Output:
    2


And that is the current state of things. I don't know what you were expecting. Ok, I think this is enough Python. I'll do some research and find something else fun and interesting to share!
