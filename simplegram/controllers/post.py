import os
from flask import render_template, redirect, request, flash, jsonify
from simplegram.forms import CommentForm, PostForm, EditPostForm
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename
from sqlalchemy import select, text

from simplegram.models.models import Post, User, Comment
from config import db

@login_required
def index():
    sql = '''select 
            post.id, user_id, image, post.description, 
            post.created_at, post.updated_at, username, fullname,
            (select count(*) from comment c where c.post_id = post.id) as jml_comment
        from post 
        join user on (post.user_id = user.id)
        order by post.created_at desc
    '''
    postData = db.session.execute(text(sql)).all()
    return render_template('index.html', postData=postData)

@login_required
def add_post():
    from bootstrap import app

    form = PostForm()
    if form.validate_on_submit():
        imFile = form.image.data
        fileName = secure_filename(imFile.filename)
        post = Post(user_id=current_user.id,description=form.description.data,image=fileName)
        db.session.add(post)
        db.session.commit()
        imFile.save(f'./static/uploads/{fileName}')
        flash({'info': 'Berhasil posting foto'})
        return redirect('/')
    return render_template('add_post.html', form=form)

@login_required
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = EditPostForm()
    if form.validate_on_submit():
        if post.user_id == current_user.id:
            post.description = form.description.data
            db.session.commit()
            flash({'info': 'posting berhasil dirubah'})
        else:
            flash({'error': 'posting gagal dirubah'})
        return redirect('/mypost')
    else:
        form.submit.label.text = 'Edit Postingan'
        form.description.data = post.description
        return render_template('edit_post.html', form=form, post=post)

@login_required
def del_post(post_id):
    post = Post.query.get(post_id)
    if post and post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash({'info': 'berhasil hapus postingan'})
    else:
        flash({'error': 'tidak berhasil hapus posting'})
    return redirect('/mypost')

@login_required
def add_comment(post_id):
    sql = '''select 
            post.id, user_id, image, post.description, 
            post.created_at, post.updated_at, username, fullname
        from post
        join user on (post.user_id = user.id)
        where post.id = :id
    '''
    postData = db.session.execute(text(sql), {'id': post_id}).one()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(post_id=postData.id, user_id=current_user.id, comment=form.comment.data)
        db.session.add(comment)
        db.session.commit()
        flash({'info': 'Berhasil menambahkan komentar'})
        return redirect('/')
    return render_template('add_comment.html', form=form, postData=postData)

@login_required
def my_post():
    postData = db.session.execute(db.select(Post).filter_by(user_id=current_user.id)).scalars()
    return render_template('my_posts.html', postData=postData)

def api_comments(post_id):
    commentData = db.session.query(Comment, User).join(User)\
                    .filter(Comment.post_id==post_id)\
                    .order_by(Comment.created_at.desc())\
                    .all()
    commentDict = []
    for comment, user in commentData:
        adict = {'id': comment.id, 'comment': comment.comment, 
                 'username': user.username, 'fullname': user.fullname,
                 'created_at': comment.created_at.strftime('%Y-%m-%d'), 
                 'updated_at': comment.updated_at.strftime('%Y-%m-%d')}
        commentDict.append(adict)
    return jsonify(commentDict)