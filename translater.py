import global_constants

def Get_text(description,params=None,language=None):
    """ 
    give it language of frase and description, where
    used text, translayter gives frase on need language\n
    Sintaxis:
    <module>_<description>\n
    Example:
        'settings_back_button'\n
        'chess_surrend_error'
    """
    """   
    ru русский
    en английский
    fr французский
    de  немецкий
    es  испанский
    """
    realised = ['ru','en','fr','es','de']
    if not language:
        language = global_constants.Settings.lang
    if len(description) < 4:
        return 'error length'
    if language not in realised:
        return 'error language'
    try:
        if description[:4] == 'bace':
            return bace_text(language,description[5:])
        elif description[:4] == 'game':
            return game_text(language,description[5:],params)
        elif description[:3] == 'all':
            return standart_text(language,description[4:])
        elif description [:6] == 'change':
            return change_text(language,description[7:])
        elif description[:8] == 'settings':
            return settings_text(language,description[9:])
        elif description[:8] == 'tutorial':
            return tutorial(language,description[9:])
        elif 'connection' in description:
            return connection(language,description[11:],params)
        elif 'interface' in description:
            return interface_text(language,description[10:],params)
        else:
            return 'error'
    except Exception as ex:
        return 'error critical  -> ' + str(ex)


def bace_text(language,description):
    if description == 'title_app':
        if language == 'ru':     return 'Шахматы'
        elif language == 'en':   return 'Chess'
        elif language == 'fr':   return 'Jeu d\'échecs'
        elif language == 'es':   return 'Ajedrez'
        elif language == 'de':   return 'Schach'
    
    elif description == 'settings':
        if language == 'ru':   return 'Настройки'
        elif language == 'en': return 'Settings'
        elif language == 'fr': return 'Réglages'
        elif language == 'es':   return 'Ajustos'
        elif language == 'de':return 'Einstellungen'

    
    elif description == 'exit':
        if language == 'ru':    return 'Выход'
        elif language == 'en':  return 'Exit'
        elif language == 'fr':  return 'Sortie'
        elif language == 'es':   return 'Salir'
        elif language == 'de':   return 'Beenden'

    elif description == 'classic':
        if language == 'ru':    return 'Классические'
        elif language == 'en':  return 'Classic'
        elif language == 'fr':  return 'Classique'
        elif language == 'es':   return 'Clásicos'
        elif language == 'de':  return 'Klassische'
    
    elif description == 'fisher':
        if language == 'ru':    return 'Шахматы \nФишера'
        elif language == 'en':  return 'Fisсher \nChess'
        elif language == 'fr':  return 'échecs de \nFisher'.title()
        elif language == 'es':   return 'Ajedrez de\n Fisher'
        elif language == 'de':  return 'Fischers \nSchach'
    
    elif description == 'horse':
        if language == 'ru':     return 'Битва коней'
        elif language == 'en':   return 'Horse Battle'
        elif language == 'fr':   return 'Bataille \ndes chevaux'
        elif language == 'es':   return 'Batallade \nlos cabalos'
        elif language == 'de':   return 'Kampf der Pferd'
    
    elif description == 'magic':
        if language == 'ru':     return 'Волшебные'
        elif language == 'en':   return 'Magik'
        elif language == 'fr':   return 'Magiques'
        elif language == 'es':   return 'Mágicos'
        elif language == 'de':   return "Magische"
    
    elif description == 'alamos':  
        if language == 'ru':   return 'Лос-Аламос'
        elif language == 'en': return 'Los-Alamos'
        elif language == 'fr': return 'Los Alamos'
        elif language == 'es':   return 'Los' + 'álamos'.title()
        elif language == 'de':  return 'Los Alamos'

    elif description == 'circle':
        if language == 'ru':   return 'Круглые \nшахматы'
        elif language == 'en': return 'Circle Chess'
        elif language == 'fr': return 'échecs ronds'.title()
        elif language == 'es':   return 'Ajedrez \n Redondo'   
        elif language == 'de':   return 'Rundes Schach'

    elif description == 'bizantion':
        if language == 'ru':    return 'Византийские'
        elif language == 'en':  return 'Bizantion'
        elif language == 'fr':  return 'échecs \nbyzantins'.title()
        elif language == 'es':   return 'Ajedrez \nBizantino'
        elif language == 'de':   return 'Byzantinisches'
    
    elif description == 'permutation':
        if language == 'ru':   return 'Шахматы с \n заменами'
        elif language == 'en': return 'Permutation \n chess'
        elif language == 'fr': return 'Permutation \néchecs'
        elif language == 'es': return 'Ajedrez con sustitociones'
        elif language == 'de':  return 'Schach mit Ersa'
    
    elif description == 'glinskiy':
        if language == 'ru':   return 'Шахматы\n Глинского'
        elif language == 'en': return 'Glinskiy\n chess'
        elif language == 'fr': return 'Glinskiy \n échecs'
        elif language == 'es': return 'ajerdez \nde Glinskiy'
        elif language == 'de': return 'Schach Glinsky'
    
    elif description == 'kuej':
        if language == 'ru':   return 'Шахматы\n Мак Куэя'
        elif language == 'en': return 'Mak Quey\n chess'
        elif language == 'fr': return 'Mak Quey \n échecs'
        elif language == 'es': return 'ajerdez \nde Mak Quey'
        elif language == 'de': return 'Schach Mak Quey'  
    elif description == 'garner':
        if language == 'ru':   return 'Шахматы\n Гарнера'
        elif language == 'en': return 'Garner\n chess'
        elif language == 'fr': return 'Garner \n échecs'
        elif language == 'es': return 'ajerdez \nde Garner'
        elif language == 'de': return 'Schach Garner'  

    elif description == 'horde':
        if language == 'ru':   return 'Орда'
        elif language == 'en': return 'HORDE'
        elif language == 'fr': return 'HORDE'
        elif language == 'es': return 'HORDA'
        elif language == 'de': return 'HORDE'  
    
    elif description == 'week':
        if language == 'ru':   return 'Слабый!'
        elif language == 'en': return 'Weak!'
        elif language == 'fr': return 'Faible!'
        elif language == 'es': return '¡ Débil !'
        elif language == 'de': return 'Schwach!'

    elif description == 'kamikadze':
        if language == 'en':    return 'Kamikaze'
        elif language == 'ru':  return 'Камикадзе'
        elif language == 'fr': return 'Kamikaze'
        elif language == 'es': return 'Kamikaze'
        elif language == 'de': return 'Kamikaze!'
    
    elif description == 'bad':
        if language == 'ru':    return 'Действительно \n плохие шахматы'
        elif language == 'en':  return 'Really \n bad chess'
        elif language == 'fr': return 'Vraiment \n mauvais échecs'
        elif language == 'es': return 'Realmente \n ajedrez malo'
        elif language == 'de': return 'Wirklich \n schlechtes Schach'
    
    elif description == 'rasing':
        if language == 'ru':    return 'Гонки\nкоролей'
        elif language == 'en':  return 'King\'s \nrasing'
        elif language == 'fr': return 'La Course \nDes Rois'
        elif language == 'es': return 'Carreras de\n Reyes'
        elif language == 'de': return 'Racing \nKings'

    elif description == 'haotic':
        if language == 'ru':    return 'Хаотические'
        elif language == 'en':  return 'Chaotic'
        elif language == 'fr': return 'Chaotique'
        elif language == 'es': return 'Caótico'
        elif language == 'de': return 'Chaotisch'
    
    elif description == 'dark_chess':
        if language == 'ru':    return 'Тёмные \n шахматы'
        elif language == 'en':  return 'Dark chess'
        elif language == 'fr': return 'Sombre jeu d\'échecs'
        elif language == 'es': return 'Ajedrez oscuro'
        elif language == 'de': return 'Dunkles Schach'

    elif description == 'schatranj':
        if language == 'ru':    return 'Шатрандж'
        elif language == 'en':  return 'Shatranj'
        elif language == 'fr': return 'Shatrange'
        elif language == 'es': return 'Shatrange'
        elif language == 'de': return 'Shatrange'

    elif description == 'frozen':
        if language == 'ru':    return 'Ледниковый \n период'
        elif language == 'en':  return 'Ice Period '
        elif language == 'fr': return 'Âge de glace '
        elif language == 'es': return 'Período glacial'
        elif language == 'de': return 'Eiszeit'
    
    elif description == 'exit?':
        if language == 'ru':   return 'Выйти?'
        elif language == 'en': return 'Leave?'
        elif language == 'fr': return 'Congé?'
        elif language == 'es': return '¿Irme?'
        elif language == 'de': return 'Verlassen?'
    
    elif description == 'exit_message':
        if language == 'ru':   return 'Это действие уничтожит \n       Ваш прогресс.  \n      Вы уверены?'
        elif language == 'en': return 'This action destroys your \nprogress. Do you agree?'
        elif language == 'fr': return 'Cette action détruit votre \n progression. Tu es d\'accord?'
        elif language == 'es': return 'Esta acción destruye su progreso. \n ¿Estás de acuerdo?'
        elif language == 'de': return "Diese Aktion zerstört Ihren \nFortschritt. Stimmen Sie zu?"
    
    elif description == 'save?':
        if language == 'ru':   return 'Сохранить'
        elif language == 'en': return 'Save'
        elif language == 'fr': return 'Enregistrer'
        elif language == 'de': return 'Speichern'
        elif language == 'es': return 'Guardar'

    elif description == 'saved':
        if language == 'ru':   return 'Сохранённые'
        elif language == 'en': return 'Saved'
        elif language == 'es': return 'Guardaron'
        elif language == 'de': return 'Behieltet'
        elif language == 'fr': return 'Conservâtes'
    
    elif description == 'remove':
        if language == 'ru':   return 'Удалить'
        elif language == 'en': return 'Remove'
        elif language == 'es': return 'Quitar'
        elif language == 'de': return 'Entfernen'
        elif language == 'fr': return 'Supprimer'
    
    elif description == 'repeat_text':
        if language == 'ru':   return 'Что делать?'
        elif language == 'en': return 'What to do?'
        elif language == 'es': return 'Qué hacer?'
        elif language == 'de': return 'Was zu tun?'
        elif language == 'fr': return 'Que faire?'

    else:
        return 'error_2'


def standart_text(language,description):
    if description == 'start':
        if language == 'ru':     return 'Старт'
        elif language == 'en':   return 'Start'
        elif language == 'fr':   return 'Lancement'
        elif language == 'es':   return 'Comienzo'
        elif language == 'de':   return  'Start' 
    elif description == 'back':
        if language == 'ru':   return 'Назад'
        elif language == 'en': return 'Back'
        elif language == 'fr': return 'Arrière'
        elif language == 'es':   return 'Atrás'
        elif language == 'de':   return 'Zurück'
    
    elif description == 'exit':
        if language == 'ru':  return 'Выход'
        elif language == 'en':return 'Exit'
        elif language == 'fr':return 'Sortie'
        elif language == 'es':   return 'Salida'
        elif language == 'de':  return 'Beenden'

    elif description == 'ok':
        if language == 'ru':  return 'OK'
        elif language == 'en':return 'OK'
        elif language == 'fr':return 'yeux'.upper()
        elif language == 'es':   return 'OK'
        elif language == 'de':  return 'OK'
    
    else:
        return 'error_2'


def change_text(language,description):
    if description == 'study':
        if language == 'ru':   return 'Обучение'
        elif language == 'en': return 'Education'
        elif language == 'fr': return 'Formation'
        elif language == 'es': return 'Formación'
        elif language == 'de': return 'Ausbildung'
    
    elif description == 'play':
        if language == 'ru':      return 'Играть'
        elif language == 'en':    return 'Play'
        elif language == 'fr':    return 'Jouer'
        elif language == 'es':    return 'Jugar'
        elif language == 'de':    return 'Spielen'


    elif description == 'sec':
        if language == 'ru':   return 'cек'
        elif language == 'en': return 'sec'
        elif language == 'fr': return 'sec'
        elif language == 'es': return 'seg'
        elif language == 'de': return 'sek'

    
    elif description == 'min':
        if language == 'ru':   return 'мин'
        elif language == 'en': return 'min'
        elif language == 'fr': return 'min'
        elif language == 'es': return 'min'
        elif language == 'de': return 'min'

    
    elif description == 'nik':
        if language == 'ru':   return 'Ники'
        elif language == 'en': return 'Names'
        elif language == 'fr': return 'Pseudo'
        elif language == 'es': return 'Nicky'
        elif language == 'de': return 'Spitznamen'


    elif description == 'time':
        if language == 'ru':   return 'Времени'
        elif language == 'en': return 'All time'
        elif language == 'fr': return 'Temps'
        elif language == 'es': return 'Tiempo'
        elif language == 'de': return 'Zeit'

    
    elif description == 'add':
        if language == 'ru':   return 'Добавлять'
        elif language == 'en': return 'Add time'
        elif language == 'fr': return 'Ajout'
        elif language == 'es': return 'Agregar'
        elif language == 'de': return 'Hinzufügen'

    
    elif description == 'tips':
        if language == 'ru':   return 'Подсказки'
        elif language == 'en': return 'Do hints?'
        elif language == 'fr': return 'Bulles'
        elif language == 'es': return 'Sugerencias'
        elif language == 'de': return 'Vorsagen'
    
    elif description == 'magia':
        if language == 'ru':   return 'Магия каждые\nходов'
        elif language == 'en': return 'Magik every\nmoves'
        elif language == 'fr': return 'Magie tous les\n mouvements'
        elif language == 'es': return 'magia cada\n movimientos'
        elif language == 'de': return 'Magie alle\n Züge'
    
    elif description == 'warning':
        if language == 'ru':
            return 'Предупреждение'
        if language == 'en':
            return 'Warning'
        if language == 'fr':
            return  'Avertissement'
        if language == 'es':
            return 'Advertencia'
        if language == 'de':
            return 'Warnung'

    elif description == 'error_who':
        if language == 'ru':
            return 'Вы не можете начать игру!\nИгру должен начать хост.\nНастройки игры ставит так-же он,\nПоэтому ваши будут проигнорированы!'
        if language == 'en':
            return 'You can\'t start the game!\nThe host must start the game.\nThe game settings are set in the same way,\nso your settings will be ignored!'
        if language == 'fr':
            return  'Vous ne pouvez pas commencer le jeu!\nLe jeu doit démarrer l\'hôte.\nParamètres du jeu met de la même manière,\ndonc votre sera ignoré!'
        if language == 'es':
            return '¡No puedes comenzar el juego!\n El juego debe comenzar el anfitrión.\n La configuración del juego se pone\n de la misma manera,por lo que el suyo\n será ignorado!'
        if language == 'de':
            return 'Sie können das Spiel nicht\n starten! Das Spiel muss vom Host\n gestartet werden.Die Einstellungen des\n Spiels setzt die\n gleiche Weise es,so wird Ihr\n ignoriert werden!'

    elif description == 'white':
        if language == 'ru':
            return 'Белый'
        if language == 'en':
            return 'White'
        if language == 'fr':
            return  'Blanc'
        if language == 'es':
            return 'Blanco'
        if language == 'de':
            return 'weiß'

    elif description == 'black':
        if language == 'ru':
            return 'Чёрный'
        if language == 'en':
            return 'Black'
        if language == 'fr':
            return  'Noir'
        if language == 'es':
            return 'Negro'
        if language == 'de':
            return 'schwarz'

    elif description == 'your_color':
        if language == 'ru':
            return 'Ваш цвет'
        if language == 'en':
            return 'My color'
        if language == 'fr':
            return  'Ma couleur'
        if language == 'es':
            return 'Mi color'
        if language == 'de':
            return 'Meine Farbe'

    if description == 'all':
        if language == 'ru':
            return 'Всё, что есть'
        if language == 'en':
            return 'All types'
        if language == 'fr':
            return  'Toutes sortes'
        if language == 'es':
            return 'Todo tipo'
        if language == 'de':
            return 'alle Arten'.title()

    if description == 'random':
        if language == 'ru':
            return 'Выбрать рандомный'
        if language == 'en':
            return 'Choose randomly'
        if language == 'fr':
            return  'Choisir aléatoire'
        if language == 'es':
            return 'Seleccione \naleatoriamente'
        if language == 'de':
            return 'Wählen Sie zufällig'

    if description == 'classic':
        if language == 'ru':
            return 'Классическая \nрасстановка'
        if language == 'en':
            return 'Classic arrangement'
        if language == 'fr':
            return  'Arrangement \n classique '
        if language == 'es':
            return 'Disposición clásica'
        if language == 'de':
            return 'Klassische \ n anordnung'

    if description == 'positions':
        if language == 'ru':
            return 'Необычные позиции'
        if language == 'en':
            return 'Unusual positions'
        if language == 'fr':
            return  'Positions inhabituelles'
        if language == 'es':
            return 'Posiciones inusuales'
        if language == 'de':
            return 'Ungewöhnliche Positionen'

    if description == 'effects':
        if language == 'ru':
            return 'C эффектами'
        if language == 'en':
            return 'With effects'
        if language == 'fr':
            return  'Avec des effets'
        if language == 'es':
            return 'Con efectos'
        if language == 'de':
            return 'mit Effekten'

    if description == 'honestlessly':
        if language == 'ru':
            return 'Несимметричные'
        if language == 'en':
            return 'Not symmetrical'
        if language == 'fr':
            return  'Asymétriques'
        if language == 'es':
            return 'Asimétricos'
        if language == 'de':
            return 'Nicht symmetrisch'
    
    if description == 'boards':
        if language == 'ru':
            return 'Необычные доски'
        if language == 'en':
            return 'Unusual \nchess boards'
        if language == 'fr':
            return  'Planches \nd\'échecs insolites'
        if language == 'es':
            return 'Tablero de \najedrez inusual'
        if language == 'de':
            return 'Ungewöhnliche \nSchachbretter'
    
    if description == 'others':
        if language == 'ru':
            return 'Другие правила'
        if language == 'en':
            return 'other rules'
        if language == 'fr':
            return  'd\'autres règles'
        if language == 'es':
            return 'otras normas'
        if language == 'de':
            return 'andere Regeln'
    
    if description == 'frozen':
        if language == 'ru':
            return 'Заморозка'
        if language == 'en':
            return 'Freeze'
        if language == 'fr':
            return  "Geler"
        if language == 'es':
            return 'Congelar'
        if language == 'de':
            return 'Frosten'


    else:
        return 'error_2'


