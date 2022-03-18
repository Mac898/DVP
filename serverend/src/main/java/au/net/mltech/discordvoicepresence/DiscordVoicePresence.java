package au.net.mltech.discordvoicepresence;

import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitRunnable;
import org.bukkit.scheduler.BukkitTask;

public final class DiscordVoicePresence extends JavaPlugin {

    private WSClient ws;

    BukkitTask task = new BukkitRunnable() {
        public void run() {

        }
    }.runTaskTimer(this,1000, 40);

    @Override
    public void onEnable() {
        // Plugin startup logic
        ws = new WSClient(this);
        getServer().getPluginManager().registerEvents(new EventHandle(), this);
    }

    @Override
    public void onDisable() {
        // Plugin shutdown logic
    }
}
