from socket import *
from datetime import datetime
import base64
import sys

now = datetime.now()
now_string = now.strftime("%H:%M:%S")

class smtpClientClass: # This class contains all the useful smtpClient functions

    # Class declaration: holds a socket for the connection.
    def __init__(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

    # smtpClient begins the connection with the server.
    def smtpClient(self, serverMachine, portNumber):
        # Connects to smtp.bgsu.edu: use port 25 to connect.
        print("almost connected")
        self.clientSocket.connect((serverMachine, portNumber)) 
        print("connected")

        # Receives and decodes the greeting, then prints it.
        serverGreeting = self.clientSocket.recv(1024).decode()
        print(serverGreeting)

        # Sends greeting back to server.
        greeting = "HELO brywhit-UBUNTU\r\n"
        # Verification that greeting is correct.
        print(greeting)
        self.clientSocket.send(greeting.encode())
        print("Sent greeting")
        # Receives server response, then prints it for user to read.
        serverResponse = self.clientSocket.recv(1024).decode()
        print("Received response")
        print(serverResponse)
        print("Connection is open.")

    # senderAndReceiver sets the receiver and sender for the current message.
    def senderAndReceiver (self, sender, receiver):
        # Sends a MAIL FROM message to server indicating that you would like to send mail from sender's email address.
        self.clientSocket.send(f'MAIL FROM: <{sender}>\r\n'.encode())
        print("Mail command sent.")
        response = self.clientSocket.recv(1024).decode()
        print("Response received.")
        print(response)
        # Sends a RCPT TO message to server indicating the receiver's email address.
        self.clientSocket.send(f"RCPT TO: <{receiver}>\r\n".encode())
        print(self.clientSocket.recv(1024).decode())

    # addAttachment is used within messageBody if an option attachment is indicated.
    def addAttachment(fileName, encodedContent):	
        
        fileAttachment = f"""{encodedContent}\r\n\r\n"""
        
        return fileAttachment

    # messageBody sends a data command to the server to let the server know what the data of the message is.
    def messageBody (self, sender, receiver, message, fileName="", encodedContent=""):
        # Send the initial DATA command to the server.
        self.clientSocket.send("DATA\r\n".encode())
        response = self.clientSocket.recv(1024).decode()
        print(response)
        fileAttachment = ""
        contentType2 = ""
        contentDis = ""
        # Actual data to send
        subject = "Subject: Test of SMTP Client\r\n"
        ToMsg = f"To: {receiver}\r\n"
        data =  f"{message}\r\n\r\n"
        if (fileName != ""):
            fileAttachment = smtpClientClass.addAttachment(fileName, encodedContent)
            contentType2 = "Content-Type: text/plain;\r\n"       
            contentDis = f"""Content-Disposition:attachment; filename="{fileName}"\r\n\r\n"""
        
        endmsg = "\r\n.\r\n"

	# MIME HEADER INFORMATION USED FOR ATTACHING TXT FILES
        mimeCont = "MIME-Version: 1.0\r\n"
        contentType = f"""Content-Type: multipart/mixed; boundary="BOUNDTEXT"\r\n"""
        boundary1 = "--BOUNDTEXT\r\n"
        contentType3 = f"Content-type: text/plain\r\n\r\n"
        boundary2 = "--BOUNDTEXT--\r\n"

        # Send the data to the server.
        self.clientSocket.send(subject.encode())
        self.clientSocket.send(ToMsg.encode())
        self.clientSocket.send(mimeCont.encode())
        self.clientSocket.send(contentType.encode())
        self.clientSocket.send(boundary1.encode())
        self.clientSocket.send(contentType3.encode())
        self.clientSocket.send(data.encode())
        if fileName != "":
            self.clientSocket.send(boundary1.encode())
            self.clientSocket.send(contentType2.encode())
            self.clientSocket.send(contentDis.encode())
            self.clientSocket.send(fileAttachment.encode())
        self.clientSocket.send(boundary2.encode())
        self.clientSocket.send(endmsg.encode())
        print(self.clientSocket.recv(1024).decode())

    # endTheSession closes the connection and closes the socket.
    def endTheSession (self):
        # Send a QUIT message to the server to let the server know client is done.
        self.clientSocket.send("QUIT\r\n".encode())
        print(self.clientSocket.recv(1024).decode())
        self.clientSocket.close()
        del self
        
print("collect args")
serverMachine = sys.argv[1] # Use smtp.bgsu.edu.
portNO = int(sys.argv[2]) # Use port 25.
senderEmail = sys.argv[3] # USE YOUR EMAIL ONLY. CRIME IF NOT.
rcvEmail = sys.argv[4] # Receiver email.
emailText = sys.argv[5] # Body of the email.
emailFileAttachment = "" # Declaration of emailFileAttachment. Optional.
if (len(sys.argv) == 7): # If the attachment exists, then it will assign emailFileAttachment with the name.
    emailFileAttachment = sys.argv[6]

client = smtpClientClass() # Client initialization.
encodedContent = "" # Encoded content of the file for it to be sent. Optional.
if (emailFileAttachment != ""): # If emailFileAttachment exists, open the file and encode the file in base64.
    openFile = open(emailFileAttachment, "r")
    encodedContent = openFile.read()
    print(encodedContent)

# Function calls.
print("About to call client")
client.smtpClient(serverMachine, portNO)
client.senderAndReceiver(senderEmail, rcvEmail)
client.messageBody(senderEmail, rcvEmail, emailText, emailFileAttachment, encodedContent)
client.endTheSession()


