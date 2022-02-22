on user join to server:
    if user has associated discord id:
        if user has active websocket:
            send ask to join voice chat
        else:
            send ask to download software
    else:
        send ask to link discord
        wait until discord oauth flow has completed and discord id is present
        forward to if loop contents

on user clicks join voice chat command:
    if user is in B&B server:
        if user is in B&B vc:
            move user to appropriate channel for server according to config
            add user to active list
            get local volumes of all active players from this user, store in user object
            get volume of this user from all other current users and store in user object
        else:
            ask user to join AFK
            once user is in B&B VC loop to if
    else:
        send invite link
        once user is in server loop to if

for user on active list:
    if global vc is off:
        get distance of all players in game from player
        if player is out of speaking distance:
            enable local mute
        else if player is within speaking distance:
            scale volume of user by distance with expontential falloff
    else:
        unmute all players that have global mute enabled

on user leaving server:
    set local volumes of all players to normal
    unmute all players
    disconnect user from call


# Handle it with the bukkit api
https://github.com/SpigotMC/Spigot-API/blob/master/src/main/java/org/bukkit/event/player/PlayerJoinEvent.java
https://github.com/SpigotMC/Spigot-API/blob/master/src/main/java/org/bukkit/event/player/PlayerQuitEvent.java

https://hub.spigotmc.org/javadocs/spigot/org/bukkit/scheduler/BukkitScheduler.html
https://www.spigotmc.org/threads/optimizing-bukkit-schedulers-and-less-tick-dependent.363992/