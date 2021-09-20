import os
from os import path
from  zipfile import ZipFile
import shutil
import json
import random
from git import Git, Repo
import requests


REPO = None

PATH = path.abspath(path.relpath("."))
PROJECTS_DIR = PATH + "/Projects"

def refresh(first_commit = False):
	""" checks for untracked files and adds them to the repo then fetches and checks for changes """
	print("\nRefreshing Git Repo...")
	files = []
	for base, _, in_files in os.walk(PATH):
		for file in in_files:
			if ".git" not in base and "__pycache__" not in base:
				file = base.replace(PATH, "") + "/" + file
				files.append(os.path.join(base, file))
				
				
				
	if len(REPO.untracked_files) > 0:
		print(REPO.untracked_files, "untracked")
	REPO.git.add(all=True)
	i = len(REPO.untracked_files)
	#i = 0
	#for file in files:
	#	if file in REPO.untracked_files:
	#		#print("New", PATH+file)
	#		REPO.index.add(PATH + file)
	#		i += 1
		#else:
			#REPO.index.add(PATH + file)
			
			
	
	print("Repo Refreshed\n")
	if i > 0:
		print(i, "Untracked Files added to tracking")
	diffs = []
	if not first_commit:
		diffs = REPO.index.diff("HEAD")
	if len(diffs) > 0:
		print_diffs = input(str(len(diffs)) + " Differences, print y/N")
		if print_diffs.lower() == "y":
			for i, diff in enumerate(diffs):
				print(i, diff)
				cont = input("Continue Y/n/s")
				if cont.lower() == "s":
					break
				if cont.lower() == "n":
					return
		REPO.git.add(all=True)
		com = input("Commit message (n to cancel): ")
		if com.lower() != "n":
			REPO.index.commit(com)
		if len(REPO.remotes) > 0:
			p = input("Push to remote Y/n: ")
			if p.lower() == "n":
				return
			else:
				push_source()
	if first_commit:
		REPO.index.commit("Initial Commit")
	


def start_all_default_projects():
	""" Starts all the projects it the default projects file """
	
	if path.exists(PROJECTS_DIR + "/DefaultProjects.json"):
		with open(PROJECTS_DIR + "/DefaultProjects.json") as f:
			string = ""
			for line in f:
				string+= line + "\n"
		projects = json.loads(string)["Projects"]
		for project in projects.keys():
			print(project)
			i = projects[project]
			portfolio.new_proj(title=project, description=i["description"], category=i["category"], subcategory=i["subcategory"])
			
	else:
		with open(PROJECTS_DIR + "/DefaultProjects.json", "w") as f:
			f.write(json.dumps({"Projects":{"title":{"category":"", "subcategory":"", "description":""}}}, indent = 4))

def init():
	""" Initialises the portfolio if unpacked or loads it if its initialised"""
	global REPO
	if not path.exists(PATH + "/.git"):
		git_init = input("Initialise Git: Y/n")
		if git_init.lower() != "n":
			REPO = Repo.init(PATH)
			refresh(True)
	
	if not path.exists(PROJECTS_DIR):
		print("First Time Setup")
		
		with ZipFile('Portfolio.zip', 'r') as zip_f:
			zip_f.extractall(PATH)
			
		os.mkdir("init")
			
		original = PATH + "/main.py"
		target = PATH + "/init/main.py"

		shutil.copyfile(original, target)
			
		original = PATH + "/Portfolio.zip"
		target = PATH + "/init/Portfolio.zip"

		shutil.copyfile(original, target)
		os.remove("Portfolio.zip")
		init()
		start_all = input("Start All Default Projects y/N")
		if start_all.lower() == "y":
			start_all_default_projects()
		
	else:
		print("Loading Portfolio")
		REPO = Repo(PATH)
		refresh()
		
		
def save_portfolio():
	""" Saves the portfolio to disk """	
	portfolio.save()
	
def load_portfolio():
	""" Loads the portfolio from disk """
	portfolio.load()
	
def list_projects(started = True, implemented = False):
	""" prints a list of your projects

if started == True it will only show started projects """
	print("\nProjects:")
	for i, project in enumerate(portfolio.projects["Projects"].keys()):
		if implemented and len(portfolio.get(list(portfolio.projects["Projects"].keys())[i]).implementations.keys()) > 0:
			print(project)
		if not implemented:
			print(project)
	print()
	
def check_connection():
	url = "http://www.google.com"
	timeout = 5
	try:
		requests.get(url, timeout=timeout)
		print("Connected")
		return True
	except (requests. ConnectionError, requests. Timeout) as exception:
		print("No Internet Connection")
		return False
		
	
def remove_project(title):
	""" deletes a project and all its implementations then refreshes """
	project = portfolio.get(title)
	if project is None:
		print("Project Not Found")
		return
		
	ays = input(f"Are you sure? this will delete {title} y/N: ")
	if ays.lower() == "y":
		
		shutil.rmtree(project.path)
		print(f"Deleted {title}")
		portfolio.projects["Projects"].pop(title)
		portfolio.save()
	
def fetch_source():
	""" fetches source from remote repo """
	if not check_connection():
		return
	REPO.remote().fetch()
	
def pull_source():
	""" pull the source from remote overwriting changes """
	if not check_connection():
		return
	fetch_source()
	REPO.remote().pull()
	
def push_source():
	""" pushes the source to remote """
	if not check_connection():
		return
		
	if not has_remote():
		REPO.create_remote("origin", input("Remote URL"))
	REPO.git.add(all=True)
	REPO.index.commit("Commit")
	print("Pushing to remote...")
	REPO.remote().push()
	
