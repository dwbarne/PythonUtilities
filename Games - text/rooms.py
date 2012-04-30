#!/usr/bin/python
# 2008-01-30

import random

# setup environment
#             N S E W U D T
travelTable=[[0,2,0,0,0,0,0],    # ROOM 1
             [1,3,3,0,0,0,0],    # ROOM 2
             [2,0,5,2,0,0,0],    # ROOM 3
             [0,5,0,0,0,0,0],    # ROOM 4
             [4,0,0,3,5,13,0],   # ROOM 5
             [0,0,1,0,0,0,0],    # ROOM 6
             [0,8,0,0,0,0,0],    # ROOM 7
             [7,0,0,0,0,0,0],    # ROOM 8
             [0,9,0,0,0,8,0],    # ROOM 9
             [8,0,11,0,0,0,0],   # ROOM 10
             [0,0,10,0,0,0,0],   # ROOM 11
             [0,0,0,13,0,0,0],   # ROOM 12
             [0,0,12,0,5,0,0],   # ROOM 13
             [0,15,17,0,0,0,0],  # ROOM 14
             [14,0,0,0,0,5,0],   # ROOM 15
             [17,0,19,0,0,0,0],  # ROOM 16
             [18,16,0,14,0,0,0], # ROOM 17
             [0,17,0,0,0,0,0],   # ROOM 18
             [9,0,0,16,0,0,0]]   # ROOM 19

# distribute positive numbers 10 to 109
# place in last element of 4 random lists
# nothing is placed in list 6 or 11
cnt=0
while cnt <= 3:
#    a = range(1,20)
#    room = random.choice(a)
    room = random.randint(1, 19)
    if room != 6 and room != 11 and travelTable[room-1][6] == 0:
#        b = range(10,110)
#        treasure = random.choice(b)
        treasure=random.randint(10,109)
        travelTable[room-1][6] = treasure
    else:
        cnt -= 1
    cnt += 1

# distribute negtive numbers -4 to -1
# place in last element of 4 random lists
# nothing is placed in list 6 or 11
cnt=4
while cnt > 0:
    a = range(1,20)
    room = random.choice(a)
    if room != 6 and room != 11 and travelTable[room-1][6] == 0:
        travelTable[room-1][6] = -cnt
    else:
        cnt += 1
    cnt -= 1

# put positive numbers in the last element
# of two specific lists overwriting any
# number that exists
a = range(1,99)
travelTable[3][6]= 100 + random.choice(a)
travelTable[15][6]= 100 + random.choice(a)

print " 1:", travelTable[0][6]
print " 2:", travelTable[1][6]
print " 3:", travelTable[2][6]
print " 4:", travelTable[3][6]
print " 5:", travelTable[4][6]
print " 6:", travelTable[5][6]
print " 7:", travelTable[6][6]
print " 8:", travelTable[7][6]
print " 9:", travelTable[8][6]
print "10:", travelTable[9][6]
print "11:", travelTable[10][6]
print "12:", travelTable[11][6]
print "13:", travelTable[12][6]
print "14:", travelTable[13][6]
print "15:", travelTable[14][6]
print "16:", travelTable[15][6]
print "17:", travelTable[16][6]
print "18:", travelTable[17][6]
print "19:", travelTable[18][6]
# end of program

