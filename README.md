# WhatsApp Personal Message Automation (WAPMA)

*WAPMA is still a Work In Progress.*

A desktop application for sending bulk personal messages in WhatsApp Web
automatically. It utilises the Tkinter library for its desktop GUI and Selenium
library for its automation.

## Platform
Any desktop that can run Python and Bash.

## How does it work?
It uses Selenium library to search certain HTML elements and do actions on them.

## What does it do?
It sends bulk personal and personalized messages for groups that the user are a part of by iterating each member of the group.

## What does it do, after "run"?
1. Open Chrome/Firefox
2. Open WhatsApp Web
3. Wait for succesfull login by QR code
4. Search for the destined group name
5. Enter the destined group
6. Open the group info (Now it only works until here, the next steps are programmed but doesn't work yet)
7. Open the "View all (xx more)"
8. Open the first/next user and save his/her name
9. Write the personalized message with the user's first name
10. Send the message
11. Redo step 4 to 7
12. Move the cursor one user column width, if the user is the last on the screen, scroll instead moving the cursor
13. Redo step 8 to 12 until the sender's user is the one below the cursor
