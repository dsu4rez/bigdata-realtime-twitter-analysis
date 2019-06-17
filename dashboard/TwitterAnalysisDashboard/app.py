from flask import Flask, jsonify, request
from flask import render_template
import ast

app = Flask(__name__)

tweet_counters = {'total': 0, 'negative': 0, 'neutral': 0, 'positive': 0}
most_used_hashtags = {'labels': [], 'negative': [], 'neutral': [], 'positive': []}
most_active_users = {'labels': [], 'negative': [], 'neutral': [], 'positive': []}
most_mentioned_users = {'labels': [], 'negative': [], 'neutral': [], 'positive': []}


@app.route("/")
def get_dashboard_page():
	global most_used_hashtags, most_active_users, most_mentioned_users

	return render_template(
		'dashboard.html',
		tweet_counters=tweet_counters,
		most_used_hashtags=most_used_hashtags,
		most_active_users=most_active_users,
		most_mentioned_users=most_mentioned_users)


@app.route('/refresh_tweet_counters')
def refresh_tweet_counters_data():
	global tweet_counters
	return jsonify(
		sTotal=tweet_counters['total'],
		sNegative=tweet_counters['negative'],
		sNeutral=tweet_counters['neutral'],
		sPositive=tweet_counters['positive'])


@app.route('/refresh_most_used_hashtags')
def refresh_most_used_hashtags_data():
	global most_used_hashtags

	return jsonify(
		sLabel=most_used_hashtags['labels'],
		sNegative=most_used_hashtags['negative'],
		sNeutral=most_used_hashtags['neutral'],
		sPositive=most_used_hashtags['positive'])


@app.route('/refresh_most_active_users')
def refresh_most_active_users_data():
	global most_active_users

	return jsonify(
		sLabel=most_active_users['labels'],
		sNegative=most_active_users['negative'],
		sNeutral=most_active_users['neutral'],
		sPositive=most_active_users['positive'])


@app.route('/refresh_most_mentioned_users')
def refresh_most_mentioned_users_data():
	global most_mentioned_users

	return jsonify(
		sLabel=most_mentioned_users['labels'],
		sNegative=most_mentioned_users['negative'],
		sNeutral=most_mentioned_users['neutral'],
		sPositive=most_mentioned_users['positive'])


@app.route('/update_tweet_counters', methods=['POST'])
def update_tweet_counters_data():
	global tweet_counters
	if not request.form not in request.form:
		return "error", 400

	tweet_counters['total'] = request.form['total']
	tweet_counters['negative'] = request.form['negative']
	tweet_counters['neutral'] = request.form['neutral']
	tweet_counters['positive'] = request.form['positive']

	return "success", 201


@app.route('/update_most_used_hashtags', methods=['POST'])
def update_most_used_hashtags_data():
	global most_used_hashtags
	if not request.form not in request.form:
		return "error", 400

	most_used_hashtags['labels'] = ast.literal_eval(request.form['label'])
	most_used_hashtags['negative'] = ast.literal_eval(request.form['negative'])
	most_used_hashtags['neutral'] = ast.literal_eval(request.form['neutral'])
	most_used_hashtags['positive'] = ast.literal_eval(request.form['positive'])

	return "success", 201


@app.route('/update_most_active_users', methods=['POST'])
def update_most_active_users_data():
	global most_active_users
	if not request.form not in request.form:
		return "error", 400

	most_active_users['labels'] = ast.literal_eval(request.form['label'])
	most_active_users['negative'] = ast.literal_eval(request.form['negative'])
	most_active_users['neutral'] = ast.literal_eval(request.form['neutral'])
	most_active_users['positive'] = ast.literal_eval(request.form['positive'])

	return "success", 201


@app.route('/update_most_mentioned_users', methods=['POST'])
def update_most_mentioned_users_data():
	global most_mentioned_users
	if not request.form not in request.form:
		return "error", 400

	most_mentioned_users['labels'] = ast.literal_eval(request.form['label'])
	most_mentioned_users['negative'] = ast.literal_eval(request.form['negative'])
	most_mentioned_users['neutral'] = ast.literal_eval(request.form['neutral'])
	most_mentioned_users['positive'] = ast.literal_eval(request.form['positive'])

	return "success", 201


if __name__ == "__main__":
	app.run(host='localhost', port=5001)