def settings_text(language,description):
    if description == 'music':
        if language == 'ru':   return 'Музыка'
        elif language == 'en': return 'Music'
        elif language == 'fr': return 'Musique'
        elif language == 'es': return 'Música'
        elif language == 'de': return 'Musik'

    
    elif description == 'see':
        if language == 'ru':  return 'Вид'
        elif language == 'en': return 'Form'
        elif language == 'fr': return 'Apparence'
        elif language == 'es': return 'Apariencia'
        elif language == 'de': return 'Aussehen'
    
    elif description == 'all':
        if language == 'ru':  return 'Общие'
        elif language == 'en':return 'Сommon'
        elif language == 'fr':return 'Généraux'
        elif language == 'es': return 'General'
        elif language == 'de': return 'Allgemeine'
    
    elif description == 'effects':
        if language == 'ru':   return 'Эффекты'
        elif language == 'en': return 'Effects'
        elif language == 'fr': return 'Effets'
        elif language == 'es': return 'Efectos'
        elif language == 'de': return 'Effekte'
    
    elif description == 'volume':
        if language == 'ru':  return 'Громкость'
        elif language == 'en':return 'Volume'
        elif language == 'fr':return 'Volume'
        elif language == 'es': return 'Volumen'
        elif language == 'de': return 'Lautstärke'
    
    elif description == 'check_music':
        if language == 'ru':  return 'Выбор музыки'
        elif language == 'en':return 'Choice music'
        elif language == 'fr':return 'Sélection \nde musique'
        elif language == 'es': return 'Selección \nde música'
        elif language == 'de': return 'Musikauswahl'
    
    elif description == 'change_effect':
        if language == 'ru':   return 'Выбор эффекта'
        elif language == 'en': return 'Choice effect'
        elif language == 'fr': return 'Sélection \nde effet'
        elif language == 'es': return 'Selección \nde efectos'
        elif language == 'de':  return 'Effekte \nauswählen'

    
    elif description == 'change_fon':
        if language == 'ru'   :return 'Смена фона'
        elif language == 'en' :return 'Choice \nbackground'
        elif language == 'fr': return 'Sélection \nd\'arrière-plan'
        elif language == 'es': return 'Cambio de \nfondo'
        elif language == 'de': return 'Hintergrund ändern'

    
    elif description == 'change_game_fon':
        if language == 'ru' :  return 'Игровой фон'
        elif language == 'en': return 'Play \nbackground'
        elif language == 'fr': return 'Fond de jeu'
        elif language == 'es': return 'Fondo \nde Juego'
        elif language == 'de': return 'Spiel hintergrund'

    
    elif description == 'change_board':
        if language == 'ru':  return 'Сменить \nдоску'
        elif language == 'en':return 'Choice board'
        elif language ==  'fr':return 'Changer \nde planche'
        elif language == 'es': return 'Cambiar \nel tablero'
        elif language == 'de':  return 'Tafel wechseln'
    
    elif description == 'change_figure':
        if language == 'ru':  return 'Сменить \nфигуры'
        elif language == 'en':return 'Choice \nfigures'
        elif language == 'fr':return 'Changer \nde forme'
        elif language == 'es': return 'Cambiar \nla figura'
        elif language == 'de':return 'Form ändern'

    
    elif description == 'language':
        if language == 'ru':  return 'Язык'
        elif language == 'en':return 'Language'  
        elif language == 'fr':return 'Langue' 
        elif language == 'es': return 'Idioma'
        elif language == 'de': return 'Sprache'

    elif description == 'nick':
        if language == 'ru':  return 'Ник в сети'
        elif language == 'en':return 'Nickname in \nthe network'  
        elif language == 'fr':return 'Nick sur le \nnet' 
        elif language == 'es': return 'Nick en \nla red'
        elif language == 'de': return 'Nick online'


    else:
        print(description)
        return 'error_2'


def game_text(language,description,params):
    if description == 'return':
        if language == 'ru':  return 'Вернуться'
        elif language == 'en':return 'Return'
        elif language == 'fr':return 'Revenir'
        elif language == 'es': return 'Volver'
        elif language == 'de': return 'Zurückkehren'
    
    elif description == 'white_mate':
        if language == 'ru'  :return 'Мат белым'
        elif language == 'en':return 'Mate white'
        elif language == 'fr':return 'Mat blanc'
        elif language == 'es': return 'Mate blanco'
        elif language == 'de': return 'Matte weiß'
    
    elif description == 'black_mate':
        if language == 'ru':  return 'Мат чёрным'
        elif language == 'en':return 'Mate black'
        elif language == 'fr':return 'Mat noir'
        elif language == 'es': return 'Mate negro'
        elif language == 'de': return 'Matte schwarz'
    
    elif description == 'white_nothing':
        if language == 'ru':  return 'Белые проиграли'
        elif language == 'en':return 'White lost'
        elif language == 'fr':return 'les blancs ont perdu'
        elif language == 'es': return 'los blancos perdieron'
        elif language == 'de': return 'die Weißen verloren'
    
    elif description == 'pat':
        if params == None:
            if language == 'ru':  return 'Пат.\nНичья!'
            elif language == 'en':return 'Pat.\nDraw!'
            elif language == 'fr':return 'Pat.\nMatch nul!'
            elif language == 'es': return 'Pat.\nEmpate!'
            elif language == 'de':return 'Patt.\nUnentschieden!'
        elif params == 'white':
            if language == 'ru':  return 'Пат.\nБелые проиграли!'
            elif language == 'en':return 'Pat.\nWhite is loser!'
            elif language == 'fr':return 'Pat.\nLes blancs ont perdu!'
            elif language == 'es': return 'Pat.\nLos blancos perdieron!'
            elif language == 'de':return 'Patt.\nDie weißen verloren!'
        elif params == 'black':
            if language == 'ru':  return 'Пат.\nЧёрные проиграли!'
            elif language == 'en':return 'Pat.\nBlack is loser!'
            elif language == 'fr':return 'Pat.\nLes noirs ont perdu!'
            elif language == 'es': return 'Pat.\nLos negros perdieron!'
            elif language == 'de':return 'Patt.\nSchwarze verloren!'
    
    elif description == 'white_chax':
        if language == 'ru':   return 'Шах белым'
        elif language == 'en': return 'Сheck white'
        elif language == 'fr': return 'Shah blanc'
        elif language == 'es': return 'Jaque blanco'
        elif language == 'de': return 'Shah weiß'
    
    elif description == 'black_chax':
        if language == 'ru':   return 'Шах чёрным'
        elif language == 'en': return 'Check black'
        elif language == 'fr': return 'Shah noir'
        elif language == 'es': return 'Jaque negro'
        elif language == 'de': return 'Shah schwarz'
    
    elif description == 'black_move':
        if language == 'ru':   return 'Ход чёрных'
        elif language == 'en': return 'Black move'
        elif language == 'fr': return 'Course des noirs'
        elif language == 'es': return 'Movomientos \nde los negros'
        elif language == 'de': return 'Anschlag schwarz'
    
    elif description == 'white_move':
        if language == 'ru':   return 'Ход белых'
        elif language == 'en': return 'White move'
        elif language == 'fr': return 'Course des blancs'
        elif language == 'es': return 'Movimientos \nde los blancos'
        elif language == 'de': return 'Anschlag der weißen'
    
    elif description == 'want_draw':
        if language == 'ru':  return 'Вы хотите ничью?'
        elif language == 'en':return 'Do you want draw?'
        elif language == 'fr':return 'Vous voulez un tirage au sort?'
        elif language == 'es': return '¿Quieres un empate?'
        elif language == 'de': return 'Willst du ein Unentschieden?'
    
    elif description == 'no':
        if language == 'ru':  return 'Нет'
        elif language == 'en':return 'No'
        elif language == 'fr':return 'Pas'
        elif language == 'es': return 'No'
        elif language == 'de': return 'Nein'
    
    elif description == 'yes':
        if language == 'ru':  return 'Да'
        elif language == 'en':return 'Yes'
        elif language == 'fr':return 'Oui'
        elif language == 'es': return 'Si'
        elif language == 'de': return 'Ja'
    
    elif description == 'draw_title':
        if language == 'ru':  return 'Ваш противник предлагает вам ничью'
        elif language == 'en':return 'Your opponent offers you a draw'
        elif language == 'fr':return 'Votre adversaire vous offre un match nul'
        elif language == 'es': return 'Tu opponente te ofrece un empate'
        elif language == 'de': return 'dein Gegner bietet dir ein Unentschieden'
    
    elif description == 'end_time':
        if language == 'ru':  return 'Время вышло'
        elif language == 'en':return 'time\'s up'
        elif language == 'fr': return 'Le temps est écoulé'
        elif language == 'es': return 'Se acabó el tiempo'
        elif language == 'de': return  'Die Zeit ist vorbei'   
    elif description == 'white_lose':
        if language == 'ru':   return 'Белые проиграли'
        elif language == 'en': return 'White is loser'
        elif language == 'fr': return 'Les blancs ont perdu'
        elif language == 'es': return 'Los negros perdieron'
        elif language == 'de': return 'Die weißen verloren'
    
    elif description == 'black_lose':
        if language == 'ru':   return 'Чёрные проиграли'
        elif language == 'en': return 'Black is loser'
        elif language == 'fr': return 'Les noirs ont perdu'
        elif language == 'es': return 'Los blancos perdieron'
        elif language == 'de': return 'Schwarze verloren'

    
    elif description == 'white_surrend':
        if language == 'ru':   return 'Белые сдались'
        elif language == 'en': return 'White surrended'
        elif language == 'fr': return 'Les blancs se sont rendus'
        elif language == 'es': return 'Los blancos se rindieron'
        elif language == 'de': return 'Die weißen Gaben auf'

    
    elif description == 'black_surrend':
        if language == 'ru':   return 'Чёрные сдались'
        elif language == 'en': return 'Black surrended'
        elif language == 'fr': return 'Les noirs se sont rendus'
        elif language == 'es': return 'Los negros se rindieron'
        elif language == 'de': return 'Aufgegeben schwarz'

    
    elif description == 'cant_surrend':
        if language == 'ru':  return 'Сдаться можно только после 3 хода'
        elif language == 'en':return 'You can surrend only after 3 move'
        elif language == 'fr':return 'Vous ne pouvez abandonner \nqu\'après 3 mouvements'
        elif language == 'es': return 'rendirse sólo \ndespués de 3 movimientos'
        elif language == 'de': return 'Aufgeben kann nur nach 3 Zügen'

    
    elif description == 'want_surrend':
        if language == 'ru' :  return 'Хочу сдаться!'
        elif language == 'en': return 'I want surrend!'
        elif language == 'fr': return 'Je veux abandonner'
        elif language == 'es': return 'Quiero rendirme'
        elif language == 'de': return 'Ich will aufgeben.'
    
    elif description == 'not_surrend':
        if language == 'ru':  return 'Не хочу!'
        elif language == 'en':return 'Don\'t want!'
        elif language == 'fr':return 'Je ne veux pas!'
        elif language == 'es':return '¡No quiero!'
        elif language == 'de': return 'Will nicht'

    elif description == 'agree?':
        if language == 'ru':  return 'Вы уверены, что хотите сдаться?'
        elif language == 'en':return 'Do you want surrend?'
        elif language == 'fr':return 'Êtes-vous sûr de vouloir abandonner?'
        elif language == 'es':return '¿estás seguro de que quieres rendirte?'
        elif language == 'de': return 'Sind Sie sicher, dass Sie aufgeben wollen?'
    
    elif description == 'press_surrend':
        if language == 'ru':  return 'Вы нажали "Сдаться"'
        elif language == 'en':return 'You press "Surrend"'
        elif language == 'fr':return 'Vous avez cliqué sur "Abandonner"'
        elif language == 'es':return 'has hecho clic en "Rendirte"'
        elif language == 'de': return "Sie haben auf 'aufgeben'geklickt"
    
    elif description == 'ok':
        if language == 'es':   return 'Okey'
        else:   return 'ok'
    
    elif description == 'error':
        if language == 'ru':   return 'Ошибка'
        elif language == 'en': return 'Error'
        elif language == 'fr': return 'Erreur'
        elif language == 'es':return 'Error'
        elif language == 'de': return 'Fehler'

    elif description == 'draw_ok':
        if language == 'ru':   return 'Ничья по согласию'
        elif language == 'en': return 'Draw by consent'
        elif language == 'fr': return 'Match nul par consentement'
        elif language == 'es':return 'Empato de mutuo acuerdo'
        elif language == 'de': return 'Unentschieden im gegenseitigen \nEinvernehmen'

    
    elif description == 'cant_draw':
        if language  == 'ru':  return 'Ничью предлагают после 3 хода'
        elif language == 'en': return 'You can suggest draw after 3 move'
        elif language == 'fr':return 'Le match nul est offert après 3 tours'
        elif language == 'es':return 'Empate tras 3 movementos'
        elif language == 'de': return 'Unentschieden nach 3 Zügen angeboten'

    # for round chess
    elif description == 'white_pat_lose':
        if language == 'ru':  return 'Пат.Белые проиграли.'
        elif language == 'en':return 'Pat.White is lose.'
        elif language == 'fr':return 'Pat. Les blancs ont perdu.'
        elif language == 'es':return 'Pat.Los blancos perdieron.'
        elif language == 'de': return 'Patt.Die weißen verloren.'

    
    elif description == 'black_pat_lose':
        if language == 'ru':   return 'Пат.Чёрные проиграли.'
        elif language == 'en': return 'Pat.Black is lose.'
        elif language == 'fr': return 'Pat. Les noirs ont perdu'
        elif language == 'es':return 'Pat.Los negros perdieron.'
        elif language == 'de': return 'Patt.Die chwarz verloren.'

    
    elif description == 'white_lost_figs':
        if language == 'ru':  return 'Белые проиграли.\nКороль остался без фигур.'
        elif language == 'en':return 'White lose this game.\nOn board is 1 king.'
        elif language == 'fr':return 'Les blancs ont perdu.\nLe roi est resté sans chiffres.'
        elif language == 'es':return 'Los blancos perdieron.\nel rey se queda sin protección.'
        elif language =='de':   return 'Die weißen verloren.Der König blieb ohne Figuren.'

    
    elif description == 'black_lost_figs':
        if language == 'ru':  return 'Чёрные проиграли.\nКороль остался без фигур.'
        elif language == 'en':return 'Black lose this game.\nOn board is 1 king.'
        elif language == 'fr':return 'Les noirs ont perdu.\nLe roi est resté sans chiffres.'
        elif language == 'es':return 'Los blancos perdieron.\nel rey se queda sin figuras.'
        elif language == 'de':return 'Die chwarz verloren.Der König blieb ohne Figuren.'
    
    # for network
    elif description == 'you_surrend':
        if language == 'ru':  return 'Вы сдались!!'
        elif language == 'en':return 'You gave up!!'
        elif language == 'fr':return 'Vous avez abandonné!!'
        elif language == 'es':return '¡Te has rendido!!'
        elif language == 'de':return 'Ihr habt aufgegeben!!'
    
    elif description == 'friend_surrend':
        if language == 'ru':  return 'Противник сдался!!'
        elif language == 'en':return 'Opponent gave up!!'
        elif language == 'fr':return 'l\'ennemi s\'est rendu!!'
        elif language == 'es':return '¡Enmigo has rendido!!'
        elif language == 'de':return 'Gegner habt aufgegeben!!'

    elif description == 'offer_draw?':
        if language == 'ru':  return 'Предложить ничью?'
        elif language == 'en':return 'Offer a draw?'
        elif language == 'fr':return 'Offrir un tirage au sort?'
        elif language == 'es':return '¿Proponer un empate?'
        elif language == 'de':return 'Ein Unentschieden anbieten?'

    elif description == 'draw?':
        if language == 'ru':  return 'Ничья?'
        elif language == 'en':return 'Draw?'
        elif language == 'fr':return 'Tirage?'
        elif language == 'es':return '¿Empate?'
        elif language == 'de':return 'Anbieten?'
    
    elif description == 'leave':
        if language == 'ru':  return 'Противник вышел.\n Вы победили!'
        elif language == 'en':return 'The enemy is out.\n You won!'
        elif language == 'fr':return 'L\'ennemi est sorti.\n Vous avez gagné!'
        elif language == 'es':return 'El enemigo salió.\ N ¡has ganado!'
        elif language == 'de':return 'Der Gegner ist raus.\n Sie haben gewonnen!'
    
    # magik
    elif description == 'both_mate':
        if language == 'ru':  return 'Ничья! Оба поставили мат! \n Это невозможно! (Разработчик)'
        elif language == 'en':return 'Draw! Both of them checkmated! \n This is not possible! (Developer)'
        elif language == 'fr':return 'Tirage au sort! Les deux ont mis le tapis! \n ce n\'est pas possible! (Développeur)'
        elif language == 'es':return '¡Empate! ¡Los dos pusieron el tapete! \n ¡es imposible! (Elaborador)'
        elif language == 'de':return 'Unentschieden! \nBeide haben eine Matte aufgestellt! \n Es ist unmöglich! (Entwickler)'
    
    elif description == 'both_chax':
        if language == 'ru':  return 'Шах обоим! \n Вот так случай!'
        elif language == 'en':return 'Check both of them! \n That\'s the case!'
        elif language == 'fr':return 'Shah à tous les deux! \n Voici le cas!'
        elif language == 'es':return '¡Jaque a ambos! \n ¡Así es el caso!'
        elif language == 'de':return 'Shah beide! \n So ist der Fall!'
    
    elif description == 'magik_black_chax':
        if language == 'ru':  return '\n Ход передан чёрным. '
        elif language == 'en':return '\n Move passed to black. '
        elif language == 'fr':return '\n la Course est passée en noir. '
        elif language == 'es':return '\n el Movimiento se transmite en negro. '
        elif language == 'de':return '\n Der Zug wird schwarz übergeben. '  
    
    elif description == 'magik_white_chax':
        if language == 'ru':  return '\n Ход передан белым. '
        elif language == 'en':return '\n Move passed to white. '
        elif language == 'fr':return '\n la Course est passée en blanc. '
        elif language == 'es':return '\n el Movimiento se transmite en blanco. '
        elif language == 'de':return '\n Der Zug wird weißen übergeben. '  

    # for rasing_chess
    elif description == 'white_king':
        if language == 'ru':  return 'Белые победили! \nКороль у цели!'
        elif language == 'en':return "The Whites have won! \n The king is on target!"
        elif language == 'fr':return "Les blancs ont gagné! \n le Roi a la cible!"
        elif language == 'es':return "¡Los blancos ganaron! \n ¡el Rey está en el blanco!"
        elif language == 'de':return "Die Weißen haben gewonnen! \n König ist am Ziel!"
    
    elif description == 'black_king':
        if language == 'ru':  return 'Чёрные победили! \nКороль у цели!'
        elif language == 'en':return "The blacks have won! \n The king is on target!"
        elif language == 'fr':return "Les noirs ont gagné! \n le Roi a la cible!"
        elif language == 'es':return "¡Los negros ganaron! \n ¡el Rey está en el blanco!"
        elif language == 'de':return "Die Schwarzen haben gewonnen! \n König ist am Ziel!"
    
    elif description == 'both_king':
        if language == 'ru':  return 'Ничья! Оба короля у цели!'
        elif language == 'en':return 'Draw! Both kings are on target!'
        elif language == 'fr':return 'Tirage au sort! \nLes deux rois sont sur la cible!'
        elif language == 'es':return '¡Empate! Ambos rey el objetivo!'
        elif language == 'de':return 'Unentschieden! \nBeide Könige sind am Ziel!'

    # for frozen chess
    elif description == 'both_frozen':
        if language == 'ru':
            return 'Оба короля погибли. \nНичья.'
        if language == 'en':
            return "Both kings are dead. \n Draw."
        if language == 'fr':
            return  "Les deux rois sont morts. \n Tirage au sort."
        if language == 'es':
            return "Ambos reyes murieron. \n Empate."
        if language == 'de':
            return "Beide Könige starben. \n Unentschieden."

    if description == 'white_frozen':
        if language == 'ru':
            return 'Белый король погиб. \n Чёрные победили!'
        if language == 'en':
            return 'The White King is dead. \n Black won!'
        if language == 'fr':
            return  'Le roi blanc est mort. \n les Noirs ont gagné!'
        if language == 'es':
            return 'El rey blanco ha muerto. \n ¡los Negros ganaron!'
        if language == 'de':
            return 'Der Weiße König ist tot. \n Die Schwarzen haben gewonnen!'

    if description == 'black_frozen':
        if language == 'ru':
            return 'Чёрный король погиб. \n Белые победили!'
        if language == 'en':
            return 'The Black King is dead. \n White won!'
        if language == 'fr':
            return  'Le roi noir est mort. \n les Blancs ont gagné!'
        if language == 'es':
            return 'El rey negro ha muerto. \n ¡los Blancos ganaron!'
        if language == 'de':
            return 'Der schwarze König ist tot. \n Die Weißen haben gewonnen!'

    else:
        print(description)
        return 'error_2'


