---
title: It's cool to make your own crypto
layout: post_page
---

Uncrackable. Unbreakable. No one will know what this does. Like seriously. Ok I have a test for you... Can you figure out the ones on the bottom of the page.

    # Using python2.7
    def rotN(message, n):
        message = message.decode('utf8')
        result = ''
        # Yes this could be a list comprehension. 
        # But now your eyes are not bleeding.
        # You are welcome.
        for c in message:
            result += (unichr((ord((c)) + n))).encode('utf8') 
        return result 

Here is a secret message for you!

    print rotN('8kj\x16i[h_ekibo\x16\\ebai"\x16_id\x1dj\x16j^_i\x16`kij\x16]h[Wj5', 10)

Here are a few more lines for you enjoyment. But... to make this interesting. I won't tell you the offset.
A secret

    '1\\\rf\\b\rX[\\d\raUR\rZbSSV[\rZN[,'

The saga continues....

    'J}|(\x7fpmv(q|(kwum{(lw\x7fv(|w(q|4(Q(|pqvs(|pmzm(q{(i(tq||tm(u}nnqv(uiv(qv(}{(itt6(0xwqv|(i|(\xc2\x81w}z(pmiz|1'

Our hero continues....

    '5h\x14h]aYg \x14`]ZY\x14WUb\x14VY\x14U\x14`]hh`Y\x14acfY\x14UVfidh\x14h\\Ub\x14=\x14]aU[]bYX"'

The boss level!!

    'Yz\xc2\x82+\x7f\xc2\x82pp\x7f+xp+3K}plop\xc2\x81lw{}ty\x7f4+~zxp\x7fstyr9'
  
