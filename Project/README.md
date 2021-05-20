Gerardo Ochoa 
918631875

#Project
Creation of a tcp client and server using socket library.
The client is able to connect & interact with the server.
The server provide services to the client through a menu,
such as sending messages and creating a chat room.

# pictures
![option 1](/Project/pictures/option%201.png)
![option 2](/Project/pictures/option2.png)
![option 4](/Project/pictures/option4.png)
![option 5](/Project/pictures/option5.png)
![option 6](/Project/pictures/option6.png)
![option 7](/Project/pictures/option7+bot%20features.png)
![option 8](/Project/pictures/option8.png)

#challenges

I struggled at a couple places mainly option 4, until the professor provided the udp tracker that made it simpler.
The chat maybe took the longest, because it took me a while to figure out how to erase a line and reprint the contents
of the input buffer. I also got held up on the rsa encryption, spent three weeks fumbling around until I figured out
that I was mistakenly using ed = 1 %n instead of ed = 1 % z. then i got stuck on trying to ping other clients without
extra libraries.