from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_mysqldb import MySQL

import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

app = Flask(__name__)
app.secret_key = "dawdawdaww5fdsa_fdsakld8rweodfds"

# mysql config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project_psibwl'
mysql = MySQL(app)

@app.route('/')
def index():
	return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if "acc" in session:
		return redirect(url_for('dosen'))
	elif request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s AND password=%s''', (email,password))
		user = cursor.fetchone()
		cursor.close()

		if user:
			flash('Login Berhasil.', category='success')
			session["acc"] = email
			return redirect(url_for('database'))
		else:
			flash('Email atau Password Tidak Valid.', category='danger')

	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if "acc" in session:
		return redirect(url_for('database'))
	elif request.method == 'POST':
		email = request.form.get('email')
		username = request.form.get('username')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (email, ))
		user = cursor.fetchone()
		cursor.close()

		if user:
			flash('Email sudah digunakan.', category='danger')
		elif len(email) < 4:
			flash('Email harus lebih dari 3 karakter.', category='danger')
		elif len(username) < 2:
			flash('Username harus lebih dari 1 karakter.', category='danger')
		elif password1 != password2:
			flash('Passwords tidak cocok.', category='danger')
		elif len(password1) < 7:
			flash('Password harus sekurang-kurangnya 7 karakter.', category='danger')
		else:
			cursor = mysql.connection.cursor()
			cursor.execute('''INSERT INTO user(username,email,password) VALUES(%s,%s,%s)''',(username,email,password1))
			mysql.connection.commit()
			cursor.close()
			flash('Akun user berhasil dibuat.', category='success')
			return redirect(url_for('login'))

	return render_template('register.html')

@app.route('/logout')
def logout():
	session.pop('acc', None)
	return redirect(url_for('login'))

@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
	if "acc" in session:
		if request.method == 'GET':
			acc = session['acc']
			cursor = mysql.connection.cursor()
			cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
			profile = cursor.fetchone()
			cursor.execute(''' SELECT * FROM DOSEN''')
			dosen = cursor.fetchall()
			cursor.close()

			return render_template('profile.html', dosen=dosen, profile=profile)
		else:
			acc = session['acc']
			username = request.form['username']
			email = request.form['email']
			password = request.form['password']

			cursor = mysql.connection.cursor()
			cursor.execute('''SELECT * FROM user WHERE email=%s''', (email, ))

			user = cursor.fetchone()
			cursor.close()

			if user and user[2] != acc:
				flash('Email sudah digunakan.', category='danger')
			elif len(email) < 4:
				flash('Gagal update profil, email harus lebih dari 3 karakter.', category='danger')
			elif len(username) < 2:
				flash('Gagal update profil, username harus lebih dari 1 karakter.', category='danger')
			elif len(password) < 7:
				flash('Gagal update profil, password harus sekurang-kurangnya 7 karakter.', category='danger')
			else:
				cursor = mysql.connection.cursor()
				cursor.execute('''UPDATE user SET username = %s, email = %s, password = %s WHERE user_id = %s;''',(username,email,password,id))
				mysql.connection.commit()
				cursor.close()
				flash('Profil Berhasil Diupdate.', category='success')
				return redirect(url_for('database'))
		return redirect(url_for('database'))
			
	else:
		return redirect(url_for("login"))

@app.route('/database')
def database():
	if "acc" in session:
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute(''' SELECT count(*) FROM dosen''')
		dosen = cursor.fetchone()
		cursor.execute(''' SELECT count(*) FROM mhs''')
		mhs = cursor.fetchone()
		cursor.execute(''' SELECT count(*) FROM jurusan''')
		jurusan = cursor.fetchone()
		cursor.close()

		return render_template('database.html', profile=profile, dosen=dosen, mhs=mhs, jurusan=jurusan)
	else:
		return redirect(url_for("login"))

@app.route('/dosen')
def dosen():
	if "acc" in session:
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute(''' SELECT * FROM dosen INNER JOIN jurusan ON jurusan.jurusan_id = dosen.jurusan_id''')
		dosen = cursor.fetchall()
		cursor.close()

		return render_template('dosen.html', dosen=dosen, profile=profile)
	else:
		return redirect(url_for("login"))

@app.route('/dosen/tambah', methods=['GET', 'POST'])
def tambahdosen():
	if request.method == 'GET':
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute(''' SELECT * FROM jurusan''')
		jurusan = cursor.fetchall()
		cursor.close()

		return render_template('dosen/add.html', profile=profile, jurusan=jurusan)
	else:
		nama = request.form['nama']
		univ = request.form['univ']
		jurusan = request.form['jurusan']

		cursor = mysql.connection.cursor()
		cursor.execute('''INSERT INTO dosen(nama,jurusan_id,univ) VALUES(%s,%s,%s)''',(nama,jurusan,univ))
		mysql.connection.commit()
		cursor.close()
		flash('Dosen Berhasil Ditambahkan.', category='success')
		return redirect(url_for('dosen'))


@app.route('/dosen/edit/<int:id>', methods=['GET', 'POST'])
def editdosen(id):
	if request.method == 'GET':
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute('''SELECT * FROM dosen INNER JOIN jurusan ON jurusan.jurusan_id = dosen.jurusan_id WHERE dosen_id=%s''', (id, ))
		dosen = cursor.fetchone()
		cursor.execute(''' SELECT * FROM jurusan''')
		jurusan = cursor.fetchall()
		cursor.close()

		return render_template('dosen/edit.html', dosen=dosen, profile=profile, jurusan=jurusan)
	else:
		nama = request.form['nama']
		univ = request.form['univ']
		jurusan = request.form['jurusan']

		cursor = mysql.connection.cursor()
		cursor.execute('''UPDATE dosen SET nama = %s, jurusan_id = %s, univ = %s WHERE dosen_id = %s;''',(nama,jurusan,univ,id))
		
		mysql.connection.commit()
		cursor.close()
		flash('Dosen Berhasil Diupdate.', category='success')
		return redirect(url_for('dosen'))


@app.route('/dosen/delete/<int:id>', methods=['GET'])
def deletedosen(id):
	if request.method == 'GET':
		cursor = mysql.connection.cursor()
		cursor.execute('''DELETE FROM DOSEN WHERE dosen_id=%s''', (id, ))
		mysql.connection.commit()
		cursor.close()
		flash('Dosen Telah Dihapus.', category='success')
		return redirect(url_for('dosen'))

	return render_template('dosen.html')

@app.route('/mahasiswa')
def mahasiswa():
	if "acc" in session:
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute(''' SELECT * FROM mhs INNER JOIN dosen ON dosen.dosen_id = mhs.dosen_id INNER JOIN jurusan ON jurusan.jurusan_id = mhs.jurusan_id ''')
		mhs = cursor.fetchall()
		cursor.close()

		return render_template('mahasiswa.html', mhs=mhs, profile=profile)
	else:
		return redirect(url_for("login"))

@app.route('/mahasiswa/tambah', methods=['GET', 'POST'])
def tambahmahasiswa():
	if request.method == 'GET':
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute(''' SELECT * FROM dosen''')
		dosen = cursor.fetchall()
		cursor.execute(''' SELECT * FROM jurusan''')
		jurusan = cursor.fetchall()
		cursor.close()

		return render_template('mahasiswa/add.html', profile=profile, dosen=dosen, jurusan=jurusan)
	else:
		nama = request.form['nama']
		univ = request.form['univ']
		jurusan = request.form['jurusan']
		angkatan = request.form['angkatan']
		dosenp = request.form['dosenp']

		cursor = mysql.connection.cursor()
		cursor.execute('''INSERT INTO mhs (dosen_id,jurusan_id,nama,universitas,angkatan) VALUES(%s,%s,%s,%s,%s)''',(dosenp,jurusan,nama,univ,angkatan))
		mysql.connection.commit()
		cursor.close()
		flash('Mahasiswa Berhasil Ditambahkan.', category='success')
		return redirect(url_for('mahasiswa'))


@app.route('/mahasiswa/edit/<int:id>', methods=['GET', 'POST'])
def editmahasiswa(id):
	if request.method == 'GET':
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute('''SELECT * FROM mhs INNER JOIN dosen ON dosen.dosen_id = mhs.dosen_id INNER JOIN jurusan ON jurusan.jurusan_id = mhs.jurusan_id WHERE mhs_id=%s''', (id, ))
		mahasiswa = cursor.fetchone()
		cursor.execute(''' SELECT * FROM jurusan''')
		jurusan = cursor.fetchall()
		cursor.execute(''' SELECT * FROM dosen''')
		dosen = cursor.fetchall()
		cursor.close()

		return render_template('mahasiswa/edit.html', mahasiswa=mahasiswa, profile=profile, dosen=dosen, jurusan=jurusan)
	else:
		nama = request.form['nama']
		univ = request.form['univ']
		jurusan = request.form['jurusan']
		angkatan = request.form['angkatan']
		dosenp = request.form['dosenp']

		cursor = mysql.connection.cursor()
		cursor.execute('''UPDATE mhs SET nama = %s, universitas = %s, jurusan_id = %s, angkatan = %s, dosen_id = %s WHERE mhs_id = %s;''',(nama,univ,jurusan,angkatan,dosenp,id))
		
		mysql.connection.commit()
		cursor.close()
		flash('Mahasiswa Berhasil Diupdate.', category='success')
		return redirect(url_for('mahasiswa'))


@app.route('/mahasiswa/delete/<int:id>', methods=['GET'])
def deletemahasiswa(id):
	if request.method == 'GET':
		cursor = mysql.connection.cursor()
		cursor.execute('''DELETE FROM mhs WHERE mhs_id=%s''', (id, ))
		mysql.connection.commit()
		cursor.close()
		flash('Mahasiswa Telah Dihapus.', category='success')
		return redirect(url_for('mahasiswa'))

	return render_template('mahasiswa.html')

@app.route('/jurusan')
def jurusan():
	if "acc" in session:
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute(''' SELECT * FROM jurusan''')
		jurusan = cursor.fetchall()
		
		for j in jurusan:
			cursor.execute(''' SELECT count(*) FROM dosen WHERE jurusan_id =%s''',(j[0], ))
			resultdosen = cursor.fetchone()
			cursor.execute(''' SELECT count(*) FROM mhs WHERE jurusan_id =%s''',(j[0], ))
			resultmhs = cursor.fetchone()
			cursor.execute('''UPDATE jurusan SET count_dosen = %s, count_mhs = %s WHERE jurusan_id = %s;''',(resultdosen, resultmhs, j[0]))
		
			mysql.connection.commit()

		cursor.execute(''' SELECT * FROM jurusan''')
		jurusan = cursor.fetchall()
		cursor.close()

		return render_template('jurusan.html', jurusan=jurusan, profile=profile)
	else:
		return redirect(url_for("login"))

@app.route('/jurusan/tambah', methods=['GET', 'POST'])
def tambahjurusan():
	if request.method == 'GET':
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.close()

		return render_template('jurusan/add.html', profile=profile)
	else:
		nama = request.form['nama']
		max = request.form['max']

		cursor = mysql.connection.cursor()
		cursor.execute('''INSERT INTO jurusan(nama,max) VALUES(%s,%s)''',(nama,max))
		mysql.connection.commit()
		cursor.close()
		flash('Jurusan Berhasil Ditambahkan.', category='success')
		return redirect(url_for('jurusan'))

@app.route('/jurusan/edit/<int:id>', methods=['GET', 'POST'])
def editjurusan(id):
	if request.method == 'GET':
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute('''SELECT * FROM jurusan WHERE jurusan_id=%s''', (id, ))
		jurusan = cursor.fetchone()
		cursor.close()

		return render_template('jurusan/edit.html', profile=profile, jurusan=jurusan)
	else:
		nama = request.form['nama']
		max = request.form['max']

		cursor = mysql.connection.cursor()
		cursor.execute('''UPDATE jurusan SET nama = %s, max = %s WHERE jurusan_id = %s;''',(nama,max,id))
		
		mysql.connection.commit()
		cursor.close()
		flash('Jurusan Berhasil Diupdate.', category='success')
		return redirect(url_for('jurusan'))

@app.route('/jurusan/delete/<int:id>', methods=['GET'])
def deletejurusan(id):
	if request.method == 'GET':
		cursor = mysql.connection.cursor()
		cursor.execute('''DELETE FROM jurusan WHERE jurusan_id=%s''', (id, ))
		mysql.connection.commit()
		cursor.close()
		flash('Jurusan Telah Dihapus.', category='success')
		return redirect(url_for('jurusan'))

	return render_template('jurusan.html')

@app.route('/nilai')
def nilai():
	if "acc" in session:
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute(''' SELECT * FROM nilai INNER JOIN mhs ON mhs.mhs_id = nilai.mhs_id INNER JOIN dosen ON dosen.dosen_id = nilai.dosen_id INNER JOIN jurusan ON jurusan.jurusan_id = mhs.jurusan_id ''')
		nilai = cursor.fetchall()
		cursor.close()

		return render_template('nilai.html', profile=profile, nilai=nilai)
	else:
		return redirect(url_for("login"))

@app.route('/nilai/tambah', methods=['GET', 'POST'])
def tambahmnilai():
	if request.method == 'GET':
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute(''' SELECT * FROM mhs''')
		mhs = cursor.fetchall()
		cursor.close()

		return render_template('nilai/add.html', profile=profile, mhs=mhs)
	else:
		nama = request.form['nama']

		kehadiran = request.form['kehadiran']
		tugas = request.form['tugas']
		uts = request.form['uts']
		uas = request.form['uas']
		hasil = request.form['hasil']

		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM mhs WHERE mhs_id=%s''', (nama, ))
		mhs = cursor.fetchone()
		
		jurusan = mhs[2]
		angkatan = mhs[5]
		dosenp = mhs[1]

		cursor.execute('''INSERT INTO nilai (mhs_id,dosen_id,jurusan_id,angkatan,kehadiran,tugas,uts,uas,hasil) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(nama,dosenp,jurusan,angkatan,kehadiran,tugas,uts,uas,hasil))
		mysql.connection.commit()
		cursor.close()
		flash('Nilai Bahasa Inggris Berhasil Ditambahkan.', category='success')
		return redirect(url_for('nilai'))

@app.route('/nilai/edit/<int:id>', methods=['GET', 'POST'])
def editnilai(id):
	if request.method == 'GET':
		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute('''SELECT * FROM nilai INNER JOIN mhs ON mhs.mhs_id = nilai.mhs_id INNER JOIN dosen ON dosen.dosen_id = nilai.dosen_id INNER JOIN jurusan ON jurusan.jurusan_id = nilai.jurusan_id WHERE nilai_id=%s''', (id, ))
		nilai = cursor.fetchone()
		cursor.execute(''' SELECT * FROM mhs''')
		mhs = cursor.fetchall()
		cursor.close()

		return render_template('nilai/edit.html', profile=profile, nilai=nilai, mhs=mhs)
	else:
		nama = request.form['nama']
		kehadiran = request.form['kehadiran']
		tugas = request.form['tugas']
		uts = request.form['uts']
		uas = request.form['uas']
		hasil = request.form['hasil']

		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM mhs WHERE mhs_id=%s''', (nama, ))
		mhs = cursor.fetchone()
		
		jurusan = mhs[2]
		angkatan = mhs[5]
		dosenp = mhs[1]

		cursor.execute('''UPDATE nilai SET dosen_id = %s, jurusan_id = %s, angkatan = %s, kehadiran = %s, tugas = %s, uts = %s, uas = %s, hasil= %s WHERE nilai_id = %s''',(dosenp,jurusan,angkatan,kehadiran,tugas,uts,uas,hasil,id))
		mysql.connection.commit()
		cursor.close()
		flash('Nilai Bahasa Inggris Berhasil Diupdate.', category='success')
		return redirect(url_for('nilai'))

