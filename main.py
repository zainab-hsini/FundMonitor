import requests
from bs4 import BeautifulSoup
import json
import re
from collections import defaultdict

# Fixed exchange rates as of today (can be updated manually if needed)
exchange_rates = {
    "USD": 1,       # USD to USD
    "CAD": 0.75,    # Canadian Dollar to USD
    "EUR": 1.10,    # Euro to USD
    "GBP": 1.25,    # British Pound to USD
    # Add other currencies as necessary
}

# Function to convert currencies to USD
def convert_to_usd(amount, currency, rates):
    # Skip if currency is already in USD
    if currency == 'USD':
        return amount
    
    # Convert to USD using the fixed exchange rate if available, otherwise return the original amount
    if currency in rates:
        return amount * rates[currency]  # Convert using the fixed rate
    return amount  # If we don't have the exchange rate, return the original amount

# Function to scrape from the website
def scrape(url):
    # Error handling
    try:
        response = requests.get(url)
        # Error handling
        if response.status_code != 200:
            print(f"Failed to scrape. Code: {response.status_code}")
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the script tag containing the data
        script_tag = soup.find('script', string=re.compile('window.Chuffed.campaigns'))  # Use 'string'

        # Error handling if the script tag was not found
        if not script_tag:
            print("Couldn't find the campaigns script tag.")
            return None
        
        # Extract the script content
        script_content = script_tag.string
        
        # Use regex to extract JSON-like data
        json_data_match = re.search(r'window.Chuffed.campaigns = ({.*});', script_content, re.DOTALL)

        # Error handling
        if not json_data_match:
            print("Couldn't extract the JSON data.")
            return None
        
        json_data = json_data_match.group(1)
        
        # Convert to a proper Python dictionary
        campaigns_data = json.loads(json_data.replace("window.Chuffed.campaigns = ", ""))
        
        return campaigns_data

    # Error handling
    except Exception as e:
        print(f"Error: {e}")
        return None


# Function to extract country information
def get_country_from_location(location):
    # Split the location by commas and strip spaces, returning the last part (the country)
    return location.split(',')[-1].strip()

# Function to calculate average data for display
def calculate_campaign_metrics(data, rates):

    # Calculate average money raised, target, fund percentage, and average time period for each category and location
    category_data = defaultdict(lambda: {'moneyRaised': 0, 'totalTarget': 0, 'fundPercentages': [], 'totalTimePeriods': [], 'numCampaigns': 0})
    location_data = defaultdict(lambda: {'moneyRaised': 0, 'totalTarget': 0, 'fundPercentages': [], 'totalTimePeriods': [], 'numCampaigns': 0})

    # For each campaign in the extract relevant data and store them
    for campaign in data['data']:
        category = campaign.get('focus')
        location = get_country_from_location(campaign.get('location'))  # Extract only the country
        money_raised = campaign.get('moneyRaised', 0)
        target = campaign.get('target', 1)  # Avoid division by zero
        currency = campaign.get('currency', 'USD')  # Default to USD if not provided
        time_left = campaign.get('timeLeftInWords')
        
        # Convert money raised and target to USD
        money_raised_usd = convert_to_usd(money_raised, currency, rates)
        target_usd = convert_to_usd(target, currency, rates)
        
        # Calculate fund percentage
        fund_percentage = (money_raised_usd / target_usd) * 100
        
        # Calculate the average time period from "timeLeftInWords"
        time_period_days = extract_days_from_time(time_left)
        
        # Update category data
        category_data[category]['moneyRaised'] += money_raised_usd
        category_data[category]['totalTarget'] += target_usd
        category_data[category]['fundPercentages'].append(fund_percentage)
        category_data[category]['totalTimePeriods'].append(time_period_days)
        category_data[category]['numCampaigns'] += 1

        # Update location data
        location_data[location]['moneyRaised'] += money_raised_usd
        location_data[location]['totalTarget'] += target_usd
        location_data[location]['fundPercentages'].append(fund_percentage)
        location_data[location]['totalTimePeriods'].append(time_period_days)
        location_data[location]['numCampaigns'] += 1

    return category_data, location_data

# Function to convert days in words to number
def extract_days_from_time(time_left_in_words):
    time_map = {"day": 1, "week": 7, "month": 30, "year": 365}  # A rough mapping for conversion to days
    time_period = 0
    # Extract the number and unit from the time left in words (e.g., "2 days", "3 weeks", "1 month", "4 years") using regular expressions
    match = re.search(r'(\d+)\s*(day|week|month|year)', time_left_in_words)
    if match:
        number = int(match.group(1))
        unit = match.group(2)
        time_period = number * time_map.get(unit, 0)
    return time_period

# Functino to find the best category and location
def find_best(data, label):
    best_value = float('-inf')
    best_key = None
    for key, value in data.items():
        if value > best_value:
            best_value = value
            best_key = key
    return best_key, best_value

# Functino to calculate the average
def calculate_averages(data):
    metrics = {
        'Average Money Raised': {},
        'Average Fund Percentage': {},
        'Average Money Raised Per Day': {}
    }

    # Display the results for each category and location
    for key, value in data.items():
        num_campaigns = value['numCampaigns']
        if num_campaigns == 0:
            continue
        
        # Calculate averages
        average_fund_percentage = sum(value['fundPercentages']) / num_campaigns
        average_money_raised = value['moneyRaised'] / num_campaigns
        average_money_raised_per_day = value['moneyRaised'] / (sum(value['totalTimePeriods']) or 1)  # Avoid division by zero
        
        # Store values in metrics dictionary
        metrics['Average Money Raised'][key] = average_money_raised
        metrics['Average Fund Percentage'][key] = average_fund_percentage
        metrics['Average Money Raised Per Day'][key] = average_money_raised_per_day
        
        # Display results
        print(f"{key}:")
        print(f"  Average Money Raised (USD): {average_money_raised:.2f} USD")
        print(f"  Average Fund Percentage: {average_fund_percentage:.2f}%")
        print(f"  Average Money Raised Per Day (USD): {average_money_raised_per_day:.2f} USD")
        print("-----")

    return metrics

# Display conclusion on the location and category with the best performance
def print_conclusion(category_metrics, location_metrics):
    # Find best category and location for each metric
    print("\nConclusion:")

    # For each metric
    for metric_name in ['Average Money Raised', 'Average Fund Percentage', 'Average Money Raised Per Day']:
        best_category, best_category_value = find_best(category_metrics[metric_name], "Category")
        best_location, best_location_value = find_best(location_metrics[metric_name], "Location")
        
        # Formatting numbers
        if metric_name == 'Average Fund Percentage':
            print(f"Best {metric_name}:")
            print(f"  Category: {best_category} - {best_category_value:.2f}%")
            print(f"  Location: {best_location} - {best_location_value:.2f}%")
        else:
            print(f"Best {metric_name}:")
            print(f"  Category: {best_category} - {best_category_value:.2f} USD")
            print(f"  Location: {best_location} - {best_location_value:.2f} USD")
        print("-----")


# Main function
def main():
    # url to the website
    url = "https://chuffed.org/discover"
    data = scrape(url)

    # Error handling
    if not data:
        return
    
    # Use the fixed exchange rates defined earlier
    category_data, location_data = calculate_campaign_metrics(data, exchange_rates)
    
    print("Category Analysis:")
    category_metrics = calculate_averages(category_data)
    
    print("\nLocation Analysis:")
    location_metrics = calculate_averages(location_data)
    
    # Display conclusion
    print_conclusion(category_metrics, location_metrics)

if __name__ == "__main__":
    main()