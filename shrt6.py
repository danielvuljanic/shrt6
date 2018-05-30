import sublime
import sublime_plugin
import re

class shrt6Command(sublime_plugin.TextCommand):

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/
#/	MAIN
#/
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	def run(self, edit):
		
		##################
		# USER INPUT
		##################

		# Input elements
		cursorPos 	= self.view.sel()[0].end()
		row,col 	= self.view.rowcol(cursorPos)
		lineInput 	= self.view.substr(self.view.line(cursorPos))[0:col]

		# valid text input?
		shrtInput 	= re.search('(\s)*([\w.-])+$', lineInput)
		if not shrtInput:
			print("no shrt6 command")
			return
		shrtInput = shrtInput.group().lstrip()


		##################
		# SHRT6 COMMANDS
		##################
		
		shrtOutput = self.getShrt6Command(edit,shrtInput)
		if not shrtOutput:
			return


		##################
		# OUTPUT
		##################

		cursorPos = self.view.sel()[0].end()
		self.view.erase(edit,sublime.Region(cursorPos-len(shrtInput), cursorPos))
		self.view.run_command('insert_snippet', {'contents': shrtOutput})



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/
#/	SHRT COMMANDS
#/
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	def getShrt6Command(self, edit, shrtInput):

		# Variables		
		if shrtInput.startswith("cv"):
			return self.createVariable(shrtInput)

		# References
		elif shrtInput.startswith("cr"):
			return self.createVariable(shrtInput,isReference=True)

		# Pointer
		elif shrtInput.startswith("cp"):
			return self.createVariable(shrtInput,isPointer=True)

		# Methods
		elif shrtInput.startswith("cm"):
			return self.createMethod(shrtInput, True)
		elif shrtInput.startswith("dm"):
			return self.createMethod(shrtInput, False)

		# Flow
		elif shrtInput.startswith("cf"):
			return self.createFlow(shrtInput);

		# File Structure
		elif shrtInput.startswith("cs"):
			return self.createStructure(edit,shrtInput);

		# No command
		else:
			return False



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/
#/	VARIABLES / REFERENCES / POINTER
#/
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	def createVariable(self,shrtInput,isReference=False,isPointer=False):

		syntax 		= self.getSyntax()
		parameter 	= self.getParameter(shrtInput)
		shrtInput 	= shrtInput.split(".")[0]		# remove parameter from input
		shrtOutput 	= ""


		#########################
		# DEFAULTS DATA TYPES
		#########################
		
		if len(shrtInput)==2:
			shrtInput = 'cvi'
		elif shrtInput == 'cva':
			shrtInput = 'cvai'
		elif shrtInput == 'cvl':
			shrtInput = 'cvli'
		elif shrtInput == 'cvm':
			shrtInput = 'cvmi'
		

		#########################
		# PARAMETER
		#########################
		
		# Parameter values
		varName 	= False
		varCount 	= 1
		varIndex 	= 1

		# Iterate parameter
		for param in parameter:
			# Multiple Variables
			if self.isInt(param):
				varCount = int(param)
			# Variable name
			elif (len(param)>=2) or param == "i":
				varName = param

		# Reference or Pointer
		if isReference:
			varPrefix = "&"
		elif isPointer:
			varPrefix = "*"
		else:
			varPrefix = ""
			

		#########################
		# INTEGER
		#########################

		if shrtInput[2]=="i":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex)+":myInt"+(str(i+1) if varCount > 1 else "")+"}";
				value = '${'+str(varIndex+1)+':0}'
				shrtOutput += self.setVarOutput(syntax, "c++", "int", varPrefix+name ,value if not isPointer else '${'+str(varIndex+1)+':new int(${'+str(varIndex+2)+'})}')
				shrtOutput += self.setVarOutput(syntax, "javascript" ,"var", name, value)
				shrtOutput += self.setVarOutput(syntax, "java", "int", name, value)
				shrtOutput += self.setVarOutput(syntax, "php", "$", name, value)
				shrtOutput += self.setVarOutput(syntax, "objective-c", "int", name, value)
				shrtOutput += self.setVarOutput(syntax, "python", "", name, value)
				varIndex+=3
		

		#########################
		# UNSIGNED INTEGER
		#########################

		elif shrtInput[2]=="u":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex)+":myUint"+(str(i+1) if varCount > 1 else "")+"}";
				value = '${'+str(varIndex+1)+':0}'
				shrtOutput += self.setVarOutput(syntax,	"c++", "uint", varPrefix+name, value if not isPointer else '${'+str(varIndex+1)+':new uint(${'+str(varIndex+2)+'})}')
				shrtOutput += self.setVarOutput(syntax,	"javascript", "var", name, value)
				shrtOutput += self.setVarOutput(syntax,	"java", "int", name, value)
				shrtOutput += self.setVarOutput(syntax,	"php", "$" , name, value)
				shrtOutput += self.setVarOutput(syntax,	"objective-c", "int", name, value)
				shrtOutput += self.setVarOutput(syntax,	"python", "", name, value)
				varIndex+=3


		#########################
		# FLOAT
		#########################

		elif shrtInput[2]=="f":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex)+":myFloat"+(str(i+1) if varCount > 1 else "")+"}";
				value = '${'+str(varIndex+1)+':0.0}'
				shrtOutput += self.setVarOutput(syntax, "c++", "float", varPrefix+name, value if not isPointer else '${'+str(varIndex+1)+':new float(${'+str(varIndex+2)+'})}')
				shrtOutput += self.setVarOutput(syntax, "javascript", "var", name, value)
				shrtOutput += self.setVarOutput(syntax, "java", "float", name, value)
				shrtOutput += self.setVarOutput(syntax, "php", "$", name, value)
				shrtOutput += self.setVarOutput(syntax, "objective-c", "float", name, value)
				shrtOutput += self.setVarOutput(syntax, "python", "", name, value)
				varIndex+=3


		#########################
		# BOOLEAN
		#########################

		elif shrtInput[2]=="b":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex)+":myBool"+(str(i+1) if varCount > 1 else "")+"}";
				value = '${'+str(varIndex+1)+':false}'
				shrtOutput += self.setVarOutput(syntax,	"c++", "bool", varPrefix+name, value if not isPointer else '${'+str(varIndex+1)+':new bool(${'+str(varIndex+2)+'})}')
				shrtOutput += self.setVarOutput(syntax,	"javascript", "var", name, value)
				shrtOutput += self.setVarOutput(syntax,	"java", "boolean", name, value)
				shrtOutput += self.setVarOutput(syntax,	"php", "$", name, value)
				shrtOutput += self.setVarOutput(syntax,	"objective-c", "bool", name, value)
				shrtOutput += self.setVarOutput(syntax,	"python", "", name, value)
				varIndex+=3


		#########################
		# CHAR
		#########################

		elif shrtInput[2]=="c":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex)+":myChar"+(str(i+1) if varCount > 1 else "")+"}";
				value = '\'${'+str(varIndex+1)+':A}\''
				shrtOutput += self.setVarOutput(syntax, "c++", "char", varPrefix+name, value if not isPointer else '${'+str(varIndex+1)+':new char(${'+str(varIndex+2)+'})}')
				shrtOutput += self.setVarOutput(syntax, "javascript", "var", name, value)
				shrtOutput += self.setVarOutput(syntax, "java", "char", name, value)
				shrtOutput += self.setVarOutput(syntax, "php", "$",  name, value)
				shrtOutput += self.setVarOutput(syntax, "objective-c", "char", name, value)
				shrtOutput += self.setVarOutput(syntax, "python", "", name, value)
				varIndex+=3


		#########################
		# STRING
		#########################

		elif shrtInput[2]=="s":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex)+":myString"+(str(i+1) if varCount > 1 else "")+"}";
				value = '"${'+str(varIndex+1)+':}"'
				shrtOutput += self.setVarOutput(syntax, "c++", "std::string", varPrefix+name, value if not isPointer else '${'+str(varIndex+1)+':new std::string(${'+str(varIndex+2)+'})}')
				shrtOutput += self.setVarOutput(syntax, "javascript", "var", name, value)
				shrtOutput += self.setVarOutput(syntax, "java", "string", name, value)
				shrtOutput += self.setVarOutput(syntax, "php", "$", name, value)
				shrtOutput += self.setVarOutput(syntax, "objective-c", "string", name, value)
				shrtOutput += self.setVarOutput(syntax, "python", "", name, value)
				varIndex+=3


		#########################
		# OBJECT
		#########################

		elif shrtInput[2]=="o":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex+1)+":myObject"+(str(i+1) if varCount > 1 else "")+"}";
				value = '${'+str(1)+':Object}(${'+str(varIndex+3)+'})'
				shrtOutput += self.setVarOutput(syntax, "c++", "${1:Object}", varPrefix+name, value if not isPointer else '${'+str(varIndex+2)+':new ' +value+'}')
				shrtOutput += self.setVarOutput(syntax, "javascript", "var", name, value)
				shrtOutput += self.setVarOutput(syntax, "java", "${1:Object}", name, value)
				shrtOutput += self.setVarOutput(syntax, "php","$", name, value)
				shrtOutput += self.setVarOutput(syntax, "objective-c", "${1:Object}", name, value)
				shrtOutput += self.setVarOutput(syntax, "python", "", name, value)
				varIndex+=4


		#########################
		# ARRAY
		#########################
		
		elif shrtInput[2]=="a" and len(shrtInput)>3:

			# Array Integer
			if shrtInput[3] == "i":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myIntArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+2)+':0}'
					shrtOutput += self.setVarOutput(syntax, "c++", "int", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "javascript", "var", name, '['+value+']')
					shrtOutput += self.setVarOutput(syntax, "java", "int", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "php", "$", name, 'array('+value+')')
					shrtOutput += self.setVarOutput(syntax, "objective-c", "int", name+'[${'+str(varIndex+1)+':}]','{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "python", "", name, '['+value+']')
					varIndex+=3

			# Array Unsigned Integer
			elif shrtInput[3] == "u":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myUintArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+2)+':0}'
					shrtOutput += self.setVarOutput(syntax, "c++", "uint", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "javascript", "var", name, '['+value+']')
					shrtOutput += self.setVarOutput(syntax, "java", "int", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "php", "$", name, 'array('+value+')')
					shrtOutput += self.setVarOutput(syntax, "objective-c", "int", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "python", "", name, '['+value+']')
					varIndex+=3

			# Array Float
			if shrtInput[3] == "f":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myFloatArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+2)+':0.0}'
					shrtOutput += self.setVarOutput(syntax, "c++", "float", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "javascript", "var", name, '['+value+']')
					shrtOutput += self.setVarOutput(syntax, "java", "float", name+'[${'+str(varIndex+1)+':}]','{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "php", "$", name, 'array('+value+')')
					shrtOutput += self.setVarOutput(syntax, "objective-c", "float", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "python", "", name, '['+value+']')
					varIndex+=3

			# Array Boolean
			if shrtInput[3] == "b":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myBoolArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+2)+':false}'
					shrtOutput += self.setVarOutput(syntax, "c++", "bool", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "javascript", "var", name,  '['+value+']')
					shrtOutput += self.setVarOutput(syntax, "java", "boolean", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "php",'$'+name+' = array('+value+');\n')
					shrtOutput += self.setVarOutput(syntax, "objective-c", "bool", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "python", name, '['+value+']\n')
					varIndex+=3

			# Array Char
			if shrtInput[3] == "c":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myBoolArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+2)+':false}'
					shrtOutput += self.setVarOutput(syntax, "c++", "char", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "javascript", "var",name, '['+value+']')
					shrtOutput += self.setVarOutput(syntax, "java", "char", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "php", "$", name, 'array('+value+')')
					shrtOutput += self.setVarOutput(syntax, "objective-c", "char", name+'[${'+str(varIndex+1)+':}]','{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "python", "", name, '['+value+']')
					varIndex+=3

			# Array String
			if shrtInput[3] == "s":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myBoolArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '"${'+str(varIndex+2)+':}"'
					shrtOutput += self.setVarOutput(syntax, "c++", "std::string", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "javascript", "var", name, '['+value+']')
					shrtOutput += self.setVarOutput(syntax, "java", "string", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "php", "$", name, 'array('+value+')')
					shrtOutput += self.setVarOutput(syntax, "objective-c", "string", name+'[${'+str(varIndex+1)+':}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "python", "", name, '['+value+']')
					varIndex+=3

			# Array Object
			if shrtInput[3] == "o":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex+1)+":myObjectArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+3)+':Object}'
					shrtOutput += self.setVarOutput(syntax, "c++", "${1:Object}", name+'[${'+str(varIndex+2)+':1}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "javascript", "var", name, '['+value+']')
					shrtOutput += self.setVarOutput(syntax, "java", "${1:Object}", name+'[${'+str(varIndex+2)+':1}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "php", "$", name, 'array('+value+')')
					shrtOutput += self.setVarOutput(syntax, "objective-c", "${1:Object}", name+'[${'+str(varIndex+2)+':1}]', '{'+value+'}')
					shrtOutput += self.setVarOutput(syntax, "python", "", name, '['+value+']')
					varIndex+=3


		#########################
		# OUTPUT
		#########################

		if shrtOutput == "":
			return False
		else:
			return shrtOutput.rstrip("\n")



	def setVarOutput(self,currentSyntax,targetSyntax,varType,varName,varValue):
		if currentSyntax==targetSyntax:
			return (varType+' ' if not targetSyntax=='python' else '') + varName + ' = ' + varValue + (';' if not targetSyntax == 'python' else '') + '\n'
		else:
			return ''




#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/
#/	METHODS
#/
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	def createMethod(self, shrtInput, methodBody):

		syntax 		= self.getSyntax()
		parameter 	= self.getParameter(shrtInput)
		shrtInput 	= shrtInput.split(".")[0]		# remove parameter from input
		shrtOutput 	= ""

		#########################
		# PARAMETER
		#########################
		
		# Parameter values
		methodName 	= "myMethod"

		# Iterate parameter
		for param in parameter:
			# Method name
			if (len(param)>=2):
				methodName = param


		#########################
		# ACCESS MODIFIER
		#########################

		# Define modifier
		accessModifier = False
		if shrtInput[2:4]=="pr":
			accessModifier = "private"
		elif shrtInput[2:4]=="pu":
			accessModifier = "public"
		elif shrtInput[2:4]=="po":
			accessModifier = "protected"
		if accessModifier == False:
			return False
		accessModifier = accessModifier + " "

		# Adapt language
		if syntax == "c++":
			accessModifier = ""


		#########################
		# RETURN VALUE
		#########################

		returnValue = "void"
		if shrtInput[4:6] == "vi":
			returnValue = "int"
		elif shrtInput[4:6] == "vu":
			returnValue = "uint"
		elif shrtInput[4:6] == "vf":
			returnValue = "float"
		elif shrtInput[4:6] == "vb":
			returnValue = "bool"
		elif shrtInput[4:6] == "vc":
			returnValue = "char"
		elif shrtInput[4:6] == "vs":
			returnValue = "string"
		elif shrtInput[4:6] == "vo":
			returnValue = "Object"
		elif shrtInput[4:6] == "va":
			returnValue = "array"


		#########################
		# FIND CLASS NAME
		#########################

		# name of file
		fileName 		= self.view.file_name().split("/")
		fileName 		= fileName[len(fileName)-1].split(".")
		fileExtension 	= fileName[1]
		fileName 		= fileName[0]


		#########################
		# METHOD
		#########################

		if syntax == "c++":
			shrtOutput = accessModifier + returnValue + " ${1:CLASS}::" + methodName + "()" + (";" if methodBody==False else " {\n\t${2:}\n}")
		else:
			return False


		#########################
		# OUTPUT
		#########################

		if shrtOutput == "":
			return False
		else:
			return shrtOutput.rstrip("\n")



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/
#/	FLOW
#/
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	def createFlow(self, shrtInput):

		syntax 		= self.getSyntax()
		parameter 	= self.getParameter(shrtInput)
		shrtInput 	= shrtInput.split(".")[0]		# remove parameter from input
		shrtOutput 	= ""


		#########################
		# IF / ELSE IF
		#########################

		if shrtInput[2]=="i":

			# Default values
			ifContent 		= "=="
			contentAnd 		= False
			contentOr 		= False
			contentLT		= False
			contentGT 		= False
			addElse 		= False
			ifCount 		= 1
			ifIndex			= 1

			# Parameter
			for param in parameter:
				# &&
				if param == "an":
					contentAnd = True
				elif param == "or":
					contentOr = True
				elif param == "lt":
					contentLT = True
				elif param == "gt":
					contentGT = True
				# count if
				elif self.isInt(param):
					ifCount = int(param)
				# add else statement
				elif param == "el":
					addElse = True

			# Statement
			for i in range(0,ifCount):

				# If or else if?
				ifStatement = "if" if i==0 else ("else if" if not syntax == "python" else "elif" )

				# If content
				if contentAnd or contentOr:
					if syntax == "python":
						ifContent = "and" if contentAnd else "or"
					else:	
						ifContent = "&&" if contentAnd else "||"
				elif contentLT or contentGT:
					ifContent = "<" if contentLT else ">"
				ifContent = " ${"+str(ifIndex+1)+":"+ifContent+"} ${"+str(ifIndex+2)+":}"


				# output
				if syntax == "python":
					shrtOutput += ifStatement + " ${"+str(ifIndex)+":}" + ifContent + "}:\n\t${" + str(ifIndex+1) + ":}\n"
					ifIndex += 2
				else:
					shrtOutput += ifStatement + "(${" + str(ifIndex) + ":}" + ifContent + ")${" + str(ifIndex+3) + ":} {\n\t${" + str(ifIndex+4) + ":}\n}\n"
					ifIndex += 5
			
			# Add else			
			if addElse:
				if syntax == "python":
					shrtOutput += "else: \n\t${"+str(ifIndex)+":}\n"
				else:
					shrtOutput += "else {\n\t${"+str(ifIndex)+":}\n}"



		#########################
		# OUTPUT
		#########################

		if shrtOutput == "":
			return False
		else:
			return shrtOutput.rstrip("\n")



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/
#/	FILE STRUCTURE
#/
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	def createStructure(self, edit, shrtInput):

		syntax 		= self.getSyntax()
		parameter 	= self.getParameter(shrtInput)
		shrtInput 	= shrtInput.split(".")[0]		# remove parameter from input
		shrtOutput 	= ""

		# Input elements
		cursorPos 	= self.view.sel()[0].end()
		row,col 	= self.view.rowcol(cursorPos)
		lineInput 	= self.view.substr(self.view.line(cursorPos))[0:col]


		#########################
		# COMMENT BOX / LINE
		#########################
		
		if shrtInput[2]=="c":

			# empty line before
			for i in range(1,20):
				if row-i < 0:
					break
				lineContent = self.view.text_point(row-i,0)
				lineContent = self.view.substr(self.view.line(lineContent))[0:]
				if lineContent.strip() != "":
					break

			# Add empty lines if less than 3
			if i < 4 and not row == 0:
				for j in range(0,4-i):
					shrtOutput += "\n"

			# remove empty line if more than 3
			if i > 4:
				self.view.erase(edit,sublime.Region(self.view.text_point(row-(i-4),0), cursorPos-len(shrtInput)))
			
			# Remove tabs in current line
			tabCount = 0
			for i in range(0, col):
				if lineInput[i] == "\t":
					tabCount += 1
			self.view.erase(edit,sublime.Region(cursorPos-tabCount-len(shrtInput), cursorPos-len(shrtInput)))

			# Default text
			commentTitle = ""
			commentInput = "# " if syntax == "python" else "// "

			# Parameter
			for param in parameter:
				if param == "in":
					commentTitle = "INCLUDES"
				elif param == "cl":
					commentTitle = "CLASS DECLARATION"
				elif param == "co":
					commentTitle = "CONSTRUCTOR & DESTRUCTOR"

			# comment box or line
			if len(shrtInput)==3 or shrtInput[3] == "b":
				if syntax == "python":
					shrtOutput += "#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n#/\n#/	${1:"+commentTitle+"}\n#/\n#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n\n\n\t${2:"+commentInput+"}"
				else:
					shrtOutput += "/*///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n//\n//	${1:"+commentTitle+"}\n//\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// */\n\n\n\t${2:"+commentInput+"}"
			elif shrtInput[3] == "l":
				if syntax == "python":
					shrtOutput += "#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n\n\n\t"
				else:
					shrtOutput += "/*///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// */\n\n\n\t"


		#########################
		# OUTPUT
		#########################

		if shrtOutput == "":
			return False
		else:
			return shrtOutput.rstrip("\n")



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/
#/	HELPER
#/
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	def getSyntax(self):

		# Current Syntax
		syntax = self.view.settings().get('syntax')
		#print(syntax)

		# Return parsed syntax
		if 'C++' in syntax:
			return 'c++'
		elif 'JavaScript' in syntax:
			return 'javascript'
		elif 'Java' in syntax:
			return 'java'
		elif 'PHP' in syntax:
			return 'php'
		elif 'Objective-C' in syntax:
			return 'objective-c'
		elif 'Python' in syntax:
			return 'python'


	
	def getParameter(self,shrtInput):
		parameter = shrtInput.split('.')
		parameter.pop(0)
		return parameter



	def isInt(self, s):
		try:
			int(s)
			return True
		except ValueError:
			return False




		