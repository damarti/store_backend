from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base
import settings

dev_engine = create_engine(settings.dev_mysql_uri, convert_unicode=True, pool_size=0, pool_timeout=60, max_overflow=20)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=dev_engine))

Base = declarative_base(bind=dev_engine)
Base.query = db_session.query_property()

class ShopItemGroup(Base):
    __tablename__ = "shop_item_group"
    hash_key = Column(String(255), primary_key=True)
    group_ud = Column(String(255))
    rate_type = Column(String(255))
    single_code = Column(String(255))

    current_cost = relationship("CurrentCost", cascade="delete,all", backref="shop_item_group")
    historical_cost = relationship("HistoricalCost", cascade="delete,all", backref="shop_item_group")
    corrected_cost = relationship("CorrectedCost", cascade="delete,all", backref="shop_item_group")

class CurrentCost(Base):
    __tablename__ = "current_cost"
    id = Column(Integer, primary_key=True)
    shop_item_group_id = Column(String(255), ForeignKey("shop_item_group.hash_key", ondelete="CASCADE"))
    amount = Column(Float, nullable=False)
    payment_type = Column(String(255))

class HistoricalCost(Base):
    __tablename__ = "historical_cost"
    id = Column(Integer, primary_key=True)
    shop_item_group_id = Column(String(255), ForeignKey("shop_item_group.hash_key", ondelete="CASCADE"))
    version_num = Column(Integer)
    amount = Column(Float, nullable=False)
    payment_type = Column(String(255))

class CorrectedCost(Base):
    __tablename__ = "corrected_cost"
    id = Column(Integer, primary_key=True)
    shop_item_group_id = Column(String(255), ForeignKey("shop_item_group.hash_key", ondelete="CASCADE"))
    amount = Column(Float, nullable=False)
    payment_type = Column(String(255))

class NegotiatedDates(Base):
    __tablename__ = "negotiated_dates"
    id = Column(Integer, primary_key=True)
    legacy_group_ud = Column(String(255))
    effective_start = Column(Date)
    effective_end = Column(Date)

class GroupToItem(Base):
    __tablename__ = "group_to_item"
    id = Column(Integer, primary_key=True)
    group_ud = Column(String(255))
    npi = Column(String(255))

#recreating the databases every time for debugging
Base.metadata.create_all()
