import os
from pybo import create_app
from flask import Blueprint, render_template, request,  url_for, g, flash
from pybo.models import Question
from pybo.forms import QuestionForm, AnswerForm
from pybo import db
from werkzeug.utils import redirect, secure_filename
from datetime import datetime
from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

def allowed_file(filename):
    return'.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'webp', 'gif'}

@bp.route('/list/')
def _list():
    page = request.args.get('page', type = int,default=1)
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods = ('GET','POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        if 'uploaded_img_file' in request.files:
            file = request.files['uploaded_img_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                app = create_app()
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
                file_path_abs = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],secure_filename(filename))
                file.save(file_path_abs) #disk
                question = Question(subject=form.subject.data, content=form.content.data,
                                    uploaded_img_file=file_path, #DB
                                    create_date=datetime.now(),user=g.user)
                db.session.add(question)
                db.session.commit()
                return redirect(url_for('main.index'))
            else:
                flash('attached image file format is not allowed')
        else:
            flash('image file is not attached')
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))     #20230722
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("You don't have permission to edit")
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)        #20230722

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("You don't have permission to delete")
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))