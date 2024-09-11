# from guizero import App, Text, TextBox

# app = App(title="Hello world")

# message = Text(app, text="Enter your name", font="Courier")
# name = TextBox(app)
# name.font = "Courier"



# app.display()

# from guizero import App, PushButton
# def do_start():
#     print("Start button was pressed")
#     startbutton.toggle()
#     stopbutton.toggle()

# def do_stop():
#     print("Stop button was pressed")
#     startbutton.toggle()
#     stopbutton.toggle()

# app = App()
# startbutton = PushButton(app, command=do_start, text='Start')
# stopbutton = PushButton(app, command=do_stop, text='Stop')
# stopbutton.disable()
# app.display()

from guizero import App, ButtonGroup

def clicked():
    print("toggled")
    print(choice.value)

app = App()
choice = ButtonGroup(app, options=["on", "off"], selected="off", command=clicked)
app.display()