"""
Message: 3
Date: Tue, 29 Jan 2008 20:17:13 -0500
From: bhaaluu <bhaaluu@gmail.com>
Subject: [Tutor] results not quite 100 percent yet
To: tutor-python <tutor@python.org>
Message-ID:
	<ea979d70801291717v25a5bfb7l20ac4056bc3c38e6@mail.gmail.com>
Content-Type: text/plain; charset=ISO-8859-1

Greetings,

I'm having a problem with the following test.
I make a dictionary with 19 keys (1 to 19).
Each key has a list of 7 numbers  (A to G)

# Set up the table
#    key#   A  B  C  D  E  F  G
tablE= {1:[ 0, 2, 0, 0, 0, 0, 0],    # 1
        2:[ 1, 3, 3, 0, 0, 0, 0],    # 2
        3:[ 2, 0, 5, 2, 0, 0, 0],    # 3
        4:[ 0, 5, 0, 0, 0, 0, 0],    # 4
        5:[ 4, 0, 0, 3,15,13, 0],    # 5
        6:[ 0, 0, 1, 0, 0, 0, 0],    # 6
        7:[ 0, 8, 0, 0, 0, 0, 0],    # 7
        8:[ 7,10, 0, 0, 0, 0, 0],    # 8
        9:[ 0,19, 0, 0, 0, 8, 0],    # 9
       10:[ 8, 0,11, 0, 0, 0, 0],   # 10
       11:[ 0, 0,10, 0, 0, 0, 0],   # 11
       12:[ 0, 0, 0,13, 0, 0, 0],   # 12
       13:[ 0, 0,12, 0, 5, 0, 0],   # 13
       14:[ 0,15,17, 0, 0, 0, 0],   # 14
       15:[14, 0, 0, 0, 0, 5, 0],   # 15
       16:[17, 0,19, 0, 0, 0, 0],   # 16
       17:[18,16, 0,14, 0, 0, 0],   # 17
       18:[ 0,17, 0, 0, 0, 0, 0],   # 18
       19:[ 9, 0, 0,16, 0, 0, 0]}   # 19
#    key#   A  B  C  D  E  F  G


The first loop is supposed to populate G with
a random range of 4 integers 10 to 109
in random keys 1-19 that have a zero (except keY 6 and  keY 11)
So keY 6 and keY 11 should both have a zero in G after the
four integers have been sown.

# populate G column with range of 4 integers 10 to 109
# in random keys that have a zero [except keYs 6 and 11]
print "%"*69
cnt=0
while cnt <= 3:
    print "CNT111=",cnt  #debug-remove when done
    a = range(1,20) # 1 to 19
    keY = random.choice(a)
    if keY == 6 or keY == 11 or tablE.values()[keY-1][6] != 
0:
        tablE.values()[5][6] = 0
        tablE.values()[10][6] = 0
        cnt -= 1
        keY = random.choice(a)
    if keY != 6 or keY != 11 or table.values()[keY-1][6] == 0:
        b = range(10,110) # 10 to 109
        integer = random.choice(b)
        tablE.values()[keY-1][6] = integer
        cnt += 1


The second loop is supposed to populate G with
numbers -4 to -1 in random keys 1-19 that have a zero
(except keY 6 and keY11). So once again, 6 and 11 should have
a zero in G after the loop is finished.

# populate G with range of integers -1 to -4
# in random keYs that have a zero [except keYs 6 and 11]
cnt=4
while cnt > 0:
    print "CNT222=",cnt
    a = range(1,20)
    if keY != 6 or keY != 11 and tablE.values()[keY-1][6] == 0:
        keY = random.choice(a)
        tablE.values()[keY-1][6] = -cnt
        cnt -= 1
    if keY == 6 or keY == 11:
        tablE.values()[5][6] = 0
        tablE.values()[10][6] = 0
        cnt += 1


The last thing is that two integers are placed in specific keys
4 and 16, overwriting anything that may be in G whether a
negative number or a number > 9.

# Put an integer in G at two specific keys: 4 & 16
# These will overwrite anything placed there previously
#a = range(1,99)
#tablE.values()[3][6]= 100 + random.choice(a)
#tablE.values()[15][6]= 100 + random.choice(a)

The above has been commented out so I see if the two loops are
each distributing four numbers each, without putting anything
in G of keys 6 and 11.

I've approached the problem by trying to get the loop to repeat
if a number ends up in G at key 6 or key 11. I've done this changing
the loop count. This seems to work about 97% of the time, or so.
I'm looking for 100%.

I know I can always just set those keys to zero before the table is
written, but I'd rather have the table as fully populated by the two
loops and just not have anything get in G in keys 6 & 11.

Anyway, this is just a short test, part of a larger program.
Here's the test code:

#!/usr/bin/python

import random

print "\n"*30

# Set up the table
#    key#   A  B  C  D  E  F  G
tablE= {1:[ 0, 2, 0, 0, 0, 0, 0],    # 1
        2:[ 1, 3, 3, 0, 0, 0, 0],    # 2
        3:[ 2, 0, 5, 2, 0, 0, 0],    # 3
        4:[ 0, 5, 0, 0, 0, 0, 0],    # 4
        5:[ 4, 0, 0, 3,15,13, 0],    # 5
        6:[ 0, 0, 1, 0, 0, 0, 0],    # 6
        7:[ 0, 8, 0, 0, 0, 0, 0],    # 7
        8:[ 7,10, 0, 0, 0, 0, 0],    # 8
        9:[ 0,19, 0, 0, 0, 8, 0],    # 9
       10:[ 8, 0,11, 0, 0, 0, 0],   # 10
       11:[ 0, 0,10, 0, 0, 0, 0],   # 11
       12:[ 0, 0, 0,13, 0, 0, 0],   # 12
       13:[ 0, 0,12, 0, 5, 0, 0],   # 13
       14:[ 0,15,17, 0, 0, 0, 0],   # 14
       15:[14, 0, 0, 0, 0, 5, 0],   # 15
       16:[17, 0,19, 0, 0, 0, 0],   # 16
       17:[18,16, 0,14, 0, 0, 0],   # 17
       18:[ 0,17, 0, 0, 0, 0, 0],   # 18
       19:[ 9, 0, 0,16, 0, 0, 0]}   # 19
#    key#   A  B  C  D  E  F  G

# populate G column with range of 4 integers 10 to 109
# in random keys that have a zero [except keYs 6 and 11]
print "%"*69
cnt=0
while cnt <= 3:
    print "CNT111=",cnt
    a = range(1,20) # 1 to 19
    keY = random.choice(a)
    if keY == 6 or keY == 11 or tablE.values()[keY-1][6] != 
0:
        tablE.values()[5][6] = 0
        tablE.values()[10][6] = 0
        cnt -= 1
        keY = random.choice(a)
    if keY != 6 or keY != 11 or table.values()[keY-1][6] == 0:
        b = range(10,110) # 10 to 109
        integer = random.choice(b)
        tablE.values()[keY-1][6] = integer
        cnt += 1

# populate G with range of integers -1 to -4
# in random keYs that have a zero [except keYs 6 and 11]
cnt=4
while cnt > 0:
    print "CNT222=",cnt
    a = range(1,20)
    if keY != 6 or keY != 11 and tablE.values()[keY-1][6] == 0:
        keY = random.choice(a)
        tablE.values()[keY-1][6] = -cnt
        cnt -= 1
    if keY == 6 or keY == 11:
        tablE.values()[5][6] = 0
        tablE.values()[10][6] = 0
        cnt += 1

# Put an integer in G at two specific keys: 4 & 16
# These will overwrite anything placed there previously
#a = range(1,99)
#tablE.values()[3][6]= 100 + random.choice(a)
#tablE.values()[15][6]= 100 + random.choice(a)

# print-out tablE
print "    data table"
print "---------------------"
print "       values"
print "key A B C D E F G"
for roomNum in range(0,19):
    print " ",roomNum+1,
    for compass in range(0,7):
        xVal = tablE.values()[roomNum][compass]
        print xVal,
        if compass == 6:
            print

I'm looking for suggestions on how to improve the two
loops so that I get 100% distribution each time (eight
numbers total).

I'm running a GNU/Linux OS,
Python 2.4.3
-- 
b h a a l u u at g m a i l dot c o m
"You assist an evil system most effectively by obeying its
orders and decrees. An evil system never deserves such
allegiance.  Allegiance to it means partaking of the evil.
A good person will resist an evil system with his or her
whole soul." [Mahatma Gandhi]


------------------------------

Message: 4
Date: Tue, 29 Jan 2008 21:26:05 -0500
From: Kent Johnson <kent37@tds.net>
Subject: Re: [Tutor] results not quite 100 percent yet
To: bhaaluu <bhaaluu@gmail.com>
Cc: tutor-python <tutor@python.org>
Message-ID: <479FE03D.5050406@tds.net>
Content-Type: text/plain; charset=ISO-8859-1; format=flowed

bhaaluu wrote:
>     if keY == 6 or keY == 11 or tablE.values()[keY-1][6] !=
0:
>         tablE.values()[5][6] = 0
>         tablE.values()[10][6] = 0

This is not the right way to access the values of a dict. tablE.values() 
is a list of the values in tablE, but it is not in the order you expect; 
it is easiest to think that it is in a random or indeterminate order.

Try
     if keY == 6 or keY == 11 or tablE[keY-1][6] != 0:
         tablE[5][6] = 0
         tablE[10][6] = 0

etc.

Kent

PS what's with the strange capitalization of variable names?

"""

