---
layout: post_page
title: My first Erlang program
---

Enough reading and watching [great videos](https://www.youtube.com/watch?v=xrIjfIjssLE]). It's time to 
get our grubby little virtual fingers dirty in some code.

A great way to get in the mix is [Project Euler](https://projecteuler.net/problem=1)! The first problem is 
essentially fizz-buzz. "Find the sum of all the multiples of 3 or 5 below 1000." This is a great one 
because you can learn the built in functions first!


    
    # File eular.erl
    -module(eular).
    -export([three_or_five/1]).
    
    three_or_five(A) ->
        if
            A rem 3 == 0 ->
                A;
            A rem 5 == 0 ->
                A;
            true ->
                0
        end.


Then call it

    $ erl
    Erlang R16B01 (erts-5.10.2) [source] [64-bit] [smp:8:8] [async-threads:10] [kernel-poll:false]
    
    Eshell V5.10.2  (abort with ^G)
    1> c(eular).
    {ok,eular}
    2> lists:sum(lists:map(fun eular:three_or_five/1, lists:seq(0,10-1))).  
    23
    3> lists:sum(lists:map(fun eular:three_or_five/1, lists:seq(0,1000-1))).
    <no spoiler you cheat!>

This was a lot of fun! The hardest part was navagating the docs and understanding how to call the built in functions. I could have done everything myself. Including iterating over the list. But no. Function code has `map`, and `sum`. You should use them. I am still not sure why `lists:map` needs `fun` before the function...
