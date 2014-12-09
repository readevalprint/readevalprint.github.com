---
layout: post_page
title: Getting Polished with Rust
---

So my coworker is the local [Rust](http://www.rust-lang.org/) acolyte and he has persuaded me to give it a try. So here is a stream of though.

## curl | bash

Ugh, I hate the security implications of having people piping things directly to bash. That is the path of sadness.

## If is assignment?!

    y = if x < 5 { "x is not less than 5" } else { "x is greater than 5"}


So that means `y` will be assigned a string. Very strange but it is making sense
because

> Rust is primarily an expression based language. There are only two kinds of
> statements, and everything else is an expression ...  if is an expression,
> which means that it returns a value. We can then use this value to initialize
> the binding.


Ok ok ok I get it! Now I got the "hello world" to compile and run.

    hello world

hahah wooo!!!



