console.log("Application Loaded");

const loginBtn = document.getElementById('loginBtn');
const logoutBtn = document.getElementById('logoutBtn');
const loginDialog = document.getElementById('loginDialog');
const cancelLogin = document.getElementById('cancelLogin');
const loginForm = document.getElementById('loginForm');
const contentArea = document.getElementById('contentArea');
const guestMessage = document.getElementById('guestMessage');

loginBtn.addEventListener('click', () => loginDialog.showModal());
cancelLogin.addEventListener('click', () => loginDialog.close());

// --- HASHING HELPER ---
async function sha256(message) {
    // 1. Encode the message as an array of bytes
    const msgBuffer = new TextEncoder().encode(message);
    // 2. Hash the bytes using SHA-256
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    // 3. Convert result to a Hex string
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const plainPassword = document.getElementById('password').value;

    try {
        // HASH PASSWORD HERE
        const hashedPassword = await sha256(plainPassword);

        // Send the HASH, not the password
        const response = await fetch('http://localhost:3000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password: hashedPassword })
        });

        const data = await response.json();

        if (data.success) {
            alert("Login Successful!");
            loginDialog.close();
            handleLoginState(true);
        } else {
            alert("Error: " + data.message);
        }
    } catch (err) {
        console.error(err);
        alert("Cannot connect to server");
    }
});

function handleLoginState(isLoggedIn) {
    if (isLoggedIn) {
        contentArea.classList.remove('hidden');
        guestMessage.classList.add('hidden');
        loginBtn.style.display = 'none';
        logoutBtn.style.display = 'inline-block';
        loadGallery();
        initChat();
        initMap();
    } else {
        location.reload();
    }
}
logoutBtn.addEventListener('click', () => handleLoginState(false));

function loadGallery() {
    const galleryGrid = document.getElementById('galleryGrid');
    const images = ['https://picsum.photos/id/101/300/200','https://picsum.photos/id/102/300/200','https://picsum.photos/id/103/300/200','https://picsum.photos/id/104/300/200'];
    galleryGrid.innerHTML = '';
    images.forEach(url => {
        const img = document.createElement('img');
        img.src = url;
        galleryGrid.appendChild(img);
    });
}

function initChat() {
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const socket = new WebSocket('ws://localhost:3000');

    socket.addEventListener('message', (event) => {
        addMessage(event.data, 'server');
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const text = chatInput.value;
            socket.send(text);
            addMessage("You: " + text, 'user');
            chatInput.value = '';
        }
    });

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.innerText = text;
        div.style.textAlign = sender === 'user' ? 'right' : 'left';
        div.style.color = sender === 'user' ? '#5E81AC' : '#BF616A';
        div.style.marginBottom = '5px';
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function initMap() {
    const map = L.map('map').setView([40.64427, -8.64554], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OSM' }).addTo(map);
    const marker = L.marker([40.64427, -8.64554]).addTo(map);
    const geoSocket = new WebSocket('ws://localhost:8000/ws/location');
    geoSocket.addEventListener('message', (event) => {
        const data = JSON.parse(event.data);
        const newLatLng = [data.lat, data.lng];
        marker.setLatLng(newLatLng);
        map.panTo(newLatLng);
    });
}
