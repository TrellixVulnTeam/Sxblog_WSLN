from flask import Flask, render_template, request, session, url_for, redirect, g
from flask_sqlalchemy import SQLAlchemy #Sqlite操作
from  sqlalchemy.sql.expression import func
from flask_compress import Compress #Gzip压缩
import time,random
from functools import wraps
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'r(*&9e0Y7rby(fr&*by9t77'
Compress(app)
db = SQLAlchemy(app)

#去掉首页和分类页的文章的html标签
def nohtml(content):
    return(re.compile(r'<[^>]+>',re.S).sub('',content))
app.jinja_env.globals.update(nohtml=nohtml)

#装饰器校验用户是否登录
def wapper(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if not session.get('user'):
            return redirect('/login')
        return func(*args,**kwargs)
    return inner

@app.context_processor
def make_template_context():
    title = Setting.query.filter_by().first()
    category_nav = db.session.query(Category).all()
    check = User.query.filter_by().first()
    recommends = Article.query.order_by(func.random()).limit(6)
    newaticles = Article.query.order_by(Article.created.desc()).limit(4)
    article_count = db.session.query(func.count(Article.id)).first()
    comment_count = db.session.query(func.count(Comment.id)).first()
    category_count = db.session.query(func.count(Category.id)).first()
    friend_count = db.session.query(func.count(Friend.id)).first()
    user_count = db.session.query(func.count(User.id)).first()
    hots = db.session.query(Article).filter(Article.hot.isnot(None)).order_by(Article.hot.desc()).all()
    friends = db.session.query(Friend).all()
    return dict(title=title,category_nav=category_nav,check=check,recommends=recommends,newaticles=newaticles,article_count=article_count,comment_count=comment_count,category_count=category_count,friend_count=friend_count,user_count=user_count,hots=hots,friends=friends)

#错误处理
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(400)
def page_not_found(e):
    return render_template('404.html')

#数据库模型定义
class Setting(db.Model):
    """设置"""
    __tablename__ = 'setting'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    discription = db.Column(db.Text)
    about = db.Column(db.Text)
    keywords = db.Column(db.Text)

class User(db.Model):
    """用户"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    
class Category(db.Model):
    """分类"""
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

class Friend(db.Model):
    """友情链接"""
    __tablename__ = 'friend'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    url = db.Column(db.Text)
    describe = db.Column(db.Text)

class Article(db.Model):
    """文章"""
    __tablename__ = 'articles'
    PER_PAGE = 5
    ADMIN_PER_PAGE = 12

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    created = db.Column(db.Text)
    author = db.Column(db.Text)
    category_id = db.Column(db.Integer)
    hot = db.Column(db.Integer)
    tags = db.Column(db.Text)
    @property
    def link(self):
        return url_for('article', id=self.id, _external=True)

class Comment(db.Model):
    """留言"""
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    website = db.Column(db.Text)
    articleid = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created = db.Column(db.Text)
    email = db.Column(db.Text)

#路由定义
@app.route('/')
def index():
    pagination = Article.query.order_by(
        Article.created.desc()).paginate(
        int(request.args.get('page', 1)), per_page=Article.PER_PAGE,
        error_out=False)
    return render_template('index.html', articles=pagination.items, pagination=pagination)

@app.route('/search')
def search():
    keyword = request.args.get('s')
    pagination = Article.query.filter(
        Article.title.ilike("%"+keyword+"%")).order_by(Article.id.desc()).paginate(int(request.args.get('page', 1)), per_page=Article.PER_PAGE,
        error_out=False)
    return render_template('index.html',articles=pagination.items,keyword=keyword,pagination=pagination)

@app.route('/admin/search')
def adminsearch():
    keyword = request.args.get('search')
    pagination = Article.query.filter(
        Article.title.ilike("%"+keyword+"%")).order_by(Article.id.desc()).paginate(int(request.args.get('page', 1)), 
        per_page=Article.ADMIN_PER_PAGE,error_out=False)
    return render_template('/admin/index.html',articles=pagination.items,keyword=keyword,pagination=pagination)
                           
@app.route('/category/<int:id>/')
def category(id):
    pagination = Article.query.filter_by(category_id=id).order_by(Article.id.desc()).paginate(
        int(request.args.get('page', 1)), per_page=Article.PER_PAGE,
        error_out=False)
    category=db.session.query(Category.name).filter(Category.id == id).first()
    return render_template('category.html', articles=pagination.items,pagination=pagination,id=id, category_id=id,category=category)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/article/<int:id>.html', methods=['GET', 'POST'])
def article(id):
    if request.method == 'GET':
        category=db.session.query(Category.name,Category.id).join(Article,Article.category_id == Category.id).filter(Article.id == id).first()
        comments = db.session.query(Comment.username,Comment.website,Comment.comment,Comment.created).filter_by(articleid = id)
        comment_count = db.session.query(func.count(Comment.id)).filter(Comment.articleid == id).first()
        return render_template('article.html',article=Article.query.get_or_404(id),comments=comments,category=category)
    if request.method == 'POST':
        db.session.add(Comment(username=request.form.get("author"),email=request.form.get("email"),website=request.form.get("url"),
        articleid=id,comment=request.form.get("text"),created=time.strftime("%Y-%m-%d", time.localtime())))
    
        db.session.commit()
        return redirect(url_for('article',id=id ))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    check = User.query.filter_by().first()
    if request.method == 'GET':
        return render_template('admin/login.html')
    if request.method == 'POST':
        if request.form.get("username") == check.username and request.form.get("password") == check.password:
            session["user"] = request.form.get("username")
            return redirect(url_for('admin'))
        else:
            return render_template('admin/login.html',loginerror='用户名或密码错误！')

@app.route('/admin/')
@wapper
def admin():
    if request.method == 'GET':
        pagination = Article.query.order_by(
            Article.created.desc()).paginate(
            int(request.args.get('page', 1)), per_page=Article.ADMIN_PER_PAGE,
            error_out=False)
        return render_template('admin/index.html',articles=pagination.items,pagination=pagination)

@app.route('/admin/friend/add', methods=['GET', 'POST'])
@wapper
def addfriend():
    if request.method == 'GET':
        pagination = db.session.query(Friend).paginate(
        int(request.args.get('page', 1)), per_page=Article.ADMIN_PER_PAGE,
        error_out=False)
        return render_template('admin/addfriend.html',pagination=pagination,admin_friend=pagination.items)
    if request.method == 'POST':
        db.session.add(Friend(title=request.form.get("friends"),url=request.form.get("links"),describe=request.form.get("describe")))
    
        db.session.commit()
        return redirect(url_for('addfriend'))

@app.route('/admin/category/add', methods=['GET', 'POST'])
@wapper
def addcategory():
    if request.method == 'GET':
        pagination = db.session.query(Category).paginate(
        int(request.args.get('page', 1)), per_page=Article.ADMIN_PER_PAGE,
        error_out=False)
        return render_template('admin/addcategory.html',pagination=pagination,admin_category=pagination.items)
    if request.method == 'POST':
        db.session.add(Category(name=request.form.get("name")))
    
        db.session.commit()
        return redirect(url_for('addcategory'))

@app.route('/admin/setting/', methods=['GET', 'POST'])
@wapper
def setting():
    if request.method == 'GET':
        pagination = db.session.query(Setting).paginate(
        int(request.args.get('page', 1)), per_page=Article.ADMIN_PER_PAGE,
        error_out=False)
        return render_template('admin/setting.html',pagination=pagination,admin_setting=pagination.items)
    if request.method == 'POST':
        setting_item = Setting.query.filter().first()
        setting_item.title=request.form.get("title")
        setting_item.discription=request.form.get("discription")
        setting_item.keywords=request.form.get("keywords")
        setting_item.about=request.form.get("about")
    
        db.session.commit()
        return redirect(url_for('admin'))

@app.route('/admin/article/edit/<int:id>/', methods=['GET', 'POST'])
@wapper
def editarticle(id):
    edit_article = Article.query.filter(Article.id == id).first()
    if request.method == 'GET':
        edit_title=edit_article.title
        edit_content=edit_article.content
        edit_category=Category.query.filter(Category.id==edit_article.category_id).first()
        edit_tags=edit_article.tags
        return render_template('admin/editarticle.html',edit_title=edit_title,edit_content=edit_content, edit_category=edit_category,edit_tags=edit_tags,created=time.strftime("%Y-%m-%d", time.localtime())) 
    if request.method == 'POST':
        article_item = Article.query.filter(Article.id == id).first()
        article_item.title=request.form.get("title")
        article_item.content=request.form.get("editor")
        article_item.category_id=request.form.get("category")
        article_item.tags=request.form.get("tags")
        article_item.created=request.form.get("time")
    
        db.session.commit()
        return redirect(url_for('admin'))

@app.route('/admin/article/add', methods=['GET', 'POST'])
@wapper
def addarticle():
    if request.method == 'GET':
        return render_template('admin/addarticle.html',created=time.strftime("%Y-%m-%d", time.localtime()))
    if request.method == 'POST':
        db.session.add(Article(title=request.form.get("title"),content=request.form.get("editor"),
        created=time.strftime("%Y-%m-%d", time.localtime()),category_id=request.form.get("category"),author='王殊勋',tags=request.form.get("tags")))
    
        db.session.commit()
        return redirect(url_for('admin'))

@app.route('/admin/category/<int:id>/')
@wapper
def admincategory(id):
    pagination = Article.query.filter_by(category_id=id).order_by(Article.id.desc()).paginate(
        int(request.args.get('page', 1)), per_page=Article.ADMIN_PER_PAGE,
        error_out=False)
    return render_template('/admin/index.html',articles=pagination.items,pagination=pagination)

@app.route('/admin/comment/')
@wapper
def admincomment():
    pagination = db.session.query(Comment).paginate(
        int(request.args.get('page', 1)), per_page=Article.ADMIN_PER_PAGE,
        error_out=False)
    return render_template('/admin/comment.html',admin_comment=pagination.items,pagination=pagination)

@app.route('/admin/article/delete/<int:id>/')
@wapper
def articledelete(id):
    db.session.delete(Article.query.filter(Article.id == id).first())
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/comment/delete/<int:id>/')
@wapper
def commentdelete(id):
    db.session.delete(Comment.query.filter(Comment.id == id).first())
    db.session.commit()
    return redirect(url_for('admincomment'))

@app.route('/admin/friend/delete/<int:id>/')
@wapper
def frienddelete(id):
    db.session.delete(Friend.query.filter(Friend.id == id).first())
    db.session.commit()
    return redirect(url_for('addfriend'))

@app.route('/admin/category/delete/<int:id>/')
@wapper
def categorydelete(id):
    db.session.delete(Category.query.filter(Category.id == id).first())
    db.session.commit()
    return redirect(url_for('addcategory'))
    
@app.route('/logout', methods=['GET'])
@wapper
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if  __name__ == '__main__':
    app.run(host='0.0.0.0',port='80')
