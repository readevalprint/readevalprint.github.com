---
title: Code generation for Fun and Profit.
layout: post_page
---


So these past few posts have been about parsing python and manipulating the AST. But now I'm wondering if there are other ways. We could use Lex-Yacc which I've been wanting to get into for a long time. But also I wanted to enumerate ofer the possible output programs of a specific depth. So I did what any sensable programmer would do and asked Virtual Noam Chomsky.

    >>> from nltk.misc.chomsky import generate_chomsky
    >>> generate_chomsky(times=1, line_length=80)
    
    It may be, then, that a case of semigrammaticalness of a different sort is not
    quite equivalent to a general convention regarding the forms of the grammar.

I whole heartedly agree with Virtual Chomsky and couldn't have worded it better myself. But seriously, this is a bad idea. I'm sure you are sitting there judging my lack of foresight and choice of blog typography. But who cares. I will google and read and get distracted and I just learned nltk has a stemmer for German! That's cool.

Reading about [LFG](http://en.wikipedia.org/wiki/Lexical_functional_grammar) and [Chomsky normal form](http://en.wikipedia.org/wiki/Chomsky_normal_form).


    import nltk
    print nltk.__version__
    from nltk.parse import generate
    from nltk import nonterminals, Production, CFG
    
    grammar = CFG.fromstring("""M -> E
    E -> EE
    E -> "(" B ")"
    E -> 'a' | 'b' 
    B -> E '+' E|E '-' E|E '*' E|E '/' E
    """)
    
    print(repr(grammar.productions()).replace(',', ',\n'))

Out:

    3.0b1
    [M -> E,
     E -> EE,
     E -> '(' B ')',
     E -> 'a',
     E -> 'b',
     B -> E '+' E,
     B -> E '-' E,
     B -> E '*' E,
     B -> E '/' E]
     
Ok that's cool! That some sweet grammar you got there... But do you know what to do with it?

    for s in generate.generate(grammar, depth=7, n=50):
    print ''.join(s)
    
Out:

    ((a+a)+(a+a))
    ((a+a)+(a+b))
    ((a+a)+(b+a))
    ((a+a)+(b+b))
    ((a+a)+(a-a))
    ((a+a)+(a-b))
    ((a+a)+(b-a))
    ((a+a)+(b-b))
    ((a+a)+(a*a))
    ((a+a)+(a*b))
    ((a+a)+(b*a))
    ((a+a)+(b*b))
    ((a+a)+(a/a))
    ((a+a)+(a/b))
    ((a+a)+(b/a))
    ((a+a)+(b/b))
    ((a+a)+a)
    ((a+a)+b)
    ((a+b)+(a+a))
    ((a+b)+(a+b))
    ((a+b)+(b+a))
    ((a+b)+(b+b))
    ((a+b)+(a-a))
    ((a+b)+(a-b))
    ((a+b)+(b-a))
    ((a+b)+(b-b))
    ((a+b)+(a*a))
    ((a+b)+(a*b))
    ((a+b)+(b*a))
    ((a+b)+(b*b))
    ((a+b)+(a/a))
    ((a+b)+(a/b))
    ((a+b)+(b/a))
    ((a+b)+(b/b))
    ((a+b)+a)
    ((a+b)+b)
    ((b+a)+(a+a))
    ((b+a)+(a+b))
    ((b+a)+(b+a))
    ((b+a)+(b+b))
    ((b+a)+(a-a))
    ((b+a)+(a-b))
    ((b+a)+(b-a))
    ((b+a)+(b-b))
    ((b+a)+(a*a))
    ((b+a)+(a*b))
    ((b+a)+(b*a))
    ((b+a)+(b*b))
    ((b+a)+(a/a))
    ((b+a)+(a/b))
    
Hummmm. Let's see if we can make a solver?! Can you guess what I'm getting at? Code generation + UnitTests = Robotic programmer overlords!

    from __future__ import division
    import functools
    import sys
    
    # [(a,b),...]
    inputs = [(3, 4), (4, 3), (5, 12), (12, 5), (8, 15), (15, 8)]
    #[c, ...]
    answers = [x*x for x in [5, 5, 13, 13, 17, 17]]
    
    def test(code, *args):
        ((a, b), c), = args
        
        try:
            return c == eval(code)
        except ZeroDivisionError:
            return False
        except Exception as e:
            print e
            
    for s in generate.generate(grammar, depth=7):
        code = ''.join(s)
        test_case = functools.partial(test, code)
        print '.',
        if all(map(test_case, zip(inputs, answers))):
            print ''
            print 'PASS: ', code
        sys.stdout.flush()
    
    print 'Done!'
    
Out:

     . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
    PASS:  ((a*a)+(b*b))
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
    PASS:  ((b*b)+(a*a))
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . Done!
    
Now we see that `a*a` + `b*b` == `c*c` which is a programmatic way of saying: a<sup>2</sup> + b<sup>2</sup> = c<sup>2</sup>! Good job. And thanks for tuning in!
