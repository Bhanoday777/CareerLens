-- Total Jobs
SELECT
                COUNT(*) AS total_jobs
            FROM jobs;

-- Top Hiring Companies
SELECT
                company_name,
                COUNT(*) AS hiring_count
            FROM jobs
            GROUP BY company_name
            ORDER BY hiring_count DESC
            LIMIT 10;

-- Top Hiring Locations
SELECT
                location,
                COUNT(*) AS hiring_count
            FROM jobs
            GROUP BY location
            ORDER BY hiring_count DESC
            LIMIT 10;

-- Top Industries
SELECT
                industries,
                COUNT(*) AS hiring_count
            FROM jobs
            GROUP BY industries
            ORDER BY hiring_count DESC
            LIMIT 10;

-- Average Salary
SELECT
                ROUND(
                    AVG(annual_salary_usd),
                    2
                ) AS average_salary
            FROM jobs
            WHERE annual_salary_usd
            IS NOT NULL;

-- Highest Paying Companies
SELECT
                company_name,
                ROUND(
                    AVG(annual_salary_usd),
                    2
                ) AS average_salary
            FROM jobs
            WHERE annual_salary_usd
            IS NOT NULL
            GROUP BY company_name
            ORDER BY average_salary DESC
            LIMIT 10;

-- Experience Distribution
SELECT
                experience_bucket,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY experience_bucket;

-- Remote Distribution
SELECT
                remote_classification,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY remote_classification;

-- Monthly Hiring
SELECT
                posting_month,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY posting_month
            ORDER BY posting_month;

-- Yearly Hiring
SELECT
                posting_year,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY posting_year;

