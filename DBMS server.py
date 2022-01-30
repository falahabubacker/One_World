import socket, pickle
from _thread import start_new_thread
import mysql.connector as mys
import smtplib
from email.message import EmailMessage

# SOCKET SETUP

# CONSTANTS
BUFFER = 1024
ADDR = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ADDR, PORT))
server.listen(5)

# MySQL Connection
myconn = mys.connect(host=ADDR, user='root', port=3306,
                     passwd='adis', database='oneworld')

mycur = myconn.cursor()

if myconn.is_connected(): print('\n•CONNECTION SUCCESSFUL•')


def handle_client():
    print('[ONLINE AND READY!]')
    while True:
        client, addr = server.accept()

        print(addr[0])

        start_new_thread(request_manager, (client,))


def request_manager(client):
    while True:
        info = pickle.loads(client.recv(1024))
        if info[0] == 'register':
            register(client, info)
        if info[0] == 'login':
            login(client, info)
        if info[0] == 'transfer':
            transfer(client, info[1:])
        if info[0] == 'transactions':
            transactions(client, info)
        if info[0] == 'completeInfo':
            completeInfo(client, info)
        if info[0] == 'announce':
            print(info[1])


def register(client, info):
    try:
        mycur.execute(
            f'INSERT INTO users (username, password, firstname, lastname, emailaddress, phonenumber, balance) VALUES("{str(info[1])}", "{str(info[2])}", "{str(info[3])}", "{str(info[4])}", "{str(info[5])}", {int(info[6])}, 1000);')

        mycur.execute('update users set balance = balance-1000 where username = "oneworld"')

        myconn.commit()

        # email the new user
        email(info[5])

        # register successful message
        client.send(b'v/')

    except Exception as e:
        print(e)
        client.send(b'x/')


def login(client, info):
    try:
        query = "SELECT username, password FROM users;"

        mycur.execute(query)

        rs = mycur.fetchall()  # Record Set

        if tuple(info[1:]) in rs:
            print(f'User: {info[1]} is online')

            query = f"select firstname, balance from users where username = '{info[1]}';"

            mycur.execute(query)
            rs = mycur.fetchall()

            client.send(pickle.dumps(rs))

        else:
            client.send(pickle.dumps('An Error occurred!'))

    except Exception as e:
        print(e)


def transfer(client, info):
    sendUser, recvUser, amt, password = info
    print(sendUser, recvUser, int(amt), password)

    try:
        mycur.execute(f"select username from users;")

        rs = mycur.fetchall()
        print(rs)

        sig = 0
        for i in rs:
            if recvUser in i:
                sig += 1
        if sig == 0:
            print('transaction failed')
            client.send(pickle.dumps(['An error occurred!', 0]))
            return

        mycur.execute(f"UPDATE users SET balance = balance+{amt} where username = '{recvUser}';")
        myconn.commit()

        mycur.execute(f"UPDATE users SET balance = balance-{amt} where username = '{sendUser}';")
        myconn.commit()

        client.send(pickle.dumps(['Transaction successful!', int(amt)]))
        print('Transaction successful!')

        # Update transactions table
        mycur.execute(
            f"insert into transactions (sendUser, recvUser, bankname, amt) values('{sendUser}', '{recvUser}', 'One World', {amt});")
        myconn.commit()

    except Exception as e:
        print(str(e))
        client.send(pickle.dumps(['An error occurred!', 0]))


def transactions(client, info):
    try:
        mycur.execute(f"select * from transactions where sendUser = '{info[1]}' or recvUser = '{info[1]}';")

        rs = mycur.fetchall()

        client.send(pickle.dumps(rs))

    except Exception as e:
        print(e)


def completeInfo(client, info):
    try:
        mycur.execute(f"select firstname, lastname, username, emailaddress from users where username = '{info[1]}'")

        rs = mycur.fetchall()

        client.send(pickle.dumps(rs[0]))
    except Exception as e:
        print(e)


