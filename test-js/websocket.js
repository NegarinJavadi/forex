const WebSocket = require('ws');

const socket = new WebSocket('wss://marginalttdemowebapi.fxopen.net:3000');

socket.onopen = () => {
    console.log('WebSocket connection opened');
    // Send authentication message
    socket.send(JSON.stringify({
        type: 'authenticate',
        id: 'd8312554-8085-43f5-aadd-884a035a80e0',
        key: 'TdF4W5RXMHhqeF9B',
        secret: 'x7jfDAwkjenFYmXWnZeFj8anmrzsYbse2P9KPGdEz4WyXN5xd2r5msRy775macyg'
    }));
};

socket.onmessage = (event) => {
    console.log('Message received:', event.data);
};

socket.onerror = (error) => {
    console.error('WebSocket error:', error.message);
    console.error('Error details:', error);
};

socket.onclose = (event) => {
    console.log('WebSocket connection closed:', event);
    console.log('Close event code:', event.code);
    console.log('Close event reason:', event.reason);
};
