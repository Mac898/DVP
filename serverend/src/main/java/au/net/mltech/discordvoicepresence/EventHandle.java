package au.net.mltech.discordvoicepresence;

import org.bukkit.event.Listener;
import org.bukkit.event.EventHandler;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;

import java.io.IOException;

public class EventHandle implements Listener {

    @EventHandler
    public void onPlayerJoinEvent(PlayerJoinEvent event) {
        try {
            WSClient.session.getBasicRemote().sendText("PLAYERCONNECTED;");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @EventHandler
    public void onPlayerQuitEvent(PlayerQuitEvent event) {
        try {
            WSClient.session.getBasicRemote().sendText("PLAYERCONNECTED;");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
