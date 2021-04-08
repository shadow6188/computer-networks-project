Gerardo Ochoa 
918631875

Project
    Creation of a tcp client and server using socket library.
    Client able to connect to server and interact
    Server has a menu it provides to the client,
    and the client is able to access server features through interacting with server

challenges

    Well my first struggle was figuring out how to communicate back and forth between the client and the server.
    After my first failure I believe I came up with a better idea on how to direct the client what to do from the server.
    After that the first three options were straight forward to implement, I didn't get stuck again until option 4 where I had to figure out how to setup the udp tracker.
    I eventually managed to figure that out in large part thanks to the tracker provided by the proffesor.
    Then I got to option 5 and I had no idea how to approach the encoding and decoding and the advice of of broadcasting to all client handlers makes me think I did not 
    implement option 2 how it was intended. I implemented in such a way that the client handler for the client recieved the message and put it in the recivers list,
    but the advice implies its the reciver's client handler that should have recieved the message and stored it.