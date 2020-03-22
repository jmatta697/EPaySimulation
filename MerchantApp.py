import tkinter
import QR_Reader
import Merchant_Client_POI


class MerchantUserWindow:
    def __init__(self):
        self.window = None
        self.label1 = None
        self.price_label = None
        self.pin_label = None
        self.scan_button = None
        self.price_text_entry = None
        self.pin_text_entry = None
        self.radioButtonVar = None
        self.chargeRadButton = None
        self.refundRadButton = None
        self.issuer_response = None

    def setup(self):
        self.window = tkinter.Tk()
        self.window.title("JPay Merchant")
        self.window.geometry('300x350')

        self.label1 = tkinter.Label(self.window, text="Welcome to JPay Merchant\n\nSelect a transaction type:",
                                    font=("Arial Bold", 12))
        self.label1.place(x=40, y=0)

        self.price_label = tkinter.Label(self.window, text="Amount:",
                                         font=("Arial Bold", 10))
        self.price_label.place(x=50, y=153)

        self.pin_label = tkinter.Label(self.window, text="Customer PIN:",
                                       font=("Arial Bold", 10))
        self.pin_label.place(x=13, y=205)

        self.scan_button = tkinter.Button(self.window, text="Scan", command=self.run_qr_reader, bg="black", fg="white")
        self.scan_button.place(x=90, y=280, width=120, height=25)

        self.price_text_entry = tkinter.Entry(self.window, width=12)
        self.price_text_entry.place(x=110, y=150, width=125, height=25)

        self.pin_text_entry = tkinter.Entry(self.window, width=12)
        self.pin_text_entry.place(x=110, y=200, width=40, height=25)

        self.radioButtonVar = tkinter.StringVar()

        self.chargeRadButton = tkinter.Radiobutton(self.window, text='Charge', variable=self.radioButtonVar,
                                                   value="charge")
        self.chargeRadButton.place(x=90, y=75, width=100, height=25)

        self.chargeRadButton.select()

        self.refundRadButton = tkinter.Radiobutton(self.window, text='Refund', variable=self.radioButtonVar,
                                                   value="refund")
        self.refundRadButton.place(x=90, y=100, width=100, height=25)

    def run(self):
        self.window.mainloop()

    def run_qr_reader(self):
        # set up QR Reader Object - Enter '0' as a parameter to use built-in computer web cam as reader
        qr_reader_obj = QR_Reader.QRReader(0)
        qr_code_return = qr_reader_obj.run_reader()
        print(f'The Merchant App Received from QR Reader >>> {qr_code_return}')
        # this variable will hold the money amount sent to the issuer
        absolute_price_amount = self.price_text_entry.get()
        # check if refund is being issued - if so add '-' to price to make it negative
        if self.radioButtonVar.get() == 'refund':
            absolute_price_amount = '-' + self.price_text_entry.get()
        # add PIN entry and money amount entry to qr code data to make complete token
        complete_token = qr_code_return + '|'.encode() + self.pin_text_entry.get().encode() + '|'.encode() + \
            absolute_price_amount.encode()
        # send customer EMV data to issuer server
        self.issuer_response = Merchant_Client_POI.initiate_issuer_authorization(complete_token)
        # DEBUG
        print(f'issuer server returned >>> {self.issuer_response}')


def main():
    user_window = MerchantUserWindow()
    user_window.setup()
    user_window.run()


if __name__ == '__main__':
    main()
