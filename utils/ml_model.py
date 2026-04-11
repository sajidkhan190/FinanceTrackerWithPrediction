import numpy as np
from sklearn.linear_model import LinearRegression

def predict_next_month_expense(db, user_id):
    # Database se har maheene ka total expense nikalna
    data = db.execute("""
        SELECT strftime('%Y-%m', date) as month_year, SUM(amount) as total
        FROM transactions 
        WHERE user_id = ? AND type = 'expense' 
        GROUP BY month_year 
        ORDER BY month_year ASC
    """, (user_id,)).fetchall()

    if len(data) < 2:
        return None 

    X = np.array(range(1, len(data) + 1)).reshape(-1, 1)
    y = np.array([row['total'] for row in data])

    model = LinearRegression()
    model.fit(X, y)

    next_month_index = np.array([[len(data) + 1]])
    predicted_amount = model.predict(next_month_index)

    # Naya Hissa: Average nikalein aur threshold set karein
    average_expense = np.mean(y)
    min_realistic_expense = average_expense * 0.5

    # Realistic prediction return karein
    final_prediction = max(min_realistic_expense, predicted_amount[0])
    
    return final_prediction