def tutorial(language,description):
    if description == 'to_game':
        if language == 'ru':    return 'К игре'
        elif language == 'en':  return 'To game'
        elif language == 'fr':  return 'Au jeu'
        elif language == 'es': return 'Al juego'
        elif language == 'de': return 'zum Spiel'

    elif description == 'next': 
        if language == 'ru':     return 'Далее'
        elif language == 'en':   return 'Go on'
        elif language == 'fr':   return 'Ensuite'
        elif language == 'es': return 'Adelante'
        elif language == 'de':  return 'Weiter'

    elif description == 'repeat':
        if language == 'ru' :  return 'Ещё раз'
        elif language == 'en': return 'Repeat'
        elif language == 'fr': return 'Une fois de plus'
        elif language == 'es': return 'una vez más'
        elif language == 'de': return 'Noch einmal'

    elif description == 'see':
        if language == 'ru' :return 'Смотреть'
        elif language == 'en': return 'To see'
        elif language == 'fr': return 'regarder'
        elif language == 'es': return 'mirar'
        elif language == 'de': return 'sehen'

    elif description == 'move':
        if language == 'ru' :return 'Фигуру можно двигать!'
        elif language == 'en': return 'You can move figure!'
        elif language == 'fr': return 'la figure peut être déplacée!'
        elif language == 'es': return 'la figura se puede mover!'
        elif language == 'de': return '!'

    elif 'classic' in description:
        return get_classic(language,description[8:])
    
    elif 'fisher' in description:
        return get_fisher(language,description[7:])
    
    elif description[:5] == 'horse':
        return get_horse(language,description[6:] )

    elif 'alamos' in description:
        return get_alamos(language,description[7:])

    elif 'permut' in description:
        return get_permutation(language,description[7:])
    
    elif 'magik' in description:
        return get_magik(language,description[6:])
    
    elif 'glinskiy' in description:
        return get_glinskiy(language,description[9:])
    
    elif 'round' in description:
        return get_round(language,description[6:])

    elif 'bizantion' in description:
        return get_biz(language,description[10:])

    elif 'kuej' in description:
        return get_kuej(language,description[5:])
    
    elif 'garner' in description:
        return get_garner(language,description[7:])

    elif 'horde' in description:
        return get_horde(language,description[6:])
    
    elif 'weak' in description:
        return get_weak(language,description[5:])

    elif 'kamikadze' in description:
        return get_kamikadze(language,description[10:])
    
    elif 'bad' in description:
        return get_bad_chess(language,description[4:])
    
    elif 'rase' in description:
        return get_rasing(language,description[5:])
    
    elif 'haos' in description:
        return get_haos(language,description[5:])
    
    elif 'shcatranj' in description:
        return get_schatranj(language,description[10:])

    elif 'dark' in description:
        return get_dark(language,description[5:])

    else:
        return 'error_2'


def interface_text(language,description,params=None):
    if description == 'file':
        if language == 'ru':
            return 'Файл'
        if language == 'en':
            return 'File'
        if language == 'fr':
            return  'Fichier'
        if language == 'es':
            return 'File'
        if language == 'de':
            return 'File'

    if description == 'mode':
        if language == 'ru':
            return 'Режим'
        if language == 'en':
            return 'Mode'
        if language == 'fr':
            return  'Mode'
        if language == 'es':
            return 'Modo'
        if language == 'de':
            return 'Modus'
    
    if description == 'saved':
        if language == 'ru':
            return 'Cохранено'
        if language == 'en':
            return 'Saved'
        if language == 'fr':
            return  'Enregistré'
        if language == 'es':
            return 'Guardado'
        if language == 'de':
            return 'Spielstand'

    if description == 'playtime':
        if language == 'ru':
            return 'Времени'
        if language == 'en':
            return 'You have time'
        if language == 'fr':
            return  'Temps'
        if language == 'es':
            return 'Tienes tiempo'
        if language == 'de':
            return 'haben Zeit'

    if description == 'cur_move':
        if language == 'ru':
            return 'Ход'
        if language == 'en':
            return 'Move'
        if language == 'fr':
            return  'Déplacer'
        if language == 'es':
            return 'Movimiento'
        if language == 'de':
            return 'Umzug'

    if description == 'color_move':
        if language == 'ru':
            return 'Цвет ходит'
        if language == 'en':
            return 'Color move'
        if language == 'fr':
            return  'Couleur déplacer'
        if language == 'es':
            return 'Color mover'
        if language == 'de':
            return 'Color bewegen'

    if description == '':
        if language == 'ru':
            return ''
        if language == 'en':
            return ''
        if language == 'fr':
            return  ''
        if language == 'es':
            return ''
        if language == 'de':
            return ''
    
    print(description)
    return 'error in interface'


def get_classic(language,description):
    if 'description' in description:
        if language == 'ru':
            return 'Классические шахматы являются очень популяронй игрой. На квaдратном поле 8х8 два игрока по очереди двигают фигуры своего цвета( начинают белые). Возможно 3 исхода партии( победа белых , чёрных или ничья). Цель - поставить мат. Расстановка фигур в начале игры изображена на картинке.'
        if language == 'en':
            return 'Classic chess is a very popular game. On an 8x8 square field, two players take turns moving figures of their own color( white starts). There are 3 possible outcomes of the game( white wins, black wins, or draws). The goal is to checkmate. The placement of the figures at the beginning of the game is shown in the picture.'
        if language == 'fr':
            return 'Les échecs classiques sont un jeu très populaire. Sur un terrain carré de 8x8, deux joueurs se relaient pour déplacer les pièces de leur couleur( commencent en blanc). Peut-être 3 résultats du parti (victoire des blancs , des noirs ou un match nul). Le but est de mettre un tapis. L\'arrangement des formes au début du jeu est représenté dans l\'image.'
        if language == 'es':
            return 'El ajedrez clásico es un juego muy popular. En un campo cuadrado de 8x8, dos jugadores se turnan para mover las piezas de su color( comienzan en blanco). Tal vez 3 resultados del partido (victoria blanca , negra o empate). El objetivo es poner un tapete. La disposición de las piezas al comienzo del juego se muestra en la imagen.'
        if language == 'de':
            return 'Klassisches Schach ist ein sehr beliebtes Spiel. Auf einem quadratischen Feld 8x8 bewegen sich zwei Spieler abwechselnd die Figuren Ihrer Farbe( beginnen weiß). Vielleicht 3 Ergebnisse der Partei (Sieg der weißen , schwarzen oder Unentschieden). Ziel ist es, die Matte zu setzen. Die Anordnung der Figuren zu Beginn des Spiels ist auf dem Bild dargestellt.'

    if description == 'horse':
        if language == 'ru':
            return 'У каждой фигуры свой ход. Конь - единственная фигура, которая может ходить всегда, если нет шаха( вражеские фигуры никогда не загораживают, не мешают). Ходит так: сначала 2 клетки в одну сторону, потом 1 клетка в другую, в бок от направления двух клеток.'
        if language == 'en':
            return 'Each piece has its own turn. The knight is the only piece that can always walk if there is no check( enemy pieces never block, do not interfere). It goes like this: first 2 cells in one direction, then 1 cell in the other, sideways from the direction of the two cells.'
        if language == 'fr':
            return  'Chaque chiffre a son propre mouvement. Le cheval est la seule figure qui peut toujours marcher s\'il n\'y a pas de Shah( les figures ennemies ne bloquent jamais, n\'interfèrent pas). Il va comme ceci: d\'abord 2 cellules dans un sens, puis 1 cellule dans l\'autre, sur le côté de la direction des deux cellules.'
        if language == 'es':
            return 'Cada figura tiene su propio movimiento. El caballo es la única figura que puede caminar siempre si no hay Shah (las figuras enemigas nunca se bloquean, no interfieren). Va así: primero 2 células en un lado, luego 1 célula en el otro, en el lado de la dirección de las dos células.'
        if language == 'de':
            return 'Jede Figur hat Ihren eigenen Zug. Das Pferd ist die einzige Figur, die immer gehen kann, wenn es keinen Shah gibt( die feindlichen Figuren blockieren niemals, stören nicht). Geht so: zuerst 2 Zellen in einer Richtung, dann 1 Zelle in der anderen Seite aus der Richtung der beiden Zellen.'

    if description == 'bishop':
        if language == 'ru':
            return 'Cлон ходит по диагонали на любое колличество клеток, если на пути к ней не стоит другая фигура( любого цвета).'
        if language == 'en':
            return 'The bishop moves diagonally on any number of squares, if there is no other figure( of any color) on the way to it. '
        if language == 'fr':
            return  'L\'éléphant marche en diagonale sur n\'importe quel nombre de cellules, à moins qu\'il n\'y ait une autre figure( de n\'importe quelle couleur) sur le chemin. '
        if language == 'es':
            return 'El elefante camina en diagonal sobre cualquier número de células, a menos que haya otra figura( de cualquier color) en el camino hacia ella.'
        if language == 'de':
            return 'Der Elefant geht Diagonal auf jede Anzahl von Zellen, es sei denn, eine andere Figur( jede Farbe) steht auf dem Weg zu Ihr. '

    if description == 'rook':
        if language == 'ru':
            return 'Ладья ходит по горизонтали и по вертикали на любое количество клеток, если путь не преграждают другие фигуры. '
        if language == 'en':
            return 'The rook moves horizontally and vertically on any number of squares, if the path is not blocked by other pieces.'
        if language == 'fr':
            return  'La tour marche horizontalement et verticalement sur n\'importe quel nombre de cellules, à moins que le chemin ne soit bloqué par d\'autres formes. '
        if language == 'es':
            return 'La torre camina horizontal y verticalmente en cualquier número de células, a menos que el camino esté bloqueado por otras formas.'
        if language == 'de':
            return 'Der Turm geht horizontal und vertikal auf eine beliebige Anzahl von Zellen, wenn der Weg nicht von anderen Figuren blockiert wird. '

    if description == 'queen':
        if language == 'ru':
            return  'Ферзь считается самой сильной фигурой. Он ходит ,как слон и  ладья. Поэтому новички часто увлекаются \"охотой\" на вражеского ферзя и проигрывают. Есть много примеров, когда игрок проигрывал, имея лишнего ферзя. Помните, что главное - расположение фигуры, а не её сила, ведь шахматы - игра на логику и тактику!'
        if language == 'en':
            return 'The queen is considered the strongest piece. He moves like a bishop and a rook. Therefore, beginners often get carried away \ "hunting\" for the enemy queen and lose. There are many examples of a player losing with an extra queen. Remember that the main thing is the location of the piece, not its strength, because chess is a game of logic and tactics!'
        if language == 'fr':
            return  'La reine est considérée comme la figure la plus forte. Il marche comme un éléphant et une tour. Par conséquent, les nouveaux arrivants sont souvent accro à la"chasse" à la reine ennemie et perdent. Il y a beaucoup d\'exemples où un joueur a perdu en ayant une reine supplémentaire. Rappelez - vous que l\'essentiel est l\'emplacement de la figure, et non sa force, car les échecs sont un jeu de logique et de tactique!'
        if language == 'es':
            return 'La reina es considerada la figura más fuerte. Camina como un elefante y una torre. Por lo tanto, los principiantes a menudo se dejan llevar por la \"caza\" de la reina enemiga y pierden. Hay muchos ejemplos en los que un jugador pierde por tener una reina extra. Recuerde que lo principal es la ubicación de la pieza, y no su fuerza, porque el ajedrez es un juego de lógica y táctica.'
        if language == 'de':
            return 'Die Königin gilt als die stärkste Figur. Er geht wie ein Elefant und ein Turm. Daher sind Anfänger oft süchtig \ "Jagd\" auf die feindliche Königin und verlieren. Es gibt viele Beispiele, in denen ein Spieler verloren hat, indem er eine zusätzliche Königin hat. Denken Sie daran, dass die Hauptsache - die Lage der Figur, nicht Ihre Stärke, denn Schach - ein Spiel der Logik und Taktik!'

    if description == 'pawn':
        if language == 'ru':
            return 'Пешка является единственной фигурой, которая не может ходить назад! Только в сторону врага! По 1 клетке за ход, но если пешка ещё не ходила, она может сходить на две. Дойдя до последней линии, пешка превращается в любую фигуру из 4 предыдущих. Рубит и атакует пешка наискосок, не так, как ходит.'
        if language == 'en':
            return 'The pawn is the only piece that can\'t move backwards! Only in the direction of the enemy! 1 square per turn, but if the pawn has not yet moved, it can go to two. After reaching the last line, the pawn turns into any piece from the previous 4. The pawn cuts and attacks diagonally, not as it moves.'
        if language == 'fr':
            return  'Un pion est la seule pièce qui ne peut pas marcher en arrière! Seulement vers l\'ennemi! 1 cellule par tour, mais si le pion n\'a pas encore marché, il peut aller à deux. Après avoir atteint la Dernière ligne, le pion se transforme en n\'importe quelle pièce des 4 précédentes. Le pion coupe et attaque obliquement, pas comme il marche.'
        if language == 'es':
            return 'El peón es la única pieza que no puede caminar hacia atrás! ¡Solo en la dirección del enemigo! 1 casilla por turno, pero si el peón aún no ha caminado, puede ir a dos. Al llegar a la Última línea, el peón se transforma en cualquier figura de los 4 anteriores. Corta y ataca al peón de forma oblicua, no como camina.'
        if language == 'de':
            return 'Der Bauer ist die einzige Figur, die nicht rückwärts gehen kann! Nur in Richtung des Feindes! 1 Zelle pro Runde, aber wenn der Bauer noch nicht gegangen ist, kann er für zwei gehen. Wenn Sie die Letzte Zeile erreichen, verwandelt sich der Bauer in eine beliebige Figur aus den vorherigen 4. Hackt und greift der Bauer schräg, nicht wie er geht.'

    if description == 'pawn2':
        if language == 'ru':
            return 'Если белая пешка дошла до 5 горизонтали (чёрная до четвёртой) , а вражеская пешка воспользовалась шансом сходить на 2 поля сразу, то вы можете срубить её, но сразу, следующим ходом уже нельзя. Это называется \"взятие на проходе\". Если враг ходит по красной стрелке, вы можете сходить по зелёной и срубить.'
        if language == 'en':
            return 'If the white pawn reached the 5th horizontal (the black pawn reached the fourth), and the enemy pawn took the chance to go to 2 squares at once, then you can cut it down, but immediately, the next move is no longer possible. This is called \ " taking on the pass\". If the enemy walks on the red arrow, you can go on the green and cut down.'
        if language == 'fr':
            return  'Si le pion blanc a atteint la 5e ligne horizontale (noire à la 4e) et que le pion ennemi a profité de la chance d\'aller sur 2 champs à la fois, vous pouvez le couper, mais vous ne pouvez pas le faire immédiatement. C\'est ce qu\'on appelle"prendre sur le passage". Si l\'ennemi marche sur la flèche rouge, vous pouvez aller sur le vert et couper.'
        if language == 'es':
            return 'Si el peón blanco llegó a la horizontal 5 (negro a la cuarta), y el peón enemigo aprovechó la oportunidad de ir a 2 campos a la vez, entonces puedes cortarlo, pero inmediatamente, el siguiente movimiento ya no es posible. Esto se llama \ " tomar en el pasillo\". Si el enemigo camina por la flecha roja, puede ir por el verde y cortar.'
        if language == 'de':
            return 'Wenn der weiße Bauer 5 horizontale (schwarze bis vierte) erreicht hat und der gegnerische Bauer die Chance genutzt hat, auf zwei Felder auf einmal zu gehen, dann kannst du ihn abschneiden, aber sofort ist der nächste Zug nicht mehr möglich. Dies wird als \ "take on Pass\" bezeichnet. Wenn der Feind auf dem roten Pfeil geht, können Sie auf dem grünen gehen und schneiden.'

    if description == 'king':
        if language == 'ru':
            return 'Король является самой ценной фигурой.Но его нельзя срубить.Если на него напали, а убежать им, закрыть его или срубить врага не получается, то он получает мат, и игрок этого цвета проигрывает.Иначе это - шах, и короля нужно спасать! Ходит король на любую соседнюю клетку, Если она не атакована врагом. '
        if language == 'en':
            return 'The king is the most valuable piece.But it can\'t be cut down.If he is attacked, and it is not possible to escape, close him or cut down the enemy, then he gets a checkmate, and the player of this color loses.Otherwise, it is the check, and the king must be saved! The king moves to any adjacent square, if it is not attacked by the enemy. '
        if language == 'fr':
            return  'Le roi est la figure la plus précieuse.Mais il ne peut pas être coupé.S\'il est attaqué et qu\'il ne peut pas s\'échapper, le fermer ou abattre l\'ennemi, il reçoit un tapis et le joueur de cette couleur perd.Sinon, c\'est Shah, et le roi doit être sauvé! Le roi marche sur n\'importe quelle cellule voisine, Si elle n\'est pas attaquée par l\'ennemi. '
        if language == 'es':
            return 'El rey es la figura más valiosa.Pero no se puede cortar.Si es atacado, y escapar de ellos, cerrarlo o cortar al enemigo no funciona, entonces recibe una estera, y el jugador de este color pierde.De lo contrario, es un jaque, ¡y el rey debe ser salvado! El rey camina sobre cualquier jaula cercana, A menos que sea atacada por el enemigo.'
        if language == 'de':
            return 'Der König ist die wertvollste Figur.Aber es kann nicht geschnitten werden.Wenn er angegriffen wird, und Ihnen zu entkommen, schließen Sie es oder schneiden Sie den Feind nicht funktioniert, bekommt er eine Matte, und der Spieler dieser Farbe verliert.Sonst ist es der Schah, und der König muss gerettet werden! Der König geht auf jede benachbarte Zelle, Wenn Sie nicht vom Feind angegriffen wird.'

    if description == 'rocking':
        if language == 'ru':
            return 'Рокировка - особый ход! Она позволяет спрятать короля в углу. Она возможна, если короли и ладья ещё не ходили. А ещё не должно быть шаха королю, и все поля между королём и ладьёй должны быть свободны и не атакованы врагом! Белые сделали короткую рокировку, чёрные - длинную. Рокировка - ход короля, это важно!'
        if language == 'en':
            return 'Castling is a special move! It allows you to hide the king in a corner. It is possible if the kings and the rook have not yet moved. And there should be no check to the king, and all the fields between the king and the rook should be free and not attacked by the enemy! White made a short castling, black - a long castling. Castling is the king\'s move, it\'s important!'
        if language == 'fr':
            return  'Rocking est un mouvement spécial! Elle permet de cacher le roi dans un coin. Elle est possible si les rois et la tour n\'ont pas encore marché. Et il ne devrait pas y avoir de Shah au roi, et tous les champs entre le roi et la tour devraient être libres et non attaqués par l\'ennemi! Les blancs ont fait une courte Roque, les noirs une longue. Le Roc est le mouvement du roi, c\'est important!'
        if language == 'es':
            return '¡El enroque es un movimiento especial! Te permite esconder al rey en la esquina. Es posible si los reyes y la torre aún no han caminado. ¡Y no debe haber Shah para el rey, y todos los campos entre el rey y la torre deben ser libres y no ser atacados por el enemigo! Los blancos hicieron un enroque corto, los negros hicieron uno largo. ¡El enroque es el movimiento del rey, es importante!'
        if language == 'de':
            return 'Rochade ist ein besonderer Zug! Es ermöglicht Ihnen, den König in einer Ecke zu verstecken. Es ist möglich, wenn Könige und Türme noch nicht gegangen sind. Und es sollte keinen Schah für den König geben, und alle Felder zwischen dem König und dem Turm sollten frei sein und nicht vom Feind angegriffen werden! Die weißen machten eine kurze Rochade, die schwarzen eine lange. Rochade ist der Zug des Königs, das ist wichtig!'

    if description == 'end':
        if language == 'ru':
            return 'Все поля, кудa может сходить фигура, она атакует(кроме пешки, она атакует иначе). Если фигура атакует врага, то она может его срубить. При этом фигура врага безвозвратно снимается с доски, а своя встаёт на его место. Это поможет победить! Но не увлекайтесь , главное - позиция, а не количество и сила фигур, хотя и они тоже важны. Думайте и побеждайте! Удачных ходов и красивых партий!'
        if language == 'en':
            return 'All fields, where figure can move , it attacks(except for the pawn, it attacks differently). If a piece attacks an enemy, it can cut it down. In this case, the enemy\'s piece is permanently removed from the board, and its own piece takes its place. This will help you win! But do not get carried away, the main thing is the position, not the number and strength of the pieces, although they are also important. Think and win! Good moves and beautiful games!'
        if language == 'fr':
            return  'Tous les champs où la figure peut aller, elle attaque(sauf le pion, elle attaque autrement). Si un personnage attaque un ennemi, il peut le couper. Dans le même temps, la figure de l\'ennemi est irrévocablement retirée du tableau et la Sienne prend sa place. Cela aidera à gagner! Mais ne vous laissez pas emporter , l\'essentiel est la position, pas le nombre et la force des figures, bien qu\'elles soient également importantes. Pensez et gagnez! Coups réussis et belles parties!'
        if language == 'es':
            return 'Todos los campos donde la figura puede ir, ataca (excepto el peón, ataca de otra manera). Si la figura ataca al enemigo, puede cortarlo. Al mismo tiempo, la figura del enemigo se retira irrevocablemente del tablero, y la suya cae en su lugar. ¡Esto ayudará a ganar! Pero no se deje llevar, lo principal es la posición, no la cantidad y la fuerza de las figuras, aunque también son importantes. ¡Piensa y gana! ¡Buenos movimientos y hermosas fiestas!'
        if language == 'de':
            return 'Alle Felder, in die die Figur gehen kann, greift Sie an(außer dem Bauern greift Sie sonst an). Wenn eine Figur einen Feind angreift, kann Sie ihn abschneiden. In diesem Fall wird die Figur des Feindes unwiderruflich vom Brett entfernt, und seine eigene steht an seiner Stelle. Es wird helfen, zu gewinnen! Aber lass dich nicht hinreißen , die Hauptsache ist die Position, nicht die Anzahl und Stärke der Figuren, obwohl Sie auch wichtig sind. Denken und gewinnen! Erfolgreiche Züge und schöne Parteien!'

    return 'error3 classic'


