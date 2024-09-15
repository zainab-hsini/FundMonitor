# FundMonitor: Crowdfunding Campaign Data Scraper & Analysis

## Project Overview

FundMonitor is a Python project that scrapes data from the crowdfunding platform Chuffed.org, which hosts campaigns to raise funds for social, community, and charitable causes. The primary goal of this scraper is to extract data related to active campaigns and analyze the performance based on:

- Categories (e.g., Community, Environment, Refugees and Asylum Seekers)
- Locations (e.g., Canada, Australia, United States, United Kingdom)

The program calculates and compares:

- The average money raised per category and location
- The average fund percentage achieved per category and location
- The average money raised per day per category and location

The results provide insights into the most successful categories and locations for fundraising, making it useful for organizations or individuals interested in understanding which types of campaigns perform the best.

## Purpose

The main purpose of FundMonitor is to provide an analysis of the best-performing crowdfunding campaigns based on category and location. By scraping and analyzing this data, the project aims to:

- Identify trends in fundraising success
- Highlight the best categories and locations for fundraising
- Provide data-driven insights to campaigners for optimizing their strategies

## Website

The data is scraped from Chuffed.org, a popular crowdfunding platform focused on social impact projects. Chuffed.org was chosen because it hosts a wide variety of campaigns related to community and social projects, making it an ideal source for analyzing trends across different regions and campaign types.

## Output

Here is a sample output from running the program:

Category Analysis:  
Community:  
Average Money Raised (USD): 869930.25 USD  
Average Fund Percentage: 58.00%  
Average Money Raised Per Day (USD): 3624.71 USD  

Environment:  
Average Money Raised (USD): 169281.00 USD  
Average Fund Percentage: 53.42%  
Average Money Raised Per Day (USD): 4575.16 USD  

Location Analysis:  
Canada:  
Average Money Raised (USD): 869930.25 USD  
Average Fund Percentage: 58.00%  
Average Money Raised Per Day (USD): 3624.71 USD  

United Kingdom:  
Average Money Raised (USD): 51973.75 USD  
Average Fund Percentage: 21.82%  
Average Money Raised Per Day (USD): 4949.88 USD  

Conclusion:  
Best Average Money Raised:  
Category: Community - 869930.25 USD  
Location: Canada - 869930.25 USD  

Best Average Fund Percentage:  
Category: Refugees and Asylum Seekers - 100.41%  
Location: Australia - 82.08%  

Best Average Money Raised Per Day:  
Category: Environment - 4575.16 USD  
Location: United Kingdom - 4949.88 USD  

## Dependencies

The project uses the following external libraries, listed in `requirements.txt`:

- `requests` - For sending HTTP requests to retrieve HTML content from the website.
- `beautifulsoup4` - For parsing the HTML content and extracting the relevant data.

To install these dependencies, run:

pip install -r requirements.txt

## Running the Program

To run the program and analyze the scraped data, use the following command:

python3 main.py

This will execute the scraper and perform an analysis of the campaigns based on category and location.

## Potential Use of FundMonitor

FundMonitor collects valuable data on social causes and their fundraising performance, including the amount raised, geographic location, and pace of fundraising. This dataset can benefit multiple sectors by enabling more informed decision-making and strategic interventions. Here’s how:

- **Nonprofits** can optimize their campaigns and benchmark their performance to improve fundraising outcomes and strategy.
- **Philanthropists and donors** can allocate funds more effectively by targeting high-impact or underfunded causes.
- **Corporations** involved in **Corporate Social Responsibility (CSR)** can align their giving with causes that resonate most with their stakeholders.
- **Governments** can use the data to support policymaking, ensuring that resources are allocated where they are most needed.
- **Academics** and **researchers** can study social behavior and cause effectiveness, identifying trends and donor motivations.
- **Media and journalists** can raise public awareness of underfunded causes, contributing to more visibility and engagement.
- **Investors** focused on social impact can make informed decisions by identifying causes that offer measurable returns.
- **Technology providers** like fundraising platforms can use the data to improve user experiences and develop predictive models for future trends.

By providing these insights, FundMonitor creates a positive feedback loop that helps drive support for social causes and enables organizations to maximize their impact.
