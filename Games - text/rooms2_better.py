#!/usr/bin/python
# 2008-01-30
# bob gailer [Tutor]
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

# Table of Rooms
rooms = [
      Room([0,2,0,0,0,0,0]),    # 1 Hallway
      Room([1,3,3,0,0,0,0]),    # 2 Audience Chamber
      Room([2,0,5,2,0,0,0]),    # 3 Great Hall
      Room([0,5,0,0,0,0,0]),    # 4 Private Meeting Room
      Room([4,0,0,3,15,13,0]),  # 5 Inner Hallway
      Room([0,0,1,0,0,0,0],False),  # 6 Entrance (Not Updatable)
      Room([0,8,0,0,0,0,0]),    # 7 Kitchen
      Room([7,10,0,0,0,0,0]),   # 8 Store Room
      Room([8,8,8,8,8,8,0]),    # 9 Lift
      Room([8,0,11,0,0,0,0]),   #10 Rear Vestibule
      Room([0,0,10,0,0,0,0],False), #11 Exit (Not Updatable)
      Room([0,0,0,13,0,0,0]),   #12 Dungeon
      Room([0,0,12,0,5,0,0]),   #13 Guardroom
      Room([0,15,17,0,0,0,0]),  #14 Master Bedroom
      Room([14,0,0,0,0,5,0]),   #15 Upper Hall
      Room([17,0,19,0,0,0,0]),  #16 Treasury
      Room([18,16,0,14,0,0,0]), #17 Chambermaid's Bedroom
      Room([0,17,0,0,0,0,0]),   #18 Dressing Chamber
      Room([9,0,0,16,0,0,0])]   #19 Small Room

# note I omitted the initial treasure value since it is always 0
# use random.sample to create random subsets of values and rooms
# - eliminates all the loops and tests
# note this ensures no duplicate treasures (do you want that?)

# create list of 8 random treasure values
values = random.sample(range(10,110),4) + random.sample(range(-4, 0),4)
print " values:",values

# create list of 8 randomly selected updatable rooms
roomsToUpdate = random.sample([room for room in rooms if room.updatable], 8)
print "8 rooms:",roomsToUpdate

# update the rooms' Treasures
for room, value in zip(roomsToUpdate, values):
 room.updateTreasure(value)

a = range(1,99)
for room in (3,15):
 rooms[room].updateTreasure(100 + random.choice(a))

for room in rooms:
    print room
# end code ################################

"""

------------------------------

Message: 3
Date: Wed, 30 Jan 2008 15:52:08 -0500
From: bhaaluu <bhaaluu@gmail.com>
Subject: Re: [Tutor] results not quite 100 percent yet
To: "bob gailer" <bgailer@alum.rpi.edu>
Cc: tutor@python.org
Message-ID:
	<ea979d70801301252r3f383d28k163d37a125e4c437@mail.gmail.com>
Content-Type: text/plain; charset=ISO-8859-1

I got Bob's code running!
Here it is for all nineteen rooms:

#!/usr/bin/python
# 2008-01-30
# bob gailer [Tutor]
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

# Table of Rooms
rooms = [
      Room([0,2,0,0,0,0,0]),    # 1 Hallway
      Room([1,3,3,0,0,0,0]),    # 2 Audience Chamber
      Room([2,0,5,2,0,0,0]),    # 3 Great Hall
      Room([0,5,0,0,0,0,0]),    # 4 Private Meeting Room
      Room([4,0,0,3,15,13,0]),  # 5 Inner Hallway
      Room([0,0,1,0,0,0,0],False),  # 6 Entrance (Not Updatable)
      Room([0,8,0,0,0,0,0]),    # 7 Kitchen
      Room([7,10,0,0,0,0,0]),   # 8 Store Room
      Room([8,8,8,8,8,8,0]),    # 9 Lift
      Room([8,0,11,0,0,0,0]),   #10 Rear Vestibule
      Room([0,0,10,0,0,0,0],False), #11 Exit (Not Updatable)
      Room([0,0,0,13,0,0,0]),   #12 Dungeon
      Room([0,0,12,0,5,0,0]),   #13 Guardroom
      Room([0,15,17,0,0,0,0]),  #14 Master Bedroom
      Room([14,0,0,0,0,5,0]),   #15 Upper Hall
      Room([17,0,19,0,0,0,0]),  #16 Treasury
      Room([18,16,0,14,0,0,0]), #17 Chambermaid's Bedroom
      Room([0,17,0,0,0,0,0]),   #18 Dressing Chamber
      Room([9,0,0,16,0,0,0])]   #19 Small Room

# note I omitted the initial treasure value since it is always 0
# use random.sample to create random subsets of values and rooms
# - eliminates all the loops and tests
# note this ensures no duplicate treasures (do you want that?)

# create list of 8 random treasure values
values = random.sample(range(10,110),4) + random.sample(range(-4, 0),4)
print " values:",values

# create list of 8 randomly selected updatable rooms
roomsToUpdate = random.sample([room for room in rooms if room.updatable], 8)
print "8 rooms:",roomsToUpdate

# update the rooms' Treasures
for room, value in zip(roomsToUpdate, values):
 room.updateTreasure(value)

a = range(1,99)
for room in (3,15):
 rooms[room].updateTreasure(100 + random.choice(a))

for room in rooms:
    print room
# end code ################################


On Jan 30, 2008 2:24 PM, bob gailer <bgailer@alum.rpi.edu> wrote:
> bhaaluu wrote:
> > #             N S E W U D T
> > travelTable=[[0,2,0,0,0,0,0],    # ROOM 1
> >              [1,3,3,0,0,0,0],    # ROOM 2
> It is good to finally see that you are building an adventure game.
>
> Consider creating a instance of a Room class for each room and saving
> them in a collection such as a list.
>
> This will give you much more flexibility as your game grows.
>
> Inevitably I wound up doing a bunch of things more "Pythonically"
so
> there may be stuff here you don't relate to yet. But is is all worth
> studying and will save you hours of headache later.
>
>[code snipped - see at top]
>
> Things I did not do, but suggest:
> - store the room destinations in a text file rather than hard-coding
> them in the program. It is almost always a good idea to separate logic
> from data.
>
>  -create a Treasure class, storing instances directly in roo,s rather
> than indexes, and storing treasure definitions in the text file.
>
> -store room instances in the destinations rather than indexes.
>
> At this point you no longer need indexes!
>
> --
> Bob Gailer
> 919-636-4239 Chapel Hill, NC
>
>

Thanks!
Happy Programing!
"""