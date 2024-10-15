const API_URL = 'http://localhost:8000'; // Adjust if your backend is hosted elsewhere

document.addEventListener('DOMContentLoaded', () => {
  // Fetch unique ingredients, regions, and countries from the backend
  fetchUniqueOptions();

  // Update weight display values
  const sliders = document.querySelectorAll('.slider input[type="range"]');
  sliders.forEach(slider => {
    const span = slider.nextElementSibling;
    slider.addEventListener('input', () => {
      span.textContent = slider.value;
    });
  });

  // Handle form submission
  const form = document.getElementById('recipe-form');
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    await getRecommendations();
  });

  // Handle "Get Another Recipe" button
  const nextRecipeButton = document.getElementById('next-recipe-button');
  nextRecipeButton.addEventListener('click', displayNextRecipe);

  // Handle ingredient selection changes
  const ingredientsSelect = document.getElementById('ingredients');
  const selectedIngredientsList = document.getElementById('selected-ingredients-list');

  ingredientsSelect.addEventListener('change', () => {
    // Clear the list of selected ingredients
    selectedIngredientsList.innerHTML = '';

    // Get the selected options and display them in the selected ingredients list
    const selectedOptions = Array.from(ingredientsSelect.selectedOptions);
    selectedOptions.forEach(option => {
      const listItem = document.createElement('li');
      listItem.textContent = option.textContent;
      selectedIngredientsList.appendChild(listItem);
    });
  });
});

let selectedRecipes = [];
let recipeOffset = 0;

async function fetchUniqueOptions() {
  // Fetch ingredients
  const ingredientsResponse = await fetch(`${API_URL}/unique_ingredients`);
  const ingredients = await ingredientsResponse.json();
  const ingredientsSelect = document.getElementById('ingredients');
  ingredients.forEach(ingredient => {
    const option = document.createElement('option');
    option.value = ingredient;
    option.textContent = ingredient;
    ingredientsSelect.appendChild(option);
  });

  // Fetch regions
  const regionsResponse = await fetch(`${API_URL}/unique_regions`);
  const regions = await regionsResponse.json();
  const regionSelect = document.getElementById('region');
  const defaultOption = document.createElement('option');
  defaultOption.value = '';
  defaultOption.textContent = '--Select Region--';
  regionSelect.appendChild(defaultOption);
  regions.forEach(region => {
    const option = document.createElement('option');
    option.value = region;
    option.textContent = region;
    regionSelect.appendChild(option);
  });

  // Fetch countries
  const countriesResponse = await fetch(`${API_URL}/unique_countries`);
  const countries = await countriesResponse.json();
  const countrySelect = document.getElementById('country');
  const defaultCountryOption = document.createElement('option');
  defaultCountryOption.value = '';
  defaultCountryOption.textContent = '--Select Country--';
  countrySelect.appendChild(defaultCountryOption);
  countries.forEach(country => {
    const option = document.createElement('option');
    option.value = country;
    option.textContent = country;
    countrySelect.appendChild(option);
  });
}

