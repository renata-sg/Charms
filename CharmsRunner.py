from antlr4 import *
from antlr4.tree.Trees import Trees
from CharmsLexer import CharmsLexer
from CharmsParserListener import CharmsParserListener
from CharmsParser import CharmsParser
from Quad import Quad
from SemanticCube import arithmeticOperators
from SemanticCube import relationalOperators
from SemanticCube import assignmentOperator
from Variable import Variable
from VariableTable import VariableTable
from Function import Function
from FunctionDirectory import FunctionDirectory
import sys

class CharmsPrintListener(CharmsParserListener):
	def exitType_id(self, ctx):
		global varType
		if ctx.INT():
			varType = "int"
		elif ctx.CHAR():
			varType = "char"
		elif ctx.BOOL():
			varType = "bool"
		else:
			Exception("{} is not a valid data type".format(varType))

	def exitVar_cte(self, ctx):
		myId = str(ctx.ID())
		myCTE_INT = str(ctx.CTE_INT())
		if myId != "None":
			stackOperands.append(myId)
			stackTypes.append(varTable.getVariableType(myId))
		else:
			stackOperands.append(int(myCTE_INT))
			stackTypes.append("int")
		# print("stackOperands:")
		# print(stackOperands)
		# print("stackTypes:")
		# print(stackTypes)

	def enterE1(self, ctx):
		operator = ctx.PLUS() or ctx.MINUS()
		operator = str(operator)
		if operator != "None":
			stackOperators.append(operator)

	def enterT(self, ctx):
		operator = ctx.TIMES() or ctx.DIVIDE()
		operator = str(operator)
		if operator != "None":
			stackOperators.append(operator)
		# print("stackOperator:")
		# print(stackOperators)

	def exitTerm(self, ctx):
		if len(stackOperators) > 0:
			if stackOperators[-1] == '+' or stackOperators[-1] == '-':
				right_operand = stackOperands.pop()
				right_type = stackTypes.pop()
				left_operand = stackOperands.pop()
				left_type = stackTypes.pop()
				operator = stackOperators.pop()
				result_type = arithmeticOperators(operator, right_type, left_type)
				# print("right_operand")
				# print(right_operand)
				# print("right_type")
				# print(right_type)
				# print("left_operand")
				# print(left_operand)
				# print("left_type")
				# print(left_type)
				# print("operator")
				# print(operator)
				if result_type == "int":
					global tCount
					tCount +=1
					result = "t"+str(tCount)
					global qCount
					qCount += 1
					quad = Quad(operator, left_operand, right_operand, result)
					queueQuads.append(quad)
					stackOperands.append(result)
					stackTypes.append(result_type)
				else:
					Exception("Type mismatch")

	def enterFactor(self, ctx):
		operator = str(ctx.LPARENTHESES())
		if operator != "None":
			stackOperators.append(operator)
			# print("stackOperators")
			# print(stackOperators)

	def exitFactor(self, ctx):
		operator = str(ctx.RPARENTHESES())
		if operator != "None":
			stackOperators.pop()
			# print("stackOperators")
			# print(stackOperators)
		if len(stackOperators) > 0:
			if stackOperators[-1] == '*' or stackOperators[-1] == '/':
				right_operand = stackOperands.pop()
				right_type = stackTypes.pop()
				left_operand = stackOperands.pop()
				left_type = stackTypes.pop()
				operator = stackOperators.pop()
				result_type = arithmeticOperators(operator, right_type, left_type)
				# print("right_operand")
				# print(right_operand)
				# print("right_type")
				# print(right_type)
				# print("left_operand")
				# print(left_operand)
				# print("left_type")
				# print(left_type)
				# print("operator")
				# print(operator)
				if result_type == "int":
					global tCount
					tCount +=1
					result = "t"+str(tCount)
					global qCount
					qCount += 1
					quad = Quad(operator, left_operand, right_operand, result)
					queueQuads.append(quad)
					stackOperands.append(result)
					stackTypes.append(result_type)
				else:
					Exception("Type mismatch")

	def addVar(self, ctx):
		global varId
		varId = str(ctx.ID()) # cast to string to avoid dealing with TerminalNode objects
		if varId != "None":
			varTable.insertVariable(varId, varType, "global")
			# varTable.printTable()

	def enterV(self, ctx):
		self.addVar(ctx)

	def enterV1(self, ctx):
		self.addVar(ctx)

	def enterE(self, ctx):
		operator = ctx.GREATERTHAN() or ctx.LESSTHAN()
		operator = str(operator)
		if operator != "None":
			stackOperators.append(operator)
		# print("stackOperator:")
		# print(stackOperators)

	def exitE(self, ctx):
		if len(stackOperators) > 0:
			if stackOperators[-1] == '<' or stackOperators[-1] == '>':
				right_operand = stackOperands.pop()
				right_type = stackTypes.pop()
				left_operand = stackOperands.pop()
				left_type = stackTypes.pop()
				operator = stackOperators.pop()
				result_type = relationalOperators(operator, right_type, left_type)
				# print("right_operand")
				# print(right_operand)
				# print("right_type")
				# print(right_type)
				# print("left_operand")
				# print(left_operand)
				# print("left_type")
				# print(left_type)
				# print("operator")
				# print(operator)
				if result_type == "bool":
					global tCount
					tCount +=1
					result = "t"+str(tCount)
					global qCount
					qCount += 1
					quad = Quad(operator, left_operand, right_operand, result)
					queueQuads.append(quad)
					stackOperands.append(result)
					stackTypes.append(result_type)
				else:
					Exception("Type mismatch")

	def enterAssignment(self, ctx):
		operator = str(ctx.ASSIGN())
		if operator != "None":
			assignmentId = str(ctx.ID())
			stackOperators.append(operator)
			stackOperands.append(assignmentId)
			stackTypes.append(varTable.getVariableType(assignmentId))

	def exitAssignment(self, ctx):
		if len(stackOperators) > 0:
			if stackOperators[-1] == '=':
				right_operand = stackOperands.pop()
				right_type = stackTypes.pop()
				left_operand = stackOperands.pop()
				left_type = stackTypes.pop()
				operator = stackOperators.pop()
				result_type = assignmentOperator(operator, right_type, left_type)
				# print("right_operand")
				# print(right_operand)
				# print("right_type")
				# print(right_type)
				# print("left_operand")
				# print(left_operand)
				# print("left_type")
				# print(left_type)
				# print("operator")
				# print(operator)
				if result_type == "true":
					result = ""
					global qCount
					qCount += 1
					quad = Quad(operator, left_operand, right_operand, result)
					queueQuads.append(quad)
				else:
					Exception("Type mismatch")

	def enterWrite(self, ctx):
		operator = str(ctx.PRINT())
		if operator != "None":
			stackOperators.append(operator)

	def exitWrite(self, ctx):
		if len(stackOperators) > 0:
			if stackOperators[-1] == 'print':
				left_operand = stackOperands.pop()
				right_operand = ""
				operator = stackOperators.pop()
				# print("right_operand")
				# print(right_operand)
				# print("right_type")
				# print(right_type)
				# print("left_operand")
				# print(left_operand)
				# print("left_type")
				# print(left_type)
				# print("operator")
				# print(operator)
				result = ""
				global qCount
				qCount += 1
				quad = Quad(operator, left_operand, right_operand, result)
				queueQuads.append(quad)

	def enterRead(self, ctx):
		operator = str(ctx.READ())
		if operator != "None":
			assignmentId = str(ctx.ID())
			stackOperators.append(operator)
			stackOperands.append(assignmentId)

	def exitRead(self, ctx):
		if len(stackOperators) > 0:
			if stackOperators[-1] == 'read':
				left_operand = stackOperands.pop()
				right_operand = ""
				operator = stackOperators.pop()
				# print("right_operand")
				# print(right_operand)
				# print("right_type")
				# print(right_type)
				# print("left_operand")
				# print(left_operand)
				# print("left_type")
				# print(left_type)
				# print("operator")
				# print(operator)
				result = ""
				global qCount
				qCount += 1
				quad = Quad(operator, left_operand, right_operand, result)
				queueQuads.append(quad)

	def enterLoop(self, ctx):
		stackJumps.append(qCount+1)
		global executionSource
		executionSource = "loop"

	def exitLoop(self, ctx):
		end = stackJumps.pop()
		operator = "goto"
		left_operand = stackJumps.pop()
		right_operand = ""
		result = ""
		global qCount
		qCount += 1
		quad = Quad(operator, left_operand, right_operand, result)
		queueQuads.append(quad)
		queueQuads[end-1].rightOperand = qCount+1

	def enterSection(self, ctx):
		global executionSource
		if executionSource == "loop" or executionSource == "condition":
			exp_type = stackTypes.pop()
			if exp_type == "bool":
				operator = "gotoF"
				left_operand = stackOperands.pop()
				right_operand = ""
				result = ""
				global qCount
				qCount += 1
				quad = Quad(operator, left_operand, right_operand, result)
				queueQuads.append(quad)
				stackJumps.append(qCount)
				executionSource = ""
		if executionSource == "function":
			functionDirectory.dictionary[functionName].quadCount = qCount
			executionSource = ""


	def enterCondition(self, ctx):
		global executionSource
		executionSource = "condition"

	def enterC(self, ctx):
		operator = str(ctx.ELSE())
		if operator == "else":
			global qCount
			qCount += 1
			operator = "goto"
			left_operand = ""
			right_operand = ""
			result = ""
			quad = Quad(operator, left_operand, right_operand, result)
			queueQuads.append(quad)
			false = stackJumps.pop()
			stackJumps.append(qCount)
			queueQuads[false-1].rightOperand = qCount+1

	def exitC(self, ctx):
		end = stackJumps.pop()
		queueQuads[end-1].leftOperand = qCount+1

	def enterFunction(self, ctx):
		global executionSource
		executionSource = "function"
		global functionName
		functionName = str(ctx.ID())
		if functionName != "None":
			function = Function(0, 0, [], "")
			functionDirectory.insertFunc(functionName, function)
			# functionDirectory.printDirectory()

	def enterF1(self, ctx):
		global localVarTable
		localVarTable = VariableTable({}, ["int", "void", "bool", "char", "if", "else", "while", "print", "read", "return", "function", "id"])
		global varId
		varId = str(ctx.ID()) # cast to string to avoid dealing with TerminalNode objects
		if varId != "None":
			localVarTable.insertVariable(varId, varType, "global")
			global pCount
			pCount += 1
		# localVarTable.printTable()

	def enterF2(self, ctx):
		global localVarTable
		localVarTable = VariableTable({}, ["int", "void", "bool", "char", "if", "else", "while", "print", "read", "return", "function", "id"])
		global varId
		varId = str(ctx.ID()) # cast to string to avoid dealing with TerminalNode objects
		if varId != "None":
			localVarTable.insertVariable(varId, varType, "global")
			global pCount
			pCount += 1

	def exitF2(self, ctx):
		# insert into DirFunc the number of parameters defined (pCount)
		functionDirectory.dictionary[functionName].numParams = pCount

	def exitFunction(self, ctx):
		localVarTable.clearVariableTable()
		operator = "ENDPROC"
		left_operand = ""
		right_operand = ""
		result = ""
		global qCount
		qCount += 1
		quad = Quad(operator, left_operand, right_operand, result)
		queueQuads.append(quad)

def main(argv):
	global tCount
	global varTable
	global functionDirectory
	global stackOperands
	global stackOperators
	global stackTypes
	global stackJumps
	global queueQuads
	global executionSource # to indicate if "Section" block is being called from a condition or loop
	global qCount # quadruple count
	global pCount # parameter count (for functions)
	tCount = 0
	qCount = 0
	pCount = 0
	stackOperands = []
	stackOperators = []
	stackTypes = []
	stackJumps = []
	queueQuads = []
	executionSource = ""

	varTable = VariableTable({}, ["int", "void", "bool", "char", "if", "else", "while", "print", "read", "return", "function", "id"])
	functionDirectory = FunctionDirectory()
	lexer = CharmsLexer(StdinStream())
	stream = CommonTokenStream(lexer)
	parser = CharmsParser(stream)
	printer = CharmsPrintListener()
	walker = ParseTreeWalker()
	tree = parser.program()
	walker.walk(printer, tree)
	for quad in queueQuads:
		quad.printQuad()
	# print(Trees.toStringTree(tree, None, parser))

if __name__ == '__main__':
    main(sys.argv)
