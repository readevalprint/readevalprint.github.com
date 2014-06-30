
## Let see what makes python tick...
So python can be compiled into an Abstract Syntax Tree
([AST](https://docs.python.org/3/library/ast.html)). And there just happens to
be a module with that exact name. Wonders never cease! Let's see what the normal
print statement looks like...


    #import the module
    import ast
    
    tree = ast.parse("print('hello world')")
    print tree

    <_ast.Module object at 0x25cde10>


Well that was less than interesting... But let's not pass judgement too soon.
Who really _are_ you `<_ast.Module>`? What makes you tick?


    exec(compile(tree, filename="<ast>", mode="exec"))

    hello world


Ha! Well then... I do say... Something just happened. We were able to `compile`
and run `tree` and it still worked! I want to tease it apart. See the gritty
details. The first thing I would is print the `__dict__` on it. (haha what are
these "docs" you speak of? Begone with you.)


    tree.__dict__




    {'body': [<_ast.Print at 0x25bdc50>]}



Ok. Well there is `body` and it is a `list`... of one item. A certian
`<_ast.Print>`. That makes sense because the original was just a print
statement. She's a beauty, let's get a little closer.


    print_node = tree.body[0]
    print_node.__dict__




    {'col_offset': 0,
     'dest': None,
     'lineno': 1,
     'nl': True,
     'values': [<_ast.Str at 0x25bdc90>]}



This is cool! Now we can see it has a few more properties. `col_offset` and
`lineno` are likly to be related to tracebacks. I could look it up. But that is
not fun. No spoilers! The `values` property is a list and it contains a
`<_ast.Str>` which does makes sense as the original goal was to print a string.


    string_node = print_node.values[0]
    string_node.__dict__




    {'col_offset': 6, 'lineno': 1, 's': 'hello world'}



And there you go! `<_ast.Str>` has a `s` property that is in fact the profound
greeting we had intstructed it to proclaim. The mighty "hello world"! But that's
old news. In this modern and international world, we like to be a bit more
forward thinking. Let's use Portuguese!


    string_node.s = "Oi Mundo!"
    string_node.__dict__




    {'col_offset': 6, 'lineno': 1, 's': 'Oi Mundo!'}




    exec(compile(tree, filename="<ast>", mode="exec"))

    Oi Mundo!


Yay! It worked! But the inital thrill is wearing off. I need something more.
Something stronger.


    # This is obviously not going to work
    'a' ^ 'b'


    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)

    <ipython-input-37-8496cbf2925d> in <module>()
          1 # This is obviously not going to work
    ----> 2 'a' ^ 'b'
    

    TypeError: unsupported operand type(s) for ^: 'str' and 'str'


What was I thinking? Am I insane? One does not merely XOR two strings. That is
path of darkness, madness, and `TypeErrors`. No, no, this will not do at all.
Let us fix this. Because I don't just WANT to `^` one string to another. I
**need** to. It's a deeper, more **fundamental** yearning in my loins. Because
that is were all great thoughts originate. Your loins. Heh. Loin.


    tree2 = ast.parse("'cat' ^ 'dog'")
    print tree2

    <_ast.Module object at 0x257b910>


Ugh this no longer amuses me. This `<_ast.Module>` hiding all the juicy filling
behind a boring facade. I want more instanter gratification. So how about we
take a detour to shave a yak. Nay, full body wax it. If Django is a pony with
wings, this will be the worlds most aerodynamic yak. Like a rocket. Rocket Yak.


    def parse_ast(node):
        # check if this is a node or list 
        if isinstance(node, list):
            result = []
            for child_node in node: # A list of nodes, really
                result += [parse_ast(child_node)]
            return result
        
        # A node it seems
        if '_ast' == getattr(node, '__module__', False):
            result = {}
            for k in node.__dict__:
                result[k] = parse_ast(getattr(node, k))
            # The original class would be nice if we want to reconstruct the tree
            return node.__class__, result 
        
        # Who knows what it is, just return it.
        return node
    
    parse_ast(tree2)




    (_ast.Module,
     {'body': [(_ast.Expr,
        {'col_offset': 0,
         'lineno': 1,
         'value': (_ast.BinOp,
          {'col_offset': 0,
           'left': (_ast.Str, {'col_offset': 0, 'lineno': 1, 's': 'cat'}),
           'lineno': 1,
           'op': (_ast.BitXor, {}),
           'right': (_ast.Str, {'col_offset': 8, 'lineno': 1, 's': 'dog'})})})]})



Progress!! Now we get a nice and organized dict and lists of class and values.
And now we can see the... stuff. Sure. So that `_ast.BitXor` seems interesting.
But what does it mean?! (No one know what it means, it gets the people going!)
Now that I'm here, it makes sense to think about what XORing two strings really
means. Should it be algebraic? Or maybe fun? Ook ok ok. We won't use the caret
(^) on two strings. Instead it will be between a string and a number. And that
number is how far to rotate the string. And by "rotate" I mean increment the
bytes. What you say? Allow me to take out every zig. All of them.


    def rotN(message, n):
        result = ''
        # Yes this could be a list comprehension. 
        # But now your eyes are not bleeding.
        # You are welcome.
        for c in message:
            result += (unichr((ord((c)) + n))).encode('utf8') 
        return result 
    
    
    # No one will ever guess it!!
    so_freaking_secret = rotN('Eu gousto de açaí'.decode('utf8'), 4)
    print repr(so_freaking_secret)
    print so_freaking_secret

    'Iy$ksywxs$hi$e\xc3\xabe\xc3\xb1'
    Iy$ksywxs$hi$eëeñ


So now the question comes. How can I wedge in `rotN` where the `BitXor` is
within the AST tree? What if this function were parsed into an AST as well, then
everytime we come across a `BinOp` that has a `left` of `_ast.String` and a
`right` with a `_ast.Num` and an `op` of `_ast.BitXor`, we substitute the AST of
out new and impressive (and totaly secure) rotN function? Sounds like a plan!

Can we parse this?


    import inspect
    inspect.getsourcelines(rotN)




    ([u'def rotN(message, n):\n',
      u"    result = ''\n",
      u'    # Yes this could be a list comprehension. \n',
      u'    # But now your eyes are not bleeding.\n',
      u'    # You are welcome.\n',
      u'    for c in message:\n',
      u"        result += (unichr((ord((c)) + n))).encode('utf8') \n",
      u'    return result \n'],
     1)



Quick! To the AST parser!!


    rotN_source = '\n'.join(inspect.getsourcelines(rotN)[0])
    rotN_tree = ast.parse(rotN_source)
    parse_ast(rotN_tree)




    (_ast.Module,
     {'body': [(_ast.FunctionDef,
        {'args': (_ast.arguments,
          {'args': [(_ast.Name,
             {'col_offset': 9,
              'ctx': (_ast.Param, {}),
              'id': 'message',
              'lineno': 1}),
            (_ast.Name,
             {'col_offset': 18, 'ctx': (_ast.Param, {}), 'id': 'n', 'lineno': 1})],
           'defaults': [],
           'kwarg': None,
           'vararg': None}),
         'body': [(_ast.Assign,
           {'col_offset': 4,
            'lineno': 3,
            'targets': [(_ast.Name,
              {'col_offset': 4,
               'ctx': (_ast.Store, {}),
               'id': 'result',
               'lineno': 3})],
            'value': (_ast.Str, {'col_offset': 13, 'lineno': 3, 's': ''})}),
          (_ast.For,
           {'body': [(_ast.AugAssign,
              {'col_offset': 8,
               'lineno': 13,
               'op': (_ast.Add, {}),
               'target': (_ast.Name,
                {'col_offset': 8,
                 'ctx': (_ast.Store, {}),
                 'id': 'result',
                 'lineno': 13}),
               'value': (_ast.Call,
                {'args': [(_ast.Str,
                   {'col_offset': 50, 'lineno': 13, 's': 'utf8'})],
                 'col_offset': 19,
                 'func': (_ast.Attribute,
                  {'attr': 'encode',
                   'col_offset': 19,
                   'ctx': (_ast.Load, {}),
                   'lineno': 13,
                   'value': (_ast.Call,
                    {'args': [(_ast.BinOp,
                       {'col_offset': 27,
                        'left': (_ast.Call,
                         {'args': [(_ast.Name,
                            {'col_offset': 32,
                             'ctx': (_ast.Load, {}),
                             'id': 'c',
                             'lineno': 13})],
                          'col_offset': 27,
                          'func': (_ast.Name,
                           {'col_offset': 27,
                            'ctx': (_ast.Load, {}),
                            'id': 'ord',
                            'lineno': 13}),
                          'keywords': [],
                          'kwargs': None,
                          'lineno': 13,
                          'starargs': None}),
                        'lineno': 13,
                        'op': (_ast.Add, {}),
                        'right': (_ast.Name,
                         {'col_offset': 38,
                          'ctx': (_ast.Load, {}),
                          'id': 'n',
                          'lineno': 13})})],
                     'col_offset': 19,
                     'func': (_ast.Name,
                      {'col_offset': 19,
                       'ctx': (_ast.Load, {}),
                       'id': 'unichr',
                       'lineno': 13}),
                     'keywords': [],
                     'kwargs': None,
                     'lineno': 13,
                     'starargs': None})}),
                 'keywords': [],
                 'kwargs': None,
                 'lineno': 13,
                 'starargs': None})})],
            'col_offset': 4,
            'iter': (_ast.Name,
             {'col_offset': 13,
              'ctx': (_ast.Load, {}),
              'id': 'message',
              'lineno': 11}),
            'lineno': 11,
            'orelse': [],
            'target': (_ast.Name,
             {'col_offset': 8,
              'ctx': (_ast.Store, {}),
              'id': 'c',
              'lineno': 11})}),
          (_ast.Return,
           {'col_offset': 4,
            'lineno': 15,
            'value': (_ast.Name,
             {'col_offset': 11,
              'ctx': (_ast.Load, {}),
              'id': 'result',
              'lineno': 15})})],
         'col_offset': 0,
         'decorator_list': [],
         'lineno': 1,
         'name': 'rotN'})]})



**Gnarly!** It worked. (I pronounced the "g" cause I've been in Germany for a
while and they do that sort of thing. It is acutally satisfying and I would
wholy suggest you give it a try. guh-NAR-ly.)


    # So this still does not work. As expected, but let us see.....
    caret_string_tree = ast.parse("print 'Secret message: ','i like cheese' ^ 4") 
    exec(compile(caret_string_tree, filename="<ast>", mode="exec"))

    Secret message: 


    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)

    <ipython-input-477-e05450ad786b> in <module>()
          1 # So this still does not work. As expected, but let us see.....
          2 caret_string_tree = ast.parse("print 'Secret message: ','i like cheese' ^ 4")
    ----> 3 exec(compile(caret_string_tree, filename="<ast>", mode="exec"))
    

    <ast> in <module>()


    TypeError: unsupported operand type(s) for ^: 'str' and 'int'



    parse_ast(caret_string_tree)




    (_ast.Module,
     {'body': [(_ast.Print,
        {'col_offset': 0,
         'dest': None,
         'lineno': 1,
         'nl': True,
         'values': [(_ast.Str,
           {'col_offset': 6, 'lineno': 1, 's': 'Secret message: '}),
          (_ast.BinOp,
           {'col_offset': 25,
            'left': (_ast.Str,
             {'col_offset': 25, 'lineno': 1, 's': 'i like cheese'}),
            'lineno': 1,
            'op': (_ast.BitXor, {}),
            'right': (_ast.Num, {'col_offset': 43, 'lineno': 1, 'n': 4})})]})]})



    


