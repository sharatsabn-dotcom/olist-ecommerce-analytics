import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql+psycopg2://postgres:{db_password}@localhost:5432/olist_analytics")

order_reviews_df = pd.read_csv("data/olist_order_reviews_dataset.csv")

order_reviews_df = order_reviews_df.drop_duplicates(subset="review_id", keep="first")
# Keep only the columns that exist in our products table


# Clear out any partial/previous data so we can safely re-run
with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE order_reviews RESTART IDENTITY CASCADE"))
    conn.commit()


order_reviews_df.to_sql(
    "order_reviews",
    engine,
    if_exists="append",
    index=False
)

print("Order_reviews loaded successfully!")
