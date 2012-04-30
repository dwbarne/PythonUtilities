from Tkinter import *

master = Tk()

w = Canvas(master, width=220, height=100)
w.pack()

left_bottom_arc=w.create_arc(
	0,90,20,70,
	start=-90,
	extent=90,
	style=ARC,
	outline="red"
	)
left_line=w.create_line(
	20,80,20,20
	)
left_top_arc=w.create_arc(
	20,30,40,10,
	start=90,
	extent=90,
	style=ARC,
	outline="red"
	)

top_line=w.create_line(30,10,170,10)

right_top_arc=w.create_arc(
	160,30,180,10,
	start=90,
	extent=-90,
	style=ARC,
	outline="red"
	)
right_line=w.create_line(
	180,20,180,80
	)
right_bottom_arc=w.create_arc(
	180,90,200,70,
	start=180,
	extent=90,
	style=ARC,
	outline="red"
	)



mainloop()