So let's just brute force it. We could get elegant at a later time. But errr, so
that `rotn` function is, well, a function. But we need to call something. I
don't think this will be a drop in replacement. Perhaps this is more like a
macro? Maybe the list comprehension was a good idea. I am sorry for laughing at
you.


    message = 'Eu gousto de açaí'
    n= 4
    ''.join((unichr((ord((c)) + n))).encode('utf8') for c in message.decode('utf8'))
    # Ok. It's done.




    'Iy$ksywxs$hi$e\xc3\xabe\xc3\xb1'




    single_line_rotn = ast.parse("''.join((unichr((ord((c)) + n))).encode('utf8') for c in message.decode('utf8'))")
    parse_ast(single_line_rotn)




    (_ast.Module,
     {'body': [(_ast.Expr,
        {'col_offset': 0,
         'lineno': 1,
         'value': (_ast.Call,
          {'args': [(_ast.GeneratorExp,
             {'col_offset': 8,
              'elt': (_ast.Call,
               {'args': [(_ast.Str, {'col_offset': 40, 'lineno': 1, 's': 'utf8'})],
                'col_offset': 9,
                'func': (_ast.Attribute,
                 {'attr': 'encode',
                  'col_offset': 9,
                  'ctx': (_ast.Load, {}),
                  'lineno': 1,
                  'value': (_ast.Call,
                   {'args': [(_ast.BinOp,
                      {'col_offset': 17,
                       'left': (_ast.Call,
                        {'args': [(_ast.Name,
                           {'col_offset': 22,
                            'ctx': (_ast.Load, {}),
                            'id': 'c',
                            'lineno': 1})],
                         'col_offset': 17,
                         'func': (_ast.Name,
                          {'col_offset': 17,
                           'ctx': (_ast.Load, {}),
                           'id': 'ord',
                           'lineno': 1}),
                         'keywords': [],
                         'kwargs': None,
                         'lineno': 1,
                         'starargs': None}),
                       'lineno': 1,
                       'op': (_ast.Add, {}),
                       'right': (_ast.Name,
                        {'col_offset': 28,
                         'ctx': (_ast.Load, {}),
                         'id': 'n',
                         'lineno': 1})})],
                    'col_offset': 9,
                    'func': (_ast.Name,
                     {'col_offset': 9,
                      'ctx': (_ast.Load, {}),
                      'id': 'unichr',
                      'lineno': 1}),
                    'keywords': [],
                    'kwargs': None,
                    'lineno': 1,
                    'starargs': None})}),
                'keywords': [],
                'kwargs': None,
                'lineno': 1,
                'starargs': None}),
              'generators': [(_ast.comprehension,
                {'ifs': [],
                 'iter': (_ast.Call,
                  {'args': [(_ast.Str,
                     {'col_offset': 72, 'lineno': 1, 's': 'utf8'})],
                   'col_offset': 57,
                   'func': (_ast.Attribute,
                    {'attr': 'decode',
                     'col_offset': 57,
                     'ctx': (_ast.Load, {}),
                     'lineno': 1,
                     'value': (_ast.Name,
                      {'col_offset': 57,
                       'ctx': (_ast.Load, {}),
                       'id': 'message',
                       'lineno': 1})}),
                   'keywords': [],
                   'kwargs': None,
                   'lineno': 1,
                   'starargs': None}),
                 'target': (_ast.Name,
                  {'col_offset': 52,
                   'ctx': (_ast.Store, {}),
                   'id': 'c',
                   'lineno': 1})})],
              'lineno': 1})],
           'col_offset': 0,
           'func': (_ast.Attribute,
            {'attr': 'join',
             'col_offset': 0,
             'ctx': (_ast.Load, {}),
             'lineno': 1,
             'value': (_ast.Str, {'col_offset': 0, 'lineno': 1, 's': ''})}),
           'keywords': [],
           'kwargs': None,
           'lineno': 1,
           'starargs': None})})]})



