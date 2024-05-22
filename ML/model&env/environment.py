class RecSys:
    def __init__(self):
        # инициализация моделей для ембеддингов
        self.embedding_model = keras.models.load_model(
            os.path.join(os.path.dirname(file), 'static', 'embedding_user_model.keras'))
        embedded_user_output = embedding_model.get_layer("user_embedding").output
        embedded_user_input = embedding_model.get_layer("user").output
        embedded_book_output = embedding_model.get_layer("book_embedding").output
        embedded_book_input = embedding_model.get_layer("book").output
        self.book_embedding_model = keras.Model(inputs=[embedded_user_input, embedded_book_input],
                                                outputs=embedded_book_output)
        self.user_embedding_model = keras.Model(inputs=[embedded_user_input, embedded_book_input],
                                                outputs=embedded_user_output)

        # инициализация CatBoostRegressor
        model = CatBoostRegressor()
        self.main_model = model.load_model(os.path.join(os.path.dirname(file), 'static', 'main_model.cbm'))

        # инициализация LabelEncoder
        with open(os.path.join(os.path.dirname(file), 'static', 'label_encoder_book.pkl'), 'rb') as fl:
            self.le = pickle.load(fl)

    def get_recommendations(self, user_id, n=10):
        query = f"""
        WITH user_data AS (
          -- Проверь, что одна строчка
          SELECT user_id, location, age
          FROM main_user
          WHERE user_id = {user_id}
        ),
        user_interactions as (
          SELECT
          user_id,
          book_id,
            rating
          FROM data_userbook ub
          WHERE user_id = {user_id}
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

        # Исполнение запроса
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # создание датафрейма
        data = pd.DataFrame(data)
        known_labels = set(self.le.classes_)
        data = data[data['book_id'].isin(known_labels)]
        data['book_id'] = self.le.transform(data['book_id'])
        data['age'] = data['age'].fillna(data['age'].median())
        data['year_of_publication'] = data['year_of_publication'].fillna(data['year_of_publication'].median())

        # получение рекомендаций
        user_feature = self.user_embedding_model.predict(x=[data['user_id'], data['book_id']]).reshape(
            (data.shape[0], 32)).tolist()
        user_df = pd.DataFrame(user_feature)
        user_df = user_df.add_suffix('_user')
        book_feature = self.book_embedding_model.predict(x=[data['user_id'], data['book_id']]).reshape(
            (data.shape[0], 32)).tolist()
        book_df = pd.DataFrame(book_feature)
        book_df = book_df.add_suffix('_book')
        data_copy = data.copy()
        data = data.drop(columns=['user_id', 'book_id'])
        data = pd.concat([data, user_df, book_df], axis=1)

        X = data.drop(columns=['book_rating'])
        predictions = self.main_model.predict(X).tolist()
        data_copy['book_id'] = self.le.inverse_transform(data_copy['book_id'])
        recommendations = pd.DataFrame({'book_id': data_copy.iloc[X.index]['book_id'], 'rating': predictions})
        recommendations = recommendations.sort_values(by='rating', ascending=False)
        return recommendations.head(n)['book_id'].tolist()

    def add_fitting(self, user_id):
        # sql запрос

        # дообучение book embeddings
        self.embedding_model.fit(x=[data['user_id'], data['book_id']], y=data['rating'], batch_size=256, epochs=40,
                                 validation_split=0.1)
        embedded_user_output = embedding_model.get_layer("user_embedding").output
        embedded_user_input = embedding_model.get_layer("user").output
        embedded_book_output = embedding_model.get_layer("book_embedding").output
        embedded_book_input = embedding_model.get_layer("book").output
        self.book_embedding_model = keras.Model(inputs=[embedded_user_input, embedded_book_input],
                                                outputs=embedded_book_output)
        self.user_embedding_model = keras.Model(inputs=[embedded_user_input, embedded_book_input],
                                                outputs=embedded_user_output)

        # дообучение catboost
        user_feature = self.user_embedding_model.predict(x=[data['user_id'], data['book_id']]).reshape(
            (data.shape[0], 32)).tolist()
        user_df = pd.DataFrame(user_feature)
        user_df = user_df.add_suffix('_user')
        book_feature = self.book_embedding_model.predict(x=[data['user_id'], data['book_id']]).reshape(
            (data.shape[0], 32)).tolist()
        book_df = pd.DataFrame(book_feature)
        book_df = book_df.add_suffix('_book')
        data = data.drop(columns=['user_id', 'book_id'])
        data = pd.concat([data, user_df, book_df], axis=1)
        X = data.drop(columns=['book_rating'])
        y = data['book_rating']
        cat_features = ['book_author', 'location', 'category']
        self.main_model.fit(X, y, cat_features=cat_features, verbose=False, init_model=self.main_model)

    def get_user_history(self, user_id, n=10):

    # sql запрос
    def get_popular_books(self, n=10):
# sql запрос