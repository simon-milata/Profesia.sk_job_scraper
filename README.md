# Profesia.sk Job Scraper

This Python project is designed to scrape job listings from the profesia.sk website and insert them into a MySQL database. It provides a convenient way to gather job data for analysis or other purposes.

## Requirements
1. **Selenium**
2. **mysql.connector**

## Setup
1. **Create a database:**<br>
```sql
CREATE DATABASE database_name;
```
2. **Use the newly created database:**<br>
```sql
USE database_name;
```
3. **Create a table:** <br>
```sql
CREATE TABLE table_name(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    employer VARCHAR(200) NOT NULL,
    address VARCHAR(200),
    pay VARCHAR(6) NOT NULL
);
```
## Usage
1. **Clone the repository:**
```shell
git clone https://github.com/Tamzuu/Profesia.sk_job_scraper.git
```
2. **Navigate to the project directory:**
```shell
cd profesia.sk_job_scraper
```
3. **Run the scraper script:**
```shell
python main.py
```
4. **The script will prompt you to enter search criteria for job listings. Follow the prompts to initiate the scraping process.**
