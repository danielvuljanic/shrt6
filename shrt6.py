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
			return
		shrtInput = shrtInput.group().lstrip()


		##################
		# SHRT6 COMMANDS
		##################
		
		shrtOutput = self.getShrt6Command(shrtInput)
		if not shrtOutput:
			return
		

		##################
		# OUTPUT
		##################

		self.view.erase(edit,sublime.Region(cursorPos-len(shrtInput), cursorPos))
		self.view.run_command('insert_snippet', {'contents': shrtOutput})



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/
#/	SHRT COMMANDS
#/
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	def getShrt6Command(self, shrtInput):

		# Variables		
		if shrtInput.startswith("cv"):
			return self.createVariable(shrtInput)

		# References
		if shrtInput.startswith("cr"):
			return self.createVariable(shrtInput,isReference=True)

		# Pointer
		if shrtInput.startswith("cp"):
			return self.createVariable(shrtInput,isPointer=True)

		# No command
		else:
			return False



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/
#/	VARIABLES
#/
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	def createVariable(self,shrtInput,isReference=False,isPointer=False):

		shrtOutput 	= ""
		syntax 		= self.getSyntax()
		parameter 	= self.getParameter(shrtInput)
		shrtInput 	= shrtInput.split(".")[0]		# remove parameter from input


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
				shrtOutput += self.setVarOutput(syntax,"c++",'int '+varPrefix+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"java",'int '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"objective-c",'int '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"python",name+' = '+value+'\n')
				varIndex+=2
		

		#########################
		# UNSIGNED INTEGER
		#########################

		elif shrtInput[2]=="u":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex)+":myUint"+(str(i+1) if varCount > 1 else "")+"}";
				value = '${'+str(varIndex+1)+':0}'
				shrtOutput += self.setVarOutput(syntax,"c++",'uint '+varPrefix+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"java",'int '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"objective-c",'int '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"python",name+' = '+value+'\n')
				varIndex+=2


		#########################
		# FLOAT
		#########################

		elif shrtInput[2]=="f":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex)+":myFloat"+(str(i+1) if varCount > 1 else "")+"}";
				value = '${'+str(varIndex+1)+':0.0}'
				shrtOutput += self.setVarOutput(syntax,"c++",'float '+varPrefix+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"java",'float '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"objective-c",'float '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"python",name+' = '+value+'\n')
				varIndex+=2


		#########################
		# BOOLEAN
		#########################

		elif shrtInput[2]=="b":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex)+":myBool"+(str(i+1) if varCount > 1 else "")+"}";
				value = '${'+str(varIndex+1)+':false}'
				shrtOutput += self.setVarOutput(syntax,"c++",'bool '+varPrefix+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"java",'boolean '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"objective-c",'bool '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"python",name+' = '+value+'\n')
				varIndex+=2


		#########################
		# CHAR
		#########################

		elif shrtInput[2]=="c":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex)+":myChar"+(str(i+1) if varCount > 1 else "")+"}";
				value = '\'${'+str(varIndex+1)+':A}\''
				shrtOutput += self.setVarOutput(syntax,"c++",'char '+varPrefix+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"java",'char '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"objective-c",'char '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"python",name+' = '+value+'\n')
				varIndex+=2


		#########################
		# STRING
		#########################

		elif shrtInput[2]=="s":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex)+":myString"+(str(i+1) if varCount > 1 else "")+"}";
				value = '"${'+str(varIndex+1)+':}"'
				shrtOutput += self.setVarOutput(syntax,"c++",'std::string '+varPrefix+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"java",'string '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"objective-c",'string '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"python",name+' = '+value+'\n')
				varIndex+=2


		#########################
		# OBJECT
		#########################

		elif shrtInput[2]=="o":
			for i in range(0,varCount):
				name = varName if varName else "${"+str(varIndex+1)+":myObject"+(str(i+1) if varCount > 1 else "")+"}";
				value = '${'+str(1)+':Object}(${'+str(varIndex+2)+'})'
				shrtOutput += self.setVarOutput(syntax,"c++",'${1:Object} '+varPrefix+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"java",'${1:Object} '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"objective-c",'${1:Object} '+name+' = '+value+';\n')
				shrtOutput += self.setVarOutput(syntax,"python",name+' = '+value+'\n')
				varIndex+=3


		#########################
		# ARRAY
		#########################
		elif shrtInput[2]=="a" and len(shrtInput)>3:

			# Array Integer
			if shrtInput[3] == "i":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myIntArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+2)+':0}'
					shrtOutput += self.setVarOutput(syntax,"c++",'int '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = ['+value+'];\n')
					shrtOutput += self.setVarOutput(syntax,"java",'int '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = array('+value+');\n')
					shrtOutput += self.setVarOutput(syntax,"objective-c",'int '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"python",name+' = ['+value+']\n')
					varIndex+=3

			# Array Unsigned Integer
			elif shrtInput[3] == "u":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myUintArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+2)+':0}'
					shrtOutput += self.setVarOutput(syntax,"c++",'uint '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = ['+value+'];\n')
					shrtOutput += self.setVarOutput(syntax,"java",'int '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = array('+value+');\n')
					shrtOutput += self.setVarOutput(syntax,"objective-c",'int '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"python",name+' = ['+value+']\n')
					varIndex+=3

			# Array Float
			if shrtInput[3] == "f":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myFloatArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+2)+':0.0}'
					shrtOutput += self.setVarOutput(syntax,"c++",'float '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = ['+value+'];\n')
					shrtOutput += self.setVarOutput(syntax,"java",'float '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = array('+value+');\n')
					shrtOutput += self.setVarOutput(syntax,"objective-c",'float '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"python",name+' = ['+value+']\n')
					varIndex+=3

			# Array Boolean
			if shrtInput[3] == "b":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myBoolArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+2)+':false}'
					shrtOutput += self.setVarOutput(syntax,"c++",'bool '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = ['+value+'];\n')
					shrtOutput += self.setVarOutput(syntax,"java",'boolean '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = array('+value+');\n')
					shrtOutput += self.setVarOutput(syntax,"objective-c",'bool '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"python",name+' = ['+value+']\n')
					varIndex+=3

			# Array Char
			if shrtInput[3] == "c":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myBoolArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+2)+':false}'
					shrtOutput += self.setVarOutput(syntax,"c++",'char '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = ['+value+'];\n')
					shrtOutput += self.setVarOutput(syntax,"java",'char '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = array('+value+');\n')
					shrtOutput += self.setVarOutput(syntax,"objective-c",'char '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"python",name+' = ['+value+']\n')
					varIndex+=3

			# Array String
			if shrtInput[3] == "s":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex)+":myBoolArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '"${'+str(varIndex+2)+':}"'
					shrtOutput += self.setVarOutput(syntax,"c++",'std::string '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = ['+value+'];\n')
					shrtOutput += self.setVarOutput(syntax,"java",'string '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = array('+value+');\n')
					shrtOutput += self.setVarOutput(syntax,"objective-c",'string '+name+'[${'+str(varIndex+1)+':}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"python",name+' = ['+value+']\n')
					varIndex+=3

			# Array Object
			if shrtInput[3] == "o":
				for i in range(0,varCount):
					name = varName if varName else "${"+str(varIndex+1)+":myObjectArray"+(str(i+1) if varCount > 1 else "")+"}";
					value = '${'+str(varIndex+3)+':Object}'
					shrtOutput += self.setVarOutput(syntax,"c++",'${1:Object} '+name+'[${'+str(varIndex+2)+':1}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"javascript",'var '+name+' = ['+value+'];\n')
					shrtOutput += self.setVarOutput(syntax,"java",'${1:Object} '+name+'[${'+str(varIndex+2)+':1}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"php",'$'+name+' = array('+value+');\n')
					shrtOutput += self.setVarOutput(syntax,"objective-c",'${1:Object} '+name+'[${'+str(varIndex+2)+':1}] = {'+value+'};\n')
					shrtOutput += self.setVarOutput(syntax,"python",name+' = ['+value+']\n')
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
			return (varType) + varName + ' = ' + varValue + (';' if not targetSyntax == 'python' else '') + '\n'
		else:
			return ""



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




		