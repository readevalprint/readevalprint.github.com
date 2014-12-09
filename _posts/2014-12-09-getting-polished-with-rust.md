---
layout: post_page
title: Getting Polished with Rust
---

So my coworker is the local [Rust](http://www.rust-lang.org/) acolyte and he has persuaded me to give it a try. So here is a stream of thought from this journey.

## `curl | bash` is sad

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

Now I attempt to do [fizzbuzz](http://c2.com/cgi/wiki?FizzBuzzTest)!

Was getting a strange error, `print!("hi")` would not flush the buffer when the
program ended unless there was a trailing newline. So strange. But it only happened
on my computer so it is ok, we will move on.

## Done!

  fn main() {
    for i in range(0, 100i) {
      if i % 3 == 0 {
        print!("Fizz");
      }
      if i % 5 == 0 {
        print!("Buzz");
      }
      if (i % 5 == 0) | (i % 3 == 0)  {
        println!("");
      }
    }
  }


Woot!woot!


