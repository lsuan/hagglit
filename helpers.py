from collections import defaultdict
from datetime import datetime, date, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from artist import Artist
from to1member import TO1Member
from projects import Project

def is_new_day(d: datetime):
  return date.today() > d

def get_index_for(sheet: gspread.Worksheet):
  sheet_values = sheet.get_values()
  
  row = 1
  for sv in sheet_values:
    if sv[0] == "":
      break
    row += 1

  return row

def get_record_row(sheet_values, first_attr):
  row = 2
  for i in range(0, len(sheet_values)):
    if str(sheet_values[i][0]) == first_attr:
      row = i+1
      break
  return row

# first_attr is the first attribute of the worksheet; the identifier
def update_db(sheet: gspread.Worksheet, first_attr, col, value):
  sheet_values = sheet.get_values(value_render_option="UNFORMATTED_VALUE")
  row = get_record_row(sheet_values, first_attr)
  sheet.update_cell(row, col, value)

# def _insert(sheet: gspread.Worksheet, col, value):
#   sheet_values = sheet.get_all_values()
#   empty_cell_row = len(sheet_values)
#   sheet.update_cell(empty_cell_row, col, value)

# cols is a list of letters A-Z that correspond to the spreadsheet
def batch_update(sheet: gspread.Worksheet, row, cols, values):
  cell_range_list = [col + str(row) for col in cols]
  cell_range = cell_range_list[0] + ":" + cell_range_list[-1]
  cells = sheet.range(cell_range)
  
  for i in range(len(cells)):
    cells[i].value = values[i]
  
  sheet.update_cells(cells)

def initialize_db():
  scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
  credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
  client = gspread.authorize(credentials)
  
  test = client.open("Test Database")
  live = client.open("Database")

  # sheet = client.create("Test Database")
  # sheet.share('Haggethers@gmail.com', perm_type='user', role='writer')
  return live

def initialize_to1():
  members_sheet = SHEET_DB.get_worksheet(0)
  members_records = members_sheet.get_all_records()
  to1_members = {}

  for member in members_records:
    to1_members[member["name"]] = TO1Member(member["name"], member["emoji"], member["embed_color"], member["image"])
  
  return to1_members

def initialize_artists():
  artists_records = ARTISTS_SHEET.get_all_records(default_blank="", value_render_option="UNFORMATTED_VALUE")
  collections_records = COLLECTIONS_SHEET.get_all_records(value_render_option="UNFORMATTED_VALUE")

  artists = {}
  artists_ids = {}
  for artist in artists_records:
    counter = None
    if artist["id"] != "":
      if artist["daily_counter"] == "":
        counter = 0
      else:
        counter = artist["daily_counter"]
      artists[artist["name"]] = Artist(str(artist["id"]).lower(), artist["stage_name"], counter, artist["last_daily_log"])
      artists_ids[str(artist["id"]).lower()] = artist["name"]

  for artist in artists.values():
    ldl = artist.get_last_daily_log()
    if ldl != "" and is_new_day(ldl):
      update_db(ARTISTS_SHEET, artist.get_id(), 4, 0)

  artists_collections = defaultdict(list)
  
  for cr in collections_records:
    if cr["date_received"] != "":
      artists_collections[str(cr["aid"])].append( (cr["member_name"], datetime.strptime(cr["date_received"], "%m/%d/%y").date()) )

  for id, collection in artists_collections.items():
    artist_name = artists_ids[id]
    artists[artist_name].set_daily_collection(collection)  

  return artists

def initialize_projects():
  project_records = PROJECTS_SHEET.get_all_records(value_render_option="UNFORMATTED_VALUE")
  projects = {}

  for project in project_records:
    artist_names = set(project["group_members"].split(","))
    artist_names_keys = set(ARTISTS.keys())
    group_members = list(artist_names.intersection(artist_names_keys))
    platform_emojis = project["platforms"].split("+")
    projects[project["id"]] =  \
      Project(project["id"], project["title"], project["leader"], project["category"], project["is_group"], project["release_date"], platform_emojis, group_members)
  
  return projects


# DB GLOBALS
SHEET_DB = initialize_db()
ARTISTS_SHEET = SHEET_DB.get_worksheet(1)
COLLECTIONS_SHEET = SHEET_DB.get_worksheet(2)
PROJECTS_SHEET = SHEET_DB.get_worksheet(3)
# GROUPS_SHEET = SHEET_DB.get_worksheet(4)

# DB INDEX GLOBALS (for insert methods)
COLLECTIONS_INDEX = get_index_for(COLLECTIONS_SHEET)
PROJECTS_INDEX = get_index_for(PROJECTS_SHEET)
# GROUPS_INDEX = get_index_for(GROUPS_SHEET)

# CLASS GLOBALS
TO1_MEMBERS = initialize_to1()
ARTISTS = initialize_artists()
PROJECTS = initialize_projects()