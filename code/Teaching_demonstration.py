import tkinter
import time
 
window = tkinter.Tk()       #实例化object，建立窗口window
window.title('Learn')       #给窗口的可视化起名字

canvas1 = tkinter.Canvas(window, width=700, height=400)
canvas1.pack()

rectangle1 = canvas1.create_rectangle(250, 125, 450, 275, fill="", width=4)
rectangle2 = canvas1.create_rectangle(250, 125, 450, 275, fill="Red")
rectangle3 = canvas1.create_rectangle(450, 125, 650, 275, fill="Blue")
window.update()

rectangle2_left = 250
rectangle3_left = 450
while True:
    time.sleep(0.1)
    canvas1.move(rectangle3, -10, 0)
    canvas1.move(rectangle2, -10, 0)
    rectangle2_left -= 10
    rectangle3_left -= 10
    if rectangle2_left < 50:
        canvas1.delete(rectangle2)
        rectangle2 = canvas1.create_rectangle(440, 125, 650, 275, fill="Red")
        rectangle2_left = 450
    if rectangle3_left < 50:
        canvas1.delete(rectangle3)
        rectangle3 = canvas1.create_rectangle(450, 125, 650, 275, fill="Blue")
        rectangle3_left = 450
    rectangle1 = canvas1.create_rectangle(250, 125, 450, 275, fill="", width=4)
    window.update()

# window.mainloop()