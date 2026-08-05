from sklearn.linear_model import LogisticRegression

attendance = [[95], [90], [85], [80], [75], [60], [50]]
risk = [0, 0, 0, 0, 1, 1, 1]

model = LogisticRegression()
model.fit(attendance, risk)

prediction = model.predict([[70]])

if prediction[0] == 1:
    print("Student is at risk")
else:
    print("Student is safe")