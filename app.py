from flask import Flask, request, session, redirect, render_template
import random, time
import string

app = Flask(__name__)
app.secret_key = 'secret'

def parse(expression, var='n'):
    expression = expression.replace('^', '**') 
    expression = expression.replace(' ', '')
    i = 0
    while i < len(expression) - 1:
        if expression[i].isdigit() and expression[i+1] == var:
            expression = expression[:i+1] + '*' + expression[i+1:]
        i += 1
    return expression

def mfrac(n):
    return [n[0] % n[1], n[1], int(n[0]/n[1])]

def trim(s):
    s = s.replace('e', '')
    try:
        i = s.index('.')
        return s[:i]
    except:
        return s

def fracans(raw):
    for i in range(2, abs(min(raw)) + 1):
        while raw[0] % i == raw[1] % i == 0:
            raw[0] /= i
            raw[1] /= i
    return int(raw[0]), int(raw[1])

@app.route('/')
def home():
    try:
        session['clr']
    except:
        session['clr'] = 1
    return render_template('settings.html', session = session, int = int)

@app.route('/game', methods=['POST'])
def game():
    include_integers = 'includeIntegers' in request.form
    include_negatives = 'includeNegatives' in request.form
    include_decimals = 'includeDecimals' in request.form
    decimal_places = int(trim(request.form.get('decimalPlaces', '0')))
    include_addition = 'includeAddition' in request.form
    addition_bounds1 = int(trim(request.form.get('additionBounds1', '0')))
    addition_bounds2 = int(trim(request.form.get('additionBounds2', '0')))
    include_subtraction = 'includeSubtraction' in request.form
    subtraction_bounds1 = int(trim(request.form.get('subtractionBounds1', '0')))
    subtraction_bounds2 = int(trim(request.form.get('subtractionBounds2', '0')))
    include_multiplication = 'includeMultiplication' in request.form
    multiplication_bounds1 = int(trim(request.form.get('multiplicationBounds1', '0')))
    multiplication_bounds2 = int(trim(request.form.get('multiplicationBounds2', '0')))
    include_division = 'includeDivision' in request.form
    division_bounds1 = int(trim(request.form.get('divisionBounds1', '0')))
    division_bounds2 = int(trim(request.form.get('divisionBounds2', '0')))
    time_limit = int(trim(request.form.get('timeLimit', '0')))

    # Store the settings in the session object
    session['include_integers'] = include_integers
    session['include_negatives'] = include_negatives
    session['include_decimals'] = include_decimals
    session['decimal_places'] = decimal_places
    session['include_addition'] = include_addition
    session['addition_bounds1'] = addition_bounds1
    session['addition_bounds2'] = addition_bounds2
    session['include_subtraction'] = include_subtraction
    session['subtraction_bounds1'] = subtraction_bounds1
    session['subtraction_bounds2'] = subtraction_bounds2
    session['include_multiplication'] = include_multiplication
    session['multiplication_bounds1'] = multiplication_bounds1
    session['multiplication_bounds2'] = multiplication_bounds2
    session['include_division'] = include_division
    session['division_bounds1'] = division_bounds1
    session['division_bounds2'] = division_bounds2
    session['time_limit'] = time.time() + time_limit

    return redirect('/game')

