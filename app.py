from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('Notebook\popular.pkl','rb'))
pt = pickle.load(open('Notebook\pt.pkl','rb'))
book = pickle.load(open(r'Notebook\book.pkl','rb'))
similarity_score = pickle.load(open('Notebook\similarity_score.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_Rating'].values),
                           rating = list(popular_df['avg_Rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_book', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]

    # Get similar items sorted by similarity score
    similar_items = sorted(
        list(enumerate(similarity_score[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:5]  # Skip the first one (it's the book itself)

    data = []
    for i in similar_items:
        # Filter books matching the title
        temp_df = book[book['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')

        # Extract details
        item = [
            temp_df['Book-Title'].values[0],
            temp_df['Book-Author'].values[0],
            temp_df['Image-URL-M'].values[0]
        ]

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)


if __name__ == "__main__":
    app.run(debug = True)