def email(emailAddr):
    EMAIL_ADDRESS = 'selbot6959@gmail.com'
    EMAIL_PASSWORD = 'Telluriumbot'

    msg = EmailMessage()
    msg['Subject'] = 'One World'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = emailAddr

    msg.set_content('')

    msg.add_alternative("""\
    
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
        <head>
        <!--[if gte mso 9]>
        <xml>
          <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
          </o:OfficeDocumentSettings>
        </xml>
        <![endif]-->
          <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <meta name="x-apple-disable-message-reformatting">
          <!--[if !mso]><!--><meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
          <title></title>
          
            <style type="text/css">
              table, td { color: #000000; } @media only screen and (min-width: 520px) {
          .u-row {
            width: 500px !important;
          }
          .u-row .u-col {
            vertical-align: top;
          }
        
          .u-row .u-col-100 {
            width: 500px !important;
          }
        
        }
        
        @media (max-width: 520px) {
          .u-row-container {
            max-width: 100% !important;
            padding-left: 0px !important;
            padding-right: 0px !important;
          }
          .u-row .u-col {
            min-width: 320px !important;
            max-width: 100% !important;
            display: block !important;
          }
          .u-row {
            width: calc(100% - 40px) !important;
          }
          .u-col {
            width: 100% !important;
          }
          .u-col > div {
            margin: 0 auto;
          }
        }
        body {
          margin: 0;
          padding: 0;
        }
        
        table,
        tr,
        td {
          vertical-align: top;
          border-collapse: collapse;
        }
        
        p {
          margin: 0;
        }
        
        .ie-container table,
        .mso-container table {
          table-layout: fixed;
        }
        
        * {
          line-height: inherit;
        }
        
        a[x-apple-data-detectors='true'] {
          color: inherit !important;
          text-decoration: none !important;
        }
        
        </style>
          
          
        
        <!--[if !mso]><!--><link href="https://fonts.googleapis.com/css?family=Montserrat:400,700&display=swap" rel="stylesheet" type="text/css"><link href="https://fonts.googleapis.com/css?family=Pacifico&display=swap" rel="stylesheet" type="text/css"><!--<![endif]-->
        
        </head>
        
        <body class="clean-body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #e7e7e7;color: #000000">
          <!--[if IE]><div class="ie-container"><![endif]-->
          <!--[if mso]><div class="mso-container"><![endif]-->
          <table style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #e7e7e7;width:100%" cellpadding="0" cellspacing="0">
          <tbody>
          <tr style="vertical-align: top">
            <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
            <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #e7e7e7;"><![endif]-->
            
        
        <div class="u-row-container" style="padding: 0px;background-color: #ecf0f1">
          <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 500px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
            <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
              <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: #ecf0f1;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:500px;"><tr style="background-color: transparent;"><![endif]-->
              
        <!--[if (mso)|(IE)]><td align="center" width="500" style="width: 500px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]-->
        <div class="u-col u-col-100" style="max-width: 320px;min-width: 500px;display: table-cell;vertical-align: top;">
          <div style="width: 100% !important;">
          <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]-->
          
        <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
          <tbody>
            <tr>
              <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
                
          <h1 style="margin: 0px; color: #57b8f8; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Pacifico',cursive; font-size: 43px;">
            One World
          </h1>
        
              </td>
            </tr>
          </tbody>
        </table>
        
          <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
          </div>
        </div>
        <!--[if (mso)|(IE)]></td><![endif]-->
              <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
            </div>
          </div>
        </div>
        
        
        
        <div class="u-row-container" style="padding: 0px;background-color: #ecf0f1">
          <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 500px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;">
            <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
              <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: #ecf0f1;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:500px;"><tr style="background-color: #ffffff;"><![endif]-->
              
        <!--[if (mso)|(IE)]><td align="center" width="500" style="width: 500px;padding: 46px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]-->
        <div class="u-col u-col-100" style="max-width: 320px;min-width: 500px;display: table-cell;vertical-align: top;">
          <div style="width: 100% !important;">
          <!--[if (!mso)&(!IE)]><!--><div style="padding: 46px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]-->
          
        <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
          <tbody>
            <tr>
              <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
                
          <div style="line-height: 150%; text-align: left; word-wrap: break-word;">
            <p style="font-size: 14px; line-height: 150%;"><span style="font-family: Montserrat, sans-serif; font-size: 26px; line-height: 39px;">You&rsquo;re now part of one of the world&rsquo;s leading banks. Welcome, we&rsquo;re glad you&rsquo;re here!</span></p>
        <p style="font-size: 14px; line-height: 150%;">&nbsp;</p>
        <p style="font-size: 14px; line-height: 150%;"><span style="font-family: Montserrat, sans-serif; font-size: 26px; line-height: 39px;">We've deposited a credit of 1000 USD for creating this account.</span></p>
        <p style="font-size: 14px; line-height: 150%;">&nbsp;</p>
        <p style="font-size: 14px; line-height: 150%;"><span style="font-family: Montserrat, sans-serif; font-size: 26px; line-height: 39px;">​Happy exploring,</span><br /><span style="font-family: Montserrat, sans-serif; font-size: 26px; line-height: 39px;">One World</span></p>
          </div>
        
              </td>
            </tr>
          </tbody>
        </table>
        
          <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
          </div>
        </div>
        <!--[if (mso)|(IE)]></td><![endif]-->
              <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
            </div>
          </div>
        </div>
        
        
        
        <div class="u-row-container" style="padding: 0px;background-color: #ecf0f1">
          <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 500px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
            <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
              <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: #ecf0f1;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:500px;"><tr style="background-color: transparent;"><![endif]-->
              
        <!--[if (mso)|(IE)]><td align="center" width="500" style="width: 500px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]-->
        <div class="u-col u-col-100" style="max-width: 320px;min-width: 500px;display: table-cell;vertical-align: top;">
          <div style="width: 100% !important;">
          <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]-->
          
        <table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
          <tbody>
            <tr>
              <td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
                
          <div style="line-height: 270%; text-align: left; word-wrap: break-word;">
            <p style="font-size: 14px; line-height: 270%; text-align: center;">​OneWorld, Inc 1600 Amphitheatre Pkwy Mountain View, CA 94043<br />You&rsquo;ve received this email to confirm that you're registered for OneWorld.</p>
          </div>
        
              </td>
            </tr>
          </tbody>
        </table>
        
          <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
          </div>
        </div>
        <!--[if (mso)|(IE)]></td><![endif]-->
              <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
            </div>
          </div>
        </div>
        
        
            <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
            </td>
          </tr>
          </tbody>
          </table>
          <!--[if mso]></div><![endif]-->
          <!--[if IE]></div><![endif]-->
        </body>
        
        </html>
        
    """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


handle_client()
