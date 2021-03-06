# coding=utf-8
from __init__ import *
import collections
from dao.dbHonor import Honor
from dao.dbBase import User
import resource_server


class UserNotExist(BaseException):
    pass


def get_users(data):
    user_list = []
    for name in data:
        if name == '':
            continue
        user = User.query.filter(User.username == name).first()
        if not user:
            raise UserNotExist(u'user not exist')
        else:
            user_list.append(user)
    return user_list


def add_honor(honor_attr, honor_resource):
    try:
        honor = Honor()
        user_list = get_users(honor_attr.users.data)
        honor.contest_name = honor_attr.contest_name.data
        honor.contest_level = honor_attr.contest_level.data
        honor.acquire_time = honor_attr.acquire_time.data
        honor.team_name = honor_attr.team_name.data

        honor.resources = honor_resource
        honor.users = user_list
        honor.save()
        return u'添加成功'
    except UserNotExist, e:
        return e.message
    except Exception:
        return u'添加失败'


def delete_honor(honor_id):
    try:
        Honor.query.filter(Honor.id==honor_id).delete()
        db.session.commit()
        return u'OK'
    except:
        return u'FAIL'


def modify_honor(honor, honor_attr, honor_resource):
    try:
        honor = Honor.query.filter(Honor.id==honor_attr.id.data).first_or_404()
        user_list = get_users(honor_attr.users.data)
        honor.contest_name = honor_attr.contest_name.data
        honor.contest_level = honor_attr.contest_level.data
        honor.acquire_time = honor_attr.acquire_time.data
        honor.team_name = honor_attr.team_name.data
        honor.resources = honor.resources + honor_resource
        honor.users = user_list
        honor.save()
        return u'修改成功'
    except UserNotExist, e:
        return e.message
    except Exception, e:
        return u'修改失败'


def get_by_id(id):
    return Honor.query.filter(Honor.id == id).first_or_404()


def get_honor_list(offset=0, limit=10):
    return Honor.query.order_by(Honor.acquire_time.desc())\
                        .offset(offset).limit(limit).all()


def get_list_pageable(page, per_page, search=None):
    query = Honor.query
    if search:
        query = query.filter(Honor.contest_name.like('%' + search + '%'))
    return query.order_by(Honor.acquire_time.desc())\
                .paginate(page, per_page)


def get_honor_wall(offset=0, limit=10, query_type=None, keyword=''):
    if query_type == 'user' and keyword != '':
        user = User.query.filter(User.name==keyword).first()
        return user.honors.order_by(Honor.acquire_time.desc(),Honor.contest_level.asc())\
                        .offset(offset).limit(limit).all() if user else []
    elif query_type == 'time' and keyword != '':
        try:
            year = int(keyword)
            year_start = datetime(year, 1, 1)
            year_end = datetime(year, 12, 31)
        except:
            from datetime import date
            year_start = year_end = date.min
        return Honor.query\
            .filter(Honor.acquire_time.between(year_start, year_end))\
            .order_by(Honor.acquire_time.desc(),Honor.contest_level.asc())\
            .offset(offset).limit(limit).all()
    elif query_type == 'level' and keyword != '':
        return Honor.query\
            .filter(Honor.contest_level==keyword)\
            .order_by(Honor.acquire_time.desc(),Honor.contest_level.asc())\
            .offset(offset).limit(limit).all()
    elif query_type == 'contest_name' and keyword != '':
        return Honor.query\
            .filter(Honor.contest_name.like('%' + keyword + '%'))\
            .order_by(Honor.acquire_time.desc(),Honor.contest_level.asc())\
            .offset(offset).limit(limit).all()
    elif query_type == 'team_name' and keyword != '':
        return Honor.query\
            .filter(Honor.team_name.like('%' + keyword + '%'))\
            .order_by(Honor.acquire_time.desc(),Honor.contest_level.asc())\
            .offset(offset).limit(limit).all()
    else:
        return Honor.query\
            .order_by(Honor.acquire_time.desc(),Honor.contest_level.asc())\
            .offset(offset).limit(limit).all()


def get_honor_wall_by_year(query_type=None, keyword=''):
    total = get_honor_count(query_type, keyword)
    honor_list = get_honor_wall(0, total, query_type, keyword)
    honor_wall = collections.OrderedDict()
    for honor in honor_list:
        year = honor.acquire_time.year
        if year not in honor_wall:
            honor_wall[year] = []
        honor_wall[year].append(honor)
    return honor_wall


def get_honor_count(query_type=None, keyword=''):
    if query_type == 'user' and keyword != '':
        user = User.query.filter(User.name==keyword).first()
        return user.honors\
            .count() if user else 0
    elif query_type == 'time' and keyword != '':
        try:
            year = int(keyword)
            year_start = datetime(year, 1, 1)
            year_end = datetime(year, 12, 31)
        except:
            from datetime import date
            year_start = year_end = date.min
        return Honor.query\
            .filter(Honor.acquire_time.between(year_start, year_end))\
            .count()
    elif query_type == 'level' and keyword != '':
        return Honor.query\
            .filter(Honor.contest_level==keyword)\
            .count()
    elif query_type == 'contest_name' and keyword != '':
        return Honor.query\
            .filter(Honor.contest_name.like('%' + keyword + '%'))\
            .count()
    elif query_type == 'team_name' and keyword != '':
        return Honor.query\
            .filter(Honor.team_name.like('%' + keyword + '%'))\
            .count()
    else:
        return Honor.query.count()