def get_fisher(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Шахматы фишера имеют много названий : "Рэндом 960" , "Шахматы 960" и пр. Были придуманы для борьбы с компьютерами и с дебютными просчётами до конца партии. Как нетрудно догадаться, своё название они получили потому, что все фигуры в начале игры расставляются рандомно(но с некоторыми правилами), поэтому возможно 960 начальных расстановок'
        if language == 'en':
            return 'Fischer\'s chess has many names : "Random 960", "Chess 960", etc. Were invented to deal with computers and with opening miscalculations until the end of the game. As you might guess, they got their name because all the pieces at the beginning of the game are placed randomly(but with some rules), so 960 initial positions are possible'
        if language == 'fr':
            return  'Les échecs de Fisher ont de nombreux noms : "Random 960", "Chess 960", etc. Ont été inventés pour lutter contre les Ordinateurs et les erreurs de calcul initiales jusqu\'à la fin de la partie. Comme il n\'est pas difficile de deviner, ils ont reçu leur nom parce que toutes les pièces au début du jeu sont placés au hasard (mais avec certaines règles), il est donc possible 960 arrangements initiaux'
        if language == 'es':
            return 'El ajedrez de Fisher tiene muchos nombres : "random 960", "Chess 960", etc. Fueron inventados para luchar contra las computadoras y con errores de cálculo de debut hasta el final de la fiesta. Como no es difícil adivinar, recibieron su nombre porque todas las figuras al comienzo del juego se colocan aleatoriamente(pero con algunas reglas), por lo que es posible 960 posiciones iniciales'
        if language == 'de':
            return 'Fischers Schach hat viele Namen:" Rand 960"," Schach 960 " usw. wurden erfunden, um Computer und Debüt-Fehlkalkulationen bis zum Ende der Partie zu bekämpfen. Wie leicht zu erraten, Ihren Namen haben Sie, weil alle Figuren zu Beginn des Spiels zufällig angeordnet sind (aber mit einigen Regeln), so dass es möglich ist, 960 anfängliche Aufstellungen'

    if description == 'second':
        if language == 'ru':
            return 'Все фигуры ходят , как в классических шахматах.Как ходят в них, можно посмотрать в обучении классических шахмат. Теперь обсудим особенности этих шахмат... Рандом вносит свои  поправки. Думать нужно с 1 хода. И рокировка делается иначе.'
        if language == 'en':
            return 'All the pieces move like in classical chess.How to walk in them, you can see in the training of classical chess. Now we will discuss the features of these chess games... Random makes his own corrections. You need to think from the 1st turn. And castling is done differently.'
        if language == 'fr':
            return  'Toutes les pièces marchent comme dans les échecs classiques.Comment ils vont, vous pouvez regarder dans la formation des échecs classiques. Maintenant, nous allons discuter des caractéristiques de ces échecs... Random apporte ses modifications. Vous devez penser avec 1 mouvement. Et le Roque est fait différemment.'
        if language == 'es':
            return 'Todas las piezas caminan como en el ajedrez clásico.Cómo caminar en ellos, se puede ver en el aprendizaje de ajedrez clásico. Ahora vamos a discutir las características de este ajedrez... Random presenta sus enmiendas. Es necesario pensar con 1 movimiento. Y el enroque se hace de manera diferente.'
        if language == 'de':
            return 'Alle Figuren laufen wie im klassischen Schach.Wie man in Ihnen geht, kann man im Unterricht des klassischen Schachs sehen. Jetzt besprechen wir die Besonderheiten dieses Schachs... Random nimmt seine änderungen vor. Denken Sie mit 1 Zug. Und die Rochade wird anders gemacht.'
    
    if description == 'rocking':
        if language == 'ru':
            return 'Сначала хотели вообще выкинуть рокировку. Но потом рeшили ставить фигуры туда, где должна стоять фигура при рокировке в классических, где бы не стояли король и ладья . Вот как это выглядит. Ладья и король не должны были до этого ходить.'
        if language == 'en':
            return 'At first, authors wanted to throw out rocking. But then they decided to put the pieces where the figure should stand when rocking in the classic ones, where the king and rook would not stand . Here\'s what it looks like. The rook and the king should not have moved before.'
        if language == 'fr':
            return 'Au début, ils voulaient jeter le Rock. Mais ensuite, ils ont décidé de mettre les chiffres à l\'endroit où la figure devrait se tenir lorsqu\'elle est roquée dans le classique, où qu\'il y ait un roi et une tour . Voici à quoi ça ressemble. La tour et le roi n\'auraient pas dû marcher avant.'
        if language == 'es':
            return 'Primero querían tirar el enroque por completo. Pero luego decidieron poner las figuras donde debería estar la figura cuando se enroque en los clásicos, donde no estuviera el rey y la torre . Así es como se ve. La torre y el rey no deberían haber caminado antes.'
        if language == 'de':
            return 'Zuerst wollten Sie die Rochade überhaupt rauswerfen. Aber dann beschlossen, die Figuren dort zu platzieren, wo die Figur bei der Rochade im klassischen stehen sollte, wo der König und der Turm nicht standen . So sieht es aus. Der Turm und der König sollten vorher nicht gehen.'

    if description == 'end':
        if language == 'ru':
            return 'Рандом - это весело. Вы быстро это поймёте!!! Наслаждайтесь игрой!'
        if language == 'en':
            return 'Random is fun. You will quickly understand this!!! Enjoy the game!'
        if language == 'fr':
            return  'Random est amusant. Vous comprendrez vite!!! Profitez du jeu!'
        if language == 'es':
            return 'Random es divertido. ¡Lo entenderás rápidamente!!! ¡Disfruta el juego!'
        if language == 'de':
            return 'Random macht Spaß. Sie werden es schnell verstehen!!! Genießen Sie das Spiel!'

    return 'error3 fisher'


def get_horse(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Как вам такое, мастер? Все правила из классических шахмат, но есть только конь, король и пешка! В бой, воекомандующий!'
        if language == 'en':
            return 'How do you like that, master? All the rules are from classic chess, but you have only a knight, a king and a pawn! Into battle, Commander!'
        if language == 'fr':
            return  'Comment ça va, maître? Toutes les règles sont des échecs classiques, mais il n\'y a que le cheval, le roi et le pion! Au combat, commandant!'
        if language == 'es':
            return '¿Qué le parece, maestro? Todas las reglas del ajedrez clásico, pero sólo hay un caballo, un rey y un peón! ¡A la batalla, comandante!'
        if language == 'de':
            return 'Wie geht \' s Ihnen, Meister? Alle Regeln des klassischen Schachspiels, aber es gibt nur ein Pferd, König und Bauer! In die Schlacht, Kommandant!'

    if description == 'horse':
        if language == 'ru':
            return 'У каждой фигуры свой ход. Конь ходит так: сначала 2 клетки в одну сторону, потом 1 клетка в другую, в бок от направления двух клеток. Можно двигать фигуру.'
        if language == 'en':
            return 'Each piece has its own turn. The knight moves like this: first 2 cells in one direction, then 1 cell in the other, sideways from the direction of the two cells. .'
        if language == 'fr':
            return  'Chaque chiffre a son propre mouvement. Le cheval marche comme ceci: d\'abord 2 cellules dans un sens, puis 1 cellule dans l\'autre, sur le côté de la direction des deux cellules. Vous pouvez déplacer la figure.'
        if language == 'es':
            return 'Cada figura tiene su propio movimiento. El caballo camina así: primero 2 células en un lado, luego 1 célula en el otro, a un lado de la dirección de las dos células. Puedes mover la figura.'
        if language == 'de':
            return 'Jede Figur hat Ihren eigenen Zug. Das Pferd geht so: zuerst 2 Zellen in einer Richtung, dann 1 Zelle in der anderen Seite aus der Richtung der beiden Zellen. Sie können die Figur bewegen.'

    if description == 'pawn':
        if language == 'ru':
            return 'Пешка является единственной фигурой, которая не может ходить назад! Только в сторону врага! По 1 клетке за ход, но если пешка ещё не ходила, она может сходить на две. Дойдя до последней линии, пешка превращается в коня. Рубит и атакует пешка наискосок, не так, как ходит.'
        if language == 'en':
            return 'The pawn is the only piece that can\'t move backwards! Only in the direction of the enemy! 1 square per turn, but if the pawn has not yet moved, it can go to two. After reaching the last line, the pawn turns into a knight. The pawn cuts and attacks diagonally, not as it moves.'
        if language == 'fr':
            return  'Un pion est la seule pièce qui ne peut pas marcher en arrière! Seulement vers l\'ennemi! 1 cellule par tour, mais si le pion n\'a pas encore marché, il peut aller à deux. Après avoir atteint la Dernière ligne, le pion se transforme en cheval. Le pion coupe et attaque obliquement, pas comme il marche.'
        if language == 'es':
            return 'El peón es la única pieza que no puede caminar hacia atrás! ¡Solo en la dirección del enemigo! 1 casilla por turno, pero si el peón aún no ha caminado, puede ir a dos. Al llegar a la Última línea, el peón se convierte en un caballo. Corta y ataca al peón de forma oblicua, no como camina.'
        if language == 'de':
            return 'Der Bauer ist die einzige Figur, die nicht rückwärts gehen kann! Nur in Richtung des Feindes! 1 Zelle pro Runde, aber wenn der Bauer noch nicht gegangen ist, kann er für zwei gehen. Die Letzte Linie erreicht, verwandelt sich der Bauer in ein Pferd. Hackt und greift der Bauer schräg, nicht wie er geht.'

    if description == 'pawn2':
        if language == 'ru':
            return 'Если белая пешка дошла до 5 горизонтали (чёрная до четвёртой) , а вражеская пешка воспользовалась шансом сходить на 2 поля сразу, то вы можете срубить её, но сразу, следующим ходом уже нельзя. Это называется \"взятие на проходе\".'
        if language == 'en':
            return 'If the white pawn reached the 5th horizontal (the black pawn reached the fourth), and the enemy pawn took the chance to go to 2 squares at once, then you can cut it down, but immediately, the next move is no longer possible. This is called \ " taking on the pass\". '
        if language == 'fr':
            return  'Si le pion blanc a atteint la 5e ligne horizontale (noire à la 4e) et que le pion ennemi a profité de la chance d\'aller sur 2 champs à la fois, vous pouvez le couper, mais vous ne pouvez pas le faire immédiatement. C\'est ce qu\'on appelle"prendre sur le passage".'
        if language == 'es':
            return 'Si el peón blanco llegó a la horizontal 5 (negro a la cuarta), y el peón enemigo aprovechó la oportunidad de ir a 2 campos a la vez, entonces puedes cortarlo, pero inmediatamente, el siguiente movimiento ya no es posible. Esto se llama \ " tomar en el pasillo\".'
        if language == 'de':
            return 'Wenn der weiße Bauer 5 horizontale (schwarze bis vierte) erreicht hat und der gegnerische Bauer die Chance genutzt hat, auf zwei Felder auf einmal zu gehen, dann kannst du ihn abschneiden, aber sofort ist der nächste Zug nicht mehr möglich. Dies wird als \ "take on Pass\" bezeichnet.'

    if description == 'king':
        if language == 'ru':
            return 'Король является самой ценной фигурой.Но его нельзя срубить.Если на него напали, а убежать им, закрыть его или срубить врага не получается, то он получает мат, и игрок этого цвета проигрывает.Иначе это - шах, и короля нужно спасать! Ходит король на любую соседнюю клетку, Если она не атакована врагом.'
        if language == 'en':
            return 'The king is the most valuable piece.But it can\'t be cut down.If he is attacked, and it is not possible to escape, close him or cut down the enemy, then he gets a checkmate, and the player of this color loses.Otherwise, it is the check, and the king must be saved! The king moves to any adjacent square, if it is not attacked by the enemy.'
        if language == 'fr':
            return  'Le roi est la figure la plus précieuse.Mais il ne peut pas être coupé.S\'il est attaqué et qu\'il ne peut pas s\'échapper, le fermer ou abattre l\'ennemi, il reçoit un tapis et le joueur de cette couleur perd.Sinon, c\'est Shah, et le roi doit être sauvé! Le roi marche sur n\'importe quelle cellule voisine, Si elle n\'est pas attaquée par l\'ennemi.'
        if language == 'es':
            return 'El rey es la figura más valiosa.Pero no se puede cortar.Si es atacado, y escapar de ellos, cerrarlo o cortar al enemigo no funciona, entonces recibe una estera, y el jugador de este color pierde.De lo contrario, es un jaque, ¡y el rey debe ser salvado! El rey camina sobre cualquier jaula cercana, A menos que sea atacada por el enemigo.'
        if language == 'de':
            return 'Der König ist die wertvollste Figur.Aber es kann nicht geschnitten werden.Wenn er angegriffen wird, und Ihnen zu entkommen, schließen Sie es oder schneiden Sie den Feind nicht funktioniert, bekommt er eine Matte, und der Spieler dieser Farbe verliert.Sonst ist es der Schah, und der König muss gerettet werden! Der König geht auf jede benachbarte Zelle, Wenn Sie nicht vom Feind angegriffen wird.'

    if description == 'end':
        if language == 'ru':
            return 'Все поля, кудa может сходить фигура, она атакует(кроме пешки, она атакует иначе). Если фигура атакует врага, то она может его срубить. При этом фигура врага безвозвратно снимается с доски, а своя встаёт на его место. Это поможет победить! Но не увлекайтесь , главное - позиция, а не количество и сила фигур, хотя и они тоже важны. Думайте и побеждайте! Удачных ходов и красивых партий!'
        if language == 'en':
            return 'All fields, where figure can go, it attacks(except for the pawn, it attacks differently). If a piece attacks an enemy, it can cut it down. In this case, the enemy\'s piece is permanently removed from the board, and its own piece takes its place. This will help you win! But do not get carried away, the main thing is the position, not the number and strength of the pieces, although they are also important. Think and win! Good moves and beautiful games!'
        if language == 'fr':
            return  'Tous les champs où la figure peut aller, elle attaque (sauf le pion, elle attaque autrement). Si un personnage attaque un ennemi, il peut le couper. Dans le même temps, la figure de l\'ennemi est irrévocablement retirée du tableau et la Sienne prend sa place. Cela aidera à gagner! Mais ne vous laissez pas emporter , l\'essentiel est la position, pas le nombre et la force des figures, bien qu\'elles soient également importantes. Pensez et gagnez! Coups réussis et belles parties!'
        if language == 'es':
            return 'Todos los campos donde la figura puede ir, ataca (excepto el peón, ella ataca de otra manera). Si la figura ataca al enemigo, puede cortarlo. Al mismo tiempo, la figura del enemigo se retira irrevocablemente del tablero, y la suya cae en su lugar. ¡Esto ayudará a ganar! Pero no se deje llevar, lo principal es la posición, no la cantidad y la fuerza de las figuras, aunque también son importantes. ¡Piensa y gana! ¡Buenos movimientos y hermosas fiestas!'
        if language == 'de':
            return 'Alle Felder, in die die Figur gehen kann, greift Sie an(außer dem Bauern greift Sie sonst an). Wenn eine Figur einen Feind angreift, kann Sie ihn abschneiden. In diesem Fall wird die Figur des Feindes unwiderruflich vom Brett entfernt, und seine eigene steht an seiner Stelle. Es wird helfen, zu gewinnen! Aber lass dich nicht hinreißen , die Hauptsache ist die Position, nicht die Anzahl und Stärke der Figuren, obwohl Sie auch wichtig sind. Denken und gewinnen! Erfolgreiche Züge und schöne Parteien!'

    return 'error3 horse'


def get_magik(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Всё, как в классических шахматах. Но каждые n ходов в центре происходит волшебство...\n Cовет: боритесь за центр!'
        if language == 'en':
            return 'It\'s just like in classic chess. But every n moves, magic happens in the center...\n Tip: Fight for the center!'
        if language == 'fr':
            return  'Tout comme dans les échecs classiques. Mais tous les n mouvements au centre, il y a de la magie...\n conseil: battez-vous pour le centre!'
        if language == 'es':
            return 'Todo es como en el ajedrez clásico. Pero cada n movimientos en el centro ocurre magia...\n Consejo: ¡lucha por el centro!'
        if language == 'de':
            return 'Alles wie im klassischen Schach. Aber alle n Züge in der Mitte passiert Magie...\n Tipp: Kämpfe für die Mitte!'


def get_alamos(language,description):

    if description == 'start':
        if language == 'ru':
            return 'Были придуманы для обучения искусственного интеллекта. Все правила классических шахмат, но убрали слонов, рокировку и двойной ход пешки'
        if language == 'en':
            return 'Were invented to train artificial intelligence. All the rules of classic chess, but removed the bishops, castling, and double pawn move.'
        if language == 'fr':
            return  'Ont été inventés pour former l\'intelligence artificielle. Toutes les règles des échecs classiques, mais ont enlevé les éléphants, le Roque et le double mouvement du pion'
        if language == 'es':
            return 'Fueron inventados para entrenar inteligencia artificial. Todas las reglas del ajedrez clásico, pero eliminaron los elefantes, el enroque y el doble movimiento del peón.'
        if language == 'de':
            return 'Wurden erfunden, um künstliche Intelligenz zu trainieren. Alle Regeln des klassischen Schachs, aber entfernt Elefanten, Rochade und Doppel-Zug Bauer.'

    if description == 'end':
        if language == 'ru':
            return 'Вы можете посмотреть обучение к классическим шахматам'
        if language == 'en':
            return 'You can watch the training for classical chess'
        if language == 'fr':
            return  'Vous pouvez regarder la formation aux échecs classiques'
        if language == 'es':
            return 'Puedes ver el entrenamiento para el ajedrez clásico'
        if language == 'de':
            return 'Ihr könnt Euch das klassische Schachtraining ansehen'

    return 'error3 alamos'

def get_permutation(language,description):

    if description == 'start':
        if language == 'ru':
            return 'В этих шахматах все фигуры ходят, как в классических шахматах, но стоит только фигуре сходить, так она сразу меняется.Эта разновидность, судя по описанию, идеально подходит для новичков, которые только учатся ценить силу фигур и мыслить стратегически. Желаем Удачи!'
        if language == 'en':
            return 'In this chess, all the pieces move like in classical chess, but as soon as a piece goes, it immediately changes.This variety, judging by the description, is ideal for beginners who are just learning to appreciate the power of figures and think strategically. Good Luck!'
        if language == 'fr':
            return  'Dans ces échecs, toutes les pièces vont comme dans les échecs classiques, mais il est seulement nécessaire d\'aller à la figure, de sorte qu\'il change immédiatement.Cette variété, à en juger par la Description, est idéale pour les débutants qui apprennent seulement à apprécier la force des formes et à penser de manière stratégique. Souhaitons Bonne Chance!'
        if language == 'es':
            return 'En este ajedrez, todas las piezas van como en el ajedrez clásico, pero solo vale la pena ir a la pieza, por lo que cambia inmediatamente.Esta variedad, a juzgar por la descripción, es ideal para principiantes que solo están aprendiendo a apreciar el poder de las figuras y pensar estratégicamente. ¡Buena Suerte!'
        if language == 'de':
            return 'In diesem Schach gehen alle Figuren wie im klassischen Schach, aber es ist nur notwendig, die Figur zu gehen, so dass es sofort ändert.Diese Art, nach der Beschreibung zu urteilen, ist ideal für Anfänger, die nur lernen, die Kraft der Figuren zu schätzen und strategisch zu denken. Viel Glück!'

    if description == 'cycle':
        if language == 'ru':
            return 'Вот цикл перестановок: \n конь -> слон\n cлон -> ладья\n ладья -> ферзь\n Ферзь -> конь\n Вы можете посмотреть \n правила классических шахмат'
        if language == 'en':
            return 'Here is the permutation cycle: \n knight -> bishop\n bishop -> rook\n rook -> queen\n Queen -> knight\n You can see \n rules of classical chess'
        if language == 'fr':
            return  'Voici une boucle de permutation: \n cheval - > éléphant \n éléphant - > tour \n tour - > reine \n Reine - > cheval \n vous pouvez regarder \n règles des échecs classiques'
        if language == 'es':
            return 'Aquí está el ciclo de permutaciones: \n caballo - > elefante \n elefante - > torre \n torre - > reina \n Reina- > caballo \n puedes ver \n reglas del ajedrez clásico'
        if language == 'de':
            return 'Hier ist ein Zyklus von Permutationen: \n Pferd - > Elefant \n Elefant - > Turm\n Turm - > Königin \n Königin- > Pferd \n Sie können \n Regeln des klassischen Schachs sehen'

    return 'error3 permutation'


def get_glinskiy(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Вот и шахматы Глинского! Изобретатель был инженером,хорошим инженером! Поле состоит из 91 шестиугольника, поэтому все ходы тут выглядят странно. Все фигуры ходят, как обычно, но форма доски накладывает свой отпечаток.'
        if language == 'en':
            return 'Here comes Glinsky\'s chess! The inventor was an engineer, a good engineer! The field consists of 91 hexagons, so all the moves here look strange. All the pieces move as usual, but the shape of the board leaves its mark.'
        if language == 'fr':
            return  'Voici les échecs de Glinsky! L\'inventeur était un ingénieur, un bon ingénieur! Le champ se compose de 91 hexagones, donc tous les mouvements ici semblent étranges. Toutes les formes marchent comme d\'habitude, mais la forme de la planche impose son empreinte.'
        if language == 'es':
            return '¡Aquí está el ajedrez de Glinsky! El inventor era un ingeniero, un buen ingeniero! El campo consta de 91 hexágonos, por lo que todos los movimientos aquí parecen extraños. Todas las formas caminan como de costumbre, pero la forma del tablero pone su huella.'
        if language == 'de':
            return 'Das ist Glinskys Schach! Der Erfinder war ein Ingenieur, ein guter Ingenieur! Das Feld besteht aus 91 Sechsecken, so dass alle Bewegungen hier seltsam Aussehen. Alle Figuren gehen wie gewohnt, aber die Form der Tafel ist geprägt.'

    if description == 'rook':
        if language == 'ru':
            return 'Ладья ходит так-же по вертикалям( тут это называется ортогоналями ), но их 3! Поэтому у ладьи так много ходов.'
        if language == 'en':
            return 'The rook also moves vertically( here it is called orthogonals), but there are 3 of them! That\'s why the rook has so many moves.'
        if language == 'fr':
            return  'La tour marche de la même manière le long des verticales (ici c\'est appelé orthogonales), mais il y en a 3! Par conséquent, la tour a tellement de mouvements.'
        if language == 'es':
            return 'La torre camina de la misma manera en las verticales (aquí se llama ortogonales), ¡pero hay 3! Por eso la torre tiene tantos movimientos.'
        if language == 'de':
            return 'Der Turm geht so vertikal (hier wird es orthogonalen genannt), aber es gibt 3! Deshalb hat der Turm so viele Züge.'

    if description == 'bishop':
        if language == 'ru':
            return 'Диагонали выглядят непривычно, но покраска в 3 цвета помогает. '
        if language == 'en':
            return 'The diagonals look strange, but painting in 3 colors helps.'
        if language == 'fr':
            return  'Les diagonales semblent inhabituelles, mais peindre en 3 couleurs aide. '
        if language == 'es':
            return 'Las diagonales se ven inusuales, pero pintar en 3 colores ayuda. '
        if language == 'de':
            return 'Diagonalen sehen ungewöhnlich aus, aber das malen in 3 Farben hilft. '

    if description == 'queen':
        if language == 'ru':
            return 'Из - за изменения геометрии ферзь становится страшно сильной фигурой. Смотрите сами:'
        if language == 'en':
            return 'Because of the geometry change, the queen becomes a terribly strong piece. See :'
        if language == 'fr':
            return  'En raison du changement de géométrie, la reine devient une figure terriblement forte. Voyez :'
        if language == 'es':
            return 'Debido al cambio de geometría, la reina se convierte en una figura terriblemente fuerte. Ver por mismo:'
        if language == 'de':
            return 'Aufgrund der änderung der geometrie wird die Königin zu einer furchtbar starken Figur. Sehen :'

    if description == 'horse':
        if language == 'ru':
            return ' Конь ходит по букве г, но она слегка изогнута. Да, и направлений движения тоже 6. А ещё он за 3 хода может сходить по большому кругу...Поищите,как!'
        if language == 'en':
            return 'The knight moves 2 in a straight line and 1 to the side, as before, but it looks curved. Yes, and the directions of movement are also 6. And he can go in a big circle in 3 moves...Find out how!'
        if language == 'fr':
            return  'Le cheval marche 2 en ligne droite et 1 sur le côté comme avant, mais il a l\'air courbé. Oui, et aussi 6. Et il peut aller dans un grand cercle en 3 mouvements...Cherchez comment!'
        if language == 'es':
            return 'El caballo camina 2 en línea recta y 1 hacia un lado como antes, pero se ve curvado. Sí, y las direcciones de tráfico también son 6. Y él en 3 movimientos puede ir en un gran círculo...¡Mira cómo!'
        if language == 'de':
            return 'Das Pferd geht 2 in einer geraden Linie und 1 zur Seite, wie zuvor, aber es sieht gekrümmt. Ja, und die Richtung der Bewegung ist auch 6. Und er kann für 3-Züge in einem großen Kreis gehen...Schauen Sie, wie!'

    if description == 'king':
        if language == 'ru':
            return 'Король ходит по ортогоналям и диагоналям по 1 клетке.Всё равно это много ходов. Король может запатовать другого в одиночку.И 2 ладьи не могут поставить линейный мат в одиночку.'
        if language == 'en':
            return 'The king moves on the orthogonals and diagonals of 1 square.It\'s still a lot of moves. The king can match the other one alone.And 2 rooks can\'t checkmate a line alone.'
        if language == 'fr':
            return  'Le roi marche sur les orthogonales et les diagonales de 1 cellule.C\'est quand même beaucoup de mouvements. Le roi peut en faire un autre seul.Et 2 tours ne peuvent pas mettre un tapis de ligne seul.'
        if language == 'es':
            return 'El rey camina sobre ortogonales y diagonales de 1 celda.Todavía son muchos movimientos. El rey puede empañar a otro solo.Y 2 torres no pueden poner la estera lineal solo.'
        if language == 'de':
            return 'Der König geht auf orthogonalen und Diagonalen auf 1 Zelle.Es sind immer noch viele Züge. Der König kann den anderen allein patentieren.Und 2 Türme können nicht allein eine lineare Matte setzen.'

    if description == 'pawn':
        if language == 'ru':
            return 'Пешка также ходит по вертикали( не на искосок по ортогонали! ) С первой позиции возможен двойной ход. Есть взятие на проходе. Стрелки это показывают. Зелёным показан ход.Красным - как рубит и атакует.'
        if language == 'en':
            return 'The pawn also moves vertically( not obliquely orthogonally! ) A double move is possible from the first position. There is a take on the pass. The arrows show this. Green shows the move.Red - as he cuts and attacks.'
        if language == 'fr':
            return  'Le pion marche aussi verticalement (pas sur les pentes orthogonales! ) À partir de la première position, un double mouvement est possible. Il y a une prise sur l\'allée. Les flèches le montrent. Le vert indique le mouvement.Rouge-comme coupe et attaque.'
        if language == 'es':
            return 'El peón también camina verticalmente (¡no en la búsqueda de ortogonali! ) Desde la primera posición es posible un doble movimiento. Hay una toma en el pasillo. Las flechas lo muestran. Verde muestra el movimiento.Rojo - como cortar y atacar.'
        if language == 'de':
            return 'Der Bauer geht auch vertikal (nicht schräg nach orthogonal! Von der ersten Position aus ist ein Doppelschlag möglich. Es gibt eine Aufnahme auf dem Gang. Die Pfeile zeigen es. Grün zeigt den Verlauf.Rot-wie schneidet und greift.'

    if description == 'end':
        if language == 'ru':
            return 'Рокировки нет. Пат приносит малозначимую победу. Примите пожелания побед, будущие полководцы!'
        if language == 'en':
            return 'There is no castling. Pat brings a minor victory. Accept the wishes of victory, future generals!'
        if language == 'fr':
            return  'Pas de Roque. Pat apporte une victoire insignifiante. Acceptez les souhaits de victoire, futurs généraux!'
        if language == 'es':
            return 'No hay enroque. Pat trae una victoria insignificante. ¡Acepta los deseos de victoria, futuros comandantes!'
        if language == 'de':
            return 'Es gibt keine Rochade. Pat bringt einen wenig aussagekräftigen Sieg. Akzeptieren Sie die Wünsche der Siege, zukünftige Generäle!'

    print('desctiption was "',description,'"')
    return 'error 3 glinskiy'

def get_round(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Посмотрите на доску!Этот вариант является современной версией древней игры в Византии. Главное, чтобы не закружилась голова от всего происходящего на поле битвы!'
        if language == 'en':
            return 'Look at the board!This version is a modern version of the ancient game in Byzantium. The main thing is not to get dizzy from everything that is happening on the battlefield!'
        if language == 'fr':
            return  'Regardez le tableau!Cette variante est une version moderne de l\'ancien jeu byzantin. L\'essentiel est de ne pas tourner la tête de tout ce qui se passe sur le champ de bataill'
        if language == 'es':
            return '¡Mira el tablero!Esta variante es una versión moderna del antiguo juego en Bizancio. ¡Lo principal es que no se Maree por todo lo que está sucediendo en el campo de batalla!'
        if language == 'de':
            return 'Schau dir das Brett an!Diese Variante ist eine moderne Version des alten Spiels in Byzanz. Die Hauptsache ist, nicht schwindlig von allem, was auf dem Schlachtfeld passiert!'

    if description == 'bishop':
        if language == 'ru':
            return 'Слон ходит по диагоналям. Всего 6 полей! Но опытный командир найдёт применение даже самой слабой фигуре! Разве не так?'
        if language == 'en':
            return 'The Bishop moves on the diagonals. Only 6 fields! But an experienced commander will find a use for even the weakest figure! Isn\'t that right?'
        if language == 'fr':
            return  'L\'éléphant marche en diagonale. 6 champs au total! Mais un commandant expérimenté trouvera une application même à la figure la plus faible! N\'est-ce pas?'
        if language == 'es':
            return 'El elefante camina en diagonal. ¡6 campos en total! ¡Pero un comandante experimentado encontrará uso incluso para la figura más débil! ¿No es así?'
        if language == 'de':
            return ''

    if description == 'rook':
        if language == 'ru':
            return 'Ладья ходит по вертикалям (радиус ) и горизонталям (по кругу ). Так что она может атаковать больше 1/4 поля!'
        if language == 'en':
            return 'The rook moves vertically (radius) and horizontally (in a circle ). So she can attack more than 1/4 of the field!'
        if language == 'fr':
            return  'La tour marche verticalement (rayon ) et horizontalement (cercle ). Donc, elle peut attaquer plus de 1/4 du terrain!'
        if language == 'es':
            return 'La torre camina verticalmente (Radio ) y horizontalmente (en un círculo ). ¡Para que pueda atacar más de 1/4 del campo!'
        if language == 'de':
            return 'Der Turm verläuft vertikal (Radius ) und horizontal (Kreis ). So kann sie mehr als 1/4 des Feldes angreifen!'

    if description == 'queen':
        if language == 'ru':
            return 'Ферзь является самой сильной фигурой! Но не намного сильнее ладьи. Вообще в этих шахматах уменьшили разрыв в силе между соседними фигурами.'
        if language == 'en':
            return 'The queen is the strongest piece! But not much stronger than a rook. In general, these chess games have reduced the gap in strength between neighboring pieces.'
        if language == 'fr':
            return  'La reine est la figure la plus forte! Mais pas beaucoup plus fort que la tour. En général, dans ces échecs, l\'écart de force entre les pièces voisines a été réduit.'
        if language == 'es':
            return 'La reina es la figura más fuerte! Pero no mucho más fuerte que la torre. En general, en este ajedrez se redujo la brecha de fuerza entre las piezas vecinas.'
        if language == 'de':
            return 'Die Königin ist die stärkste Figur! Aber nicht viel stärker als der Turm. Im Allgemeinen wurde in diesem Schach die Machtlücke zwischen den benachbarten Figuren reduziert.'

    if description == 'horse':
        if language == 'ru':
            return 'Конь ходит аналогично по букве г. Всего 6 полей! Сила коня наконец равна силе слона!'
        if language == 'en':
            return 'The knight moves similarly on 2 squares in a straight line and 1 to the side. Only 6 fields! The power of the knight is finally equal to the power of the bishop!'
        if language == 'fr':
            return  'Le cheval marche de la même manière sur 2 cellules en ligne droite et 1 sur le côté. 6 champs au total! La puissance du cheval est enfin égale à la puissance de l\'éléphant!'
        if language == 'es':
            return 'El caballo camina de manera similar en 2 celdas en línea recta y 1 hacia un lado. ¡6 campos en total! ¡El poder del caballo es finalmente igual al de un elefante!'
        if language == 'de':
            return 'Das Pferd geht ähnlich auf 2 Zellen in einer geraden Linie und 1 zur Seite. Insgesamt 6 Felder! Die Stärke des Pferdes ist endlich gleich der Stärke des Elefanten!'

    if description == 'king':
        if language == 'ru':
            return 'Король ходит на 1 поле в любую сторону,как и обычно!'
        if language == 'en':
            return 'The king moves 1 field in either direction, as usual!'
        if language == 'fr':
            return  'Le roi marche sur 1 champ dans n\'importe quel sens,comme d\'habitude!'
        if language == 'es':
            return '¡El rey camina en el campo 1 en cualquier dirección, como siempre!'
        if language == 'de':
            return 'Der König geht auf 1 Feld in jede Richtung, wie üblich!'

    if description == 'pawn':
        if language == 'ru':
            return 'Интересен ход пешек. С какой стороны она стоит, в ту сторону она и будет ходить, всегда! По часовой - иди по часовой до конца игры! И наоборот. Двойного хода нет. И превращения в фигуру тоже( КАК?).'
        if language == 'en':
            return 'Interesting pawn move. Whichever side it stands on, that\'s the way it will always go! Clockwise-go clockwise until the end of the game! And vice versa. There is no double move. And turning into a shape, too( how else?).'
        if language == 'fr':
            return  'Le mouvement des pions est intéressant. De quel côté elle se tient, de l\'autre côté elle marchera, toujours! Dans le sens horaire - allez dans le sens horaire jusqu\'à la fin du jeu! Et vice versa. Il n\'y a pas de double coup. Et se transformer en figure aussi (comment AUTREMENT?).'
        if language == 'es':
            return 'Es interesante el movimiento de los peones. ¡En qué lado está, en la otra dirección caminará, siempre! En sentido - ve en sentido hasta el final del juego! Y viceversa. No hay doble movimiento. Y la transformación en una figura también (¿de qué otra MANERA?).'
        if language == 'de':
            return 'Interessant ist der Zug der Bauern. Auf welcher Seite sie steht, auf der anderen Seite wird sie gehen, immer! Im Uhrzeigersinn-gehen Sie im Uhrzeigersinn bis zum Ende des Spiels! Und umgekehrt. Es gibt keinen Doppelschlag. Und die Verwandlung in eine Figur auch( WIE SONST?).'

    return 'error 3 round'

def get_biz(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Именно в эту игру играла вся знать Византии! Большинство партий заканчивалось почётной ничьёй. Проведите и вы время с удовольствием! ' 
        if language == 'en':
            return 'This was the game played by all the nobles of Byzantium! Most of the parties of honor ended in a draw. Spend your time with pleasure! '
        if language == 'fr':
            return  'C\'est ce jeu que toute la famille byzantine a joué! La plupart des parties se sont terminées par un match nul d\'honneur. Passez du temps avec plaisir! '
        if language == 'es':
            return '¡ Es en este juego que jugó todo el conocimiento de Bizancio! La mayoría de los partidos terminaron con un empate honorífico. Pasar tiempo y divertirse! '
        if language == 'de':
            return "Es war dieses Spiel, das alle kennen Byzanz gespielt! Die meisten Partien endeten mit einem Ehrentreffer. Verbringen Sie Zeit mit Spaß! "

    if description == 'pawn':
        if language == 'ru':
            return 'Пешка ходит на 1 поле в ту сторону,с которой стоит. Поэтому она всегда будет ходить только по часовой или против.' 
        if language == 'en':
            return 'The pawn moves 1 square in the direction from which it stands. Therefore, it will always go only clockwise or counterclockwise.'
        if language == 'fr':
            return  'Le pion marche sur 1 champ dans le sens où il se trouve. Par conséquent, elle ne marchera toujours que dans le sens des aiguilles d\'une montre ou dans le sens inverse.'
        if language == 'es':
            return 'El peón camina en el campo 1 en la dirección desde la que está parado. Por lo tanto, siempre caminará solo en sentido horario o contrario.'
        if language == 'de':
            return 'Der Bauer geht auf 1 Feld in die Richtung, von der es steht. Daher wird es immer nur im Uhrzeigersinn oder gegen gehen.'

    if description == 'rook':
        if language == 'ru':
            return 'Ладья является самой сильной фигурой! Ходит по вертикали( радиус) и горизонтали( по кругу) .'
        if language == 'en':
            return 'The rook is the strongest piece! Walks along the vertical axis( radius) and horizontally( in a circle) .'
        if language == 'fr':
            return  'Ладья является самой сильной фигурой! Ходит по вертикали( радиус) и горизонтали( по кругу) .'
        if language == 'es':
            return 'La torre es la figura más fuerte! Camina verticalmente (Radio) y horizontalmente( en un círculo).'
        if language == 'de':
            return 'Turm ist die stärkste Figur! Geht vertikal( Radius) und horizontal (Kreis) .'

    if description == 'bishop':
        if language == 'ru':
            return 'Слон вообще может попасть только на 8 полей на доске  А так он ходит через 1 поле по диагонали.'
        if language == 'en':
            return 'The bishop can only hit 8 squares on the board. And so it goes through 1 field diagonally.'
        if language == 'fr':
            return  'L\'éléphant ne peut atteindre que 8 champs sur le tableau  Et donc il marche à travers 1 champ en diagonale.'
        if language == 'es':
            return 'El elefante en general sólo puede llegar a 8 campos en el tablero Y por lo que camina a través de 1 campo en diagonal.'
        if language == 'de':
            return 'Der Elefant kann nur auf 8 Felder auf dem Brett. Und so geht er durch 1 Feld diagonal.'

    if description == 'horse':
        if language == 'ru':
            return 'Конь ходит, как обычно, буквой г. Он сильнее слона, получается...'
        if language == 'en':
            return 'The knight moves as usual, 2 in a straight line and 1 to the side. He\'s stronger than an elephant, so...'
        if language == 'fr':
            return  'Le cheval marche comme d\'habitude, 2 en ligne droite et 1 sur le côté. Il est plus fort qu\'un éléphant...'
        if language == 'es':
            return 'El caballo camina como de costumbre, 2 en línea recta y 1 a un lado. Es más fuerte que un elefante...'
        if language == 'de':
            return 'Das Pferd geht, wie gewohnt, 2 in einer geraden Linie und 1 zur Seite. Er ist stärker als ein Elefant...'

    if description == 'king':
        if language == 'ru':
            return 'Король ходит на 1 поле в любую сторону. Рокировки нет!'
        if language == 'en':
            return 'The king moves 1 field in either direction. No castling!'
        if language == 'fr':
            return  'Le roi marche sur 1 champ de chaque côté. Pas de Roque!'
        if language == 'es':
            return 'El rey va a 1 campo en cualquier dirección. Enroque no!'
        if language == 'de':
            return 'Der König geht auf ein Feld in jede Richtung. Es gibt keine Rochade!'

    if description == 'queen':
        if language == 'ru':
            return 'В этой игре ферзь слабее даже короля! Он ходит на 1 поле по диагонали, и всё!'
        if language == 'en':
            return 'In this game, the queen is weaker than even the king! He moves 1 square diagonally, and that\'s all!'
        if language == 'fr':
            return  'Dans ce jeu, la reine est plus faible que le roi! Il marche sur 1 champ en diagonale et c\'est tout!'
        if language == 'es':
            return 'En este juego, la reina es más débil que incluso el rey! Camina en 1 campo en diagonal, ¡y eso es todo!'
        if language == 'de':
            return 'In diesem Spiel ist die Königin schwächer als der König! Er geht auf 1 Feld diagonal, und das war \' s!'

    if description == 'end':
        if language == 'ru':
            return 'Желаем вам приятно проведённого времени! В бой, Коммандер!'
        if language == 'en':
            return 'We wish you a pleasant time! In battle, Commander!'
        if language == 'fr':
            return  'Nous vous souhaitons un agréable moment! Au combat, Commandant! '
        if language == 'es':
            return 'Le deseamos un tiempo agradable! ¡A la batalla, Comandante!'
        if language == 'de':
            return 'Wir wünschen Ihnen eine schöne Zeit! In die Schlacht, Commander!'

    return 'error3 bizantion'


def get_kuej(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Эти шахматы несильно отличаются от шахмат Глинского. Вот начальная расстановка. Это более компактно. Центральная пешка не может сделать двойной ход. Так что вам придётся изменить тактику. Но ведь это прекрасно! Удивите противника!'
        if language == 'en':
            return 'This chess is not much different from Glinsky\'s chess. Here is the initial placement. This is more compact. The central pawn cannot make a double move. So you\'ll have to change your tactics. But it\'s beautiful! Surprise your opponent!'
        if language == 'fr':
            return  'Ces échecs sont légèrement différents des échecs de Glinsky. Voici l\'arrangement initial. C\'est plus Compact. Le pion central ne peut pas faire un double mouvement. Vous devrez donc changer de tactique. Mais en effet, c\'est très bien! Surprenez votre adversaire!'
        if language == 'es':
            return 'Este ajedrez es ligeramente diferente del ajedrez de glinsky. Aquí está la alineación inicial. Es más compacto. El peón central no puede hacer un doble movimiento. Así que tendrás que cambiar de táctica. ¡Pero es hermoso! ¡Sorprende al enemigo!'
        if language == 'de':
            return 'Dieses Schach unterscheidet sich nicht stark von Glinskis Schach. Hier ist die anfängliche Aufstellung. Es ist kompakter. Ein zentraler Bauer kann keinen Doppelzug machen. Also musst du deine Taktik ändern. Aber es ist perfekt! Überraschen Sie den Gegner!'

    if description == 'end':
        if language == 'ru':
            return 'Пат в этих шахматах приносит ничью! Так и должно быть, разве нет? Пешка ходит иначе, чем в шахматах Глинского. Она рубит по диагонали. Это всё! Вы можете посмотреть обучение шахмат Глинского. '
        if language == 'en':
            return 'A stalemate in this chess game brings a draw! That\'s how it should be, isn\'t it? The pawn moves differently than in Glinsky chess. She cuts diagonally. That\'s it! You can watch the training of the chess Glinski. '
        if language == 'fr':
            return  'Pat dans ces échecs apporte un tirage au sort! Ça devrait l\'être, non? Le pion marche différemment des échecs de Glinsky. Elle coupe en diagonale. C\'est tout! Vous pouvez regarder la formation d\'échecs de Glinsky. '
        if language == 'es':
            return '¡Pat en este ajedrez trae un empate! Así es como debería ser, ¿no? El peón camina de manera diferente que en el ajedrez de Glinsky. Ella corta en diagonal. ¡Eso es todo! Puedes ver el entrenamiento de ajedrez de Glinsky. '
        if language == 'de':
            return 'Pat in diesem Schach bringt ein Unentschieden! Das sollte es sein, nicht wahr? Der Bauer geht anders als im Glinsky-Schach. Sie schneidet diagonal. Das ist alles! Sie können Glinsky Schach lernen sehen. '

    return 'error 3 get kuej'

def get_garner(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Игра проходит на поле 5х5. Вы скоро поймёте, что играть на столь маленькой доске намного сложнее, чем на обычной.А пока вот вам начальная расстановка.'
        if language == 'en':
            return 'The game is played on a 5x5 field. You will soon realize that playing on such a small board is much more difficult than on a regular one.In the meantime, here\'s the initial position.'
        if language == 'fr':
            return  'Le jeu se déroule sur un terrain de 5x5. Vous vous rendrez vite compte que jouer sur un si petit plateau est beaucoup plus difficile que d\'habitude.En attendant, voici l\'arrangement initial.'
        if language == 'es':
            return 'El juego se juega en un campo de 5x5. Pronto te darás cuenta de que jugar en un tablero tan pequeño es mucho más difícil que en uno normal.Mientras tanto, aquí tienes la alineación inicial.'
        if language == 'de':
            return 'Das Spiel findet auf einem 5x5-Feld statt. Sie werden bald erkennen, dass es viel schwieriger ist, auf einem so kleinen Brett zu spielen als auf einem normalen Brett.In der Zwischenzeit ist hier die anfängliche Anordnung.'

    if description == 'second':
        add = '\n1.b2 ab 2.ab cb 3.cb d3 4.b1-a2 ...'
        if language == 'ru':
            return 'Уже с первых ходов чувствуется недостаток вариантов ходов. В таких условиях фигуры теряют свою силу. Порой пешки гораздо ценнее. Не бойтесь обменять фигуру на пешку. Пара проходных пешек в центре намного сильнее кучи фигур противника. '+add
        if language == 'en':
            return 'Schon seit den ersten Zügen gibt es einen Mangel an Varianten von Zügen. Unter solchen Bedingungen verlieren die Figuren ihre Kraft. Manchmal sind Bauern viel wertvoller. Haben Sie keine Angst, die Figur gegen einen Bauern zu tauschen. Ein paar Bauern in der Mitte sind viel stärker als ein Haufen von gegnerischen Figuren. '+add
        if language == 'fr':
            return  'Dès les premiers mouvements, il y a un manque d\'options de mouvements. Dans de telles conditions, les figures perdent leur force. Parfois, les pions sont beaucoup plus précieux. N\'ayez pas peur d\'échanger la pièce contre un pion. Une paire de pions de passage au centre est beaucoup plus forte que la pile de pièces ennemies. '+add
        if language == 'es':
            return 'Ya desde los primeros movimientos se siente la falta de opciones de movimientos. En tales condiciones, las figuras pierden su poder. A veces los peones son mucho más valiosos. No tengas miedo de cambiar una pieza por un peón. Un par de peones que pasan en el centro son mucho más fuertes que un montón de piezas enemigas. '+add
        if language == 'de':
            return 'Schon seit den ersten Zügen gibt es einen Mangel an Varianten von Zügen. Unter solchen Bedingungen verlieren die Figuren ihre Kraft. Manchmal sind Bauern viel wertvoller. Haben Sie keine Angst, die Figur gegen einen Bauern zu tauschen. Ein paar Bauern in der Mitte sind viel stärker als ein Haufen von gegnerischen Figuren. '+add

    if description == 'pawn':
        if language == 'ru':
            return 'Пешка обладает огромной силой в этих шахматах, хотя ходит, как обычно, прямо, и атакует по диагонали.'
        if language == 'en':
            return 'The pawn has great power in this game, although it moves straight as usual and attacks diagonally.'
        if language == 'fr':
            return  'Le pion a un pouvoir énorme dans ces échecs, bien qu\'il marche comme d\'habitude droit et attaque en diagonale.'
        if language == 'es':
            return 'El peón tiene una gran fuerza en estos ajedrez, aunque camina, como de costumbre, recto, y ataca en diagonal.'
        if language == 'de':
            return 'Der Bauer hat eine enorme Kraft in diesem Schach, obwohl er wie gewohnt geradeaus geht und diagonal angreift.'

    if description == 'bishop':
        if language == 'ru':
            return 'Ходит и рубит по диагонали. От пешки по силе в середине партии он отличается только возможностью ходить назад. Можете спокойно менять! '
        if language == 'en':
            return 'Walks and cuts diagonally. From the pawn in strength in the middle of the game, it differs only in the ability to go back. You can safely change it! '
        if language == 'fr':
            return  'Marche et coupe en diagonale. Du pion en force au milieu de la partie, il ne diffère que par la possibilité de marcher en arrière. Vous pouvez changer en toute sécurité! '
        if language == 'es':
            return 'Camina y corta en diagonal. De un peón de fuerza en el medio del lote, solo difiere en la capacidad de caminar hacia atrás. Puede cambiar con seguridad! '
        if language == 'de':
            return 'Geht und schneidet diagonal. Vom Bauern in der Mitte der Partei unterscheidet er sich nur durch die Möglichkeit, rückwärts zu gehen. Sie können ruhig ändern! '

    if description == 'horse':
        if language == 'ru':
            return 'Ходит на 2 клетки по прямой и на 1 в сторону. Из-за этого у него чаще всего очень мало безопасных ходов. Часто приходится отдавать его за возможность сделать ход. Постарайтесь обменять его наиболее выгодно! '
        if language == 'en':
            return 'Moves 2 squares in a straight line and 1 to the side. Because of this, he often has very few safe moves. Often you have to give it away for the opportunity to make a move. Try to exchange it most profitably! '
        if language == 'fr':
            return  'Marche sur 2 cellules en ligne droite et 1 sur le côté. Pour cette raison, il a le plus souvent très peu de mouvements sûrs. Souvent, vous devez le donner pour l\'occasion de faire un mouvement. Essayez de l\'échanger le plus rentable! '
        if language == 'es':
            return 'Camina en 2 celdas en línea recta y en 1 a un lado. Debido a esto, la mayoría de las veces tiene muy pocos movimientos seguros. A menudo tienes que darlo por la oportunidad de hacer un movimiento. Trate de cambiarlo de la manera más rentable! '
        if language == 'de':
            return 'Geht auf 2 Zellen in einer geraden Linie und auf 1 zur Seite. Aus diesem Grund hat er meist sehr wenige sichere Züge. Oft ist es notwendig, es für die Gelegenheit zu geben, einen Zug zu machen. Versuchen Sie, es am profitabelsten zu tauschen! '

    if description == 'rook':
        if language == 'ru':
            return 'Ходит по прямой. Её редко приходится двигать в начале и середине. Зато в конце она превращается в монстра доски. Учтите это !'
        if language == 'en':
            return 'Walks in a straight line. It rarely has to be moved at the beginning and middle. But in the end, she turns into a monster of the board. Keep this in mind !'
        if language == 'fr':
            return   'Il marche en ligne droite. Il est rarement nécessaire de se déplacer au début et au milieu. Mais à la fin, elle se transforme en monstre. Considérez ceci !'
        if language == 'es':
            return 'Camina en línea recta. Rara vez tiene que moverse al principio y al medio. Pero al final se transforma en un monstruo del tablero. ¡Ten esto en cuenta !'
        if language == 'de':
            return 'Geht in einer geraden Linie. Es muss selten in der Mitte und am Anfang bewegt werden. Aber am Ende verwandelt sie sich in ein Brettmonster. Denken Sie daran !'

    if description == 'queen':
        if language == 'ru':
            return 'Самая сильная фигура! Но для чего нужна эта сила на таком поле боя?! Приберегите до конца партии! Ах, да! Ходит, как слон и ладья!'
        if language == 'en':
            return 'The most powerful piece! But what is this power for on such a battlefield?! Save it for the end of the game! Oh, yes! Moves like a bishop and a rook!'
        if language == 'fr':
            return  'La figure la plus forte! Mais à quoi sert cette force sur un tel champ de bataille?! Économisez jusqu\'à la fin de la fête! Ah, oui! Il marche comme un éléphant et une tour!'
        if language == 'es':
            return '¡La figura más fuerte! Pero, ¿para qué sirve esta fuerza en un campo de batalla como este?! ¡Guarden hasta el final de la fiesta! ¡Ah, sí! Camina como un elefante y una torre!'
        if language == 'de':
            return 'Die stärkste Figur! Aber wofür braucht man diese Kraft auf einem solchen Schlachtfeld?! Sparen Sie bis zum Ende der Partei! Oh, ja! Geht wie ein Elefant und Turm!'

    if description == 'king':
        if language == 'ru':
            return 'Поговорим немного о вашей цели! Рoкировки тут нет. А толку? На 2 доске был показан вариант детского мата. Будьте осторожнее! Ходит по 1 клетке в любую сторону. '
        if language == 'en':
            return 'Let\'s talk a little bit about your target! There is no castling here. What\'s the use? On Board 2, a variant of the children\'s mat was shown. Be careful! Moves on 1 square in any direction. '
        if language == 'fr':
            return  'Parlez un peu de votre objectif! Il n\'y a pas de Roque. Et confus? Sur le tableau 2, une variante du tapis de bébé a été montrée. Faites attention! Marche sur 1 cellule dans les deux sens. '
        if language == 'es':
            return '¡Hablemos un poco sobre tu objetivo! No hay enroque. ¿De qué sirve? En el tablero 2, se mostró una versión de la estera para niños. ¡Ten cuidado! Camina en 1 celda en cualquier dirección. '
        if language == 'de':
            return 'Lassen Sie uns ein wenig über Ihr Ziel sprechen! Es gibt keine Rochade. Was nützt das? Auf der 2. Tafel wurde eine Variante der Kindermatte gezeigt. Seien Sie vorsichtig! Geht auf 1 Zelle in jede Richtung. '

    if description == 'end':
        if language == 'ru':
            return 'Классические шахматы называют битвой в поле. Этот вариант называют битвой в тесных кварталах улиц! Набирайтесь опыта в игре! Где-то там ждёт успех!'
        if language == 'en':
            return 'Classic chess is called a battle in the field. This version is called the battle in the tight quarters of the streets! Gain experience in the game! Somewhere out there, success awaits!'
        if language == 'fr':
            return  'Les échecs classiques s\'appellent une bataille sur le terrain. Cette option est appelée une bataille dans les rues étroites! Gagnez de l\'expérience dans le jeu! Quelque part là-bas attend le succès!'
        if language == 'es':
            return 'El ajedrez clásico se llama batalla en el campo. ¡Esta opción se llama batalla en bloques estrechos de calles! Ganar experiencia en el juego! En algún lugar allí esperando el éxito!'
        if language == 'de':
            return 'Klassisches Schach wird Schlacht im Feld genannt. Diese Option wird als Schlacht in engen Straßenvierteln bezeichnet! Sammeln Sie Erfahrung im Spiel! Irgendwo dort wartet der Erfolg!'

    return 'error3 garner'

def get_horde(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Представляем вам уникальнейшую возможность штурмовать крепость ордой пешек! Именно так всё и происходит. 36 пешек против полного комплекта фигур! В эти шахматы трудно играть за обе стороны. '
        if language == 'en':
            return 'We present you a unique opportunity to storm the fortress with a horde of pawns! That\'s exactly what happens. 36 pawns against a full set of pieces! This chess game is difficult to play for both sides. '
        if language == 'fr':
            return  'Nous vous présentons une occasion unique de prendre d\'assaut la forteresse avec une Horde de pions! C\'est ainsi que sont les choses. 36 pions contre un ensemble complet de pièces! Ces échecs sont difficiles à jouer pour les deux parties. '
        if language == 'es':
            return '¡Te presentamos una oportunidad única para asaltar la fortaleza con una Horda de peones! Eso es exactamente lo que sucede. 36 peones contra un conjunto completo de piezas! Este ajedrez es difícil de jugar para ambos lados. '
        if language == 'de':
            return 'Wir präsentieren Ihnen eine einzigartige Gelegenheit, die Festung mit einer Horde von Bauern zu stürmen! Das ist es, was passiert. 36 Bauern gegen eine ganze Reihe von Formen! Dieses Schach ist schwer für beide Seiten zu spielen. '

    if description == 'second':
        if language == 'ru':
            return 'Цель белых - поставить мат! Цель чёрных - срубить все пешки и образованные из них фигуры! '
        if language == 'en':
            return 'White\'s goal is to checkmate! Black\'s goal is to cut down all the pawns and the pieces formed from them! '
        if language == 'fr':
            return  'Le but des blancs est de mettre un tapis! Le but des noirs est de couper tous les pions et les formes formées d\'eux! '
        if language == 'es':
            return '¡El objetivo de los blancos es poner un tapete! ¡El objetivo de los negros es cortar todos los peones y las figuras formadas a partir de ellos! '
        if language == 'de':
            return 'Das Ziel der Weißen ist es, die Matte zu setzen! Das Ziel der Schwarzen ist es, alle Bauern und von ihnen gebildeten Figuren abzuschneiden! '

    if description == 'pawn':
        if language == 'ru':
            return 'Пешка ходит прямо, рубит по диагонали. Есть двойной ход. Белые пешки могут сделать двойной ход с 1 и 2 линий. '
        if language == 'en':
            return 'The pawn moves straight, cuts diagonally. There is a double move. White pawns can make a double move from 1 and 2 lines. '
        if language == 'fr':
            return  'Le pion marche droit, coupe en diagonale. Il y a un double coup. Les pions blancs peuvent faire un double mouvement avec 1 et 2 lignes. '
        if language == 'es':
            return 'El peón camina recto, corta en diagonal. Hay un doble movimiento. Los peones blancos pueden hacer un doble movimiento con 1 y 2 líneas. '
        if language == 'de':
            return 'Der Bauer geht geradeaus, schneidet diagonal. Es gibt einen Doppelschlag. Weiße Bauern können einen doppelten Zug mit 1 und 2 Linien. '

    if description == 'also':
        if language == 'ru':
            return 'Остальные фигуры ходят, как в классических шахматах. Можете посмотреть обучение для них.'
        if language == 'en':
            return 'The other pieces move like in classical chess. You can watch the training for them.'
        if language == 'fr':
            return  'Les autres pièces marchent comme dans les échecs classiques. Vous pouvez regarder la formation pour eux.'
        if language == 'es':
            return 'El resto de las piezas van como en el ajedrez clásico. Puedes ver el entrenamiento para ellos.'
        if language == 'de':
            return 'Die anderen Figuren gehen wie im klassischen Schach. Sie können das Training für sie sehen.'

    return 'error 3 in harde'

def connection(language,description,params):
    if description == 'friend':
        if language == 'ru':
            return 'С другом'
        if language == 'en':
            return 'With friend'
        if language == 'fr':
            return  'avec un ami'
        if language == 'es':
            return 'con un amigo'
        if language == 'de':
            return 'mit Freund'

    if description == 'has':
        if language == 'ru':
            return f'Соединение успешно установлено \n Ваш ip : {params[0].my_ip} \n Ваш ник : {params[0].my_nick} \n Оппонент : {params[0].friend_nick} \n Играйте на здоровье!'
        if language == 'en':
            return f"Connection successfully established \n Your ip: {params[0]. my_ip} \n Your nickname : {params[0].my_nick} \n Opponent : {params[0].friend_nick} \n Play for your health!"
        if language == 'fr':
            return  f"La connexion a été établie avec succès \n votre adresse ip: {params[0].my_ip} \n votre pseudo: {params[0].my_nick} \n votre Adversaire: {params[0].friend_nick} \n Jouez à la santé!"
        if language == 'es':
            return f'La conexión se ha establecido correctamente \n Su ip : {params[0].my_ip} \n Su apodo: {params[0].my_nick} \n Oponente: {params[0].friend_nick} \n ¡Juega a la salud!'
        if language == 'de':
            return f'Verbindung erfolgreich hergestellt \n Deine IP: {params[0].my_ip} \n Dein Nickname : {params[0].my_nick} \n Gegner : {params[0].friend_nick} \n Gesundheit spielen!'

    if description == 'kill':
        if language == 'ru':
            return 'Разорвать'
        if language == 'en':
            return 'Break'
        if language == 'fr':
            return  'Déchirer'
        if language == 'es':
            return 'Romper'
        if language == 'de':
            return 'Brechen'

    if description == 'create':
        if language == 'ru':
            return 'Создать '
        if language == 'en':
            return 'Create'
        if language == 'fr':
            return  'Créer'
        if language == 'es':
            return 'Crear'
        if language == 'de':
            return 'Schaffen'

    if description == 'connect':
        if language == 'ru':
            return 'Подключиться'
        if language == 'en':
            return 'Connect'
        if language == 'fr':
            return  'connecter'
        if language == 'es':
            return 'Conectarse'
        if language == 'de':
            return 'Mitmachen'

    if description == 'ip':
        if language == 'ru':
            return 'Ip хоста'
        if language == 'en':
            return 'Ip of host'
        if language == 'fr':
            return  'l\'adresse ip de l\'hôte'
        if language == 'es':
            return 'IP del anfitrión'
        if language == 'de':
            return 'ip des Hosts'

    if description == 'nick':
        if language == 'ru':
            return 'Ваш ник'
        if language == 'en':
            return 'Your nickname'
        if language == 'fr':
            return  'votre pseudo'.title()
        if language == 'es':
            return 'su apodo'.title()
        if language == 'de':
            return 'ihr Spitzname'.title()

    if description == 'pass':
        if language == 'ru':
            return 'Код'
        if language == 'en':
            return 'Code'
        if language == 'fr':
            return  'Code'
        if language == 'es':
            return 'Código'
        if language == 'de':
            return 'Kode'

    if description == 'wire_error':
        if language == 'ru':
            return 'Нет подключения к интернету. \n Подключитесь к WIFI. '
        if language == 'en':
            return 'No internet connection. \n Connect to Wi-Fi. '
        if language == 'fr':
            return  'Pas de connexion Internet. \ n Connectez-vous au WIFI. '
        if language == 'es':
            return 'No hay conexión a Internet. \ n Conéctese a WIFI. '
        if language == 'de':
            return 'Keine Internetverbindung. \ n Verbinden Sie sich mit WIFI. '

    if description == 'empty_nick':
        if language == 'ru':
            return 'Ник не может быть пустым !'
        if language == 'en':
            return 'A nickname can\'t be empty !'
        if language == 'fr':
            return  'Nick ne peut pas être vide !'
        if language == 'es':
            return '¡Nick no puede estar vacío !'
        if language == 'de':
            return 'Nick darf nicht leer sein !'

    if description == 'cant':
        if language == 'ru':
            return 'Что-то пошло не так!'
        if language == 'en':
            return 'Something went wrong!'
        if language == 'fr':
            return  'Quelque chose a mal tourné!'
        if language == 'es':
            return '¡Algo salió mal!'
        if language == 'de':
            return 'Etwas ist schief gelaufen!'


    if description == 'incorrect_ip':
        if language == 'ru':
            return 'Неверный ip'
        if language == 'en':
            return 'Invalid ip'
        if language == 'fr':
            return  'Mauvaise ip'
        if language == 'es':
            return 'Ip incorrecta'
        if language == 'de':
            return 'Ungültige IP'

    if description == 'invalid_pass':
        if language == 'ru':
            return 'Неверный код'
        if language == 'en':
            return 'Invalid code'
        if language == 'fr':
            return  'Mauvaise code'
        if language == 'es':
            return 'código incorrecto'
        if language == 'de':
            return 'ungültiger Code'

    if description == 'equal_nicks':
        if language == 'ru':
            return 'Одинаковые ники'
        if language == 'en':
            return 'Equal nicks'
        if language == 'fr':
            return  'Même pseudo'
        if language == 'es':
            return 'Igual Nicky'
        if language == 'de':
            return 'Identische Nicks'

    if description == 'cancel':
        if language == 'ru':
            return 'Отмена'
        if language == 'en':
            return 'Cancel'
        if language == 'fr':
            return  'Annuler'
        if language == 'es':
            return 'Cancelar'
        if language == 'de':
            return 'Abbrechen'

    if description == 'exit':
        if language == 'ru':
            return 'Противник вышел/отключился'
        if language == 'en':
            return 'The opponent is out/disconnected'
        if language == 'fr':
            return  'L\'ennemi est sorti/déconnecté'
        if language == 'es':
            return 'El enemigo salió/se apagó'
        if language == 'de':
            return 'Der Gegner ist raus/abgeschaltet'

    if description == 'broken':
        if language == 'ru':
            return 'Связь разорвана'
        if language == 'en':
            return 'Connection was broken'
        if language == 'fr':
            return  'Lien rompu'
        if language == 'es':
            return 'Disocia'
        if language == 'de':
            return 'Verbindung abgebrochen'

    if description == 'leave':
        if language == 'ru':
            return 'Противник покинул эту партию.'
        if language == 'en':
            return 'The opponent has left this party.'
        if language == 'fr':
            return  'L\'adversaire a quitté ce match.'
        if language == 'es':
            return 'El oponente dejó este juego.'
        if language == 'de':
            return 'Der Gegner hat diese \Spiel verlassen.'
    
    print(description)
    return 'error connection'

def get_weak(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Название этих шахмат ни о чём не говорит, к сожалению. Вот начальная расстановка фигур. О них немного информации. Известно, что в них играли в 60-ые в Колумбийском университете.'
        if language == 'en':
            return 'The name of this chess game means nothing, unfortunately. Here is the initial arrangement of the pieces. There is little information about them. It is known that they were played in the 60s at Columbia University.'
        if language == 'fr':
            return  'Le nom de ces échecs ne dit rien, malheureusement. Voici l\'arrangement initial des formes. Il y a peu d\'informations à leur sujet. On sait qu\'ils ont joué dans les années 60 à l\'Université Columbia.'
        if language == 'es':
            return 'El nombre de estos ajedrez no dice nada, desafortunadamente. Aquí está la disposición inicial de las formas. Hay poca información sobre ellos. Se sabe que se jugaron en los años 60 en la Universidad de Columbia.'
        if language == 'de':
            return 'Der Name dieses Schachs sagt leider nichts aus. Hier ist die anfängliche Anordnung der Figuren. Es gibt wenig Informationen über sie. Es ist bekannt, dass sie in den 60er Jahren an der Columbia University gespielt haben.'

    if description == '2':
        if language == 'ru':
            return 'С первого взгляда может показаться, что у чёрных нет ни единого шанса. Однако в руках талантливого полководца чёрные могут задать жару!\n Ребята в университете неплохо поработали!'
        if language == 'en':
            return 'At first glance, it may seem that Black does not have a single chance. However, in the hands of a talented half-leader, black can set the heat!\n The guys at the university did a good job!'
        if language == 'fr':
            return  'À première vue, il peut sembler que les noirs n\'ont aucune chance. Cependant, entre les mains d\'un demi-guide talentueux, les noirs peuvent mettre la chaleur!\n Les gars de l\'Université ont fait du bon travail!'
        if language == 'es':
            return 'A primera vista, puede parecer que los negros no tienen una sola oportunidad. Sin embargo, en manos de un talentoso medio líder, ¡los negros pueden establecer el calor!\n ¡los Chicos de la Universidad hicieron un buen trabajo!'
        if language == 'de':
            return 'Auf den ersten Blick mag es scheinen, dass Schwarze keine Chance haben. Doch in den Händen eines talentierten Halbhüters können die Schwarzen die Hitze einstellen!\n Die Jungs an der Universität haben einen guten Job gemacht!'

    if description == '3':
        if language == 'ru':
            return 'Все фигуры ходят по правилам классических шахмат, только чёрная пешка превращается в коня. Если вы ещё не в курсе, можете глянуть, как управлять этой стихией, а так - в бой, Командир!'
        if language == 'en':
            return 'All pieces move according to the rules of classical chess, but the black pawn turns into a knight. If you don\'t know yet, you can take a look at how to control this element, and so-into battle, Commander!'
        if language == 'fr':
            return  'Toutes les pièces suivent les règles des échecs classiques, mais le pion noir se transforme en cheval. Si vous n\'êtes pas encore au courant, vous pouvez voir comment gérer cet élément, et donc - dans la bataille, Commandant!'
        if language == 'es':
            return 'Todas las piezas siguen las reglas del ajedrez clásico, pero el peón negro se convierte en un caballo. Si aún no lo sabe, puede ver cómo controlar este elemento,y así-en la batalla, Comandante!'
        if language == 'de':
            return 'Alle Figuren gehen nach den Regeln des klassischen Schachs, aber der schwarze Bauer verwandelt sich in ein Pferd. Wenn Sie noch nicht wissen, können Sie sehen, wie man dieses Element zu verwalten, und so - in den Kampf, Kommandant!'

    return 'error in get_weak'

def get_kamikadze(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Как можно догадаться, в этих шахматах фигуры жертвуют собой. Но когда? Всё просто! Но давайте по порядку...'
        if language == 'en':
            return 'As you might guess, in these chess  the pieces sacrifice themselves. But when? It\'s simple! But let\'s take it in order...'
        if language == 'fr':
            return  'Comme vous pouvez le deviner, dans ces échecs, les pièces se sacrifient. Mais quand? Tout est simple! Mais allons dans l\'ordre...'
        if language == 'es':
            return 'Como se puede adivinar, en este ajedrez, las piezas se sacrifican a sí mismas. ¿Pero cuándo? ¡Es simple! Pero vamos en orden...'
        if language == 'de':
            return 'Wie Sie sich vorstellen können, opfern sich die Figuren in diesem Schach. Aber wann? Es ist einfach! Aber lassen Sie uns in der Reihenfolge...'
        
    elif description == '2':
        if language == 'ru':
            return 'В этих шахматах действуют все правила из классических шахмат. Если хотите, можете посмотреть их. Хотя, если учесть ваш боевой опыт, Вам это уже не понадобится! Так что давайте перейдём к сути. '
        elif language == 'en':
            return 'All the rules from classical chess apply in this chess game. You can watch them if you want. Although, if you take into account your combat experience, you will not need it anymore! So let\'s get to the point. '
        elif language == 'de':
            return 'In diesem Schach gelten alle Regeln des klassischen Schachs. Wenn Sie möchten, können Sie sie sehen. Obwohl, wenn Sie Ihre Kampferfahrung berücksichtigen, werden Sie es nicht mehr brauchen! Also lasst uns auf den Punkt kommen. '
        elif language == 'fr':
            return 'Dans ces échecs, toutes les règles des échecs classiques s\'appliquent. Si vous voulez, vous pouvez les regarder. Bien que, compte tenu de votre expérience de combat, vous n\'en aurez plus besoin! Alors passons à l\'essentiel. '
        elif language == 'es':
            return 'Todas las reglas del ajedrez clásico se aplican en este ajedrez. Si quieres, puedes verlos. Aunque, si tienes en cuenta tu experiencia de combate, ¡Ya no lo necesitarás! Así que vamos al grano. '


    elif description == '3':
        if language == 'ru':
            return 'В этих шахматах фигура, которая рубит вражескую фигуру, погибает! По этой причине король не может никого рубить. '
        elif language == 'es':
            return '¡En este ajedrez, la pieza que golpea a la pieza enemiga muere! Por esta razón, el rey no puede vencer a nadie. '
        elif language == 'en':
            'In this chess game, a figure that hits an enemy piece is killed! For this reason, the king cannot beat anyone. '
        elif language == 'fr':
            return 'Dans ces échecs, la pièce qui Bat la pièce ennemie meurt! Pour cette raison, le roi ne peut pas battre les autres pièces. '
        elif language == 'de':
            return 'In diesem Schach stirbt die Figur, die die gegnerische Figur schlägt! Aus diesem Grund kann der König keine anderen Figuren schlagen. '

    elif description == '4':
        if language == 'ru':
            return 'Это простое правило порождает интересные особенности. Главное - возможность поставить мат одной фигурой. Смотрите:'
        elif language == 'de':
            return 'Diese einfache Regel erzeugt interessante Features. Die Hauptsache-die Fähigkeit, die Matte eine Figur zu setzen. Schaut:'
        elif language == 'fr':
            return 'Cette règle simple génère des caractéristiques intéressantes. L\'essentiel est la possibilité de mettre le tapis avec une seule figure. Tenez:'
        elif language == 'es':
            return 'Esta regla simple genera características interesantes. Lo principal es la posibilidad de poner un tapete en una sola figura. Mirais:'
        elif language == 'en':
            return 'This simple rule generates interesting features. The main thing is the ability to checkmate with one piece. See:'

    elif description == '5':
        if language == 'ru':
            return 'Второе - не всегда можно рубить фигуру. Будьте внимательны! Если конь срубит слона, они оба исчезнут и белые получат шах. Поэтому тут рубить нельзя!'
        elif language == 'en':
            return 'Second , you can\'t always cut a piece. Be careful! If the knight cuts the bishop, they both disappear and white gets the check. That\'s why you can\'t hack here!'
        elif language == 'fr':
            return 'Deuxièmement-vous ne pouvez pas toujours couper une figure. Soyez prudent! Si un cheval coupe un éléphant, ils disparaîtront tous les deux et les blancs auront un Shah. Par conséquent, vous ne pouvez pas couper ici!'
        elif language == 'de':
            return 'Die zweite - nicht immer möglich, eine Figur zu hacken. Seien Sie vorsichtig! Wenn das Pferd einen Elefanten zerhackt, werden sie beide verschwinden und die Weißen werden Shah bekommen. Deshalb kann man hier nicht hacken!'
        elif language == 'es':
            return 'Segundo-no siempre se puede cortar una figura. ¡Ten cuidado! Si el caballo corta al elefante, ambos desaparecerán y los blancos recibirán un jaque. Por lo tanto, no se puede cortar aquí!'

    elif description == '6':
        if language == 'ru':
            return 'Вероятно, режим вам понравится. Он научит использовать ограниченные ресурсы рационально. Учитесь, командиры! И Удачи!'
        elif language == 'de':
            return 'Wahrscheinlich wird Ihnen der Modus gefallen. Es wird gelehrt, begrenzte Ressourcen rational zu nutzen. Lernen Sie, Kommandanten! Und viel Glück!'
        elif language == 'fr':
            return 'Vous aimerez probablement le mode. Il apprendra à utiliser les ressources limitées de manière rationnelle. Apprenez, commandants! Et Bonne Chance!'
        elif language == 'es':
            return 'Probablemente te guste el modo. Él enseñará a usar recursos limitados racionalmente. ¡Entren, comandantes! ¡Y Buena Suerte!'
        elif language == 'en':
            return 'You\'ll probably like the mode. It will teach you how to use limited resources efficiently. Learn, commanders! And Good Luck!'
    
    return 'error in get_kamikadze'

def get_bad_chess(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Забудьте про дебют! Совсем! Представляем Вашему вниманию полностью рандомную расстановку! '
        if language == 'en':
            return 'Forget the debut! Absolutely! We present to your attention a completely random placement! '
        if language == 'fr':
            return  'Oubliez les débuts! Tout à fait! Nous présentons à Votre attention un arrangement entièrement aléatoire! '
        if language == 'es':
            return '¡Olvídate del debut! Todo! ¡Presentamos a Su atención la disposición completamente aleatoria! '
        if language == 'de':
            return 'Vergessen Sie das Debüt! Ganz! Wir präsentieren Ihnen eine völlig zufällige Anordnung! '

    if description == '2':
        if language == 'ru':
            return 'Фигуры ходят, как в классических шахматах. Можете глянуть, если необходимо. '
        if language == 'en':
            return 'The pieces move like in classical chess. You can take a look if you need to. '
        if language == 'fr':
            return  'Les pièces marchent comme dans les échecs classiques. Vous pouvez regarder si nécessaire. '
        if language == 'es':
            return 'Las piezas caminan como en el ajedrez clásico. Puedes echar un vistazo si es necesario. '
        if language == 'de':
            return 'Die Figuren gehen wie im klassischen Schach. Sie können sehen, wenn nötig. '

    if description == '3':
        if language == 'ru':
            return 'Особенности:\n1) Нет рокировки\n2) Пешки на 1 и 8 горизонталях могут \n        тоже делать двойной ход\n3) Пат - поражение'
        if language == 'en':
            return 'Features:\n1) No castling\n2) Pawns on 1 and 8 horizontal lines \n        can also make a double move\n3) Stalemate-defeat'
        if language == 'fr':
            return  'Caractéristiques: \n1) Pas de Roque \n2) les Pions sur 1 et 8 horizontaux \n        peuvent également faire un double coup \n3) Pat-défaite'
        if language == 'es':
            return 'Características: \n1) Sin enroque \n2)los Peones en las horizontales 1 y 8 \n        también pueden hacer doble movimiento\n3) Pat - derrota'
        if language == 'de':
            return 'Eigenschaften: \n1) Keine Rochade\n2) Bauern auf 1 und 8 Horizontalen \n      können auch doppelte Züge machen \n3) Pat - Niederlage'

    if description == '4':
        if language == 'ru':
            return 'Это - режим для игры ради удовольствия. Почувствуйте вкус лёгких матов! А потом в настоящий бой!'
        if language == 'en':
            return 'This is a mode for playing for fun. Feel the taste of light mats! And then into a real fight!'
        if language == 'fr':
            return  'C\'est un mode de jeu pour le plaisir. Sentez le goût des tapis légers! Et puis dans le vrai combat!'
        if language == 'es':
            return 'Este es un modo para jugar por diversión. ¡Siente el sabor de las esteras ligeras! ¡Y luego en una verdadera pelea!'
        if language == 'de':
            return 'Dies ist ein Modus zum Spielen zum Spaß. Spüren Sie den Geschmack von leichten Matten! Und dann in einen echten Kampf!'

    return 'error in get_bad_chess'

def get_rasing(language,description):

    if description == 'start':
        if language == 'ru':
            return 'Пожалуй, это даже не шахматы. Но это не означает, что будет просто! Все фигуры ходят, как обычно. Можете посмотреть обучение. '
        if language == 'en':
            return 'It\'s probably not even chess. But this does not mean that it will be easy! All the pieces move as usual. You can watch the training. '
        if language == 'fr':
            return  'Ce n\'est peut-être même pas un jeu d\'échecs. Mais cela ne signifie pas que ce sera facile! Toutes les figures marchent comme d\'habitude. Vous pouvez regarder la formation. '
        if language == 'es':
            return 'Tal vez ni siquiera es ajedrez. ¡Pero eso no significa que sea fácil! Todas las figuras caminan como de costumbre. Puede ver el entrenamiento. '
        if language == 'de':
            return 'Vielleicht ist es nicht einmal Schach. Aber das bedeutet nicht, dass es einfach sein wird! Alle Figuren laufen wie gewohnt. Sie können das Training sehen. '

    if description == '2':
        if language == 'ru':
            return 'Цель игры - добежать королём до 8-ой горизонтали. Если это сделают чёрные - они сразу побеждают. Если это сделают белые - чёрным будет дан 1 ход, и только после этого будут подведены итоги. '
        if language == 'en':
            return 'The goal of the game is to run the king to the 8th horizontal. If black does it, they win right away. If white does this, black will be given 1 move, and only after that the results will be summed up. '
        if language == 'fr':
            return  'Le but du jeu est d\'atteindre le roi jusqu\'à la 8ème horizontale. Si les noirs le font, ils gagnent immédiatement. Si cela est fait blanc-noir sera donné 1 mouvement, et seulement après cela sera résumé. '
        if language == 'es':
            return 'El objetivo del juego es correr rey a la 8ª horizontal. Si lo hacen los negros, ganan de inmediato. Si lo hacen los blancos, el negro se dará 1 turno, y solo después de eso se resumirán. '
        if language == 'de':
            return 'Ziel des Spiels ist es, den König bis zur 8.Horizontallinie zu führen. Wenn es die Schwarzen tun-sie sofort gewinnen. Wenn es weiß wird-schwarz wird 1 Zug gegeben, und erst danach werden die Ergebnisse zusammengefasst. '
    
    if description == '3':
        if language == 'ru':
            return 'Есть одно важное правило - в этой игре запрещены все шахи! Это придаёт игре особый интерес. Пат или 8-ая линия! '
        if language == 'en':
            return 'There is one important rule - all shahs are forbidden in this game ! This gives the game a special interest. Pat or the 8th line! '
        if language == 'fr':
            return  'Il y a une règle importante - tous les Shahs sont interdits dans ce jeu ! Cela donne au jeu un intérêt particulier. Pat ou ligne 8!'
        if language == 'es':
            return 'Hay una regla importante: ¡todos los shahis están prohibidos en este juego! Esto le da al juego un interés especial. ¡Pat o la línea 8! '
        if language == 'de':
            return 'Es gibt eine wichtige Regel - in diesem Spiel sind alle Shahis verboten! Dies gibt dem Spiel ein besonderes Interesse. Pat oder Linie 8! '

    if description == '4':
        if language == 'ru':
            return 'Вас ждут нестандартные тактические решения и гениальные позиционные финты! Так чего же вы ждёте?'
        if language == 'en':
            return 'You are waiting for non-standard tactical solutions and ingenious positional feints! So what are you waiting for?'
        if language == 'fr':
            return  'Des solutions tactiques non standard et des feintes ingénieuses vous attendent! Alors qu\'attendez-vous?'
        if language == 'es':
            return '¡Te esperan soluciones tácticas no estándar y ingeniosas fintas ! Entonces, ¿qué estás esperando?'
        if language == 'de':
            return 'Sie warten auf Nicht-Standard-taktische Lösungen und geniale Positionsfinten! Also, worauf warten Sie noch?'
    return 'error in '

def get_haos(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Это - авторский режим. Он развивает идеи волшебных шахмат. Тут происходит сплошной хаос, и вы в этом скоро убедитесь!'
        if language == 'en':
            return 'This is the author\'s mode. He develops the ideas of magic chess. There is a lot of chaos going on here, and you will soon see it!'
        if language == 'fr':
            return  'C\'est le mode auteur. Il développe des idées d\'échecs magiques. Il y a un chaos total et vous le verrez bientôt!'
        if language == 'es':
            return 'Este es el modo autor. Desarrolla ideas de ajedrez mágico. ¡Hay un caos continuo aquí, y pronto lo verás!'
        if language == 'de':
            return 'Das ist der Autorenmodus. Er entwickelt die Ideen des magischen Schachs. Hier ist ein kontinuierliches Chaos, und Sie werden es bald sehen!'

    if description == '2':
        if language == 'ru':
            return 'В этих шахматах было добавлено много новых эффектов. Строить планы в таких условиях невозможно! Это научит вас мгновенно ориентироваться в ситуации. Вперёд, шахматисты!'
        if language == 'en':
            return 'A lot of new effects have been added to this chess game. It is impossible to make plans in such conditions! This will teach you to instantly navigate the situation. Go ahead, chess players!'
        if language == 'fr':
            return  'Beaucoup de nouveaux effets ont été ajoutés à ces échecs. Faire des plans dans de telles conditions est impossible! Cela vous apprendra à naviguer instantanément dans la situation. Allez, les joueurs d\'échecs!'
        if language == 'es':
            return 'Se han agregado muchos efectos nuevos en estos juegos de ajedrez. ¡Es imposible hacer planes en tales condiciones! Esto te enseñará a navegar instantáneamente la situación. ¡Vamos, jugadores de ajedrez!'
        if language == 'de':
            return 'Viele neue Effekte wurden in diesem Schach hinzugefügt. Es ist unmöglich, Pläne unter solchen Bedingungen zu machen! Dies wird Ihnen beibringen, die Situation sofort zu navigieren. Vorwärts, Schachspieler!'

def get_schatranj(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Это - древняя игра. Играли в эти шахматы до 10 века в Азии и Африке. Из них возникли современные шахматы. '
        if language == 'en':
            return 'This is an ancient game. This chess was played until the 10th century in Asia and Africa. Modern chess emerged from them. '
        if language == 'fr':
            return  "C'est un jeu ancien. Ce jeu d'échecs a été joué jusqu'au 10ème siècle en Asie et en Afrique. Les échecs modernes en ont émergé. "
        if language == 'es':
            return 'Este es un juego antiguo. Este ajedrez se jugó hasta el siglo 10 en Asia y África. El ajedrez moderno surgió de ellos. '
        if language == 'de':
            return "Dies ist ein altes Spiel. Jahrhundert in Asien und Afrika gespielt. Modernes Schach entstand aus ihnen. "
    elif description == 'changes':
        if language == 'ru':
            return 'Правила игры немного похожи;\n Отличия:\n 1. Пат - поражение\n2. Многие фигуры ходят иначе\n3. Нет рокировки'
        if language == 'en':
            return 'The rules of the game are a bit similar;\n Differences:\n 1. Pat-defeat\n2. Many pieces move differently\n3. No castling'
        if language == 'fr':
            return  'Les règles du jeu sont un peu similaires; \n Différences: \n 1. Pat-défaite\n2. Beaucoup de figures marchent différemment\n3. Pas de Roque'
        if language == 'es':
            return 'Las reglas del juego son un poco similares; \n Diferencias:  \n 1. Pat - derrota \n2. Muchas figuras caminan de manera diferente\n3. Sin enroque'
        if language == 'de':
            return 'Die Spielregeln sind ein bisschen ähnlich; \n Unterschiede: \n 1. Pat-Niederlage\n2. Viele Figuren gehen anders\n3. Keine Rochade'
    elif description == 'pawn':
        if language == 'ru':
            return 'Пешка теперь ходит только на 1 поле. Рубит по диагонали. Дойдя до последней линии, превращается в ферзя.'
        if language == 'en':
            return 'The pawn now moves only on 1 square. Cuts diagonally. When he reaches the last line, he turns into a queen.'
        if language == 'fr':
            return  'Le pion ne marche plus que sur 1 champ. Coupe en diagonale. Après avoir atteint la Dernière ligne, il se transforme en reine.'
        if language == 'es':
            return 'El peón ahora solo camina en 1 campo. Corta en diagonal. Al llegar a la Última línea, se convierte en una reina.'
        if language == 'de':
            return 'Der Bauer geht jetzt nur noch auf 1 Feld. Schneidet diagonal. Die letzte Linie erreicht, verwandelt sich in eine Königin.'
    elif description == 'bishop':
        if language == 'ru':
            return 'Слон может ходить по диагонали через 1 поле. Всего 8 полей на доске! Зато он может перепрыгивать фигуры.'
        if language == 'en':
            return 'The bishop can walk diagonally across 1 field. There are only 8 fields on the board! But he can jump over the pieces.'
        if language == 'fr':
            return  'L\'éléphant peut marcher en diagonale à travers 1 champ. Un total de 8 champs sur le tableau! Mais il peut sauter par-dessus les chiffres.'
        if language == 'es':
            return 'El elefante puede caminar en diagonal a través de 1 campo. ¡Solo 8 campos en el tablero! Pero puede saltar sobre las figuras.'
        if language == 'de':
            return 'Der Elefant kann diagonal durch 1 Feld gehen. Insgesamt 8 Felder auf dem Brett! Aber er kann über die Figuren springen.'
    elif description == 'rook':
        if language == 'ru':
            return 'На сцене самая сильная фигура шатранжа! Ходит она, как в обычных шахматах. По прямой.'
        if language == 'en':
            return 'On the stage is the most powerful figure of Shatrange! She moves like in ordinary chess. In a straight line.'
        if language == 'fr':
            return  'Sur scène, la figure la plus forte de shatrange! Elle marche comme dans les échecs ordinaires. À vol d\'oiseau.'
        if language == 'es':
            return '¡En el escenario, la figura más poderosa de shatrange! Camina como en el ajedrez normal. En línea recta.'
        if language == 'de':
            return "Auf der Bühne ist Shatrange die stärkste Figur! Es geht, wie im gewöhnlichen Schach. In einer geraden Linie."
    elif description == 'king':
        if language == 'ru':
            return 'Король не изменил своих привычек до сих пор! Он и тогда ещё прятался от шахов и страдал от матов! Даже бегает по-прежнему!'
        if language == 'en':
            return 'The king hasn\'t changed his habits yet! Even then, he was still hiding from the shahs and suffering from the mats! Even runs as before!'
        if language == 'fr':
            return  'Le roi n\'a pas changé ses habitudes jusqu\'à présent! Il se cachait encore des Shahs et souffrait des tapis! Même courir encore!'
        if language == 'es':
            return '¡El rey no ha cambiado sus hábitos hasta ahora! ¡También se escondía de los Shah y sufría de las esteras! ¡Incluso sigue corriendo!'
        if language == 'de':
            return 'Der König hat seine Gewohnheiten bis jetzt nicht geändert! Er versteckte sich damals noch vor den Schahs und litt unter den Matten! Auch läuft noch!'
    
    elif description == 'horse':
        if language == 'ru':
            return 'Вот ещё одна фигура, которая не поменяла стиль борьбы! Всё и сейчас так, как раньше!'
        if language == 'en':
            return 'Here\'s another piece that hasn\'t changed the fighting style! Everything is still the same as before!'
        if language == 'fr':
            return  'Voici une autre figure qui n\'a pas changé le style de combat! Tout est maintenant comme avant!'
        if language == 'es':
            return '¡Aquí hay otra figura que no ha cambiado el estilo de lucha! ¡Todo ahora como antes!'
        if language == 'de':
            return 'Hier ist eine andere Figur, die den Kampfstil nicht verändert hat! Alles ist jetzt wie früher!'

    if description == 'queen':
        if language == 'ru':
            return 'Только у нас! Смотрите! Ферзь - самая слабая фигура, после пешки! Ходит по диагонали на 1 поле.'
        if language == 'en':
            return 'Only with us! Look at this! The queen is the weakest figure, after the pawn! Moves diagonally on 1 field.'
        if language == 'fr':
            return 'Seulement nous! Voyez! La reine est la figure la plus faible, après le pion! Marche en diagonale sur 1 champ.'
        if language == 'es':
            return 'Sólo nosotros! ¡Miren! ¡La reina es la figura más débil, después del peón! Camina en diagonal en 1 campo.'
        if language == 'de':
            return 'Nur bei uns! Seht mal! Die Königin ist die schwächste Figur, nach dem Bauern! Geht diagonal auf 1 Feld.'

    if description == 'end':
        if language == 'ru':
            return 'Это игра для самых терпеливых. Готовьтесь к черепашьему ходу фигур, но вас также ждут и неожиданные тактические приёмы. Учитесь! Древние были мудрее нас!'
        if language == 'en':
            return 'This is a game for the most patient. Get ready for the turtle move of the pieces, but you will also find unexpected tactics. Learn! The ancients were wiser than we!'
        if language == 'fr':
            return  'C\'est un jeu pour les plus patients. Préparez-vous pour le tour de tortue des formes, mais vous attendez aussi des techniques tactiques inattendues. Apprenez! Les anciens étaient plus sages que nous!'
        if language == 'es':
            return 'Es un juego para los más pacientes. Prepárate para el movimiento de la tortuga de las figuras, pero también te esperan técnicas tácticas inesperadas. Aprende! ¡Los antiguos eran más sabios que nosotros!'
        if language == 'de':
            return 'Es ist ein Spiel für die Geduldigsten. Machen Sie sich bereit für die Schildkröte Bewegung der Figuren, aber Sie warten auch auf unerwartete taktische Tricks. Lernen! Die Alten waren klüger als wir!'



    return 'error in get_schatranj'

def get_dark(language,description):
    if description == 'start':
        if language == 'ru':
            return 'Пора вам научиться действовать в условиях реального боя! Добро пожаловать, Командиры!'
        if language == 'en':
            return 'It\'s time for you to learn how to act in a real battle! Welcome, Commanders!'
        if language == 'fr':
            return  'Il est temps pour vous d\'apprendre à agir dans un vrai combat! Bienvenue, Commandants!'
        if language == 'es':
            return '¡Es hora de que aprendas a actuar en un combate real! ¡Bienvenidos, Comandantes!'
        if language == 'de':
            return 'Es ist Zeit, dass Sie lernen, in einem echten Kampf zu handeln! Willkommen, Kommandeure!'
    
    if description == 'second':
        if language == 'ru':
            return 'Эти шахматы отличаются от обычных тем, что во время боя вы будете видеть только свои фигуры и поля, куда они атакуют. Во время обучения затемнение не работает.'
        if language == 'en':
            return 'This chess game differs from the usual ones in that during the battle you will only see your pieces and the fields where they attack. During training, the blackout does not work.'
        if language == 'fr':
            return  'Ces échecs sont différents de la normale en ce sens que pendant le combat, vous ne verrez que leurs pièces et les champs où ils attaquent. Pendant la formation, la gradation ne fonctionne pas.'
        if language == 'es':
            return 'Este ajedrez es diferente de lo normal en que durante la batalla solo verás tus piezas y los campos donde atacan. Durante el entrenamiento, el apagón no funciona.'
        if language == 'de':
            return 'Dieses Schach unterscheidet sich von den üblichen dadurch, dass Sie während des Kampfes nur Ihre Figuren und Felder sehen, wo sie angreifen. Während des Trainings funktioniert Blackout nicht.'
    
    if description == 'purpose':
        if language == 'ru':
            return 'Цель игры - срубить короля противника. Кстати, он может ходить на атакованное поле, так как он не знает об этом. Далее, рокировку можно делать, не проверяя промежуточные поля. Также приложение не сообщает, стоит ли шах. '
        if language == 'en':
            return 'The goal of the game is to cut down the opponent\'s king. By the way, he can go to the attacked field, since he does not know about it. Further, castling can be done without checking the intermediate fields. Also, the app doesn\'t tell you if the check is worth it. '
        if language == 'fr':
            return  'Le but du jeu est d\'abattre le roi de l\'ennemi. D\'ailleurs, il peut marcher sur le terrain attaqué puisqu\'il ne le sait pas. Ensuite, le Roque peut être fait sans vérifier les champs intermédiaires. L\'application ne dit pas non plus si le Shah vaut la peine. '
        if language == 'es':
            return 'El objetivo del juego es derribar al rey enemigo. Por cierto, puede ir al campo atacado, ya que no lo sabe. A continuación, el enroque se puede hacer sin verificar los campos intermedios. Además, la aplicación no informa si el Shah vale la pena. '
        if language == 'de':
            return 'Ziel des Spiels ist es, den gegnerischen König abzuschneiden. Übrigens kann er auf das angegriffene Feld gehen, da er nichts davon weiß. Als nächstes kann die Rochade durchgeführt werden, ohne die Zwischenfelder zu überprüfen. Auch die App sagt nicht, ob Shah es wert ist. '

    if description == 'last':
        if language == 'ru':
            return 'Удачи в бою! А удача во тьме вам понадобится.'
        if language == 'en':
            return 'Good luck in the fight! And you will need luck in the darkness.'
        if language == 'fr':
            return  'Bonne chance au combat! Et vous aurez besoin de chance dans les ténèbres.'
        if language == 'es':
            return '¡Buena suerte en la batalla! Y necesitarás suerte en la oscuridad.'
        if language == 'de':
            return 'Viel Glück im Kampf! Und Sie brauchen Glück in der Dunkelheit.'

    return description


def for_copy(language,description):

    if description == '':
        if language == 'ru':
            return ''
        if language == 'en':
            return ''
        if language == 'fr':
            return  ''
        if language == 'es':
            return ''
        if language == 'de':
            return ''

    if description == '':
        if language == 'ru':
            return ''
        if language == 'en':
            return ''
        if language == 'fr':
            return  ''
        if language == 'es':
            return ''
        if language == 'de':
            return ''

    return 'error in '




__all__ = [Get_text.__name__]