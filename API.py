# Name: Chloe Fenner
# Date: September 23, 2024

import requests
import json

def search_recipes(query, diet=None, health=None, cuisineType=None, mealType=None, calories=None):
    url = "https://api.edamam.com/search"  # API endpoint
    params = {
        "q": query,
        "app_id": "d4bedc5e",  # Replace with your actual app ID
        "app_key": "91ff2193a48f4e6267a512771a9578dd",  # Replace with your actual app key
        "diet": diet,
        "health": health,
        "cuisineType": cuisineType,
        "mealType": mealType,
        "Calories": calories
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)

        # Ensure the response is in JSON format
        if 'application/json' in response.headers['Content-Type']:
            data = response.json()  # Parse JSON response
        else:
            raise ValueError("The response is not in JSON format")
        
        # Extract the first 5 recipes with additional information
        recipes = data.get("hits", [])
        minimal_output = []
        for recipe in recipes[:5]:  # Limit to first 5 recipes
            recipe_info = recipe.get("recipe", {})
            nutrition_info = recipe_info.get("totalNutrients", {})

            minimal_output.append({
                "label": recipe_info.get("label"),
                "url": recipe_info.get("url"),  # Include the recipe URL
                "tag": recipe_info.get("uri").split("#")[-1],  # Extract tag from URI (example format)
                "schemaOrgTag": recipe_info.get("schemaOrgTag"),
                "total": nutrition_info.get("ENERC_KCAL", {}).get("quantity"),  # Total calories
                "hasRDI": True,  # Assuming it has RDI information
                "daily": nutrition_info.get("ENERC_KCAL", {}).get("daily"),  # Daily value of calories
                "unit": "kcal",   # Unit for energy (calories)
                "ingredients": recipe_info.get("Ingredients", [])
            })

        return minimal_output  # Return the minimal information as a list

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except ValueError as json_err:
        print(f"JSON error: {json_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# User input for recipe search
query = input("Enter the ingredient or dish you want to search for: ")

# Optional user inputs, leave blank for no specific filter
diet = input("Enter diet type (e.g., low-carb, balanced), or leave blank: ") or None
health = input("Enter health restrictions (e.g., peanut-free, vegan), or leave blank: ") or None
cuisineType = input("Enter cuisine type (e.g., Asian, Italian), or leave blank: ") or None
mealType = input("Enter meal type (e.g., Breakfast, Dinner), or leave blank: ") or None
min_calories = input("Enter minimum calories (or leave blank): ") or None
max_calories = input("Enter maximum calories (or leave blank): ") or None

# Call the function with user inputs
recipes = search_recipes(query, diet, health, cuisineType, mealType)

if recipes:
    # Print the output in the desired format
    for recipe in recipes:
        print(json.dumps(recipe, indent=4))  # Print each recipe as a formatted JSON
