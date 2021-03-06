# Class to handle memory management and execution of programs

from QuadruplesHelper import printQuadruples
from QuadruplesHelper import convertQuadruples

class VirtualMachine:
	quadruples = []
	functionDirectory = {}
	constants = {}
	memoryStack = {}
	for key in range(0, 3300):
		memoryStack[key] = None
	memoryStartingPoint = { 'global': 0, 'local': 900, 'temp': 1800, 'const': 2700 }

	GLOBALINT = 0
	GLOBALBOOL = 300
	GLOBALCHAR = 600
	LOCALINT = 0
	LOCALBOOL = 300
	LOCALCHAR = 600
	TEMPINT = 0
	TEMPBOOL = 300
	TEMPCHAR = 600
	CONSTINT = 0
	CONSTBOOL = 300

	def __init__(self, quadruples, functionDirectory, constantTable, varTable):
		self.quadruples = quadruples
		self.functionDirectory = functionDirectory
		self.constantTable = constantTable
		self.varTable = varTable

		# Update addresses in constant, global, and local tables
		self.updateConstantAddresses(self.constantTable)
		self.updateVarAddresses(self.varTable)
		functions = self.functionDirectory.dictionary
		for key in functions:
			function = functions[key]
			parameterTable = function.parameterTable
			self.updateParameterAddresses(parameterTable)
			tempVariableTable = function.tempVariableTable
			self.updateTempVariableAddresses(tempVariableTable)

		# Update memory stack
		self.updateConstantMemoryStack(constantTable)
		self.updateGlobalMemoryStack(varTable)
		functions = self.functionDirectory.dictionary
		for key in functions:
			function = functions[key]
			parameterTable = function.parameterTable
			self.updateLocalMemoryStack(parameterTable)
			tempVariableTable = function.tempVariableTable
			self.updateTemporalMemoryStack(tempVariableTable)

		# Convert quadruples
		# self.printMemoryStack()
		convertQuadruples(quadruples, functionDirectory, constantTable, varTable)
		printQuadruples(quadruples)

		# Print memory stack
		# self.printMemoryStack()

		# Execute quadruples
		self.executeQuadruples()

		# Print memory stack
		# self.printMemoryStack()

		print("Success")

	# Functions to update addresses in tables (variable, parameter, tempVariable and constant tables)
	# They receive as a parameter the table to modify with new real address.
	def updateConstantAddresses(self, constantTable):
		constants = constantTable.constants
		for key in constants:
			constant = constants[key]
			currentAddr = constant.constantAddress
			startingPoint = self.memoryStartingPoint['const']
			if constant.constantType == 'int':
				newAddr = startingPoint + self.CONSTINT + currentAddr
			else:
				newAddr = startingPoint + self.CONSTBOOL + currentAddr
			constant.updateAddress(newAddr)

	def updateVarAddresses(self, varTable):
		vars = varTable.vars
		for key in vars:
			var = vars[key]
			currentAddr = var.varAddress
			startingPoint = self.memoryStartingPoint['global']
			varType = var.varType
			if varType == 'int':
				newAddr = startingPoint + self.GLOBALINT + currentAddr
			elif varType == 'bool':
				newAddr = startingPoint + self.GLOBALBOOL + currentAddr
			else:
				newAddr = startingPoint + self.GLOBALCHAR + currentAddr
			var.updateAddress(newAddr)

	def updateParameterAddresses(self, parameterTable):
		parameters = parameterTable.parameters
		for key in parameters:
			parameter = parameters[key]
			currentAddr = parameter.parameterAddress
			startingPoint = self.memoryStartingPoint['local']
			parameterType = parameter.parameterType
			if parameterType == 'int':
				newAddr = startingPoint + self.LOCALINT + currentAddr
			elif parameterType == 'bool':
				newAddr = startingPoint + self.LOCALBOOL + currentAddr
			else:
				newAddr = startingPoint + self.LOCALCHAR + currentAddr
			parameter.updateAddress(newAddr)

	def updateTempVariableAddresses(self, tempVariableTable):
		tempVariables = tempVariableTable.tempVariables
		for key in tempVariables:
			tempVariable = tempVariables[key]
			currentAddr = tempVariable.tempVariableAddress
			startingPoint = self.memoryStartingPoint['temp']
			tempVariableType = tempVariable.tempVariableType
			if tempVariableType == 'int':
				newAddr = startingPoint + self.TEMPINT + currentAddr
			elif tempVariableType == 'bool':
				newAddr = startingPoint + self.TEMPBOOL + currentAddr
			else:
				newAddr = startingPoint + self.TEMPCHAR + currentAddr
			tempVariable.updateAddress(newAddr)

	# Functions to update memory stack with values.
	# They receive as a parameter a table, and from there a value and address are obtained to 
	# update memoryStack.
	def updateGlobalMemoryStack(self, varTable):
		vars = varTable.vars
		for key in vars:
			var = vars[key]
			addr = var.varAddress
			self.memoryStack[addr] = key

	def updateLocalMemoryStack(self, parameterTable):
		self.clearMemorySection('local')
		parameters = parameterTable.parameters
		for key in parameters:
			parameter = parameters[key]
			addr = parameter.parameterAddress
			self.memoryStack[addr] = key

	def updateTemporalMemoryStack(self, tempVariableTable):
		self.clearMemorySection('temp')
		tempVariables = tempVariableTable.tempVariables
		for key in tempVariables:
			tempVariable = tempVariables[key]
			addr = tempVariable.tempVariableAddress
			self.memoryStack[addr] = key

	def updateConstantMemoryStack(self, constantTable):
		constants = constantTable.constants
		for key in constants:
			constant = constants[key]
			addr = constant.constantAddress
			self.memoryStack[addr] = key

	def clearMemorySection(self, scope):
		if scope == 'global':
			memorySection = range(0, 900)
		elif scope == 'local':
			memorySection = range(900, 1800)
		elif scope == 'temp':
			memorySection = range(1800, 2700)
		else: #const
			memorySection = range(2700, 3300)
		for addr in memorySection:
			self.memoryStack[addr] = None

	def executeQuadruples(self):
		quadruples = self.quadruples
		self.executeQuad(quadruples[0])

	# Recursive function that executes quadruples.
	# Receives a single quad, takes its operands and operator, and based on the operator performs an action.
	# Calls itself again with a new quad based on the operator - may be the next quad or a jump to another.
	def executeQuad(self, quad):
		global currentFunction
		global currentFunctionName
		global gosubIndex
		operator = quad.operator
		leftOperand = quad.leftOperand
		rightOperand = quad.rightOperand
		result = quad.result
		index = self.quadruples.index(quad)
		if operator != 'END':
			if operator == 'goto':
				newQuad = self.quadruples[result-1]
			elif operator == 'gotoF':
				if self.memoryStack[leftOperand]:
					newQuad = self.quadruples[index+1]
				else:
					newQuad = self.quadruples[result-1]
			elif operator == '>':
				value = self.memoryStack[leftOperand] > self.memoryStack[rightOperand]
				self.memoryStack[result] = value
				newQuad = self.quadruples[index+1]
			elif operator == '<':
				value = self.memoryStack[leftOperand] < self.memoryStack[rightOperand]
				self.memoryStack[result] = value
				newQuad = self.quadruples[index+1]
			elif operator == '==':
				value = self.memoryStack[leftOperand] == self.memoryStack[rightOperand]
				self.memoryStack[result] = value
				newQuad = self.quadruples[index+1]
			elif operator == '!=':
				value = self.memoryStack[leftOperand] != self.memoryStack[rightOperand]
				self.memoryStack[result] = value
				newQuad = self.quadruples[index+1]
			elif operator == '+':
				value = self.memoryStack[leftOperand] + self.memoryStack[rightOperand]
				self.memoryStack[result] = value
				newQuad = self.quadruples[index+1]
			elif operator == '-':
				value = self.memoryStack[leftOperand] - self.memoryStack[rightOperand]
				self.memoryStack[result] = value
				newQuad = self.quadruples[index+1]
			elif operator == '*':
				value = self.memoryStack[leftOperand] * self.memoryStack[rightOperand]
				self.memoryStack[result] = value
				newQuad = self.quadruples[index+1]
			elif operator == '/':
				value = self.memoryStack[leftOperand] / self.memoryStack[rightOperand]
				self.memoryStack[result] = int(value)
				newQuad = self.quadruples[index+1]
			elif operator == '=':
				# Get value
				self.memoryStack[rightOperand] = self.memoryStack[leftOperand]
				newQuad = self.quadruples[index+1]
			elif operator == 'ERA':
				self.clearMemorySection('local')
				self.clearMemorySection('temp')
				currentFunction = self.functionDirectory.dictionary[leftOperand]
				currentFunctionName = leftOperand
				newQuad = self.quadruples[index+1]
			elif operator == 'PARAM':
				parameterValue = self.memoryStack[leftOperand]
				parameterIndex = int(result[-1:])
				parameterTable = currentFunction.parameterTable.parameters
				parameterTableList = list(parameterTable)
				parameter = parameterTableList[parameterIndex-1]
				parameterType = parameterTable[parameter].parameterType
				if parameterType == 'int':
					startingPoint = 0
				elif parameterType == 'bool':
					startingPoint = 300
				else:
					startingPoint = 600
				addr = self.memoryStartingPoint['local'] + startingPoint + parameterIndex - 1
				self.memoryStack[addr] = parameterValue
				newQuad = self.quadruples[index+1]
			elif operator == 'GOSUB':
				functionStartingPoint = currentFunction.startPosition
				newQuad = self.quadruples[functionStartingPoint]
				gosubIndex = index
			elif operator == 'ENDPROC':
				self.clearMemorySection('local')
				self.clearMemorySection('temp')
				newQuad = self.quadruples[gosubIndex+1]
			elif operator == 'RETURN':
				currentFunctionAddr = self.varTable.vars[currentFunctionName].varAddress
				self.memoryStack[currentFunctionAddr] = self.memoryStack[leftOperand]
				newQuad = self.quadruples[index+1]
			elif operator == 'PRINT':
				print("*")
				if leftOperand in self.memoryStack:
					print(self.memoryStack[leftOperand])
				else:
					print(leftOperand)
				print("*")
				newQuad = self.quadruples[index+1]
			elif operator == 'READ':
				value = input()
				if type(self.memoryStack[leftOperand] != type(value)):
					raise Exception("Type mismatch")
				else:
					self.memoryStack[leftOperand] = value
					newQuad = self.quadruples[index+1]
			self.executeQuad(newQuad)

	def printMemoryStack(self):
		memoryStack = self.memoryStack
		for key in memoryStack:
			if memoryStack[key] != None:
				print(key, memoryStack[key])
