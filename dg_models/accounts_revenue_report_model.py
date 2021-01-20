import sys

from sqlalchemy import Column, Integer, String, Date, Float
from dg_config import settingsfile
from dg_models.base_model import Base
import argparse

settings = settingsfile.get_settings()


class RevenueReportRecord(Base):
    # Set the table name based on the program arguments.
    __tablename__ = 'Q' + sys.argv[2] + '_analyticsReport'
    __tableargs__ = {'schema': settings['db_database']}

    report_id = Column(Integer, primary_key=True)
    account_name = Column(String(length=64))
    account_region = Column(String(length=64))
    time_period = Column(Date)
    week = Column(Integer)
    revenue = Column(Float)
    conversion_rate = Column(Float)

    def __repr__(self):
        return f'Account Report: {self.account_name} Week: {self.week} - Revenue: {self.revenue}'
