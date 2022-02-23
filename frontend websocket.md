## Server -> Client
1. SETACTIVITY;(assets.large_image);(assets.large_text);(assets.small_image);(assets.small_text);(details);(instance);(party.id);(party.size);(secrets.join);(secrets.match);(secrets.spectate);(state);(timestamps.end);(timestamps.start)
2. GETACTIVITY;
3. SETLOBBY;CREATELOBBY;(int capacity);(bool locked);(int type);
4. SETVOICE;SELFMUTE;(0 or 1)
5. SETVOICE;SELFDAEF;(0 or 1)
6. SETVOICE;LOCALMUTE;(userid);(0 or 1)
7. SETVOICE;LOCALVOLUME;(userid);(0 or 1)
8. GETVOICE;SELFMUTE;
9. GETVOICE;SELFDEAF;
10. GETVOICE;LOCALMUTE;(userid);
11. GETVOICE;LOCALVOLUME;(userid);

## Client -> Server
- INIT;(IP);
- CONNECTED;(Discord User Name#Tag);
- RESPONSEFAIL;(error);
- DISCONNECT;
2. RESPONSEACTIVITY;(assets.large_image);(assets.large_text);(assets.small_image);(assets.small_text);(details);(instance);(party.id);(party.size);(secrets.join);(secrets.match);(secrets.spectate);(state);(timestamps.end);(timestamps.start)
3. RESPONSELOBBYTRANSACTION;(result);(lobby.id);(lobbby.owner_id);(lobby.secret);(lobby.capacity);(lobby.locked)
8. RESPONSEVOICE;SELFMUTE;(bool isMuted);
9. RESPONSEVOICE;SELFDEAF;(bool isDeaf);
10. REPSONSEVOICE;LOCALMUTE;(userid);(bool isMute);
11. RESPONSEVOICE;LOCALVOLUME;(userid);(int volume);