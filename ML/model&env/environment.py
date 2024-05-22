class RecSys:
    def __init__(self):
        self.book_embedding_model = keras.models.load_model("embedding_book_model.keras")
        self.user_embedding_model = keras.models.load_model("embedding_user_model.keras")
        model = CatBoostRegressor()
        self.main_model = model.load_model("main_model.cbm")
    def get_recommendations(self, user_id, n=10):
        # sql запрос
        user_feature = self.user_embedding_model.predict(x=[data['user_id'], data['book_id']]).reshape((data.shape[0], 32)).tolist()
        user_df = pd.DataFrame(user_feature)
        user_df = user_df.add_suffix('_user')
        book_feature = self.book_embedding_model.predict(x=[data['user_id'], data['book_id']]).reshape((data.shape[0], 32)).tolist()
        book_df = pd.DataFrame(book_feature)
        book_df = book_df.add_suffix('_book')
        data = data.drop(columns=['user_id', 'book_id'])
        data = pd.concat([data, user_df, book_df], axis=1)
        X = data.drop(columns=['book_rating'])
        cat_features = ['book_author', 'location', 'category']
        predictions = model_cat_boost.predict(X).tolist()
        recommendations = pd.DataFrame({'book_id': data['book_id'], 'rating': predictions})
        recommendations = recommendations.sort_values(by='rating')
        return recommendations.head(n)['book_id'].tolist() 
    def get_user_history(self, user_id, n=10):
        # sql запрос
    def get_popular_books(self, n=10):
        # sql запрос