from catboost import CatBoostRegressor
import pandas as pd


class RecSys:
    def __init__(self):
        self.books_data = pd.read_csv(r'webApp\BRS\recsys\static\books_data.csv')
        self.test_data  = pd.read_csv(r'webApp\BRS\recsys\static\merged_test_X.csv')
        self.second_level_model = CatBoostRegressor()
        self.second_level_model.load_model(r'webApp\BRS\recsys\static\catboost_model')
        
    def get_recommendations(self, user_id, n=10):
        predictions = self.second_level_model.predict(self.test_data).tolist()
        merged_test_pred = self.test_data.copy()
        merged_test_pred['pred'] = predictions
        merged_test_pred = merged_test_pred.drop('Predicted_rating', axis=1)
        result = merged_test_pred[merged_test_pred['User-ID'] == user_id].sort_values('pred', ascending=False).head(n)['ISBN'].tolist()
        return [self.process_str_to_int(i) for i in result if self.process_str_to_int(i)]
    
    def process_str_to_int(self, x):
        try:
            return int(x)
        except Exception as e:
            return None
        
