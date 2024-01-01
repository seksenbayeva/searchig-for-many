from datetime import datetime
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

try:
  with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
except FileNotFoundError:
  print("Файл data.json не найден.")
  data = {'friends': [], 'channels': [], 'posts': []}
except json.JSONDecodeError:
  print("Ошибка при чтении файла data.json. Некорректный формат JSON.")
  data = {'friends': [], 'channels': [], 'posts': []}


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
  query = request.get_json().get('query', '')

  found_friends = [
      friend for friend in data['friends']
      if query.lower() in friend['name'].lower()
  ]
  found_channels = [
      channel for channel in data['channels']
      if query.lower() in channel['name'].lower()
  ]
  found_posts = [
      post for post in data['posts'] if query.lower() in post['title'].lower()
  ]

  sort_by = request.get_json().get('sort_by', 'name')
  if sort_by == 'date':
    found_posts.sort(
        key=lambda post: datetime.strptime(post['date'], '%Y-%m-%d'),
        reverse=True)
  elif sort_by == 'popularity':
    found_posts.sort(key=lambda post: post.get('popularity', 0), reverse=True)

  return jsonify({
      'friends': found_friends,
      'channels': found_channels,
      'posts': found_posts
  })


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=500)
