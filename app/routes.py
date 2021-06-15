from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, CreatePost
from app.models import User, Post
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


# read blogs 
@app.route('/index')
def index():
	post = Post.query.order_by(Post.id.desc()).all()
	return render_template('index.html', post=post)


# hidden routes 
@app.route('/login', methods=['POST','GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			login_user(user)
			return redirect(url_for('index'))
		else:
			flash('Login Unsuccesful, Please check your credentials!!', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route('/createPost', methods=['GET','POST'])
@login_required
def createPost():
	form = CreatePost()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created','success')
		return redirect(url_for('index'))
	return render_template('createPost.html', title='Create Post', form=form)


@app.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('post.html',title=post.title ,post=post)



@app.route('/post/<int:id>/update', methods=["GET",'POST'])
@login_required
def updatePost(id):
	post = Post.query.get_or_404(id)
	form = CreatePost()
	if form.validate_on_submit():
		post.title = form.title.data 
		post.content = form.content.data 

		db.session.commit()
		flash("Your post has been updated",'success')
		return redirect(url_for('post',id=post.id))
	elif request.method=='GET':
		form.title.data = post.title
		form.content.data = post.content

	return render_template('editPost.html',
		title='Update Post', form=form)


@app.route('/post/<int:id>/delete', methods=["GET",'POST'])
@login_required
def deletePost(id):
	post = Post.query.get_or_404(id)
	db.session.delete(post)
	db.session.commit()
	flash(f"Your post has been deleted",'success')

	return redirect(url_for('index'))



@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.errorhandler(404)
def error_404(error):
	return render_template('errorPage.html'), 404
