from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from sqlalchemy import DateTime

from config import db, ma


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    shifts = db.relationship('Shift', backref='worker', lazy="dynamic")

    def __repr__(self):
        return '<Worker %s>' % self.name


class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(DateTime)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'),
                          nullable=False)


class WorkerSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")


class ShiftSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "worker_id")


worker_schema = WorkerSchema()
workers_schema = WorkerSchema(many=True)

shift_schema = ShiftSchema()
shifts_schema = ShiftSchema(many=True)


def check_time(dt):
    return dt.hour in [8, 16, 0]


class WorkerListResource(Resource):
    def get(self):
        workers = Worker.query.all()
        data = {}
        for worker in workers:
            data[worker.id] = []
            for shift in worker.shifts:
                data[worker.id].append({
                    'shift_id': shift.id,
                    'shift_date': shift.date,
                })
        return jsonify(data)

    def post(self):
        new_worker = Worker(
            name=request.json['name']
        )
        exists = db.session.query(Worker.name).filter_by(name=new_worker.name).first() is not None
        if exists:
            return "Cannot add worker " + new_worker.name + ", it already exists", 400
        db.session.add(new_worker)
        db.session.commit()
        return worker_schema.dump(new_worker)


class ShiftListResource(Resource):
    def get(self):
        shifts = Shift.query.all()
        data = {}
        for shift in shifts:
            worker = Worker.query.filter_by(id=shift.worker_id).first()
            data[shift.id] = {
                'date': shift.date,
                'worker_name': worker.name,
                'worker_id': worker.id,
            }

        return jsonify(data)

    def post(self):
        try:
            tm = datetime.strptime(request.json['date'], '%d/%m/%y %H:%M:%S')
        except Exception as e:
            return "Cannot add worker " + str(e) + ", it does not exist", 400

        if check_time(tm) == False:
            return "Cannot add shift time with such a hour, add a datetime using format %d/%m/%y %H:%M:%S and hour 0, " \
                   "8, 16", 400

        new_shift = Shift(
            date=tm
        )
        worker_name = request.json['worker_name']

        #check if worker exists
        worker = Worker.query.filter_by(name=worker_name).first()
        if worker is None:
            return "Cannot add shift for worker " + worker_name + ", it does not exist", 400

        #check if the worker has such a shift in that day
        for shift in worker.shifts:
            if abs(((shift.date - tm).total_seconds()/3600)) < 24:
                return "Cannot add shift for worker " + worker.name, 400

        new_shift.worker_id = worker.id
        db.session.add(new_shift)
        db.session.commit()
        worker.shifts.append(new_shift)

        return shift_schema.dump(new_shift)


class PostResource(Resource):
    def get(self, post_id):
        post = Worker.query.get_or_404(post_id)
        return worker_schema.dump(post)

    def patch(self, post_id):
        post = Worker.query.get_or_404(post_id)

        if 'title' in request.json:
            post.title = request.json['title']
        if 'content' in request.json:
            post.content = request.json['content']

        db.session.commit()
        return worker_schema.dump(post)

    def delete(self, post_id):
        post = Worker.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204


api.add_resource(WorkerListResource, '/workers')
api.add_resource(ShiftListResource, '/shifts')

if __name__ == '__main__':
    app.run(debug=True)
