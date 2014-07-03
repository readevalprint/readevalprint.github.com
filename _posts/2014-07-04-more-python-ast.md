---
layout: post_page
title: Further thoughts with the Python AST.
---
Ok just to come back to the whole python AST thing. I wanted to see how hard to make that nested dict into something that runs again. Let's see!!

## First the set up

    >>import ast
    >>import pprint
    
    >>tree = ast.parse("c = ' '.join(['hi' + 'world']);print c")
    >>print "AST: ", tree

    AST:  <_ast.Module object at 0x35dc910>

Derp. We knew this. Let us continue with the project. It's ever so slightly modified from an earlier post.

    # "serialize" better than "parse" don't you think?
    def serialize(node):
        """Converts and ast object into a dict. """
        # check if this is a node or list 
        if isinstance(node, list):
            result = []
            for child_node in node: # A list of nodes, really
                result += [parse_ast(child_node)]
            return result
        
        # A node it seems
        if '_ast' == getattr(node, '__module__', False):
            result = {}
            for k in node._fields:
                result[k] = parse_ast(getattr(node, k))
            # The original class would be nice if we want to reconstruct the tree
            return node.__class__, result 
        
        # Who knows what it is, just return it.
        return node
  
With a pinch of the `tree` above and a splash of python goodness we get...  
 
    >> serialized_tree = serialize(tree)
    >> print "Serialized: ", pprint.pformat(serialized_tree)
    
    Serialized:  (<class '_ast.Module'>,
 {'body': [(<class '_ast.Assign'>,
            {'col_offset': 0,
             'lineno': 1,
             'targets': [(<class '_ast.Name'>,
                          {'col_offset': 0,
                           'ctx': (<class '_ast.Store'>, {}),
                           'id': 'c',
                           'lineno': 1})],
             'value': (<class '_ast.Call'>,
                       {'args': [(<class '_ast.List'>,
                                  {'col_offset': 13,
                                   'ctx': (<class '_ast.Load'>, {}),
                                   'elts': [(<class '_ast.BinOp'>,
                                             {'col_offset': 14,
                                              'left': (<class '_ast.Str'>,
                                                       {'col_offset': 14,
                                                        'lineno': 1,
                                                        's': 'hi'}),
                                              'lineno': 1,
                                              'op': (<class '_ast.Add'>,
                                                     {}),
                                              'right': (<class '_ast.Str'>,
                                                        {'col_offset': 21,
                                                         'lineno': 1,
                                                         's': 'world'})})],
                                   'lineno': 1})],
                        'col_offset': 4,
                        'func': (<class '_ast.Attribute'>,
                                 {'attr': 'join',
                                  'col_offset': 4,
                                  'ctx': (<class '_ast.Load'>, {}),
                                  'lineno': 1,
                                  'value': (<class '_ast.Str'>,
                                            {'col_offset': 4,
                                             'lineno': 1,
                                             's': ' '})}),
                        'keywords': [],
                        'kwargs': None,
                        'lineno': 1,
                        'starargs': None})}),
           (<class '_ast.Print'>,
            {'col_offset': 31,
             'dest': None,
             'lineno': 1,
             'nl': True,
             'values': [(<class '_ast.Name'>,
                         {'col_offset': 37,
                          'ctx': (<class '_ast.Load'>, {}),
                          'id': 'c',
                          'lineno': 1})]})]})
                          
## Let's take it back to the beginning
We can build it again. Faster. Stronger. More Better.

    def deserialize(node):
        """ Returns an ast instance from an expanded dict. """
        if isinstance(node, tuple):
            klass, kws = node
            return klass(**deserialize(kws))
        elif isinstance(node, dict):
            d = {}
            for k, v in node.items():
                d[k] = deserialize(v)
            return d
        elif isinstance(node, list):
            return [deserialize(n) for n in node]
        else:
            return node
    
    >> deserialized_tree = deserialize(expanded_tree)
    >> print "Deserialized: ", deserialized_tree
    Deserialized:  <_ast.Module object at 0x36b7690>

Yay! Boring ol module object without errors!

## But will it run?

    >> exec(compile(deserialized_tree, filename="<ast>", mode="exec"))
    hello world

A bit of a round trip... I'm wondering hot to get a markov chain of nodes. Maybe generate them from scratch? And they called me mad! I'll show them... I'll show them all!

    >> rotN('K"lwuv"ycpv"vq"dg"cnkxg"cpf"hggn"vjg"ykpf"qp"o{"uecnr0')
