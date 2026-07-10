# CareerLens Data Quality Report

Total Records: 123849

Total Columns: 37

Duplicate Job IDs: 0


---

## Missing Values (%)

- skills_desc: 98.03%
- salary_median: 94.93%
- salary_max: 75.94%
- salary_min: 75.94%
- pay_period: 70.87%
- compensation_type_salary: 70.87%
- annual_salary_usd: 70.87%
- pay_period_salary: 70.87%
- compensation_type: 70.87%
- currency_salary: 70.87%
- currency: 70.87%
- normalized_salary: 70.87%
- company_id: 1.39%
- description: 0.00%
- job_title: 0.00%
- company_name: 0.00%
- job_id: 0.00%
- application_type: 0.00%
- location: 0.00%
- views: 0.00%
- work_type_standardized: 0.00%
- work_type: 0.00%
- experience_level: 0.00%
- posting_time: 0.00%
- sponsored: 0.00%
- applies: 0.00%
- original_listed_time: 0.00%
- remote_allowed: 0.00%
- skills: 0.00%
- industries: 0.00%
- skill_count: 0.00%
- posting_year: 0.00%
- posting_month: 0.00%
- experience_bucket: 0.00%
- remote_classification: 0.00%
- salary_tier: 0.00%
- job_age_days: 0.00%

---

## Expected Columns

All expected columns exist.

---

## Salary Statistics

{'minimum': np.float64(0.0), 'maximum': np.float64(120000000.0), 'average': np.float64(79766.29)}

---

## Invalid Posting Dates

0

---

## Invalid Skill Counts

0

---

## Experience Bucket Distribution

experience_bucket
Senior Level    41489
Entry Level     38157
Unknown         29409
Mid Level        9826
Lead Level       4968

---

## Recommendations

- Continue using salary only where available.
- Consider extracting technologies from descriptions in Phase 2.
- Missing salary values are expected in job-posting datasets.
- Dataset is suitable for Power BI and SQL analytics.