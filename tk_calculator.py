from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import re

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("TkCalc")
        self.textbox_clicked = False
        self.w = 217
        self.h = 207

        self.draw_menus()
        self.draw_gui()

        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (self.w / 2)
        y = (hs / 2) - (self.h / 2)

        self.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

    # def about_window(self):
    #     about mb.showinfo("Information", "msg") #=> 'ok'


    def draw_menus(self):

        # Create the menubar
        menubar = Menu(self)

        appmenu = Menu(menubar, name='apple')
        menubar.add_cascade(menu=appmenu)
        appmenu.add_command(label='About TkCalc', command=lambda: messagebox.showinfo("About TkCalc", "© 2018 - Present orlandodiaz"))
        appmenu.add_separator()

        self.config(menu=menubar)

        # Create the file menu
        file_menu = Menu(menubar)
        menubar.add_cascade(label='File', menu=file_menu)

        # File menu items
        exit_item = file_menu.add_command(label='Exit', command=sys.exit)

    def clear_terminal(self, textbox):
        if not self.textbox_clicked:
            textbox.delete(1.0, END)
            self.textbox_clicked = True
        else:
            return
    def draw_gui(self):
        x = ttk.Style()
        x.configure('padding.TFrame')
        content = ttk.Frame(self, padding=(10, 10))
        content.pack()

        x = ttk.Style()
        x.configure('small.TButton', padding=(-20))

        self.resizable(False, False)
        # result = StringVar()
        text_result = Text(content, background='black', foreground='lime',
                           borderwidth=1, relief='flat', highlightthickness=0,
                           width=25, height=3, padx=10, pady=10, blockcursor=True,
                           insertbackground='lime')
        text_result.insert(INSERT, "Enter expression:")
        text_result.pack()
        text_result.bind('<Key>', lambda _: self.clear_terminal(text_result))
        text_result.bind('<Button-1>', lambda _: self.clear_terminal(text_result))


        text_result.bind('<Return>', lambda _: self.evaluate(
            text_result.get('end-1c linestart', END), text_result))
        text_result.focus()

        for key in ("123", "456", "789", "+-*/", ["=","CLR"]):
            frame = Frame(content)
            frame.pack(expand=NO, fill=X)
            for char in key:
                button = ttk.Button(frame, text=char, style='small.TButton')
                button.pack(expand=YES, side=LEFT, fill=X)
                if char in "123456789+-*/":
                    button.bind('<Button-1>',
                                lambda _, char=char: text_result.insert(INSERT,
                                                                        char))
                elif char == 'CLR':
                    button.bind('<Button-1>', lambda _: text_result.delete(1.0, END))

                elif char == '=':
                    button.bind('<Button-1>',
                                lambda _, char=char: self.evaluate(
                                    text_result.get('end-1c linestart', END),
                                    text_result))


    def evaluate(self, expr, textbox):

        textbox.tag_configure('warning', foreground='red')

        regex = re.findall(r'[a-z]', expr)  # => list of str's

        # Only allow digits and symbols
        if regex:
            textbox.insert(INSERT, '\n>> ' + 'INVALID', 'warning')
            textbox.see(END)
        else:
            # Strip >>
            expr = expr.replace('>>','')

            try:
                result = eval(expr)
                result = str(result)
            except ZeroDivisionError:
                textbox.insert(INSERT, '\n>> ' + 'INVALID: Division by 0', 'warning')
                textbox.see(END)
            except:
                textbox.insert(INSERT, '\n>> ' + 'INVALID', 'warning')
                textbox.see(END)
            else:
                # Insert to textbox
                textbox.insert(INSERT, '\n>> ' + result )
                textbox.see(END)

if __name__ == "__main__":
    app = App()
    app.mainloop()
