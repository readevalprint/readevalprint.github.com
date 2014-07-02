---
title: Micro benchmarks for fun and profit.
layout: post_page
---
There comes a certain point in a developer's life where they have the insatiable desire to do a benchmark. And not just any bechmark but a micro benchmark of something like string manipulation or data lookups. Whatever.  

Let's set the mood. You get a lot of http requests. A ton. Metric tonne. And based on either one of two headers you need to compare it to a list and decide if this request is allowed or not. To be more specific you will have:

    header1 = "value:junk"
    header2 = "junk=value"
    
And also you will have a precomputed list with all the naugty headers. The no-no list. And now the questions is, how *do* you do it?

## Trial by fire

    import timeit
    
    #This was was my initial guess. Trying to be clever with sets and not using lists. And imaging string mangling is not great.
    
    # Simple set intersection
    denormalized_set_intersect = '{header1, header2} & denormalized_bad_list' 
    
    denormalized_setup = '''\
    header1='z:something'
    header2='something=z'
    denormalized_bad_list={
     'a:something', 'something=a',
     'b:something', 'something=b',
     'c:something', 'something=c'
     'd:something', 'something=d',
     'e:something', 'something=e',
     'f:something', 'something=f'
    }'''

    
Ok that might work, but is it worth it? No spoilers!! But anyway, these test programs are in string because they will be benchmarked in a bit.

    # But then I was wondering if it was really better than trimming the strings..

    normalized_set_intersect = '''\
    {header1.split(':')[0], header2.split('=')[1]} & normalized_bad_list  
    '''

    normalized_setup = '''\
    header1='z:something'
    header2='something=z'
    normalized_bad_list={'a', 'b', 'c', 'd', 'e', 'f'}
    '''
    
    
Now I'm on a roll! What else is there...? Derp. The obvious, booleans!

    # And then I was thinking that I was over thinking it and tried an or on a whim.
    normalized_boolean = '''\
    (header1.split(':')[0] in normalized_bad_list) or (header2.split('=')[1] in normalized_bad_list)
    '''
    
    # Then just to make it full circle, it came back to the denormilzed with an "or"
    denormalized_boolean = '''\
    (header1 in denormalized_bad_list) or (header2 in denormalized_bad_list)
    
    '''
    
## Let the games begin
    
    # Welcome to the ultimate showdown ladies and gentlemen!
    BENCHMARKS = [
        ('Senormalized Set Sammy', denormalized_set_intersect, denormalized_setup),
        ('Normalized Set Jen', normalized_set_intersect, normalized_setup),
        ('Normalized Boolean Alice', normalized_boolean, normalized_setup),
        ('Denormalized Boolean Bob', denormalized_boolean, denormalized_setup),
    ]
    
    for name, prog, setup in BENCHMARKS:
        print "{0:-<25} {1} sec".format(name, timeit.timeit(prog, setup=setup, number=1000000))


## Results 

    Senormalized Set Sammy--- 0.195351839066 sec
    Normalized Set Jen------- 0.832314968109 sec
    Normalized Boolean Alice- 0.677690982819 sec
    Denormalized Boolean Bob- 0.0748100280762 sec

    