async function getRecommendations() {
  // Collect form data
  const formData = new FormData(document.getElementById('recipe-form'));

  const meal_type = formData.get('meal_type');
  const calories = formData.get('calories');
  const carbs = formData.get('carbs');
  const protein = formData.get('protein');
  const fat = formData.get('fat');
  const ingredients = Array.from(document.getElementById('ingredients').selectedOptions).map(option => option.value);
  const diet_type = formData.get('diet_type');
  const region = formData.get('region');
  const country = formData.get('country');
  const cook_time = formData.get('cook_time');
  const flexible_matching = formData.get('flexible_matching') === 'on';

  const weights = {
    'meal_type': parseFloat(formData.get('meal_type_weight')),
    'diet_type': parseFloat(formData.get('diet_type_weight')),
    'region': parseFloat(formData.get('region_weight')),
    'cook_time': parseFloat(formData.get('cook_time_weight')),
    'calories': parseFloat(formData.get('calories_weight')),
    'carbs': parseFloat(formData.get('carbs_weight')),
    'protein': parseFloat(formData.get('protein_weight')),
    'fat': parseFloat(formData.get('fat_weight')),
    'ingredients': parseFloat(formData.get('ingredients_weight')),
    'country': parseFloat(formData.get('country_weight')),
  };

  const requestData = {
    meal_type,
    calories,
    carbs,
    protein,
    fat,
    diet_type,
    region,
    cook_time,
    ingredients,
    country,
    weights,
    flexible: flexible_matching
  };

  // Send request to backend
  const response = await fetch(`${API_URL}/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  });

  if (response.status === 200) {
    selectedRecipes = await response.json();
    recipeOffset = 0;
    if (selectedRecipes.length > 0) {
      displayRecipeInfo(selectedRecipes[recipeOffset]);
      document.getElementById('next-recipe-button').style.display = 'block';
    } else {
      alert('No matching recipes found. Please adjust your criteria and try again.');
      document.getElementById('recipe-container').innerHTML = '';
      document.getElementById('next-recipe-button').style.display = 'none';
    }
  } else {
    alert('Failed to get recommendations from the backend.');
  }
}

async function displayRecipeInfo(recipeName) {
  const response = await fetch(`${API_URL}/recipe/${recipeName}`);
  if (response.status === 200) {
    const info = await response.json();
    const container = document.getElementById('recipe-container');
    container.innerHTML = '';

    const title = document.createElement('h2');
    title.textContent = info.name;
    container.appendChild(title);

    const description = document.createElement('p');
    description.innerHTML = `<strong>Description:</strong> ${info.description || 'N/A'}`;
    container.appendChild(description);

    const mealType = document.createElement('p');
    mealType.innerHTML = `<strong>Meal Type:</strong> ${info.meal_type.join(', ')}`;
    container.appendChild(mealType);

    const dietType = document.createElement('p');
    dietType.innerHTML = `<strong>Diet Type:</strong> ${info.diet_type.join(', ')}`;
    container.appendChild(dietType);

    const healthType = document.createElement('p');
    healthType.innerHTML = `<strong>Health Type:</strong> ${info.health_type.join(', ')}`;
    container.appendChild(healthType);

    const region = document.createElement('p');
    region.innerHTML = `<strong>Region:</strong> ${info.region.join(', ')}`;
    container.appendChild(region);

    const country = document.createElement('p');
    country.innerHTML = `<strong>Country:</strong> ${info.country.join(', ')}`;
    container.appendChild(country);

    const cookTime = document.createElement('p');
    cookTime.innerHTML = `<strong>Cook Time:</strong> ${info.cook_time}`;
    container.appendChild(cookTime);

    const ingredients = document.createElement('div');
    ingredients.innerHTML = `<h3>🥗 Ingredients</h3><ul>${info.ingredients.map(ing => `<li>${ing}</li>`).join('')}</ul>`;
    container.appendChild(ingredients);

    const instructions = document.createElement('div');
    instructions.innerHTML = `<h3>📝 Instructions</h3><p>${formatInstructions(info.instructions)}</p>`;
    container.appendChild(instructions);

    const nutritionFacts = document.createElement('div');
    nutritionFacts.innerHTML = `
      <h3>🍏 Basic Nutrition Facts</h3>
      <p><strong>Calories:</strong> ${info.nutrition_facts.Calories}</p>
      <p><strong>Fat:</strong> ${info.nutrition_facts.FatContent}</p>
      <p><strong>Carbs:</strong> ${info.nutrition_facts.CarbohydrateContent}</p>
      <p><strong>Protein:</strong> ${info.nutrition_facts.ProteinContent}</p>
    `;
    container.appendChild(nutritionFacts);

    const detailedNutrition = document.createElement('div');
    detailedNutrition.innerHTML = `
      <h3>🍎 Detailed Nutrition Facts</h3>
      <p><strong>Fiber:</strong> ${info.nutrition_facts.FiberContent}</p>
      <p><strong>Sugar:</strong> ${info.nutrition_facts.SugarContent}</p>
      <p><strong>Sodium:</strong> ${info.nutrition_facts.SodiumContent}</p>
      <p><strong>Cholesterol:</strong> ${info.nutrition_facts.CholesterolContent}</p>
      <p><strong>Saturated Fat:</strong> ${info.nutrition_facts.SaturatedFatContent}</p>
    `;
    container.appendChild(detailedNutrition);

    // Display images similar to streamlit_image_select
    if (info.images && info.images.length > 0) {
      const imageContainer = document.createElement('div');
      imageContainer.innerHTML = `<h3>📷 Images</h3>`;
      const imageSelect = document.createElement('select');
      info.images.forEach((imgUrl, index) => {
        const option = document.createElement('option');
        option.value = imgUrl;
        option.textContent = `Image ${index + 1}`;
        imageSelect.appendChild(option);
      });
      imageContainer.appendChild(imageSelect);

      const imageDisplay = document.createElement('img');
      imageDisplay.src = info.images[0];
      imageDisplay.alt = info.name;
      imageDisplay.className = 'recipe-image';
      imageContainer.appendChild(imageDisplay);

      imageSelect.addEventListener('change', () => {
        imageDisplay.src = imageSelect.value;
      });

      container.appendChild(imageContainer);
    } else {
      const noImages = document.createElement('p');
      noImages.textContent = 'No images available.';
      container.appendChild(noImages);
    }
  } else {
    alert('Recipe not found.');
  }
}

function formatInstructions(instructions) {
  // Use regular expressions to split instructions based on the pattern n-)
  const instructionsList = instructions.split(/(\d+-\))/);
  let formattedInstructions = '';
  let step = '';
  instructionsList.forEach(item => {
    if (/^\d+-\)/.test(item)) {
      if (step) {
        formattedInstructions += step.trim() + '<br>';
      }
      step = item;
    } else {
      step += ' ' + item.trim();
    }
  });
  if (step) {
    formattedInstructions += step.trim();
  }
  return formattedInstructions;
}

function displayNextRecipe() {
  recipeOffset += 1;
  if (recipeOffset < selectedRecipes.length) {
    displayRecipeInfo(selectedRecipes[recipeOffset]);
  } else {
    alert("You've reached the end of the recommendations.");
    recipeOffset = selectedRecipes.length - 1;
  }
}
