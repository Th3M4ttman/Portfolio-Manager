#pylint:disable=C0301
#pylint:disable=W0102

import json
import os
from distutils.dir_util import copy_tree

from Interplus import interp as I

Loaded_Projects = {}
BASE_PATH = os.path.abspath("/sdcard/Dev/Portfolio/")
PROJECT_DIR = BASE_PATH.join("Projects/")
TEMPLATE_DIR = BASE_PATH.join("ProjectTemplate")



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
	
	def create_files(self):
		pass
		
	def to_json(self):
		return json.dumps(self.__dict__)
		
	def from_json(self, string):
		pass
		
	def __repr__(self):
		return f"implementation"
		
	def unpack_templates(self, path):
		if type(self.languages) != str:
			for language in self.languages:
				print("Unpacking", language, "Template")
		else:
			print("Unpacking", self.languages, "Template")
		pass
		
	def save(self, path):
		lang = self.languages
		if not os.path.isdir(path + "/Source/"):
			print("Creating Source Folder")
			os.mkdir(path + "/Source/")
		if not os.path.isdir(path + f"/Source/{lang.replace(',','+')}/"):
			print("Creating folder for implementation")
			os.mkdir(path + f"/Source/{lang.replace(',','+')}/")
		self.unpack_templates(path)
		
class MetaProject():
	"""Composite of projects from different languages"""
	def __init__(self, imp = {}, title = "New Project", description = "A new project.", languages = [], category = "Software"):
		global Loaded_Projects
		
		self.implementations = imp
		self.languages = languages
		self.title = title
		self.description = description
		
		Loaded_Projects[self.title] = self.implementations
		self.category = category
		self.path = "/sdcard/Dev/Portfolio/Test"

		self.path = os.path.abspath(self.path + f"/{self.category}/")
		print(self.path)
		if not os.path.isdir(self.path):
			print(f"Creating folder for {self.category}")
			os.mkdir(self.path)
			
		self.path = os.path.abspath(self.path + f"/{self.title}/")
		print(self.path)
		if not os.path.isdir(self.path):
			print(f"Creating folder for {self.title}")
			os.mkdir(self.path)
			
		self.file_path = os.path.abspath(self.path + "/" + self.title + ".proj")
		if not os.path.isfile(self.file_path):
			print(f"Creating Project file for {self.title}")
			self.save()
		
		
		
	def new_imp(self, languages = "Python"):
		"""Create new implementation"""
		new_lang = ""
		for char in languages:
			if char.isalpha():
				new_lang += char
		global Loaded_Projects
		print(f"New {new_lang} Implementation")
		if self.title not in Loaded_Projects.keys():
			print("Project not loaded")
			return False
		elif new_lang in Loaded_Projects[self.title].keys():
			print("Languages already implemented")
			return False
		else:
			new = Project(languages, imp = len(Loaded_Projects[self.title]) + 1)
			Loaded_Projects[self.title][new_lang] = new
			
		
		self.implementations[new_lang] = new.__dict__
		self.languages.append(new_lang)
		self.save()
		new.save(self.path)
		return self.implementations[new_lang]
		
		
	def __str__(self):
		return f"{self.title}: {len(self.implementations)} Implementations."
		
	def to_json(self):
		return json.dumps(self.__dict__, indent=3)
		
	def from_json(self, string):
		pass
		
	def save(self):
		with open(self.file_path, "w") as fout:
			fout.write(self.to_json())
			
	def load(self):
		pass


x = MetaProject()
x.new_imp()
#print(x)
x.new_imp("Kotlin")
print(x.to_json())
I(globals())
