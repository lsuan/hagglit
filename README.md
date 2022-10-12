# hagglit
This is a Private Discord bot for my friends' server. It has some fun and useful commands related to cover projects that we decide to do. Using Google  Sheets to simulate a relational database, this bot can read and write information to our spreadsheet and display messages with Discord Embeds. It also has the functionality to get tweet metrics from Twitter. 

### Tech Used
- Python3
- Discord API <code>discord.py</code>
- Google Sheets API <code>gspread.py</code>
- Twitter API <code>tweepy.py</code>

### Commands
- **~greeting**: randomly returns a member for a daily greeting
- **~collection**: displays a user's greeting history
- **~help**: shows all the commands and their functions
- **~add_project**: adds a project and stores its information to the database
- **~projects**: lists all the projects
- **~get_project_analytics**: gets tweet metrics for a project that was posted on Twitter
- **~menpa**: returns a 'yes' / 'no' / 'ask again' answer
- **~slaygend**: gives the user a random 'slay' percentage

### Summary and Takeaways
- Used <code>discord.py</code> and Discord Objects to access various information for server members, roles, etc.
- Implemented Google Sheets as a database — using <code>gspread</code> library to read and write data
- Extracted information from tweets using <code>tweepy</code> and Twitter API
- Practiced object-oriented design with Python classes
