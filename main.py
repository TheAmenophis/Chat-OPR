#  Dobrodošel v klepetalnici!
#  V tej datoteki se nahaja osnovna implementacija klepetalnice s Flaskom in TinyDB-jem.
#  Sledi navodilom v komentarjih in izpolni naloge.
#  Će boš tu investiral čas, ga boš prihranil pri izdelavi zaključne naloge.
#  Srečno!
#  Aja, naloga ti lahko prinese DO 10% dodatnih točk pri zaključni nalogi.
#  O bonusu se ne pogajamo! :) 

# VSA KODA RAZEN CSS MORA BITI POPOLNOMA RAZUMETA IN NAPISANA SAMOSTOJNO! 
# TESTIRAJ! TESTIRAJ! TESTIRAJ!
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime
import os
# Ustvarimo Flask aplikacijo
# Flask je mikro ogrodje za spletne aplikacije v Pythonu
# Več info: https://flask.palletsprojects.com/
app = Flask(__name__)
app.secret_key = "skrivni_kljuc_123"  # V produkciji uporabi pravi skrivni ključ!

# ---- RAZLAGA: TinyDB ----
# TinyDB je preprosta dokumentna podatkovna baza za Python
# Shranjuje podatke v JSON datoteko - brez potrebe po SQL strežniku
# Idealno za manjše aplikacije in učenje
# Več info: https://tinydb.readthedocs.io/
# --------------------------
db = TinyDB('klepet.json')
users = db.table('uporabniki')  # Tabela za uporabnike
messages = db.table('sporocila')  # Tabela za sporočila
User = Query()  # Za poizvedbe po bazi

# ---- RAZLAGA: Flask Routes (Poti) ----
# @app.route() je dekorator, ki pove Flask-u, katero URL pot naj poveže s katero funkcijo
# Ko uporabnik obišče določeno pot v brskalniku, Flask pokliče ustrezno funkcijo
# / = glavna stran (root)
# Več info: https://flask.palletsprojects.com/en/2.0.x/quickstart/#routing
# --------------------------------------
@app.route('/')
def index():
    # ---- RAZLAGA: Flask Sessions ----
    # session je Flaskov način za shranjevanje podatkov za posameznega uporabnika
    # Deluje podobno kot piškotki, vendar so podatki shranjeni na strežniku in zaščiteni
    # Seja se uporablja za preverjanje, ali je uporabnik prijavljen
    # Več info: https://flask.palletsprojects.com/en/2.0.x/quickstart/#sessions
    # ------------------------------

    # ZNAJE ZA ZAGOVOR: najdi session v brskalniku 
    # Zapiši še nekaj v cookie in nekaj preberi iz njega (npr. število obiskov,  čas zadnjega obiska, ipd.)
    # Cookie in njegovo vsebino najdi v brskalniku.
    if 'username' in session:
        return render_template('chat.html')
    return redirect(url_for('login'))

# ---- RAZLAGA: HTTP Methods ----
# methods=['GET', 'POST'] pove Flask-u, da ta pot sprejema tako GET kot POST zahteve
# GET: Pridobi stran (običajno prikaz obrazca)
# POST: Pošlji podatke na strežnik (običajno oddaja obrazca)
# Več info: https://flask.palletsprojects.com/en/2.0.x/quickstart/#http-methods
# --------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    # ---- RAZLAGA: request.method ----
    # request.method nam pove, katera vrsta HTTP zahteve je bila poslana
    # Z 'if request.method == "POST":' preverjamo, ali je bila poslana POST zahteva (oddaja obrazca)
    # Če ni bila POST, je verjetno GET (uporabnik je obiskal stran)
    # GET zahteve običajno uporabljamo za prikaz strani, POST za oddajo obrazca
    # metodo določimo v Ajax zahtevi ali v HTML formi
    # klic iz brskalnika je vedno GET
    # Več info: https://flask.palletsprojects.com/en/2.0.x/quickstart/#accessing-request-data
    # -----------------------------
    # ZNANJE ZA ZAGOVOR: nujno razumeti kdaj prikažemo predlogo in kdaj JSON

    if request.method == 'POST':
        # try v tem primeru prepreči, da bi aplikacija sesula, če pride do napake
        try:
            # ---- RAZLAGA: request.form ----
            # request.form je slovar, ki vsebuje podatke obrazca, poslane z metodo POST
            # Dostopamo do njih z request.form['ime_polja']
            # GET zahteve (običajno) uporabljajo request.args za dostop do parametrov 
            # Več info: https://flask.palletsprojects.com/en/2.0.x/quickstart/#the-request-object
            # -----------------------------
            username = request.form['username']
            password = request.form['password']
            # če bi uporabljal GET, bi uporabil request.args.get('username')
            
            # Preveri, ali uporabnik obstaja v bazi
            user = users.get(User.username == username)
            
            if user:
                # Uporabnik obstaja, preveri geslo
                # če bi želeli uporabiti cookies, bi lahko tukaj preverili tudi username iz piškotka
                if user['password'] == password:
                    session['username'] = username
                    # ---- RAZLAGA: jsonify ----
                    # jsonify pretvori Python slovar v JSON odgovor
                    # jsonify ni potreben, vendar je priporočljiv za doslednost
                    # To je uporabno za AJAX zahteve, kjer klient pričakuje JSON
                    # Več info: https://flask.palletsprojects.com/en/2.0.x/api/#flask.json.jsonify
                    # --------------------------

                    # ta return se izvede samo, če je prijava uspešna
                    return jsonify({'success': True})
                    
                else:
                    # ta return se izvede samo, če je geslo napačno
                    return jsonify({'success': False, 'error': 'Napačno geslo'})
            else:
                # Uporabnik ne obstaja, ustvari novega
                users.insert({'username': username, 'password': password})

                # ---- RAZLAGA: session['key'] ----
                # session je slovar, v katerem lahko shranjujemo podatke za uporabnika
                # session['key'] shrani vrednost pod ključ
                # Uporabljamo ga za shranjevanje podatkov o prijavi uporabnika
                # session poteče, ko uporabnik zapre brskalnik
                # za daljše seje uporabi piškotke (pogooglaj max cookie age )
                # Več info: https://flask.palletsprojects.com/en/2.0.x/quickstart/#sessions
                # --------------------------

                session['username'] = username
                # ta return se izvede samo, če je uporabnik nov
                return jsonify({'success': True})
                
        except Exception as e:
            print(f"Napaka pri prijavi: {str(e)}")
            return jsonify({'success': False, 'error': 'Prišlo je do napake'})
    
    # Če je metoda GET, prikaži predlogo za prijavo
    # ZNANJE ZA ZAGOVOR: nujno razumeti kdaj prikažemo predlogo in kdaj JSON
    return render_template('login.html')