OK OK OK! Let's try again. We need to get the `left` and `right` of the `BinOp`
in question, and tuck in that nasty list comprehension you made me write in its
place, with `left` repacing the variable `message` (variables are `_ast.Name`)
and `right` with `n`.


    parse_ast(caret_string_tree)




    (_ast.Module,
     {'body': [(_ast.Print,
        {'col_offset': 0,
         'dest': None,
         'lineno': 1,
         'nl': True,
         'values': [(_ast.BinOp,
           {'col_offset': 6,
            'left': (_ast.Str,
             {'col_offset': 6, 'lineno': 1, 's': 'i like cheese'}),
            'lineno': 1,
            'op': (_ast.BitXor, {}),
            'right': (_ast.Num, {'col_offset': 24, 'lineno': 1, 'n': 4})})]})]})




    # This is shameful, if I had space for more yaks, I would make a search a replace function. 
    single_line_rotn.body[0].value.args[0].elt.func.value.args[0].right = caret_string_tree.body[0].values[1].right
    single_line_rotn.body[0].value.args[0].generators[0].iter.func.value = caret_string_tree.body[0].values[1].left
    caret_string_tree.body[0].values[1] = single_line_rotn.body[0].value
    
    # moment of truth.
    exec(compile(caret_string_tree, filename="<ast>", mode="exec"))

    Secret message:  m$pmoi$gliiwi



    QED.

