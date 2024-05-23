import os

import pandas as pd
from catboost import CatBoostRegressor
from data.models import UserBook
import keras
from django.db import connection
import pickle
from sklearn.preprocessing import LabelEncoder


class RecSys:
    def __init__(self):
        self.book_embedding_model = keras.models.load_model(os.path.join(os.path.dirname(__file__), 'static', "embedding_book_model.keras"))
        self.user_embedding_model = keras.models.load_model(os.path.join(os.path.dirname(__file__), 'static', "embedding_user_model.keras"))
        model = CatBoostRegressor()
        self.main_model = model.load_model(os.path.join(os.path.dirname(__file__), 'static', 'main_model.cbm'))
        with open(os.path.join(os.path.dirname(__file__), 'static', 'label_encoder_book.pkl'), 'rb') as fl:
            self.le = pickle.load(fl)

    def get_recommendations(self, user_id, n=10):
        query = """
        WITH user_data AS (
          -- Проверь, что одна строчка
          SELECT user_id, location, age
          FROM main_user
          WHERE user_id = 278856
        ),
        user_interactions as (
          SELECT
          user_id,
          book_id,
            rating
          FROM data_userbook ub
          WHERE user_id = 278856
        )
        SELECT
        	mu.user_id as user_id,
        	location,
        	age,
        	ub.book_id as book_id,
            author as book_author,
            year_of_1st_publication as year_of_publication,
            genre as category,
            rating as book_rating
        FROM data_book ub
        CROSS JOIN user_data mu
        LEFT JOIN user_interactions ui ON mu.user_id = ui.user_id AND ub.book_id = ui.book_id
        WHERE rating IS NULL
        """

        # Execute the query and fetch the data
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Create a DataFrame
        data = pd.DataFrame(data)
        known_labels = set(self.le.classes_)
        data = data[data['book_id'].isin(known_labels)]
        data['book_id'] = self.le.transform(data['book_id'])

        user_feature = self.user_embedding_model.predict(x=[data['user_id'], data['book_id']]).reshape((data.shape[0], 32)).tolist()
        user_df = pd.DataFrame(user_feature)
        user_df = user_df.add_suffix('_user')
        book_feature = self.book_embedding_model.predict(x=[data['user_id'], data['book_id']]).reshape((data.shape[0], 32)).tolist()
        book_df = pd.DataFrame(book_feature)
        book_df = book_df.add_suffix('_book')
        data_copy = data.copy()
        data = data.drop(columns=['user_id', 'book_id'])
        data = pd.concat([data, user_df, book_df], axis=1)
        X = data.drop(columns=['book_rating']).dropna()

        cat_features = ['book_author', 'location', 'category']
        predictions = self.main_model.predict(X).tolist()
        data_copy['book_id'] = self.le.inverse_transform(data_copy['book_id'])
        recommendations = pd.DataFrame({'book_id': data_copy.iloc[X.index]['book_id'], 'rating': predictions})
        recommendations = recommendations.sort_values(by='rating', ascending=False)
        return recommendations.head(n)['book_id'].tolist()

    def get_user_history(self, user_id, n=10):
        result = UserBook.objects.raw(f"""
        SELECT id, book_id
        FROM data_userbook
        WHERE user_id = {user_id}
        """)
        return [user_book.book_id for user_book in result]

    def get_popular_books(self, n=10):
        result = UserBook.objects.raw(
            f"""
            SELECT
                id,
                book_id,
                count(distinct user_id) as users_count
            FROM data_userbook
            GROUP BY book_id
            ORDER BY users_count DESC
            LIMIT {n}""")
        return [user_book.book_id for user_book in result]
