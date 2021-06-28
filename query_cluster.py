from sqlalchemy import create_engine
from matplotlib import pyplot as plt
import pandas as pd
import os

aws_user = os.environ.get('AWS_USER')
aws_password = os.environ.get('AWS_PASSWORD')
aws_host = os.environ.get('AWS_HOST')
aws_port = os.environ.get('AWS_PORT')
aws_db = os.environ.get('AWS_DB')
url = f"postgresql://{aws_user}:{aws_password}@{aws_host}:{aws_port}/{aws_db}"

engine = create_engine(url)
queries = [
    """select avg(trip_distance) from trips
    where passenger_count <= 2;""",

    """select vendors.name as Vendor, sum(total_amount) as Total from trips
    join vendors on trips.vendor_id=vendors.vendor_id
    group by Vendor
    order by total desc
    limit 3;""",

    """select count(*) as Cash_Only, Datepart(Month,pickup_datetime) as Month, Datepart(Year, pickup_datetime) as Year from trips
    join payment on payment.payment_type=trips.payment_type
    where payment_lookup = 'Cash'
    group by Month, Year
    order by Year, Month
    ;""",

    """select count(*) as Not_Cash, Datepart(Month,pickup_datetime) as Month, Datepart(Year, pickup_datetime) as Year from trips
    join payment on payment.payment_type=trips.payment_type
    where payment_lookup != 'Cash'
    group by Month, Year
    order by Year, Month
    ;""",

    """select count(*) as Tips, Datepart(dayofyear, pickup_datetime) as Date from trips
    where tip_amount > 0
    and Datepart(Year,pickup_datetime) = 2012 and Datepart(Month,pickup_datetime) between 10 and 12
    group by Date
    order by Date
    ;""",

    """select count(*) as Tips, Datepart(Day,pickup_datetime) as Day, Datepart(Month, pickup_datetime) as Month from trips
    where tip_amount > 0
    and Datepart(Year,pickup_datetime) = 2012 and Datepart(Month,pickup_datetime) between 10 and 12
    group by Day, Month
    order by Month, Day
    ;""",

    """select avg(datediff(seconds, pickup_datetime, dropoff_datetime)) as Average_sec from trips
    where date_part(weekday, pickup_datetime) in (6, 0);"""
]

# Question 1
question1 = pd.read_sql(queries[0], engine)
question1.to_csv('Results/question1.csv', index=False)
question1 = pd.read_csv('Results/question1.csv')
print(question1)

# Question 2
question2 = pd.read_sql(queries[1], engine)
question2.to_csv('Results/question2.csv', index=False)
question2 = pd.read_csv('Results/question2.csv')
print(question2)

# Question 3
question3a = pd.read_sql(queries[2], engine)
question3a.to_csv('Results/question3a.csv', index=False)
question3a = pd.read_csv('Results/question3a.csv', index_col=['month', 'year'])

question3b = pd.read_sql(queries[3], engine)
question3b.to_csv('Results/question3b.csv', index=False)
question3b = pd.read_csv('Results/question3b.csv', index_col=['month', 'year'])

question3 = question3a.join(question3b, on=['month', 'year'])
question3.to_csv('Results/question3.csv')
question3 = pd.read_csv('Results/question3.csv', index_col=['month', 'year'])

question3.plot(kind='bar', title='Number of rides paid with and without cash', xlabel='(Month, Year)', ylabel='Count')
plt.tight_layout()
plt.savefig('Results/question3.png')

# question3a.plot(kind='bar', title='Number of rides with tips', xlabel='x_label', ylabel='y_label')
# plt.savefig('Results/question3a.png')

# question3b.plot(kind='bar', title='Number of rides with tips', xlabel='x_label', ylabel='y_label')
# plt.savefig('Results/question3b.png')

print(question3)

# Question 4
question4a = pd.read_sql(queries[4], engine)
question4a.to_csv('Results/question4a.csv', index=False)
question4a = pd.read_csv('Results/question4a.csv', index_col='date')
question4a.plot(kind='line', title='Number of rides with tips', xlabel='# of day of the year', ylabel='Count')
plt.tight_layout()
plt.savefig('Results/question4a_line.png')
question4a.plot(kind='bar', title='Number of rides with tips', xlabel='# of day of the year', ylabel='Count')
plt.tight_layout()
plt.savefig('Results/question4a_bar.png')
print(question4a)

question4b = pd.read_sql(queries[5], engine)
question4b.to_csv('Results/question4b.csv', index=False)
question4b = pd.read_csv('Results/question4b.csv', index_col=['day', 'month'])
question4b.plot(kind='line', title='Number of rides with tips', xlabel='(Day, Month)', ylabel='Count')
plt.tight_layout()
plt.savefig('Results/question4b_line.png')
question4b.plot(kind='bar', title='Number of rides with tips', xlabel='(Day, Month)', ylabel='Count')
plt.tight_layout()
plt.savefig('Results/question4b_bar.png')
print(question4b)

# Question 5
question5 = pd.read_sql(queries[6], engine)
question5.to_csv('Results/question5.csv', index=False)
question5 = pd.read_csv('Results/question5.csv')
print(question5)

#TODO Extra Geolocation