#---------------------------------------------------------------------------------------------------------------------

"""
	tutor@python.org

To subscribe or unsubscribe via the World Wide Web, visit
	http://mail.python.org/mailman/listinfo/tutor
or, via email, send a message with subject or body 'help' to
	tutor-request@python.org

You can reach the person managing the list at
	tutor-owner@python.org

When replying, please edit your Subject line so it is more specific
than "Re: Contents of Tutor digest..."


Today's Topics:

   1. Re: results not quite 100 percent yet (Alan Gauld)
   2. Re: how to make python program as executable (Alan Gauld)
   3. how to enable overrideredirect (brindly sujith)
   4. Re: how to make python program as executable (Luke Paireepinart)
   5. Re: how to make python program as executable (Thorsten Kampe)
   6. Iron Python and Visual Basic 2005 Express (Dick Moores)


----------------------------------------------------------------------

Message: 1
Date: Wed, 30 Jan 2008 08:35:29 -0000
From: "Alan Gauld" <alan.gauld@btinternet.com>
Subject: Re: [Tutor] results not quite 100 percent yet
To: tutor@python.org
Message-ID: <fnpcoo$up6$1@ger.gmane.org>
Content-Type: text/plain; format=flowed; charset="iso-8859-1";
	reply-type=original


"bhaaluu" <bhaaluu@gmail.com> wrote 

In addition to Kents comments about dictionaruy 
access I think there may be another problem in 
your logic.

> The first loop is supposed to populate G with
> a random range of 4 integers 10 to 109
> in random keys 1-19 that have a zero (except keY 6 and  keY 11)
> So keY 6 and keY 11 should both have a zero in G after the
> four integers have been sown.
> 
>    if keY == 6 or keY == 11 or tablE.values()[keY-1][6] !=
0:
>        tablE.values()[5][6] = 0
>        tablE.values()[10][6] = 0
>        cnt -= 1
>        keY = random.choice(a)

This detects any of the exception cases so a simple else 
clause should be sufficient for the others. However if you 
really want an explicit check...

>    if keY != 6 or keY != 11 or table.values()[keY-1][6] == 
0:

This test should use 'and' rather than 'or' since you want 
all of the conditions to be true, not just one of them.
But since the failing condituions should all have been 
caught above simply using else here would do what 
I think you want.

>        b = range(10,110) # 10 to 109
>        integer = random.choice(b)
>        tablE.values()[keY-1][6] = integer
>        cnt += 1


-- 
Alan Gauld
Author of the Learn to Program web site
http://www.freenetpages.co.uk/hp/alan.gauld

------------------------------
"""

