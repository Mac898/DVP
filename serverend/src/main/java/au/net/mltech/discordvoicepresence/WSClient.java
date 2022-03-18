package au.net.mltech.discordvoicepresence;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.concurrent.CountDownLatch;
import java.util.logging.Logger;

import org.glassfish.tyrus.client.ClientManager;

import javax.websocket.*;

@ClientEndpoint
public class WSClient {

    private final DiscordVoicePresence plugin;
    private final Logger logger = Logger.getLogger(this.getClass().getName());
    private final ClientManager client = ClientManager.createClient();
    private static CountDownLatch latch;
    public static Session session;

    public WSClient(DiscordVoicePresence discordVoicePresence) {
        this.plugin = discordVoicePresence;
    }

    public void websocketClient() {
        latch = new CountDownLatch(1);

        try {
            client.connectToServer(WSClient.class, new URI("wss://dvp.mltech.net.au:8443"));
            latch.await();

        } catch (DeploymentException | URISyntaxException | InterruptedException | IOException e) {
            throw new RuntimeException(e);
        }
    }
    @OnOpen
    public void onOpen(Session session){
        logger.info("Connected ... " + session.getId());
        WSClient.session = session;
        try {
            String InitializationDetails = this.plugin.getServer().getIp() + this.plugin.getServer().getPort();
            session.getBasicRemote().sendText("INIT;"+InitializationDetails);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    @OnMessage
    public String onMessage(String message, Session session) {
        BufferedReader bufferRead = new BufferedReader(new InputStreamReader(System.in));

        try {
            logger.info("Received ...." + message);
            return bufferRead.readLine();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    @OnClose
    public void onClose(Session session, CloseReason closeReason) {
        logger.info(String.format("Session %s close because of %s", session.getId(), closeReason));
    }
}