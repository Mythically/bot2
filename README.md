# bot2
[WIP] Python twitch chat (currently) commands bot based on TwitchIO with a postgreSQL database, locally hosted on a Raspberry Pi4 Model B. In integration hell. In need of a full rework. 

This was supposed to be a summer project that started for fun, as a means to provide type checking for pokemon and has grown into a full-fledged project.
TODO*: Created: 21/07/2022, Updated: --
 - optimize database usage (reduce total amount of queries to the database, grouping inserts, shceduling / limiting inserts);
 - enable spotify currently-playing feature & obs overlay (related to encryption);
 - add random facts, trivia mini-game, google quick searches, units/currency conversion
 - auto generate commands list & webpage for display
 - website bot with statistics, status & custom custom settings
 - code cleanup & restructuring;
 - end-to-end encryption for collected data and authorizations;
 - automate remote restarts for updated code;
 
*Higher on the list = higher priorty

Development-related learning:
 - Better understanding of asyncio and asyncpg
 - Tunneling
 - WebSockets
 - Encryption
