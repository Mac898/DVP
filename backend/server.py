import asyncio, time, os
import websockets
import discord
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, PickleType, Boolean
from dynaconf import settings

# setup
client = discord.Client()
engine = create_engine("sqlite:///test.db")
base = declarative_base()
s = sessionmaker(bind=engine)

#database setup
class User(base):
    __tablename__ = 'userdata'

    id = Column(Integer(), primary_key=True)
    
    frontendip = Column(String(256), unique=False, nullable=False) # Received via websocket packetInit
    minecraftip = Column(String(256), unique=False, nullable=True) # ProxiedPlayer.getAddress().getAddress().getHostAddress()
    
    discordid = Column(String(37), unique=True, nullable=True) # Received via websocket packetUser
    mojangid = Column(String(36), unique=True, nullable=True) # Received via websocketS packetConfirmUser
    
    serverip = Column(String(256), unique=False, nullable=True) # Received via websocketS packetInit
    serverid = Column(String(256), unique=False, nullable=True) # Received via websocketS packetChangeServer
    
    userdistances = Column(PickleType(), unique=False, nullable=True) # Store distance to other mojangids in User model
    
    usermuted = Column(Boolean(), default=False) # Is the user currently muted?
    userdeafened = Column(Boolean(), default=False) # Is the user currently deafened?

    gchat = Column(Boolean(), default=False) # Does the user have global chat enabled?
    installed = Column(Boolean(), defualt=False) # Does the user have the frontend software installed?

    clientqueue = Column(PickleType(), unique=False, nullable=True) #Hold a queue of actions to be executed on the client
    serverqueue = Column(PickleType(), unique=False, nullable=True) #Hold a queue of actions to be executed on the server
    webqueue = Column(PickleType(), unique=False, nullable=True) #Hold a queue of actions to be executed on the web

class HTTPLinks(base):
    __tablename__ = 'httplinks'

    id = Column(Integer(), primary_key=True)
    inputmojangid = Column(String(36), unique=True, nullable=True)
    purpose = Column(String(10), unique=False, nullable=False)
    url = Column(String(256), unique=True, nullable=True)
    resultdiscordid = Column(String(37), unique=True, nullable=True)

# handling websockets
async def handleClientWS(websocket, path):
    packetInit = await websocket.recv()
    init = packetInit.split(";")
    packetUser = await websocket.recv()
    user = packetUser.split(";")
    nUser = User(frontendip = str(init[1]), discordid = str(user[1]))
    s.add(nUser)
    s.commit()
    while True:


async def handleServerWS(websocket, path):
    packetServerInit = await websocket.recv()
    while True:
        

# handling discord
@client.event
async def on_ready():
    print("Bot is online!")

#asyncio setup
clientWS = websockets.serve(handleClientWS, '0.0.0.0', '8080')
asyncio.get_event_loop().run_until_complete(clientWS)
serverWS = websockets.serve(handleServerWS, '0.0.0.0', '8443')
asyncio.get_event_loop().run_until_complete(serverWS)
TOKEN = settings.get("DISCORD_TOKEN")
client.run(TOKEN)