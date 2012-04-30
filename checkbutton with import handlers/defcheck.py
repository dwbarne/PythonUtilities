def checkButtonHandler(self):
    self.doNotSend=self.var.get()
    if self.doNotSend:
        print "\nINFO: email will NOT be sent to your inbox"
    else:
        print "\nINFO: email will be sent to your inbox"
    