from flask import Flask, render_template

app = Flask(__name__)



posts = [

    {
        'author': 'Matt Hartz',
        'title': 'Blog Post 1',
        'content': 'Lorem Ipsum',
        'date_posted': 'March 19, 2022'
    },
    {
         'author': 'MH',
        'title': 'Blog Post 2',
        'content': 'Placeholder',
        'date_posted': 'March 19, 2022'


    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts, title='My Blog')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)