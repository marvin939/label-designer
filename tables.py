from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Integer, Sequence, DateTime, Boolean, Text, ForeignKey, UniqueConstraint

Base = declarative_base()

class Layout(Base):
    __tablename__ = "layout"
    id = Column(Integer,  primary_key=True)
    name = Column(String(255), unique=True)
    permit = Column(String(20))
    returnAddress = Column(Text())
    permitEnable = Column(Boolean)
    returnEnable = Column(Boolean)
    pageWidth = Column(Integer)
    pageHeight = Column(Integer)
    
    def __init__(self, name, permit, returnAddress, permitEnable, returnEnable, pageWidth, pageHeight):
        self.name = name
        self.permit = permit
        self.returnAddress = returnAddress
        self.permitEnable = permitEnable
        self.returnEnable = returnEnable
        self.pageWidth = pageWidth
        self.pageHeight = pageHeight
        
class LayoutObject(Base):
    __tablename__ = "layoutobject"
    id = Column(Integer, primary_key=True)
    layoutId = Column(Integer, ForeignKey('layout.id', ondelete="CASCADE"), nullable=False)
    name = Column(String(255))
    objType = Column(String(255))
    
    __table_args__ = (UniqueConstraint('name', 'layoutId'),)
    
    def __init__(self, layoutId, name, objType):
        self.layoutId = layoutId
        self.name = name
        self.objType = objType
        
class ObjectProperty(Base):
    __tablename__ = "objectproperty"
    id = Column(Integer, primary_key=True)
    layoutObjectId = Column(Integer, ForeignKey('layoutobject.id', ondelete="CASCADE"), nullable=False)
    propType = Column(String(255))
    propVal = Column(Text())
    
    def __init__(self, layoutObjectId, propType, propVal):
        self.layoutObjectId = layoutObjectId
        self.propType = propType
        self.propVal = propVal
    