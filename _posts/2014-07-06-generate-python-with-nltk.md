---
title: Code generation for Fun and Profit.
layout: post_page
image: https://cloud.githubusercontent.com/assets/118430/3489125/3972bc5e-0517-11e4-89b6-daeb9bb28bd5.png
---


So these past few posts have been about parsing python and manipulating the AST. But now I'm wondering if there are other ways. We could use Lex-Yacc which I've been wanting to get into for a long time. But also I wanted to enumerate over the possible output programs. So I did what any sensible programmer would do and asked Virtual Noam Chomsky.

    >>> from nltk.misc.chomsky import generate_chomsky
    >>> generate_chomsky(times=1, line_length=80)
    
    It may be, then, that a case of semigrammaticalness of a different sort is not
    quite equivalent to a general convention regarding the forms of the grammar.

I whole heartedly agree with Virtual Chomsky and couldn't have worded it better myself. But seriously, this is a bad idea. I'm sure you are sitting there judging my lack of foresight and choice of blog typography. But who cares. I will google and read and get distracted and I just learned nltk has a stemmer for German! That's cool.

Reading about [LFG](http://en.wikipedia.org/wiki/Lexical_functional_grammar) and [Chomsky normal form](http://en.wikipedia.org/wiki/Chomsky_normal_form).


    import nltk
    print nltk.__version__
    from nltk.parse import generate
    from nltk import CFG
    
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
     
Ok that's cool! That's some sweet grammar you got there... But do you know how to use it?

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
    
Code generation + test cases = Robotic programmer overlords! 

    from __future__ import division
    import functools
    import sys
    
    # [(a,b),...]
    inputs = [(3, 4), (4, 3), (5, 12), (12, 5), (8, 15), (15, 8)]
    #[c, ...]
    answers = [x*x for x in [5, 5, 13, 13, 17, 17]]
    
    def test(code, a, b, c):
        try:
            return c == eval(code)
        except Exception as e:
            print code, e
            return False
            
    passed_code = []
    for s in generate.generate(grammar, depth=7):
        code = ''.join(s)
        test_case = functools.partial(test, code)
        print '.',
        try:
            for (a, b), c in zip(inputs, answers):
                if not c == eval(code):
                    break # early exit
            else:  # Lol, don't do this in production.
                print 'PASSED: ', code
                passed_code.append(code)
    
        except Exception as e:
            print code, e
        sys.stdout.flush()
    
    print 'Done!'
    print '\n'.join(passed_code)
    
Out:

     . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . PASSED:  ((a*a)+(b*b))
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . PASSED:  ((b*b)+(a*a))
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ((a+a)/(a-a)) division by zero
    . . . ((a+a)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((a+b)/(a-a)) division by zero
    . . . ((a+b)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((b+a)/(a-a)) division by zero
    . . . ((b+a)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((b+b)/(a-a)) division by zero
    . . . ((b+b)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((a-a)/(a-a)) division by zero
    . . . ((a-a)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((a-b)/(a-a)) division by zero
    . . . ((a-b)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((b-a)/(a-a)) division by zero
    . . . ((b-a)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((b-b)/(a-a)) division by zero
    . . . ((b-b)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((a*a)/(a-a)) division by zero
    . . . ((a*a)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((a*b)/(a-a)) division by zero
    . . . ((a*b)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((b*a)/(a-a)) division by zero
    . . . ((b*a)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((b*b)/(a-a)) division by zero
    . . . ((b*b)/(b-b)) division by zero
    . . . . . . . . . . . . . . . ((a/a)/(a-a)) float division by zero
    . . . ((a/a)/(b-b)) float division by zero
    . . . . . . . . . . . . . . . ((a/b)/(a-a)) float division by zero
    . . . ((a/b)/(b-b)) float division by zero
    . . . . . . . . . . . . . . . ((b/a)/(a-a)) float division by zero
    . . . ((b/a)/(b-b)) float division by zero
    . . . . . . . . . . . . . . . ((b/b)/(a-a)) float division by zero
    . . . ((b/b)/(b-b)) float division by zero
    . . . . . . . . . . . . . . . (a/(a-a)) division by zero
    . . . (a/(b-b)) division by zero
    . . . . . . . . . . . . . . . (b/(a-a)) division by zero
    . . . (b/(b-b)) division by zero
    . . . . . . . . . . . . Done!
    ((a*a)+(b*b))
    ((b*b)+(a*a))

    
Now we see that `a*a` + `b*b` == `c*c` which is a programmatic way of saying: a<sup>2</sup> + b<sup>2</sup> = c<sup>2</sup>! Good job. And thanks for tuning in!