#----------------------------------------------------------------------------

"""
Send Tutor mailing list submissions to
	tutor@python.org

To subscribe or unsubscribe via the World Wide Web, visit
	http://mail.python.org/mailman/listinfo/tutor
or, via email, send a message with subject or body 'help' to
	tutor-request@python.org

You can reach the person managing the list at
	tutor-owner@python.org

When replying, please edit your Subject line so it is more specific
than "Re: Contents of Tutor digest..."


Today's Topics:

   1. Re: results not quite 100 percent yet (Kent Johnson)
   2. Re: results not quite 100 percent yet (bhaaluu)
   3. Re: how to make python program as executable (Michael Langford)
   4. Re: results not quite 100 percent yet (bhaaluu)
   5. Re: results not quite 100 percent yet (Kent Johnson)
   6. Re: results not quite 100 percent yet (bob gailer)
   7. Re: Iron Python and Visual Basic 2005 Express (Alan Gauld)
   8. Re: results not quite 100 percent yet (bhaaluu)


----------------------------------------------------------------------

Message: 1
Date: Wed, 30 Jan 2008 09:22:43 -0500
From: Kent Johnson <kent37@tds.net>
Subject: Re: [Tutor] results not quite 100 percent yet
To: bhaaluu <bhaaluu@gmail.com>
Cc: tutor-python <tutor@python.org>
Message-ID: <47A08833.8000206@tds.net>
Content-Type: text/plain; charset=ISO-8859-1; format=flowed

bhaaluu wrote:
> On Jan 30, 2008 8:24 AM, Kent Johnson <kent37@tds.net> wrote:
>> bhaaluu wrote:
>>> Now that you mention it, I do seem to remember that the order of
>>> a list is indeterminate.
>> No; the order of a dict is indeterminate, and consequently the order of
>> lists derived from dicts with keys(), values(), etc. is indeterminate.
> 
> The order of the dictionary is indeterminate. But the key is always
> attached to the value, and in my case, the value is a list, so
> 
> print tablE.keys() #prints all the keys [in an ordered list, 1-19]

This is implementation dependent. You should not depend on the order of 
elements in tablE.keys()

> print tablE.keys()[5] #prints the key, 6

This is implementation dependent.

> print tablE.values() #prints a list of [all [the lists]]

Yes. The order of the list (of lists) is implementation dependent.

> print tablE.values()[5] #prints only the [list for key 6]

This is implementation dependent and pointless. You are not using the 
dict at all except as a way to store a list of lists. Either use 
tablE[6], which will always return the list associated with the key 6, 
or just keep your lists in a list directly.

> So what you're saying here is that while it might work okay on
> my system, that this may not work the same way on another
> system?

Yes. The order of keys() and values() is implementation dependent. It 
may change with different versions of Python and different 
implementations. It can also change as you add more elements to the dict.

(For example, one problem the Jython folks have had getting Django to 
run on Jython is that the Django unit tests make assumptions about the 
order of dict values. These assumptions are not true in Jython and the 
unit tests fail.)

>         if travelTable.values()[roomNum-1][0] != 0:

Again, the use of travelTable.values() is pointless, inefficient (it 
creates a new list every time you call it) and indeterminate. Really, 
you shouldn't be doing this. I can't think of any reason to code this way.

Kent


------------------------------

Message: 2
Date: Wed, 30 Jan 2008 09:29:21 -0500
From: bhaaluu <bhaaluu@gmail.com>
Subject: Re: [Tutor] results not quite 100 percent yet
To: "Kent Johnson" <kent37@tds.net>
Cc: tutor-python <tutor@python.org>
Message-ID:
	<ea979d70801300629j27681ad2mf613da66cc91fda9@mail.gmail.com>
Content-Type: text/plain; charset=ISO-8859-1

On Jan 30, 2008 9:22 AM, Kent Johnson <kent37@tds.net> wrote:
> This is implementation dependent.
>[snip]
>
> >         if travelTable.values()[roomNum-1][0] != 0:
>
> Again, the use of travelTable.values() is pointless, inefficient (it
> creates a new list every time you call it) and indeterminate. Really,
> you shouldn't be doing this. I can't think of any reason to code this
way.
>
> Kent

This is good to know!
The reason I coded it that way is because I'm learning.
I seem to always be learning... that's why I'm subscribed
to THIS list. 8^D

Back to the drawing board!
Thank you very much for your help!
-- 
b h a a l u u at g m a i l dot c o m
"You assist an evil system most effectively by obeying its
orders and decrees. An evil system never deserves such
allegiance.  Allegiance to it means partaking of the evil.
A good person will resist an evil system with his or her
whole soul." [Mahatma Gandhi]


------------------------------

Message: 3
Date: Wed, 30 Jan 2008 09:32:57 -0500
From: "Michael Langford" <michael.langford@rowdylabs.com>
Subject: Re: [Tutor] how to make python program as executable
To: "brindly sujith" <brindly@gmail.com>, "python tutor"
	<tutor@python.org>
Message-ID:
	<82b4f5810801300632x53c3d14ayabb962b3da06c052@mail.gmail.com>
Content-Type: text/plain; charset=ISO-8859-1

On the command line type "which python"

Then at the top of your script put:

#!/usr/bin/python

or whatever path the which command outputted.

Then run chmod on the program:

chmod ugo+x script.py

then the following will work:
./script.py

If you actually want to build an executable that doesn't depend on the
presence of python, then this tutorial will help you:
http://wiki.python.org/moin/Freeze


          --Michael

On Jan 30, 2008 9:11 AM, brindly sujith <brindly@gmail.com> wrote:
> i am using linux...
>
> plz tell me how to do it
>
>
>



-- 
Michael Langford
Phone: 404-386-0495
Consulting: http://www.RowdyLabs.com


------------------------------

Message: 4
Date: Wed, 30 Jan 2008 12:19:05 -0500
From: bhaaluu <bhaaluu@gmail.com>
Subject: Re: [Tutor] results not quite 100 percent yet
To: "Alan Gauld" <alan.gauld@btinternet.com>
Cc: tutor@python.org
Message-ID:
	<ea979d70801300919g1dbb65e4h150985a56d017f72@mail.gmail.com>
Content-Type: text/plain; charset=ISO-8859-1

On Jan 30, 2008 3:35 AM, Alan Gauld <alan.gauld@btinternet.com> wrote:
> In addition to Kents comments about dictionaruy
> access I think there may be another problem in
> your logic.
>
>
> "bhaaluu" <bhaaluu@gmail.com> wrote
>
> > The first loop is supposed to populate G with
> > a random range of 4 integers 10 to 109
> > in random keys 1-19 that have a zero (except keY 6 and  keY 11)
> > So keY 6 and keY 11 should both have a zero in G after the
> > four integers have been sown.
> >
> >    if keY == 6 or keY == 11 or tablE.values()[keY-1][6]
!= 0:
> >        tablE.values()[5][6] = 0
> >        tablE.values()[10][6] = 0
> >        cnt -= 1
> >        keY = random.choice(a)
>
> This detects any of the exception cases so a simple else
> clause should be sufficient for the others. However if you
> really want an explicit check...
>
> >    if keY != 6 or keY != 11 or table.values()[keY-1][6] ==
0:
>
> This test should use 'and' rather than 'or' since you want
> all of the conditions to be true, not just one of them.
> But since the failing condituions should all have been
> caught above simply using else here would do what
> I think you want.
>
>
> >        b = range(10,110) # 10 to 109
> >        integer = random.choice(b)
> >        tablE.values()[keY-1][6] = integer
> >        cnt += 1
>
>
> --
> Alan Gauld
> Author of the Learn to Program web site
> http://www.freenetpages.co.uk/hp/alan.gauld

Thank you Alan and Kent.
Your suggestions caused me to completely start
from scratch. It also looks like the "nested sequence"
will be easier to use in the long run (and I'm into this
for the long run!). 8^D

This is working properly now on my
GNU/Linux system running Python 2.4.3:

#!/usr/bin/python
# 2008-01-30

import random

# setup environment
#             N S E W U D T
travelTable=[[0,2,0,0,0,0,0],    # ROOM 1
             [1,3,3,0,0,0,0],    # ROOM 2
             [2,0,5,2,0,0,0],    # ROOM 3
             [0,5,0,0,0,0,0],    # ROOM 4
             [4,0,0,3,5,13,0],   # ROOM 5
             [0,0,1,0,0,0,0],    # ROOM 6
             [0,8,0,0,0,0,0],    # ROOM 7
             [7,0,0,0,0,0,0],    # ROOM 8
             [0,9,0,0,0,8,0],    # ROOM 9
             [8,0,11,0,0,0,0],   # ROOM 10
             [0,0,10,0,0,0,0],   # ROOM 11
             [0,0,0,13,0,0,0],   # ROOM 12
             [0,0,12,0,5,0,0],   # ROOM 13
             [0,15,17,0,0,0,0],  # ROOM 14
             [14,0,0,0,0,5,0],   # ROOM 15
             [17,0,19,0,0,0,0],  # ROOM 16
             [18,16,0,14,0,0,0], # ROOM 17
             [0,17,0,0,0,0,0],   # ROOM 18
             [9,0,0,16,0,0,0]]   # ROOM 19

# distribute positive numbers 10 to 109
# place in last element of 4 random lists
# nothing is placed in list 6 or 11
cnt=0
while cnt <= 3:
    a = range(1,20)
    room = random.choice(a)
    if room != 6 and room != 11 and travelTable[room-1][6] == 0:
        b = range(10,110)
        treasure = random.choice(b)
        travelTable[room-1][6] = treasure
    else:
        cnt -= 1
    cnt += 1

# distribute negtive numbers -4 to -1
# place in last element of 4 random lists
# nothing is placed in list 6 or 11
cnt=4
while cnt > 0:
    a = range(1,20)
    room = random.choice(a)
    if room != 6 and room != 11 and travelTable[room-1][6] == 0:
        travelTable[room-1][6] = -cnt
    else:
        cnt += 1
    cnt -= 1

# put positive numbers in the last element
# of two specific lists overwriting any
# number that exists
a = range(1,99)
travelTable[3][6]= 100 + random.choice(a)
travelTable[15][6]= 100 + random.choice(a)

print " 1:", travelTable[0][6]
print " 2:", travelTable[1][6]
print " 3:", travelTable[2][6]
print " 4:", travelTable[3][6]
print " 5:", travelTable[4][6]
print " 6:", travelTable[5][6]
print " 7:", travelTable[6][6]
print " 8:", travelTable[7][6]
print " 9:", travelTable[8][6]
print "10:", travelTable[9][6]
print "11:", travelTable[10][6]
print "12:", travelTable[11][6]
print "13:", travelTable[12][6]
print "14:", travelTable[13][6]
print "15:", travelTable[14][6]
print "16:", travelTable[15][6]
print "17:", travelTable[16][6]
print "18:", travelTable[17][6]
print "19:", travelTable[18][6]
# end of program

-- 
b h a a l u u at g m a i l dot c o m
"You assist an evil system most effectively by obeying its
orders and decrees. An evil system never deserves such
allegiance.  Allegiance to it means partaking of the evil.
A good person will resist an evil system with his or her
whole soul." [Mahatma Gandhi]


------------------------------

Message: 5
Date: Wed, 30 Jan 2008 12:46:48 -0500
From: Kent Johnson <kent37@tds.net>
Subject: Re: [Tutor] results not quite 100 percent yet
To: bhaaluu <bhaaluu@gmail.com>
Cc: tutor@python.org
Message-ID: <47A0B808.7080702@tds.net>
Content-Type: text/plain; charset=ISO-8859-1; format=flowed

bhaaluu wrote:

> # distribute positive numbers 10 to 109
> # place in last element of 4 random lists
> # nothing is placed in list 6 or 11
> cnt=0
> while cnt <= 3:
>     a = range(1,20)
>     room = random.choice(a)

room = random.randint(1, 19) is simpler.

>     if room != 6 and room != 11 and travelTable[room-1][6] ==
0:
>         b = range(10,110)
>         treasure = random.choice(b)

Use randint() here too.

>         travelTable[room-1][6] = treasure
>     else:
>         cnt -= 1
>     cnt += 1

This use of cnt is a bit strange. Why not increment only in the 
successful 'if' and get rid of the 'else' entirely?

Rather than repeating the loop until you get three distinct, valid 
random numbers, you could do something like this:

# Change 7 rooms, not room 6 or 11
changeableRooms = range(1, 20)
changeableRooms.remove(6)
changeableRooms.remove(11)

roomsToChange = random.sample(changeableRooms, 7)

# First three get something good
for room in roomsToChange[:3]:
   travelTable[room-1][6] = random.randint(10, 119)

# Last four get something bad
for i, room in enumerate(roomsToChange[3:]):
   travelTable[room-1][6] = -i-1

> print " 1:", travelTable[0][6]
etc - use a loop and string formatting:

for i, room in enumerate(travelTable):
   print ' %s: %s' % (i+1, room[6])

Finally, you might consider putting a dummy entry at travelTable[0], or 
number the rooms from 0, so you don't have to adjust the indices all the 
time.

Kent


------------------------------

Message: 6
Date: Wed, 30 Jan 2008 14:24:35 -0500
From: bob gailer <bgailer@alum.rpi.edu>
Subject: Re: [Tutor] results not quite 100 percent yet
To: bhaaluu <bhaaluu@gmail.com>
Cc: tutor@python.org
Message-ID: <47A0CEF3.1080902@alum.rpi.edu>
Content-Type: text/plain; charset=ISO-8859-1; format=flowed

bhaaluu wrote:
> #             N S E W U D T
> travelTable=[[0,2,0,0,0,0,0],    # ROOM 1
>              [1,3,3,0,0,0,0],    # ROOM 2
It is good to finally see that you are building an adventure game.

Consider creating a instance of a Room class for each room and saving 
them in a collection such as a list.

This will give you much more flexibility as your game grows.

Inevitably I wound up doing a bunch of things more "Pythonically" so 
there may be stuff here you don't relate to yet. But is is all worth 
studying and will save you hours of headache later.

----------------------------- code -----------------------------
import random
class Room:
  roomNo = 0
  def __init__(self, destinations, updatable=True):
    Room.roomNo += 1
    self.roomNo = Room.roomNo
    self.destinations = destinations
    # store treasure apaart from destinations
    self.treasure = 0 # add intial treasure
    self.updatable = updatable # may have the treasure updated
  def updateTreasure(self, treasure):
    self.treasure = treasure
  def __repr__(self):
    return " %s:%s" % (self.roomNo, self.treasure)

rooms = [
  Room([0,2,0,0,0,0]),  # ROOM 1
  Room([1,3,3,0,0,0]),  # ROOM 2
  Room([2,0,5,2,0,0]),  # ROOM 3
  Room([0,5,0,0,0,0]),  # ROOM 4
  Room([4,0,0,3,5,13]), # ROOM 5
  Room([0,0,1,0,0,0], False), # ROOM 6 flagged as not updatable
  Room([0,8,0,0,0,0]), # ROOM 7
  Room([7,0,0,0,0,0]), # ROOM 8
  Room([0,9,0,0,0,8]), # ROOM 9
  # etc for the rest of the rooms -
        ]
  # note I omitted the initial treasure value since it is always 0
  # I modified the last for statement to account for only 9 rooms

# use random.sample to create random subsets of values and rooms
# - eliminates all the loops and tests
# note this ensures no duplicate treasures (do you want that?)

# create list of 8 random treasure values
values = random.sample(range(10,110),4) + random.sample(range(-4, 0),4)

# create list of 8 randomly selected updatable rooms
roomsToUpdate= random.sample([room for room in rooms if room.updatable], 8)

# update the rooms' Treasures
for room, value in zip(roomsToUpdate, values):
  room.updateTreasure(value)

a = range(1,99)
for room in (3,5):
  rooms[room].updateTreasure(100 + random.choice(a))

for room in rooms: print room 
----------------------------- end code -----------------------------

Things I did not do, but suggest:
- store the room destinations in a text file rather than hard-coding 
them in the program. It is almost always a good idea to separate logic 
from data.

 -create a Treasure class, storing instances directly in roo,s rather 
than indexes, and storing treasure definitions in the text file.

-store room instances in the destinations rather than indexes.

At this point you no longer need indexes!

-- 
Bob Gailer
919-636-4239 Chapel Hill, NC



------------------------------

Message: 8
Date: Wed, 30 Jan 2008 14:45:32 -0500
From: bhaaluu <bhaaluu@gmail.com>
Subject: Re: [Tutor] results not quite 100 percent yet
To: "Kent Johnson" <kent37@tds.net>
Cc: tutor@python.org
Message-ID:
	<ea979d70801301145i6fc3fa9doc6ea1191103be890@mail.gmail.com>
Content-Type: text/plain; charset=ISO-8859-1

On Jan 30, 2008 12:46 PM, Kent Johnson <kent37@tds.net> wrote:
> bhaaluu wrote:
>
> > # distribute positive numbers 10 to 109
> > # place in last element of 4 random lists
> > # nothing is placed in list 6 or 11
> > cnt=0
> > while cnt <= 3:
> >     a = range(1,20)
> >     room = random.choice(a)
>
> room = random.randint(1, 19) is simpler.
>
> >     if room != 6 and room != 11 and travelTable[room-1][6] ==
0:
> >         b = range(10,110)
> >         treasure = random.choice(b)
>
> Use randint() here too.
>
> >         travelTable[room-1][6] = treasure
> >     else:
> >         cnt -= 1
> >     cnt += 1
>
> This use of cnt is a bit strange. Why not increment only in the
> successful 'if' and get rid of the 'else' entirely?
>
> Rather than repeating the loop until you get three distinct, valid
> random numbers, you could do something like this:
>
> # Change 7 rooms, not room 6 or 11
> changeableRooms = range(1, 20)
> changeableRooms.remove(6)
> changeableRooms.remove(11)
>
> roomsToChange = random.sample(changeableRooms, 7)
>
> # First three get something good
> for room in roomsToChange[:3]:
>    travelTable[room-1][6] = random.randint(10, 119)
>
> # Last four get something bad
> for i, room in enumerate(roomsToChange[3:]):
>    travelTable[room-1][6] = -i-1
>
> > print " 1:", travelTable[0][6]
> etc - use a loop and string formatting:
>
> for i, room in enumerate(travelTable):
>    print ' %s: %s' % (i+1, room[6])
>
> Finally, you might consider putting a dummy entry at travelTable[0], or
> number the rooms from 0, so you don't have to adjust the indices all the
> time.
>
> Kent
>

Thank you Kent! All of these look like very useful suggestions.

What I'm trying to do is implement an old Text Adventure Game
that was written c.1983. I'm trying to keep the flavor of the game
as close as possible to the original.

I'm not old enough, in computer years, to remember the "Glory Days"
of Text Adventure Games on computers like the Apple ][, Atari,
Commodore 64, IBM PC, VIC 20, and so forth. As a result, I don't
know anything about Text Adventure Games. So this is a real
learning experience for me in more ways than just learning Python.

The book I'm using as a reference is at:
http://www.atariarchives.org/adventure/
Creating Adventure Games On Your Computer.
The author was Tim Hartnell.
http://en.wikipedia.org/wiki/Tim_Hartnell

Most of the problems so far stem from the old line-numbered BASIC's
GOTO [line-number] statements. There are other problems as well,
but _that one crops up regularly.

Nevertheless, it has been fun, so far. I'm a Hobbyist programmer, so
even if I don't succeed at making a Retro-game, I'm having fun trying.

At least I'm getting a good idea of what an old-timey Text Adventure
Game is all about. The only thing I can think of of, is that it must have
been quite a challenge to get one of those old computers to do anything
at all.... so if someone could get a TAG working, it must have been
quite a thrill! 8^D

Happy Programming!
-- 
b h a a l u u at g m a i l dot c o m
"You assist an evil system most effectively by obeying its
orders and decrees. An evil system never deserves such
allegiance.  Allegiance to it means partaking of the evil.
A good person will resist an evil system with his or her
whole soul." [Mahatma Gandhi]


------------------------------
"""