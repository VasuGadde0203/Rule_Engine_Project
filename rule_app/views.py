from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .rule_engine import RuleEngine, Node, evaluate_rule_logic
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
import ast
from .models import Rule
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.http import Http404
import urllib.parse
from urllib.parse import unquote

def current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

engine = RuleEngine()

def home(request):
    return render(request, 'rule_app/index.html')

@csrf_exempt  # Only for testing; consider CSRF protection for production
def create_rule_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            rule_string = body.get("rule")
            # Replace logical operators to Python syntax
            # rule_string = rule_string.replace("AND", "and").replace("OR", "or")
            # rule_string = rule_string.replace("=", "==")
        
            if not rule_string:
                return JsonResponse({"error": "Rule string is required"}, status=400)
            
            
            ast_node = engine.create_rule(rule_string)

            ast_dict = {"ast": ast_node.to_dict()}

            # Create or update the rule in the database
            rule, created = Rule.objects.update_or_create(
                name="Rule",
                defaults={
                    'rule_string': rule_string,
                    'rule': ast_dict
                    }  # Save the rule string
            )

            # return JsonResponse({"ast": ast_node.to_dict()}, status=201)

            # Store the response data in the session
            request.session['ast_data'] = ast_dict

            # Redirect to the display page
            # return HttpResponseRedirect(reverse('display_rule'))
            return JsonResponse({"message": "Rule created successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:

            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def display_rule(request):
    # Retrieve data from session
    ast_data = request.session.get('ast_data', {})
    # ast_data_json = json.dumps(ast_data) 
    # Pass data to template
    return render(request, 'rule_app/display_rule.html', {'ast_data': ast_data})


@csrf_exempt
def combine_rules(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            rules = data.get("rules", [])
            combined_ast_node = engine.combining_rules(rules)
            # return JsonResponse({"combined_ast": repr(combined_ast)}, status=200)

            combined_ast_dict = {"ast": combined_ast_node.to_dict()}

            # Store the combined rule in the database
            combined_rule, created = Rule.objects.update_or_create(
                name="Combined Rule",
                defaults={
                    'rule_string': json.dumps(rules),  # Optionally store original rules as string
                    'combined_rule': combined_ast_dict  # Store combined AST as JSON
                }
            )
            request.session['combined_ast_data'] = combined_ast_dict
            return JsonResponse({'message': "Combined Rule created successfully"}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def combined_display_rule(request):
    combined_ast_data = request.session.get('combined_ast_data', {})
    return render(request, 'rule_app/combined_display_rule.html', {'combined_ast_data': combined_ast_data})

@csrf_exempt
def evaluate_rule(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ast = data['ast']
            # Replace 'null' with 'None' in the 'ast' string
            rule_ast_string = data['ast'].replace('null', 'None')

            # Parse the AST safely using ast.literal_eval instead of eval
            rule_ast = ast.literal_eval(rule_ast_string)

            input_data = data['data']
            result = engine.evaluate_rule(rule_ast['ast'], input_data)

            res, evaluation_details = evaluate_rule_logic(ast, input_data)
            
            return JsonResponse({
                "evaluation_details": evaluation_details,
                "result": res
            }, status=200)
            # return JsonResponse({"result": result}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def extract_rule_value(node, field_name):
    """Recursively search AST node to find comparison value for a specific field."""
    if isinstance(node, dict) and node.get('type') == 'operator':
        # Check left and right children for matching field
        if node['left'].get('value') == field_name and node['right'].get('type') == 'operand':
            return node['right']['value']
        # Recursively search left and right subtrees
        left_result = extract_rule_value(node['left'], field_name)
        right_result = extract_rule_value(node['right'], field_name)
        return left_result if left_result is not None else right_result
    return None