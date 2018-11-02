#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/2 17:36
# @Author  : Fred Yang
# @File    : models.py
# @Role    : 数据库信息

import time
from datetime import datetime
from database import Base
from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, TIMESTAMP

class EventReminder(Base):
    __tablename__ = 'event_reminder'
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID 自增长
    name = Column(String(100), nullable=True)  # 事件名称
    content = Column(String(100), nullable=True)  # 事件的描述
    email = Column(String(100), nullable=True)  # 通知人员email
    advance_at = Column(Integer, nullable=True)  # 提前多少天提醒
    expire_at = Column(DateTime, nullable=True)  # 事件过期时间
    create_at = Column(DateTime, nullable=False, default=datetime.now())  # 记录创建时间
    update_at = Column(TIMESTAMP, nullable=False, default=datetime.now())  # 记录更新时间