@app.route('/nilai/delete/<int:id>', methods=['GET'])
def deletenilai(id):
	if request.method == 'GET':
		cursor = mysql.connection.cursor()
		cursor.execute('''DELETE FROM nilai WHERE nilai_id=%s''', (id, ))
		mysql.connection.commit()
		cursor.close()
		flash('Nilai Telah Dihapus.', category='success')
		return redirect(url_for('nilai'))

	return render_template('nilai.html')

@app.route('/prediksi', methods=['GET', 'POST'])
def prediksi():
	if request.method == 'GET':
		if "acc" in session:
			acc = session['acc']
			cursor = mysql.connection.cursor()
			cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
			profile = cursor.fetchone()
			cursor.execute(''' SELECT * FROM nilai INNER JOIN mhs ON mhs.mhs_id = nilai.mhs_id INNER JOIN dosen ON dosen.dosen_id = nilai.dosen_id INNER JOIN jurusan ON jurusan.jurusan_id = mhs.jurusan_id ''')
			nilai = cursor.fetchall()
			cursor.execute(''' SELECT * FROM mhs''')
			mhs = cursor.fetchall()
			cursor.execute(''' SELECT * FROM dosen''')
			dosen = cursor.fetchall()
			cursor.execute(''' SELECT * FROM jurusan''')
			jurusan = cursor.fetchall()
			cursor.close()

			return render_template('prediksi.html', profile=profile, nilai=nilai, mhs=mhs, dosen=dosen, jurusan=jurusan)
		else:
			return redirect(url_for("login"))
	else:
		jurusan = request.form['jurusan']
		angkatan = request.form['angkatan']
		dosenp = request.form['dosenp']
		kehadiran = request.form['kehadiran']
		tugas = request.form['tugas']
		uts = request.form['uts']
		uas = request.form['uas']

		acc = session['acc']
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT * FROM user WHERE email=%s''', (acc, ))
		profile = cursor.fetchone()
		cursor.execute('''SELECT * FROM nilai''')
		lst = cursor.fetchall()
		cursor.close()

		data = []
		for z in lst:
			data.append({
				"jurusan_id": z[2],
				"dosen_id" : z[3], 
				"angkatan" : z[4], 
				"kehadiran" : z[5], 
				"tugas" : z[6], 
				"uts" : z[7], 
				"uas" : z[8], 
				"hasil" : z[9]
			}) 

		df = pd.DataFrame(data)
		x = df.iloc[:,0:7]
		y = df.iloc[:,-1]

		x = np.asarray(x)
		y = np.asarray(y)

		x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.4, stratify=y, random_state=0)
		x_train.shape, x_test.shape

		model=SVC()
		model.fit(x_train,y_train)

		y_pred = model.predict(x_test)
		accuracy_score(y_test, y_pred)

		arr = np.array([[jurusan,angkatan,dosenp,kehadiran,tugas,uts,uas]])    
		pred = model.predict(arr)[0]
		return render_template('predict.html', profile=profile, pred=pred)

if __name__ == '__main__':
	app.run(debug=True, port='5000')
