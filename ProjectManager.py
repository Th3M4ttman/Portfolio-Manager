#pylint:disable=C0301
#pylint:disable=W0102

import json
import os
import shutil

from Interplus import interp as I

Loaded_Projects = {}
BASE_PATH = os.path.abspath(os.path.relpath("."))

PROJECT_DIR = BASE_PATH.join("Projects/")
TEMPLATE_DIR = BASE_PATH.join("ProjectTemplate")
LANGUAGES = BASE_PATH +("/ProjectTemplate/Languages.json")


with open(LANGUAGES, "r") as l:
	line = ""
	for li in l:
		line += li
		
LANGUAGES = json.loads(line)
	
#print(LANGUAGES.keys())


class Project():
	"""The project implementation class"""
	def __init__(self, languages = "Python", major = 0, minor = 0, rev = 0, imp = 0):
		
		global Loaded_Projects
		
		self.languages = languages
		self.major = major
		self.minor = minor
		self.rev = rev
		self.version = f"{self.major}.{self.minor}.{self.rev}"
		self.implementation_id = imp
		
		#Loaded_Projects[]
		
		#print(self.version)
	
	def set_ver(self, ver):
		pass
		
	def to_json(self):
		return json.dumps(self.__dict__)
		
	def __repr__(self):
		return f"{self.languages}implementation"
		
	def unpack_templates(self, path):
		if type(self.languages) == list:
			for language in self.languages:
				print("Unpacking", language, "Template")
				if type(language) == str and language in LANGUAGES.keys():
					fromDirectory = LANGUAGES[language] 
					toDirectory = path + "/Source/" + self.languages
					try:
						shutil.copytree(fromDirectory, toDirectory)
					except:
						pass
					return True
				else:
					return  True
					
					#raise Exception("Failed to unpack")
		elif self.languages in LANGUAGES.keys():
			print("Unpacking", self.languages, "Template")
			fromDirectory = LANGUAGES[self.languages]+"/"
			toDirectory = path + "/Source/" + self.languages + "/"
			
			print(toDirectory)
			try:
				shutil.copytree(fromDirectory, toDirectory)
			except:
				return True
			return True
		
	def save(self, path):
		lang = self.languages
		if not os.path.isdir(path + "/Source/"):
			print("Creating Source Folder")
			os.mkdir(path + "/Source/")
		#if not os.path.isdir(path + f"/Source/{lang.replace(',','+')}/"):
			#print("Creating folder for implementation")
			#os.mkdir(path + f"/Source/{lang.replace(',','+')}/")
		return self.unpack_templates(path)
		
class MetaProject():
	"""Composite of projects from different languages"""
	def __init__(self, imp = {}, title = "New Project", description = "A new project.", languages = [], category = "", subcategory = ""):
		global Loaded_Projects
		
		self.implementations = imp
		self.languages = languages
		self.title = title
		self.description = description
		
		Loaded_Projects[self.title] = [self, self.implementations]
		self.category = category
		self.subcategory = subcategory
		self.path = BASE_PATH + "/projects"

		self.path = os.path.abspath(self.path + f"/{self.category}")
		#print(self.path)
		if not os.path.isdir(self.path):
			print(f"Creating category for {self.category}")
			os.mkdir(self.path)
		if type(self.subcategory.split("/")) != str:
			folders = self.subcategory.split("/")
			for i, f in enumerate(folders):
				if i > 0:
					folders[i] = "".join(folders[:i-1]) + "/" + f
			for x, folder in enumerate(folders):
				if not os.path.exists(self.path+ "/".join(folders[:x])):
					print("Creating subcategory for ", folders[:x])
					os.mkdir(self.path+ "/".join(folders[:x]))
					#self.path += folder + "/"
				else:
					pass #self.path += folder
			
			#self.path += self.subcategory
		elif self.subcategory != "" and not os.path.exists(self.path + "/".join(folders)):
			print("Creating subcategory:", self.subcategory)
			self.path += self.subcategory
			os.mkdir(self.path) 
			
			
		self.path = os.path.abspath(self.path + f"{self.subcategory}{self.title}/")
		#print(self.path)
		if not os.path.isdir(self.path):
			print(f"Creating folder for {self.title}")
			print(self.path)
			os.mkdir(self.path)
			
		self.file_path = os.path.abspath(self.path + "/" + self.title + ".proj")
		if not os.path.isfile(self.file_path):
			print(f"Creating Project file for {self.title}")
			self.save()
		else:
			self.load()
		
		
		
	def new_imp(self, languages = "Python"):
		"""Create new implementation"""
		new_lang = ""
		for char in languages:
			new_lang += char
		global Loaded_Projects
		if self.title not in Loaded_Projects.keys():
			print("Project not loaded")
			return False
		elif new_lang in Loaded_Projects[self.title][1].keys():
			print("Language already implemented")
			return False
		elif not os.path.isdir(self.path + "/Source/" + new_lang + "/"):
			print(f"New {new_lang} Implementation")
			new = Project(languages, imp = len(Loaded_Projects[self.title]) + 1)
			Loaded_Projects[self.title][1][new_lang] = new
		else:
			print(new_lang, "Already Implemented")
			return True
			
		
		self.implementations[new_lang] = new.__dict__
		self.languages.append(new_lang)
		self.save()
		if not new.save(self.path):
			print("Failed to unpack")
		return self.implementations[new_lang]
		
		
	def __str__(self):
		return f"{self.title}: {len(self.implementations)} Implementations."
		
	def to_json(self):
		return json.dumps(self.__dict__, indent=3)
		
	def from_json(self, string):
		self.__dict__ = json.loads(string)
		
	def save(self):
		with open(self.file_path, "w") as fout:
			fout.write(self.to_json())
			
	def load(self, v=False):
		with open(self.file_path, "r") as fin:
			string = ""
			for line in fin:
				string += line +"\n"
				
		self.from_json(string)
		if v: print("Loaded", self.title)


"""x = MetaProject()
x.new_imp()
I(globals())"""
