#pylint:disable=C0411
#pylint:disable=W0102
import ProjectManager as pm
import os
import json

PATH = os.path.abspath( os.path.relpath("."))

class Portfolio():
	def __init__(self):
		self.save_path = PATH + "/Projects/Projects.json"
		self.projects = {"Projects": {}, "Config": {"Remote": ""}}
		
		if os.path.exists(self.save_path):
			print("Loading Projects File...")
			self.load()
		else:
			print("Creating Projects File...")
			self.save()
			
		self.discover()
		n = self.cleanup()
		if n > 0:
			print(f"Deleted {n} references")
		self.save()
			
	def load(self):
		string = ""
		with open(self.save_path, "r") as fin:
			for line in fin:
				string += line + "\n"
				
		self.projects = pm.json.loads(string)
		print("Loaded")
		
	def save(self):
		with open(self.save_path, "w") as fout:
			fout.write(pm.json.dumps(self.projects, indent=4))
		print("Saved")
		
	def load_project(self, title, category, subcategory):
		x = pm.MetaProject(title=title, category=category, subcategory=subcategory )
		self.projects["Projects"][title] = x.path
		
	def new_proj(self, title = "New Project", description = "A new project.", category = "Software", subcategory = ""):
		pm.MetaProject(title=title, description=description, category=category, subcategory=subcategory)
		
	def discover(self, v = False):
		for base, dirs, files in os.walk(PATH):
			#print("Base",base)
			#print("Dirs",dirs)
			#print("Files",files)
			for file in files:
				if ".proj" in file:
					if file[:-5] not in self.projects:
						if v: print("Discovered", file)
						with open(base + "/" + file, "r") as p:
							proj = ""
							for line in p:
								proj += line + "\n"
							proj = json.loads(proj)
						self.load_project(proj["title"], proj["category"], proj["subcategory"])
					else:
						if v: print("Already Loaded")
						
	def get(self, title, v = False):
		if v: print("Getting", title)
		for proj in pm.Loaded_Projects.items():
			#print(proj)
			if proj[0] == title:
				if v: print("Found")
				return pm.Loaded_Projects[title][0]
		if v: print("Not Found")
		return None
		
	def cleanup(self, notfound = 0, deleted = 0):
		for project, path in self.projects["Projects"].items():
			
			if not os.path.exists(path):
				notfound += 1
				input(f"Project {project} not found. Delete Project Reference Y/n")
				if input not in ("N", "n"):
					self.projects["Projects"].pop(project)
					print("Deleted")
					return self.cleanup(notfound, deleted+1)
				return deleted
					
			else:
				if os.path.exists(path):
					pass
					"""
					with open(path+"/" + project + ".proj", "r") as proj:
						string = ""
						for line in proj:
							string += line + "\n"
					"""
						
				else:
					self.projects.pop(project)
					print(project, "deleted")
		return deleted
		
	def cmd(self):
		print("Commands:\nNew")
		i = (None,)
		while i[0] not in ("qq", "quit", "Quit"):
			 terms = input(">:").split(" ")
			 if not isinstance(terms, tuple):
			 	i = terms
			 else:
			 	i = terms
			 	
			 #print(i)
			 if i[0].lower() == "new":
			 	print("New")
			 else: print(i)
			 
			
		
			
					
		

pf = Portfolio()