@app.route('/game', strict_slashes=False)
def game_1():
    time_limit = session.get('time_limit')
    if time.time() > time_limit:
        return redirect('/scoring')

    negatives = session.get('include_negatives')
    decimal_places = session.get('decimal_places')
    include_addition = session.get('include_addition')
    addition_bounds1 = session.get('addition_bounds1')
    addition_bounds2 = session.get('addition_bounds2')
    include_subtraction = session.get('include_subtraction')
    subtraction_bounds1 = session.get('subtraction_bounds1')
    subtraction_bounds2 = session.get('subtraction_bounds2')
    include_multiplication = session.get('include_multiplication')
    multiplication_bounds1 = session.get('multiplication_bounds1')
    multiplication_bounds2 = session.get('multiplication_bounds2')
    include_division = session.get('include_division')
    division_bounds1 = session.get('division_bounds1')
    division_bounds2 = session.get('division_bounds2')
    
    numt = [i for i in range(decimal_places + 1)]
    if not numt:
        numt = [0]

    equation = []
    answer = []

    negative = [1, 1, 1]
    negative += [-1 if negatives else 1]
    
    if include_addition:    
        num1 = random.randint(0, addition_bounds1) * random.choice(negative)
        num2 = random.randint(0, addition_bounds2) * random.choice(negative)
        
        a = random.choice(numt)
        num1 += round(random.randint(0, 10 ** a) / 10 ** a, a)
        b = random.choice(numt)
        num2 += random.randint(0, 10 ** b) / 10 ** b
        c = max([a, b])
        if num1 % 1 == 0:
            num1 = int(num1)
        if num2 % 1 == 0:
            num2 = int(num2)
        equation += [f"{num1} + {num2}"]
        answer += [round(num1 + num2, c)]

    if include_subtraction:
        num1 = random.randint(0, subtraction_bounds1) * random.choice(negative)
        num2 = random.randint(0, subtraction_bounds2) * random.choice(negative)
        a = random.choice(numt)
        num1 += random.randint(0, 10 ** a) / 10 ** a
        b = random.choice(numt)
        num2 += random.randint(0, 10 ** b) / 10 ** b
        c = max([a, b])
        if num1 % 1 == 0:
            num1 = int(num1)
        if num2 % 1 == 0:
            num2 = int(num2)
        equation += [f"{num1} - {num2}"]
        answer += [round(num1 - num2, c)]

    if include_multiplication:
        num1 = random.randint(0, multiplication_bounds1) * random.choice(negative)
        num2 = random.randint(0, multiplication_bounds2) * random.choice(negative)
        a = random.choice(numt)
        num1 += random.randint(0, 10 ** a) / 10 ** a
        if num1 % 1 == 0:
            num1 = int(num1)
        if num2 % 1 == 0:
            num2 = int(num2)
        equation += [f"{num1} x {num2}"]
        answer += [round(num1 * num2, a)]

    if include_division:
        num2 = random.randint(1, division_bounds1) * random.choice(negative)
        product = random.randint(1, division_bounds2) * random.choice(negative)
        num1 = num2 * product
        equation += [f"{num1} ÷ {num2}"]
        answer += [num1 / num2]
        
    print(equation)    
    try:
        a = random.choice(equation)
    except:
        return redirect('/')
    b = answer[equation.index(a)]
    

    return render_template('game.html', equation=a, answer=b, t = int(time_limit - time.time()))

@app.route('/scoring')
def bing():
    return render_template('score.html')

@app.route('/climbs/<sequence>/<tn>/finish')
def bingbongbing(sequence, tn):
    seqdict = {'n**2' : 'Square numbers', '0.5*n*(n+1)' : 'Triangle numbers', 'n**3':'Cube numbers'}
    try:
        sequence = seqdict[sequence]
    except:
        pass
    return render_template('finishclimb.html', tn = int(tn), sequence = sequence)

@app.route('/climbs', strict_slashes=False)
def climbs():
    return render_template('climbs.html')

@app.route('/climbs/<sequence>/<tn>/', methods=['GET', 'POST'])
def climb2(sequence, tn):
    if request.method == 'GET':
        if not int(tn) - 1:
            session['anss'] = []
        if sequence == 'pi':
            n = open('digits.txt').read(int(tn))
            if n == '\n':
                n = open('digits.txt').read(int(tn))
            print(n)
            print('N')
            session['ans'] = int(n[::-1][0])
            return render_template('climmisc.html', url=f'/climbs/{sequence}/{tn}', tn=tn)
        if sequence == 'fibonacci':
            if int(tn) - 1:
                session['ans'] = [session['ans'][1], sum(session['ans'])]
            else:
                session['ans'] = [0, 1]
            return render_template('climbp.html', url=f'/climbs/{sequence}/{tn}', tn=tn)
        session['ans'] = eval(sequence.replace('n', tn))
        return render_template('climmisc.html', url=f'/climbs/{sequence}/{tn}', tn=tn)
    else:
        uans = int(request.form['ans'])
        print(str(uans), session['ans'], uans == session['ans'])
        if sequence == 'fibonacci':
            if uans != session['ans'][1]:
                return redirect(f'/climbs/{sequence}/{int(tn)}/finish')
            else:
                x = str(int(tn) + 1)
                session['anss'] += [request.form['ans']]
                return redirect(f'/climbs/{sequence}/{x}')
        if session['ans'] != uans:
            return redirect(f'/climbs/{sequence}/{int(tn)}/finish')
        x = str(int(tn) + 1)
        session['anss'] += [request.form['ans']]
        return redirect(f'/climbs/{sequence}/{x}')
    