In case you want to see the final AST. Here is it in all its parsiness. You can
see where I added the original string "i like cheese".


    parse_ast(caret_string_tree)




    (_ast.Module,
     {'body': [(_ast.Print,
        {'col_offset': 0,
         'dest': None,
         'lineno': 1,
         'nl': True,
         'values': [(_ast.Str,
           {'col_offset': 6, 'lineno': 1, 's': 'Secret message: '}),
          (_ast.Call,
           {'args': [(_ast.GeneratorExp,
              {'col_offset': 8,
               'elt': (_ast.Call,
                {'args': [(_ast.Str,
                   {'col_offset': 40, 'lineno': 1, 's': 'utf8'})],
                 'col_offset': 9,
                 'func': (_ast.Attribute,
                  {'attr': 'encode',
                   'col_offset': 9,
                   'ctx': (_ast.Load, {}),
                   'lineno': 1,
                   'value': (_ast.Call,
                    {'args': [(_ast.BinOp,
                       {'col_offset': 17,
                        'left': (_ast.Call,
                         {'args': [(_ast.Name,
                            {'col_offset': 22,
                             'ctx': (_ast.Load, {}),
                             'id': 'c',
                             'lineno': 1})],
                          'col_offset': 17,
                          'func': (_ast.Name,
                           {'col_offset': 17,
                            'ctx': (_ast.Load, {}),
                            'id': 'ord',
                            'lineno': 1}),
                          'keywords': [],
                          'kwargs': None,
                          'lineno': 1,
                          'starargs': None}),
                        'lineno': 1,
                        'op': (_ast.Add, {}),
                        'right': (_ast.Num,
                         {'col_offset': 43, 'lineno': 1, 'n': 4})})],
                     'col_offset': 9,
                     'func': (_ast.Name,
                      {'col_offset': 9,
                       'ctx': (_ast.Load, {}),
                       'id': 'unichr',
                       'lineno': 1}),
                     'keywords': [],
                     'kwargs': None,
                     'lineno': 1,
                     'starargs': None})}),
                 'keywords': [],
                 'kwargs': None,
                 'lineno': 1,
                 'starargs': None}),
               'generators': [(_ast.comprehension,
                 {'ifs': [],
                  'iter': (_ast.Call,
                   {'args': [(_ast.Str,
                      {'col_offset': 72, 'lineno': 1, 's': 'utf8'})],
                    'col_offset': 57,
                    'func': (_ast.Attribute,
                     {'attr': 'decode',
                      'col_offset': 57,
                      'ctx': (_ast.Load, {}),
                      'lineno': 1,
                      'value': (_ast.Str,
                       {'col_offset': 25, 'lineno': 1, 's': 'i like cheese'})}),
                    'keywords': [],
                    'kwargs': None,
                    'lineno': 1,
                    'starargs': None}),
                  'target': (_ast.Name,
                   {'col_offset': 52,
                    'ctx': (_ast.Store, {}),
                    'id': 'c',
                    'lineno': 1})})],
               'lineno': 1})],
            'col_offset': 0,
            'func': (_ast.Attribute,
             {'attr': 'join',
              'col_offset': 0,
              'ctx': (_ast.Load, {}),
              'lineno': 1,
              'value': (_ast.Str, {'col_offset': 0, 'lineno': 1, 's': ''})}),
            'keywords': [],
            'kwargs': None,
            'lineno': 1,
            'starargs': None})]})]})




    
