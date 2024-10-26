import ast
import operator
from datetime import datetime
from time import sleep

def current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # "operator" or "operand"
        self.left = left  # reference to left child node
        self.right = right  # reference to right child node
        self.value = value  # value for operands (e.g., age > 30)

    def __repr__(self):
        return f"Node(type={self.node_type}, value={self.value}, left={self.left}, right={self.right})"
    
    def to_dict(self):
        # Convert the Node to a dictionary for JSON serialization
        node_dict = {
            "type": self.node_type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
        }
        return node_dict

class RuleEngine:
    def __init__(self):
        self.ops = {
            'AND': operator.and_,
            'OR': operator.or_,
            '>': operator.gt,
            '<': operator.lt,
            '=': operator.eq,
            '>=': operator.ge,
            '<=': operator.le
        }

    def create_rule(self, rule_string):
        """Parses the rule string and generates an AST."""
        tree = ast.parse(rule_string, mode='eval')
        return self._build_ast(tree.body)

    def _build_ast(self, node):
        """Recursively build AST nodes from Python's AST."""
        if isinstance(node, ast.BinOp):
            left = self._build_ast(node.left)
            right = self._build_ast(node.right)
            op = self._get_operator(node.op)
            return Node(node_type="operator", left=left, right=right, value=op)
        elif isinstance(node, ast.Compare):
            left = self._build_ast(node.left)
            comparator = self._get_operator(node.ops[0])
            right = self._build_ast(node.comparators[0])
            return Node(node_type="operator", left=left, right=right, value=comparator)
        elif isinstance(node, ast.BoolOp):
            # Handle logical operators (AND, OR)
            op = self._get_operator(node.op)
            # Build left and right ASTs based on the values in the `values` list
            left = self._build_ast(node.values[0])
            right = self._build_ast(node.values[1])
            return Node(node_type="operator", left=left, right=right, value=op)
        elif isinstance(node, ast.Name):
            return Node(node_type="operand", value=node.id)
        elif isinstance(node, ast.Constant):
            return Node(node_type="operand", value=node.value)
        else:
            raise TypeError(f"Unknown AST node type: {type(node)}")


    def _get_operator(self, node):
        """Convert Python AST operators to engine-supported operators."""
        if isinstance(node, ast.And):
            return 'AND'
        if isinstance(node, ast.Or):
            return 'OR'
        if isinstance(node, ast.Gt):
            return '>'
        if isinstance(node, ast.Lt):
            return '<'
        if isinstance(node, ast.Eq):
            return '='
        if isinstance(node, ast.NotEq):
            return "!="
        if isinstance(node, ast.GtE):
            return '>='
        if isinstance(node, ast.LtE):
            return '<='
        raise TypeError(f"Unsupported operator: {type(node)}")

    def combining_rules(self, rules):
        """Combines multiple rules into a single AST."""
        combined_rule = None
        for rule in rules:
            rule_ast = self.create_rule(rule)
            if combined_rule is None:
                combined_rule = rule_ast
            else:
                combined_rule = Node("operator", left=combined_rule, right=rule_ast, value='AND')
        return combined_rule

    def evaluate_rule(self, node, data):
        """Evaluates the AST against the provided data."""
        print('hii')
        if node['type'] == "operator":
            left_val = self.evaluate_rule(node['left'], data)
            right_val = self.evaluate_rule(node['right'], data)
            return self.ops[node['value']](left_val, right_val)
        elif node['type'] == "operand":
            if isinstance(node['value'], str):
                return data.get(node['value'], None)
            return node['value']
        else:
            raise TypeError(f"Unknown node type: {node['type']}")

def evaluate_rule_logic(ast, rule_data):
    """
    Evaluates the rule based on the provided AST and rule data.

    Args:
        ast (str): The AST representation of the combined rules.
        rule_data (dict): The data containing values to evaluate against the rules.

    Returns:
        tuple: A boolean indicating if the rule passed and a list of evaluation details.
    """
    evaluation_details = []
    result = True  # Start with True for AND logic, adjust if needed

    # Assuming ast is a string representation of combined rules
    rules = ast.split(" AND ")  # Split on 'AND' for conjunctions

    for rule in rules:
        field, operator, value = parse_rule(rule.strip())
        
        # Get the actual value from rule_data
        actual_value = rule_data.get(field)
        detail = {
            'field': field,
            'entered_value': actual_value,
            'rule_criteria': f"{field} {operator} {value}"
        }

        if not evaluate_condition(actual_value, operator, value):
            result = False  # If any rule fails, overall result is False
        evaluation_details.append(detail)

    return result, evaluation_details

def parse_rule(rule):
    """
    Parses a rule into its components: field, operator, and value.

    Args:
        rule (str): The rule as a string.

    Returns:
        tuple: (field, operator, value)
    """
    if '>' in rule:
        field, value = rule.split('>')
        operator = '>'
    elif '<' in rule:
        field, value = rule.split('<')
        operator = '<'
    elif '>=' in rule:
        field, value = rule.split('>=')
        operator = '>='
    elif '<=' in rule:
        field, value = rule.split('<=')
        operator = '<='
    elif '==' in rule:
        field, value = rule.split('==')
        operator = '=='
    else:
        raise ValueError("Unsupported operator in rule")

    return field.strip(), operator.strip(), value.strip()

def evaluate_condition(actual_value, operator, value):
    """
    Evaluates the condition based on the operator.

    Args:
        actual_value: The actual value from rule data.
        operator (str): The operator (e.g., '>', '<', '==').
        value: The value to compare against.

    Returns:
        bool: True if the condition is satisfied, False otherwise.
    """
    # Convert value to int if it's numeric
    if isinstance(actual_value, int) and value.isdigit():
        value = int(value)
    elif isinstance(actual_value, str):
        value = str(value)  # Ensure comparison works correctly for strings

    if operator == '>':
        return actual_value > value
    elif operator == '<':
        return actual_value < value
    elif operator == '>=':
        return actual_value >= value
    elif operator == '<=':
        return actual_value <= value
    elif operator == '==':
        return actual_value == value
    else:
        raise ValueError("Unsupported operator for evaluation")