@app.route('/logout')
def logout():
    # ---- RAZLAGA: session.pop ----
    # session.pop() odstrani ključ iz seje
    # Drugi parameter (None) je privzeta vrednost, če ključ ne obstaja
    # To se uporablja za odjavo uporabnika - odstranimo njegovo uporabniško ime iz seje
    # --------------------------

    # ZNANJE ZA ZAGOVOR: preveri razliko med session, cookies in local storage in kako se uporabljajo
    
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/get_messages')
def get_messages():
    # Tukaj preprečimo nepooblaščen dostop do sporočil
    # Torej, če uporabnik ni prijavljen, mu vrnemo napako
    if 'username' not in session:
        # ---- RAZLAGA: HTTP Status Codes ----
        # Drugi parameter v jsonify() določa HTTP status kodo
        # 401 = Unauthorized (Nepooblaščen dostop)
        # Druge pogoste kode: 200 (OK), 404 (Not Found), 500 (Server Error)
        # Več info: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
        # ----------------------------------
        return jsonify({'error': 'Niste prijavljeni'}), 401
    
    all_messages = messages.all()
    return jsonify(all_messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({'error': 'Niste prijavljeni'}), 401
    
    try:
        message_text = request.form['message']
        username = session['username']
        # NALOGA: Oblikuj timestamp v lepši format.
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Vstavi sporočilo v bazo
        messages.insert({
            'username': username,
            'message': message_text,
            'timestamp': timestamp
        })
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Napaka pri pošiljanju sporočila: {str(e)}")
        return jsonify({'success': False, 'error': 'Napaka pri pošiljanju'})

# ----- NALOGA 1 -----
# Dodaj novo pot za brisanje vseh sporočil za administratorja
# Namig: Ustvari novo pot "/clear_messages" z metodo POST
# Razmisli: Kako bi preverjal, ali je uporabnik administrator?
# Namig: dodaj admin dashboard, kjer se lahko samo admin prijavi
# Namig: Uporabi sejo za preverjanje prijave
# Namig: Preveri, ali je uporabnik administrator (npr. v bazi uporabnikov)
# Poišči v dokumentaciji TinyDB, kako izbrisati vse dokumente v tabeli
#
# Primer začetka implementacije:
# @app.route('/clear_messages', methods=['POST'])
# def clear_messages():
#    if 'username' not in session:
#        return jsonify({'error': 'Niste prijavljeni'}), 401
#    
#    # Tukaj preveri, ali je uporabnik administrator
#    # TODO: Dodaj svojo kodo za preverjanje administratorja
#    
#    # Izbriši vsa sporočila
#    # TODO: Dodaj svojo kodo za brisanje vseh sporočil
#    
#    return jsonify({'success': True})
# --------------------

@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    if 'username' not in session:
       return jsonify({'error': 'Niste prijavljeni'}), 401
    if session['username']
    
   

# ----- NALOGA 2 -----
# Dodaj novo pot za iskanje sporočil po ključnih besedah
# Namig: Ustvari novo pot "/search_messages" z metodo GET, 
# ki sprejme parameter "keyword" in vrne ustrezna sporočila
# Namig: Uporabi TinyDB poizvedbe za iskanje po ključnih besedah
# Namig: Iskanje dodaj v admin panel ali kar v chat
# Več info o parametrih GET zahtev: https://flask.palletsprojects.com/en/2.0.x/quickstart/#the-request-object
# 
# Primer začetka implementacije:
# @app.route('/search_messages', methods=['GET'])
# def search_messages():    
#     if 'username' not in session:
#         return jsonify({'error': 'Niste prijavljeni'}), 401
#     
#     # Pridobi ključno besedo iz parametrov GET zahteve
#     # TODO: Dodaj svojo kodo za pridobitev ključne besede
#     
#     # Poišči sporočila, ki vsebujejo ključno besedo
#     # TODO: Dodaj svojo kodo za iskanje po sporočilih
# --------------------

# ----- NALOGA 3 -----
# Dodaj novo pot za brisanje posameznega sporočila
# Namig: Ustvari novo pot "/delete_message" z metodo POST
# Poskrbi, da uporabnik lahko izbriše samo svoja sporočila
# Poišči v dokumentaciji TinyDB, kako izbrisati dokument po ID-ju
# --------------------

if __name__ == "__main__":
    # Ustvari direktorij za predloge, če ne obstaja
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True)