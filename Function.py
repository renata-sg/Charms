# Class to store information about a function

class Function:
	def __init__(self, startPosition, parameterTable, tempVariableTable, funcReturnType):
		self.startPosition = startPosition
		self.parameterTable = parameterTable
		self.tempVariableTable = tempVariableTable
		self.funcReturnType = funcReturnType # type of the value returned by the function
