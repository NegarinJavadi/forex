const io = require('socket.io-client');

const socket = io('wss://marginalttdemowebapi.fxopen.net:3000');


socket.on('connect', () => {
    console.log('WebSocket connection opened');
    // Send authentication message
    socket.emit('authenticate', {
        id: 'd8312554-8085-43f5-aadd-884a035a80e0',
        key: 'TdF4W5RXMHhqeF9B',
        secret: 'x7jfDAwkjenFYmXWnZeFj8anmrzsYbse2P9KPGdEz4WyXN5xd2r5msRy775macyg'
    });
});

socket.on('message', (data) => {
    console.log('Message received:', data);
});

socket.on('error', (error) => {
    console.error('WebSocket error:', error.message);
    console.error('Error details:', error);
});

socket.on('disconnect', (reason) => {
    console.log('WebSocket connection closed:', reason);
});