def start(title):
	""" if title exists it will ask for a language to implement for the existing project and attempts to create an implementation

else it asks for category, subcategory and creates a meta project.

it then will refresh the portfolio push and save """
	if title in manager.pm.Loaded_Projects.keys():
		lang = input(title + " started. What language would you like to implement?\n0 - cancel\n1 - C\n2 - C#\n3 - C++\n4 - Java\n5 - Kotlin\n6 - Python\n7 - R\n8 - Swift\n9 - Web: HTML, CSS, JS ")
		if lang.lower() in ("1", "c"):
			lang = "C"
		elif lang.lower() in ("2", "c#"):
			lang = "C#"
		elif lang.lower() in ("3", "c++"):
			lang = "C++"
		elif lang.lower() in ("4", "java"):
			lang = "Java"
		elif lang.lower() in ("5", "kotlin"):
			lang = "Kotlin"
		elif lang.lower() in ("6", "python"):
			lang = "Python"
		elif lang.lower() in ("7", "r"):
			lang = "R"
		elif lang.lower() in ("8", "swift"):
			lang = "Swift"
		elif lang.lower() in ("9", "html", "css",  "js", "web"):
			lang = "Web"
		else:
			return
		proj = portfolio.get(title)
		proj.new_imp(languages=lang)
		print(f"Language: {lang}")
		portfolio.save()
		return
	else:
		print("Title:", title)
		cat = input("Category: ")
		sub = "/" +input("Subcategory: ") + "/"
		desc = input("Description: ")
		portfolio.new_proj(title=title, category = cat, subcategory=sub, description=desc)
		portfolio.save()
		start(title)
		return
	
def cmd():
	""" input loop that digests commands so you can call the other functions

commands:



Start *Title*

start a project leave title blank to load from file



Delete *Title*

removes project with matching title



refresh

manually refresh the portfolio 

save
manually save the portfolio

task
randomly selects a project from rossetacode and launches it in the browser

random
randomly selexts a project from default projects"""
	cstart = "\033[4m\033[" #escape character
	end = "\033[0m" #escape sequence end
	
	help_string = f"\n{cstart}32mStart [project title]{end}\nstarts a new project / implementation\n{cstart}31mDelete [project title]{end}\ndeletes the project\n{cstart}32mRandom{end}\nStarts a random project\n{cstart}32mTask{end}\nStarts a random Rosetta Code programming task\n{cstart}33mList{end}\nLists all projects\n{cstart}33mSave{end}\nSaves the project\n{cstart}33mRefresh{end}\nManually refreshes the portfolio\n{cstart}34mFetch{end}\nFetches the remote via git\n{cstart}34mPush{end}\nPushes to the remote via git\n{cstart}34mPull{end}\nPulls from the remote via git\n{cstart}31mExit/QQ/Quit{end}\nExit the Portfolio Manager\n"
	print(help_string)
	while True:
		in_string = input("Portfolio Manager: ")
		command = in_string.split(" ")
		
		if type(command) == list:
			args = list(command[1:])
			command = command[0]
		else:
			args = []
		
		lower = command.lower()
		if lower in ("quit", "qq", "exit"):
			break
		#print("Command", command, "Arguments", args)
		
		if lower == "help":
			print(help_string)
			
		
		elif lower == "task":
			random_project(False)
			
		elif lower == "random":
			random_project(True)
		
		elif lower == "start":
			if args != []:
				title = ""
				for arg in args:
					title += arg + " "
					
				start(title[:-1])
			else:
				print("Title Required. Syntax start -project title-")
				
		elif lower == "delete":
			if args != []:
				title = ""
				for arg in args:
					title += arg + " "
					
				remove_project(title[:-1])
			else:
				print("Title Required. Syntax delete -project title-")
		
		elif lower == "refresh":
			refresh()
			
		elif lower == "push":
			push_source()
			
		elif lower == "pull":
			pull_source()
			
		elif lower == "fetch":
			fetch_source()
		
		elif lower == "save":
			save_portfolio()
			
		elif lower == "list":
			list_projects()
			
		elif lower != "":
			print("Command {command} not found. type help for a list of commands.")

def has_remote():
	return len(REPO.remotes) > 0

def random_project(default = True):
	""" randomly selects a project from rossetacode and launches it in the browser"""
	if not default:
		with open(PATH+"/Projects/Tasks.Json") as f:
			tasks = ""
			for line in f:
				tasks += line + "\n"
			tasks = json.loads(tasks)
		print("Selecting random project from", len(tasks.keys()), "Rosseta Code programming tasks")
		
		choice = ""
		while choice.lower() != "y":
			r = random.randint(0, len(tasks.keys()) - 1)
			title = list(tasks.keys())[r]
			link = tasks[title]
			print(title)
			print(link)
			choice = input("Create Project? y/N/s ")
			if choice.lower() == "s":
				return
			
		
		title = input("Project Name: ")
		portfolio.new_proj(title=title, category="Tasks", subcategory="/", description="RossetaCode task, more info at {link}")
		refresh()
	else:
		with open(PROJECTS_DIR + "/DefaultProjects.json") as f:
			string = ""
			for line in f:
				string+= line + "\n"
		projects = json.loads(string)["Projects"]
		choice = ""
		print("Selecting random project from", len(projects.keys()), "Default Projects")
		while choice.lower() != "y":
			r = random.randint(0, len(projects.keys()) - 1)
			project = list(projects.keys())[r]
			desc = projects[project]["description"]
			cat = projects[project]["category"]
			sub = projects[project]["subcategory"]
			print(cat, "/" ,sub[1:-1],"/", project)
			choice = input("Create Project? y/N/s ")
			if choice.lower() == "s":
				return
		portfolio.new_proj(title=project, category=cat, subcategory=sub, description= desc)

init()
import PortfolioManager as manager
portfolio = manager.pf

cmd()
refresh()
save_portfolio()
