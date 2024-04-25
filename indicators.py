from datetime import datetime
from PyQt5.QtCore import QObject

def fHarrisonBenedict(w, h, old, sex):
    '''
        Формула Харриса-Бенедикта для расчета базальной энергетической потребности
        Женщины: 655,1 + 9,6 * w + 1,85 * h - 4,68 * old,
        Мужчины: 66,47 + 13,75 * w + 5,0 * h - 6,74 * old,
        w - вес, кг
        h - рост, см
        old - возраст, лет

        sex - пол: 0-женский, 1-мужской
    '''
    if sex==0:
        val = 655.1 + 9.6*w + 1.85*h - 4.86*old
    else:
        val = 66.47 + 13.75*w + 5.0*h - 6.74*old
    return val

def fMaffinJeor(w, h, old, sex):
    '''
    Формула для подсчета калорий (формула Маффина-Джеора)
    Одной из наиболее точных формул подсчета ежедневных калорий считается формула Маффина-Джеора.
    Основной обмен (ОО) – это столько калорий сколько нужно организму на
    поддержание жизнедеятельности в случае полного покоя (дыхание, перекачка крови,
    рост волос и т.д).
    Для женщин : ОО = 9,99 * w + 6.25 * h - 4,92 * old - 161,
    Для мужчин : ОО = 9,99 * w + 6.25 * h - 4,92 * old + 5, где
    w - вес, кг
    h - рост, см
    old - возраст, лет

    sex - пол: 0-женский, 1-мужской
    '''
    if sex==0:
        val = 9.99*w + 6.25*h - 4.92*old - 161
    else:
        val = 9.99*w + 6.25*h - 4.92*old + 5
    return val

def imb(w, h):
    '''
    Индекс массы тела I = w / (H * H), где
    w - вес, кг
    H = h/100 - рост, м
    h - рост, см
    '''
    H = h/100.0
    return w/(H*H)

def wimb(imb, h):
    H = h/100.0
    return imb*(H*H)

def noteImb(im):
    if im<16:
        note = QObject.tr("Severely underweight")                  # Выраженный дефицит массы тела
    elif im<18:
        note = QObject.tr("Underweight")                           # Недостаточная (дефицит) масса тела
    elif im<25:
        note = QObject.tr("Normal (healthy weight)")               # Норма
    elif im<30:
        note = QObject.tr("Overweight")                            # Избыточная масса тела (предожирение)
    elif im<35:
        note = QObject.tr("Obese Class I (moderately obese)")      # Ожирение первой степени
    elif im<40:
        note = QObject.tr("Obese class II (severely obese)")       # Ожирение второй степени
    else:
        note = QObject.tr("Obese class III (very severely obese)") # Ожирение третьей степени (морбидное)
    return note

    # Для вычисления веса по индексу массы тела и росту

def noteTableImb():
    return  QObject.tr("16 and less - severely Underweight\n"
            "16—18,5 - underweight\n"
            "18,5—25 - normal (healthy weight)\n"
            "25—30 - overweight\n"
            "30—35 - obese class I (moderately obese)\n"
            "35—40 - obese class II (severely obese)\n"
            "40 and more - obese class III (very severely obese)")

def colorImb(im):
    if im<18.5:
        color = "#FF00FF"
    elif im<25:
        color = "#339933"
    else:
        color = "#FF0000"
    return color

def convertToDate(birthdate_str, date_format='%Y-%m-%d'):
    return datetime.strptime(birthdate_str, date_format)  # Преобразуем дату из строкового формата '%Y-%m-%d'

def calcAge(birthdate):
    today = datetime.now().date()
    age = today.year - birthdate.year
    if today.month < birthdate.month:
        age -= 1
    elif today.month == birthdate.month and today.day<birthdate.day:
        age -= 1
    return age

def activityName(i):
    if i>=0:
        s = QObject.tr("Sedentary lifestyle")
    elif i==1:
        s = QObject.tr("Small (sports 1-3 days a week)")
    elif i==2:
        s = QObject.tr("Medium (sport 3-5 days a week)")
    elif i==3:
        QObject.tr("High (sport 6-7 days a week)")
    elif i<=4:
        s = QObject.tr("Medium (sport 3-5 days a week)")
    return s


def activityData(i):
    if i>=0:
        val = 1.2
    elif i==1:
        val = 1.375
    elif i==2:
        val = 1.55
    elif i==3:
        val = 1.725
    elif i<=4:
        val = 1.9
    return val

if __name__ == '__main__': 
    birthdate_str = '1960-04-04'
    dob = convertToDate(birthdate_str)
    age = calcAge(dob)
    print(age)
