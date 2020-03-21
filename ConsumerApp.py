import tkinter
from PIL import Image, ImageTk


class UserWindow:
    def __init__(self):
        self.label1 = None
        self.button = None
        self.window = None
        self.text_entry = None
        self.selectRadButton1 = None
        self.selectRadButton2 = None
        self.QRImage = None

    def setup(self):
        self.window = tkinter.Tk()
        self.window.title("JPay")
        self.window.geometry('300x500')

        self.label1 = tkinter.Label(self.window, text="Welcome to JPay\n\nSelect a transaction type:",
                                    font=("Arial Bold", 12))
        self.label1.place(x=0, y=0)

        self.button = tkinter.Button(self.window, text="Pay", command=self.button_clicked,
                                     bg="black", fg="white")
        self.button.place(x=40, y=200, width=120, height=25)

        self.text_entry = tkinter.Entry(self.window, width=10)
        self.text_entry.place(x=40, y=150, width=120, height=25)

        self.selectRadButton1 = tkinter.Radiobutton(self.window, text='Pay', value=1,
                                                    command=self.update_button_text_to_pay)
        self.selectRadButton1.place(x=40, y=75, width=100, height=25)
        self.selectRadButton1.select()
        self.selectRadButton2 = tkinter.Radiobutton(self.window, text='Receive', value=2,
                                                    command=self.update_button_text_to_rec)
        self.selectRadButton2.place(x=40, y=100, width=100, height=25)

        # set up QR code image
        self.QRImage = ImageTk.PhotoImage(Image.open("QR_Code_Images/user_1.png"))
        QRPanel = tkinter.Label(self.window, image=self.QRImage)
        QRPanel.place(x=0, y=250, width=200, height=200)

    def run(self):
        self.window.mainloop()

    def button_clicked(self):
        self.label1.configure(text="button was clicked")

    def update_button_text_to_pay(self):
        self.button.configure(text="Pay")

    def update_button_text_to_rec(self):
        self.button.configure(text="Receive")


def main():
    user_window = UserWindow()
    user_window.setup()
    user_window.run()


if __name__ == '__main__':
    main()