@app.route('/practice')
def pracfrac():
    return redirect('/practice/0')
    
@app.route('/practice/<dif>')
def fractions(dif):
    a = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 20, 25]
    print(a)
    if dif == '1':
        print(1)
        a += [7, 11, 13, 14, 16, 17, 18 , 19]
    a = [random.randint(1, 20), random.choice(a)]
    b = [random.randint(1, 20), random.choice(a)]
    op = random.choice(['Multiplication', 'Division', 'Addition', 'Subtraction'])
    print(op)
    if op == 'Multiplication':
        n = [a[0]*b[0], a[1]*b[1]]
    elif op == 'Division':
        n = [a[0]*b[1], a[1]*b[0]]
    elif op == 'Addition':
        n = [a[1]*b[0] + a[0]*b[1], a[1]*b[1]]
    elif op == 'Subtraction':
        n = [a[1]*b[0] - a[0]*b[1], a[1]*b[1]]
    ans = fracans(n)
    print(ans)
    return render_template('fractions.html', a = a, b = b, ans = ans, op = op, int = int, dif = dif, d = {'Multiplication' : 'x', 'Division' : '÷', 'Addition' : '+', 'Subtraction' : '-'})

@app.route('/mixed/<dif>')
def mixedfrac(dif):
    a = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 20, 25]
    print(a)
    if dif == '1':
        print(1)
        a += [7, 11, 13, 14, 16, 17, 18 , 19]
    a = [random.randint(1, 20), random.choice(a)]
    b = [random.randint(1, 20), random.choice(a)]
    if not mfrac(a)[0]:
        a[0] += 1
    if not mfrac(b)[0]:
        b[0] += 1
    op = random.choice(['Multiplication', 'Division', 'Addition', 'Subtraction'])
    print(op)
    if op == 'Multiplication':
        n = [a[0]*b[0], a[1]*b[1]]
    elif op == 'Division':
        n = [a[0]*b[1], a[1]*b[0]]
    elif op == 'Addition':
        n = [a[1]*b[0] + a[0]*b[1], a[1]*b[1]]
    elif op == 'Subtraction':
        n = [a[1]*b[0] - a[0]*b[1], a[1]*b[1]]
    ans = fracans(n)
    ans = mfrac(ans)
    print(ans)
    return render_template('mixed.html', a = mfrac(a), b = mfrac(b), ans = ans, op = op, int = int, dif = dif, d = {'Multiplication' : 'x', 'Division' : '÷', 'Addition' : '+', 'Subtraction' : '-'})

@app.route('/custom-climb', methods=['POST'])
def custom():
    n = request.form['nth']
    for i in string.ascii_letters:
        if i == 'n':
            continue
        if i in n:
            return redirect('/climbs')
    n = parse(n)
    try:
        eval(n.replace('n', '1'))
    except Exception as e:
        return redirect('/climbs')
    return redirect(f'/climbs/{n}')

@app.route('/change-theme')
def duiweyuwl():
    try:
        session['clr'] = abs(session['clr'] - 1)
        print(session['clr'])
    except:
        print('err')
        session['clr'] = 1
    return redirect('/')

@app.route('/climbs/<seq>')
def climbim(seq):
    return render_template('climbp.html', seq = seq)

if __name__ == '__main__':
    app.run(debug=True)
