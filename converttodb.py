from core import LabelLayout
import tables

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.reflection import Inspector

from PyQt4 import QtCore, QtGui


engine = create_engine("postgresql://labeldesigner:labelmaker666@pldmpp:5432/labelmaker")
session = sessionmaker(engine)

tables.Base.metadata.create_all(engine)

def load():
    s = session()
    settings = QtCore.QSettings("labelcore.conf", QtCore.QSettings.IniFormat)
    
    settings.beginGroup("layouts")
    for layoutName in settings.childGroups():
        settings.beginGroup(layoutName)
        permit = str(settings.value("permit").toString())
        returnAddress = str(settings.value("return").toString())
        permitEnabled = settings.value("usepermit").toBool()
        returnEnabled = settings.value("useReturn").toBool()
        pageWidth = 90
        pageHeight = 45
        
        layout = tables.Layout(str(layoutName), permit, returnAddress, permitEnabled, returnEnabled, pageWidth, pageHeight)
        
        #commit
        s.add(layout)
        s.commit()
        
        
        layoutId = layout.id
        
        
        for objName in settings.childGroups():
            props = []
            settings.beginGroup(objName)
            objType = str(settings.value("type").toString())
            obj = tables.LayoutObject(layoutId, str(objName), objType)
            
            # commit
            s.add(obj)
            s.commit()
            
            objId = obj.id
            for propName in settings.childKeys():
                propVal = str(settings.value(propName).toString())
                props.append((propName, propVal))
                
                objProp = tables.ObjectProperty(objId, str(propName), propVal)
                s.add(objProp)
                s.commit()
                #print i, h, propName
            settings.endGroup()    
            print layoutName, objType, objType, props
        settings.endGroup()
    settings.endGroup()

load()
#app = QtGui.QApplication(0)