print('hello worlds')

import ast
import operator
import math

class Calculator:
	# safe operator mapping
	_ops = {
		ast.Add: operator.add,
		ast.Sub: operator.sub,
		ast.Mult: operator.mul,
		ast.Div: operator.truediv,
		ast.Pow: operator.pow,
		ast.USub: operator.neg,
		ast.UAdd: operator.pos,
	}

	def evaluate(self, expr: str):
		"""
		Evaluate a math expression safely using ast.
		Supports: + - * / ** unary +/-, parentheses, numbers.
		"""
		node = ast.parse(expr, mode='eval').body
		return self._eval(node)

	def _eval(self, node):
		if isinstance(node, ast.BinOp):
			left = self._eval(node.left)
			right = self._eval(node.right)
			op_type = type(node.op)
			if op_type in self._ops:
				return self._ops[op_type](left, right)
			raise ValueError(f"Unsupported operator: {op_type}")
		if isinstance(node, ast.UnaryOp):
			op_type = type(node.op)
			if op_type in self._ops:
				return self._ops[op_type](self._eval(node.operand))
			raise ValueError(f"Unsupported unary operator: {op_type}")
		if isinstance(node, ast.Num):  # Py <3.8
			return node.n
		if isinstance(node, ast.Constant):  # Py 3.8+
			if isinstance(node.value, (int, float)):
				return node.value
			raise ValueError("Only int/float constants are allowed")
		if isinstance(node, ast.Expr):
			return self._eval(node.value)
		raise ValueError(f"Unsupported expression: {type(node)}")

def repl():
	calc = Calculator()
	history = []
	print("Calculator REPL. Type 'help' for commands.")
	while True:
		try:
			line = input("calc> ").strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break
		if not line:
			continue
		if line.lower() in ("quit", "exit"):
			break
		if line.lower() == "help":
			print("Enter a math expression (e.g. 2 + 3*4). Commands: history, clear, help, quit")
			continue
		if line.lower() == "history":
			if not history:
				print("(no history)")
			else:
				for i, (expr, result) in enumerate(history, 1):
					print(f"{i}: {expr} = {result}")
			continue
		if line.lower() == "clear":
			history.clear()
			print("history cleared")
			continue
		# try evaluate expression
		try:
			result = calc.evaluate(line)
		except Exception as e:
			print("Error:", e)
			continue
		history.append((line, result))
		print(result)

if __name__ == "__main__":
	repl()