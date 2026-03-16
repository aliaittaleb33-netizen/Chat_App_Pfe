<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.min.js"></script>
<script type="text/javascript">
    document.addEventListener('DOMContentLoaded', () => {
        const socket = io.connect('http://127.0.0.1:5000');
        let selectedReceiverId = null;
        let currentRoom = null;

        // Fonction pour rejoindre un salon de chat privé
        function joinRoom(receiverId) {
            // Création d'une salle de discussion unique pour chaque paire d'étudiants
            currentRoom = `private_${sessionStorage.getItem('user_id')}_${receiverId}`;
            socket.emit('join', { room: currentRoom });
        }

        // Fonction pour sélectionner un destinataire
        window.selectReceiver = function(receiverId, username) {
            selectedReceiverId = receiverId;
            document.getElementById('message').placeholder = `Envoyer à ${username}`;
            joinRoom(receiverId); // Rejoindre la salle privée pour cette conversation
            updateChatBoxHeader(username); // Mettre à jour l'en-tête du chat
            clearChatBox(); // Réinitialiser la zone de discussion
        };

        // Fonction pour mettre à jour l'en-tête du chat
        function updateChatBoxHeader(username) {
            const chatBoxHeader = document.getElementById('chat-box-header');
            chatBoxHeader.textContent = `Chat avec ${username}`;
        }

        // Fonction pour réinitialiser la zone de discussion
        function clearChatBox() {
            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML = ''; // Efface tous les messages précédents
        }

        // Fonction pour envoyer un message
        window.sendMessage = function() {
            const messageInput = document.getElementById('message');
            const messageText = messageInput.value.trim();

            if (!selectedReceiverId) {
                alert('Veuillez sélectionner un destinataire.');
                return;
            }
            if (messageText === '') {
                alert('Veuillez entrer un message.');
                return;
            }

            // Envoi du message au serveur
            socket.emit('send_message', {
                message: messageText,
                room: currentRoom,
                receiver_id: selectedReceiverId
            });

            // Ajout du message dans la zone de discussion locale
            displayMessage(`Vous: ${messageText}`);
            messageInput.value = '';
        };

        // Afficher les messages dans la zone de discussion
        function displayMessage(messageText) {
            const chatBox = document.getElementById('chat-box');
            const message = document.createElement('p');
            message.textContent = messageText;
            chatBox.appendChild(message);
            chatBox.scrollTop = chatBox.scrollHeight; // Faire défiler vers le bas automatiquement
        }

        // Écoute de l'événement de réception de message
        socket.on('receive_message', (data) => {
            displayMessage(`${data.sender_id}: ${data.message} (${data.timestamp})`);
        });
    });
</script>
