import tkinter
import QR_Reader
import Merchant_Client_POI


class MerchantUserWindow:
    def __init__(self):
        self.window = None
        self.label1 = None
        self.scan_button = None
        self.text_entry = None
        self.selectRadButton1 = None
        self.selectRadButton2 = None
        self.issuer_response = None

    def setup(self):
        self.window = tkinter.Tk()
        self.window.title("JPay Merchant")
        self.window.geometry('300x300')

        self.label1 = tkinter.Label(self.window, text="Welcome to JPay Merchant\n\nSelect a transaction type:",
                                    font=("Arial Bold", 12))
        self.label1.place(x=0, y=0)

        self.scan_button = tkinter.Button(self.window, text="Scan", command=self.run_qr_reader, bg="black", fg="white")
        self.scan_button.place(x=40, y=200, width=120, height=25)

        self.text_entry = tkinter.Entry(self.window, width=12)
        self.text_entry.place(x=40, y=150, width=125, height=25)

        self.selectRadButton1 = tkinter.Radiobutton(self.window, text='Charge', value=1)
        self.selectRadButton1.place(x=40, y=75, width=100, height=25)

        self.selectRadButton1.select()

        self.selectRadButton2 = tkinter.Radiobutton(self.window, text='Refund', value=2)
        self.selectRadButton2.place(x=40, y=100, width=100, height=25)

    def run(self):
        self.window.mainloop()

    def run_qr_reader(self):
        # set up QR Reader Object - Enter '0' as a parameter to use built-in computer web cam as reader
        qr_reader_obj = QR_Reader.QRReader(0)
        qr_code_return = qr_reader_obj.run_reader()
        print(f'The Merchant App Received >>> {qr_code_return}')
        # send customer EMV data to issuer server
        self.issuer_response = Merchant_Client_POI.initiate_issuer_authorization(qr_code_return)
        # DEBUG
        print(f'issuer server returned >>> {self.issuer_response}')


def main():
    user_window = MerchantUserWindow()
    user_window.setup()
    user_window.run()


if __name__ == '__main__':
    main()
