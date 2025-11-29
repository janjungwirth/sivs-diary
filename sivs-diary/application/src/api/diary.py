from flask import Blueprint, render_template, jsonify, request
from src.support.db_handler import DBHandler

diary_blueprint = Blueprint('diary', __name__)
db_handler = DBHandler()
db_handler.connect()

@diary_blueprint.route('/api/diary', methods=['GET'])
def getdiaryentries():
    """
    Listet alle Tagebucheinträge eines Users in JSON-Struktur auf
    :return:
    """
    username = request.args.get('username')
    searchparameter = str(request.args.get('searchparameter')).lower()
    result = db_handler.getDiary(username=username,searchparameter=searchparameter)
    return result

@diary_blueprint.route('/api/diary', methods=['DELETE'])
def deleteDiaryentries():
    """
    Löscht einen bestimmten Tagebucheintrag (ID notwendig)
    :return:
    """
    data = request.get_json()
    id = data.get('id')
    result = db_handler.deleteDiary(id=id)
    return result

@diary_blueprint.route('/api/diary', methods=['POST'])
def creatediaryentry():
    """
    Erstellt einen Tagebucheintrag
    :return:
    """
    data = request.get_json()
    username = data.get('username')
    entry = data.get('entry')
    result = db_handler.createDiaryEntry(username=username,entry=entry)
    return result