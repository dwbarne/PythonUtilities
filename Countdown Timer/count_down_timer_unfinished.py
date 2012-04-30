#
# countdown timer
#
# needs more work to get it going, but the guts are here!


                        numberOfChecks=0 
                        numberOfChecksMax=12
                        numberOfSecondsToWait=5
                        waitTime=numberOfChecksMax * numberOfSecondsToWait
                        self.username=self.password=''
# NOTE: This ties up the computer and won't let you 'quit' the main window                       
                        print "\nWaiting for login..."
                        while not self.username and not self.password:
                            if numberOfChecks < 12:
                                print "  ... %3s seconds left" % (waitTime - (numberOfSecondsToWait * numberOfChecks))
                                numberOfChecks+=1
                                time.sleep(5)
                                continue
                            else:
                                print "\nLogin time has expired!\n"
                                self.winLoginBox.quit()
                                return
                        else:
                            try:
                                emailServer.login(self.username,self.password)
                            except smtplib.SMTPException, e:
                                print "\n ERROR: authentication to %s server FAILED!" % key
                                print " ... disconnecting from server. Try again..."
                                emailServer.quit()
                                return
                            else:
                                print ">>> ... successfully connected to %s email server ..." % key