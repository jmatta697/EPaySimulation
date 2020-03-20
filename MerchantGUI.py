import tkinter


class UserWindow:
    def __init__(self):
        self.window = None
        self.label1 = None
        self.text_entry = None
        self.selectRadButton1 = None
        self.selectRadButton2 = None

    def setup(self):
        self.window = tkinter.Tk()
        self.window.title("JPay Merchant")
        self.window.geometry('300x300')

        self.label1 = tkinter.Label(self.window, text="Welcome to JPay Merchant\n\nSelect a transaction type:",
                                    font=("Arial Bold", 12))
        self.label1.place(x=0, y=0)

        self.text_entry = tkinter.Entry(self.window, width=12)
        self.text_entry.place(x=40, y=150, width=125, height=25)

        self.selectRadButton1 = tkinter.Radiobutton(self.window, text='Charge', value=1)
        self.selectRadButton1.place(x=40, y=75, width=100, height=25)

        self.selectRadButton1.select()

        self.selectRadButton2 = tkinter.Radiobutton(self.window, text='Refund', value=2)
        self.selectRadButton2.place(x=40, y=100, width=100, height=25)

    def run(self):
        self.window.mainloop()
        # start



def main():
    user_window = UserWindow()
    user_window.setup()
    user_window.run()


if __name__ == '__main__':
    main()
