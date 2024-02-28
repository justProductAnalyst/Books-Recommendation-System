from catboost import CatBoostRegressor
import pandas as pd


class RecSys:
    def __init__(self):
        self.books_data = pd.read_csv(r'webApp\BRS\recsys\static\books_data.csv')
        self.test_data  = pd.read_csv(r'webApp\BRS\recsys\static\merged_test_X.csv')
        self.history_data = pd.read_csv(r'webApp\BRS\recsys\static\filtered_data.csv')
        self.second_level_model = CatBoostRegressor()
        self.second_level_model.load_model(r'webApp\BRS\recsys\static\catboost_model')
        
    def get_recommendations(self, user_id, n=10):
        predictions = self.second_level_model.predict(self.test_data).tolist()
        merged_test_pred = self.test_data.copy()
        merged_test_pred['pred'] = predictions
        merged_test_pred = merged_test_pred.drop('Predicted_rating', axis=1)
        result = list(set(merged_test_pred[merged_test_pred['User-ID'] == user_id].sort_values('pred', ascending=False).head(n * 2)['ISBN'].tolist()))[:10]
        return [self.process_str_to_int(i) for i in result if self.process_str_to_int(i)]

    def get_user_history(self, user_id, n=10):
        result = self.history_data[self.history_data['User-ID'] == user_id]['ISBN'].head(n).tolist()
        return [self.process_str_to_int(i) for i in result if self.process_str_to_int(i)]

    def get_popular_books(self, n=10):
        result = self.history_data.groupby('ISBN', as_index=False).agg({'User-ID': 'count'}).sort_values('User-ID', ascending=False)['ISBN'].head(n).tolist()
        return [self.process_str_to_int(i) for i in result if self.process_str_to_int(i)]

    def process_str_to_int(self, x):
        try:
            return int(x)
        except Exception as e:
            return None
        
