from flask import Flask, jsonify, request
from haversine import haversine, Unit
from controllers.calculations import getList, genCode
from flask_cors import CORS
from jennifer.getProducts import JENgetCleansers, JENgetMoisterizers, JENgetSerums, JENgetSun, JENgetToners
import smtplib
import os
import psycopg2
from psycopg2 import sql
import bcrypt
import jwt
from datetime import datetime

salt = os.environ.get("SALT")
DBNAME = os.environ.get("DBNAME")
DBHOST = os.environ.get("DBHOST")
DBPASS = os.environ.get("DBPASS")
DBUSER = os.environ.get("DBUSER")
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)
CORS(app)

def recentUpdate(USERID):
    connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
    cursor = connection.cursor()
    query = """
        SELECT su.updateat 
        FROM session_updates su
        JOIN sessions sess ON su.sessionID = sess.sessionID
        JOIN users u ON sess.userID = u.userID
        WHERE u.userID = %s
        ORDER BY su.updateat DESC
        LIMIT 1;
    """
    cursor.execute(query, (USERID,))
    data = cursor.fetchone()
    cursor.close()
    return data

def getPosNeg(USERID):
    connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
    cursor = connection.cursor()
    query = """
        SELECT 
            SUM(
                CASE
                    WHEN su.updateType = 0 THEN 1
                    ELSE 0
                END
            ) AS Positive,
            SUM(
                CASE
                    WHEN su.updateType = 1 THEN 1
                    ELSE 0
                END
            ) AS Negative
        FROM session_updates su
        JOIN sessions sess ON su.sessionID = sess.sessionID
        JOIN users u on sess.userID = u.userID
        WHERE u.userID = %s;
    """
    cursor.execute(query, (USERID,))
    data = cursor.fetchone()
    cursor.close()
    return data

def getSessions(USERID):
    connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
    cursor = connection.cursor()
    query = """
        SELECT 
            sess.sessionID,
            sess.createdAt,
            ROUND(EXTRACT(EPOCH FROM MAX(su.updateAt) - sess.createdAt) / 60, 2) AS TotalTimeMinutes,
            SUM(
                CASE 
                    WHEN su.updateType = 0 THEN 1
                    WHEN su.updateType = 1 THEN -1
                    ELSE 0
                END
            ) AS Score
        FROM 
            session_updates su
        JOIN 
            sessions sess ON su.sessionID = sess.sessionID
        JOIN 
            users u ON sess.userID = u.userID
        WHERE 
            u.userID = %s
        GROUP BY 
            sess.sessionID, sess.createdAt
        ORDER BY 
            sess.createdAt DESC
        LIMIT 15;
    """
    cursor.execute(query, (USERID,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    if (data and data != []):
        return data
    raise Exception("No Data")

def userScore(USERID, second):
    try:
        query = """SELECT score FROM users WHERE userid = %s and live = true;"""
        if(second and second == True):
            query = """SELECT score FROM users WHERE userid = %s;"""

        id = str(USERID)
        connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        data = cursor.fetchall()

        if(len(data) != 1):
            raise Exception("User not valid")
        cursor.close()
        connection.close()

        return data[0][0]
    except Exception as e:
        return -50

def update(USERID, updateType):
    try:
        connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
        cursor = connection.cursor()

        query = sql.SQL("""
            DO $$
            DECLARE
                last_update TIMESTAMP;
                most_recent_session_id INT;
                valid_session_id INT;
            BEGIN
                -- Check if the user exists and is live
                IF EXISTS (
                    SELECT 1 FROM users WHERE userID = {user_id} AND live = TRUE
                ) THEN
                    SELECT su.updateAt
                    INTO last_update
                    FROM session_updates su
                    JOIN sessions s ON su.sessionID = s.sessionID
                    WHERE s.userID = {user_id}
                    ORDER BY su.updateAt DESC
                    LIMIT 1;

                    IF last_update IS NULL OR last_update < NOW() - INTERVAL '3 hours' THEN
                        UPDATE sessions
                        SET ongoing = FALSE
                        WHERE userID = {user_id} AND ongoing = TRUE;

                        INSERT INTO sessions(userID)
                        VALUES({user_id})
                        RETURNING sessionID INTO most_recent_session_id;

                        INSERT INTO session_updates(updateType, sessionID)
                        VALUES({update_type}, most_recent_session_id);

                    ELSE
                        SELECT sessionID INTO valid_session_id
                        FROM sessions
                        WHERE userID = {user_id}
                        ORDER BY createdAt DESC
                        LIMIT 1;

                        IF valid_session_id IS NOT NULL THEN
                            INSERT INTO session_updates(updateType, sessionID)
                            VALUES({update_type}, valid_session_id);
                        ELSE
                            INSERT INTO sessions(userID)
                            VALUES({user_id})
                            RETURNING sessionID INTO most_recent_session_id;

                            INSERT INTO session_updates(updateType, sessionID)
                            VALUES({update_type}, most_recent_session_id);
                        END IF;
                    END IF;

                    -- Conditional score update based on updateType
                    IF {update_type} = 0 THEN
                        UPDATE users
                        SET score = CASE
                                        WHEN score < 99 THEN score + 1
                                        ELSE 99
                                    END
                        WHERE userID = {user_id} AND live = TRUE;
                    ELSIF {update_type} = 1 THEN
                        UPDATE users
                        SET score = CASE
                                        WHEN score > 61 THEN score - 1
                                        ELSE 60
                                    END
                        WHERE userID = {user_id} AND live = TRUE;
                    END IF;
                END IF;
            END $$;
        """).format(
            user_id=sql.Literal(USERID),
            update_type=sql.Literal(updateType)
        )


        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        score = userScore(USERID, None)
        return score

    except Exception as e:
        print(f"Error updating score: {e}")
        return -50

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route("/contact", methods=["POST"])
def sendForm():
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        body = request.get_json("info")["info"]

        email = body["email"]
        if not email or "@" not in email or not email.endswith(".com"):
            return jsonify({
                "success": False,
                "msg": "Invalid Email"
            }), 200

        subject = body["subject"]
        if not subject:
            return jsonify({
                "success": False,
                "msg": "Invalid Subject"
            }), 200

        message = body["message"]
        if not message:
            return jsonify({
                "success": False,
                "msg": "Invalid Message"
            }), 200

        newmessage = "Mapapp" + "\n" + email + "\n" + subject + "\n" + message + "\n\n" + str(ip)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("shadman2354@gmail.com", "xdhi sneq rdpa xgpl")
        server.sendmail("shadman.sohel2354@gmail.com","shadman.sohel04@gmail.com",newmessage)
        server.quit()

        return jsonify({
            "success": True,
            "msg": "Form processed successfully"
        })

    except Exception as e:
        print(str(e)) 
        return jsonify({
            "success": False,
            "msg": "Something went wrong, please try again later"
        }), 500

@app.route('/api/data', methods=["GET"])
def getData():
    try:
        address = request.args.get("address")
        schoolChoice = request.args.get("schoolChoice")
        data = getList(address= address, schoolChoice= schoolChoice)
        if data != None:
            return jsonify({
                "success": True,
                "data": data
            })
        else:
            return jsonify({
                "success": False
            })
        
    except:
        return jsonify({
            "success": False,
            "msg": "Unable to getData"
        })
    
# JENNIFER

@app.route("/JENNIFER/contact", methods=["POST"])
def postContact():
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        body = request.get_json()
        email = body["email"]
        if not email or "@" not in email or not email.endswith(".com"):
            raise NameError("Please enter a proper email")
        
        firstname = body["firstname"]
        if not firstname:
            raise NameError("Please enter first name")
        
        lastname = body["lastname"]
        if not lastname:
            raise NameError("Please enter last name")
        
        msg = body["msg"]
        if not msg:
            raise NameError("please enter message")
        
        phone = body["phone"]
        if not phone:
            raise NameError("Please enter phone number")
        
        emailBody = "SkinMatch Inquiry" + "\n" + email + "\n" + firstname + " " + lastname + "\n" + phone + "\n" + msg + "\n\n" + str(ip)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("shadman2354@gmail.com", "xdhi sneq rdpa xgpl")
        server.sendmail("shadman2354@gmail.com" ,"jennierlay@gmail.com", emailBody)
        server.quit()
        print("aaa")

        return jsonify({
            "success": True,
            "msg": "Form Submitted Sent"
        })

    except Exception as e:
        print(str(e))
        return jsonify({
            "success": False,
            "msg": str(e)
        })

@app.route("/JENNIFER/home", methods=["GET"])
def JENgetData():
    try:
        age = request.args.get("age")
        skinConcern1 = request.args.get("skinConcern1")
        skinConcern2 = request.args.get("skinConcern2")
        skinConcern3 = request.args.get("skinConcern3")

        skinType = request.args.get("skinType")
        skinConcern = []

        if skinConcern1:
            skinConcern.append(skinConcern1)
        
        if skinConcern2:
            skinConcern.append(skinConcern2)

        if skinConcern3:
            skinConcern.append(skinConcern3)
        
        if len(skinConcern) == 0:
            raise NameError("no concerns found")


        elif (skinType == None):
            raise NameError("skintype not found")

        elif not age or int(age) <= 8:
            raise NameError("no age found")

        cleanserCount = JENgetCleansers(age, skinConcern, skinType)
        moisterizerCount = JENgetMoisterizers(age, skinConcern, skinType)
        tonerCount = JENgetToners(age, skinConcern, skinType)
        serumCount = JENgetSerums(age, skinConcern, skinType)
        sunCount = JENgetSun(age, skinConcern, skinType)

        return jsonify({
            "success": True,
            "data": {
                "moisterizers": moisterizerCount,
                "cleansers": cleanserCount,
                "toners": tonerCount,
                "serums": serumCount,
                "sunscreens": sunCount
            }
        })

    except Exception as e:
        print(str(e))

        return jsonify({
            "success": False,
            "msg": str(e)
        })

# POMO APP

@app.route("/ESP8266/createAccount", methods=["POST"])
def espCreateAccount():
    try:
        body = request.get_json()
        
        email = body["email"]
        password = body["password"]
        firstname = body["firstName"]
        lastname = body["lastName"]
        
        if("@" not in email or (".com" or ".ca") not in email):
            raise Exception("Invalid email")
        if(len(password) < 4):
            raise Exception("Password too short (must be at least 4 characters)")

        #SWITCH THESE FOR THE ENV VARIABLES
        connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
        cursor = connection.cursor()
        cursor.execute(f"SELECT userID FROM users WHERE email = '{email}';")  
        users = cursor.fetchall()
        if(len(users) > 0):
            raise Exception("User already exists")

        passBytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(passBytes, salt.encode('utf-8')).decode('utf-8')
        
        while True:
            code = genCode()
            cursor.execute(f"SELECT email FROM users WHERE userID = '{code}';")
            if(len(cursor.fetchall()) == 0):
                break

        cursor.execute("""
            INSERT INTO users (firstName, lastName, email, password, userID)
            VALUES (%s, %s, %s, %s, %s);
        """, (firstname, lastname, email, hashed, code))

        connection.commit()
        connection.close()

        return jsonify({
            "success": True,
            "msg": "Registered user"
        }), 201

    except Exception as e:
        print(str(e))
        return jsonify({
            "success": False,
            "msg": str(e)
        }), 406

@app.route("/ESP8266/loginAccount", methods=["POST"])
def espLoginAccount():
    try:
        body = request.get_json()
        email = body["email"]
        password = body["password"]
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

        connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
        cursor = connection.cursor()
        
        cursor.execute(
        """
            SELECT userID, firstName, lastName, email, score FROM users
            WHERE email = %s
            AND password = %s;
        """, (email, hashed))

        users = cursor.fetchall()
        length = len(users)
        if(length > 1):
            raise Exception("Error please try again later")
        elif(length == 0):
            raise Exception("User not found")
        elif(length != 1):
            raise Exception("Error unknown user")
        
        payload = {            
            "userid": users[0][0],
            "email": users[0][3],
            "password": hashed
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "success": True,
            "msg": "Login Successfull",
            "user": {
                "userid": users[0][0],
                "firstName": users[0][1],
                "lastName": users[0][2],
                "email": users[0][3],
                "score": users[0][4]
            },
            "token": token
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "msg": str(e)
        }), 400

@app.route("/ESP8266/tokenAuth", methods=["POST"])
def espTokenAccount():
    try:
        body = request.get_json()
        token = body["token"]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload["email"]
        hashed = payload["password"]
        connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
        cursor = connection.cursor()
        
        cursor.execute(
        """
            SELECT userID, firstName, lastName, email, score FROM users
            WHERE email = %s
            AND password = %s;
        """, (email, hashed))

        users = cursor.fetchall()
        length = len(users)
        if(length > 1):
            raise Exception("Error please try again later")
        elif(length == 0):
            raise Exception("User not found")
        elif(length != 1):
            raise Exception("Error unknown user")

        return jsonify({
            "success": True
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "msg": str(e)
        }), 400

@app.route("/ESP8266/userCode/<USERID>", methods=["GET"])
def espGetUserCode(USERID):
    try:
        connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
        cursor = connection.cursor()
        cursor.execute(f"SELECT email FROM users WHERE userID = '{USERID}';")
        res = cursor.fetchall()
        if(not res and len(res) != 1):
            raise Exception("NOPE")
        
        return jsonify({
            "codeWork": True
    })

    except Exception as e:
        return jsonify({
            "codeWork": False
        })

@app.route("/ESP8266/getUserScore/<USERID>", methods=["GET"])
def espGetUserScore(USERID):
    try:
        score = userScore(USERID, None)
        
        return jsonify({
            "success": True,
            "score": score
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "err": str(e)
        })

@app.route("/ESP8266/getScore/<TOKEN>", methods=["GET"])
def espGetScoreMobile(TOKEN):
    try:
        USERID = jwt.decode(TOKEN, SECRET_KEY, algorithms=["HS256"])["userid"]

        score = userScore(USERID, True)
        pos = getPosNeg(USERID)
        recent = recentUpdate(USERID)[0]
        recent = datetime.fromisoformat(str(recent))
        recent = (datetime.now() - recent)

        if(recent.days == 0):
            recent = "Today"
        elif(recent.days < 30):
            recent = str(recent.days) + " days"
        elif(recent >= 30):
            recent = "1+ months"

        posScore = pos[0]/(pos[1] + pos[0])*100
        
        return jsonify({
            "success": True,
            "score": score,
            "posNeg": round(posScore, 0),
            "recent": recent
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "err": str(e)
        })

@app.route("/ESP8266/updateHurt/<USERID>", methods=["GET"])
def espUpdateUserScoreHurt(USERID):
    try:
        
        score = update(USERID, 1)
        
        return jsonify({
            "success": True,
            "score": score
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "err": str(e)
        })

@app.route("/ESP8266/updateGood/<USERID>", methods=["GET"])
def espUpdateUserScoreGood(USERID):
    try:
        score = update(USERID, 0)
        
        return jsonify({
            "success": True,
            "score": score
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "err": str(e)
        })

@app.route("/ESP8266/sessionStats/", methods=["GET"])
def espGetSessions():
    try:
        TOKEN = request.headers.get("Authorization")
        if not TOKEN:
            raise Exception("NO AUTH")
        
        USERID = jwt.decode(TOKEN, SECRET_KEY, algorithms=["HS256"])["userid"]
        sessions = getSessions(USERID)

        return jsonify({
            "success": True,
            "sessions": sessions
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "err": str(e)
        })

@app.route("/ESP8266/oneSessionStat/<SESSIONID>", methods=["GET"])
def espGetOneSession(SESSIONID):
    try:        
        connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
        cursor = connection.cursor()
        query = """ 
            select updateType, updateat from session_updates
            where sessionID = %s;
        """
        cursor.execute(query, (SESSIONID,))
        data = cursor.fetchall()
        cursor.close()

        return jsonify({
            "success": True,
            "updates": data
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
        })

@app.route("/ESP8266/activate", methods=["PUT"])
def espActivate():
    try:
        setter = request.get_json()["toggle"]
        token = request.headers.get("Authorization")
        USERID = jwt.decode(token, SECRET_KEY, algorithms="HS256")["userid"]
        connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
        cursor = connection.cursor()
        query = """ 
            UPDATE users
            SET live = %s
            WHERE userid IN (
                SELECT userid
                WHERE userid = %s
                LIMIT 1
            );
        """
        cursor.execute(query, (setter, USERID,))
        connection.commit()
        cursor.close()

        return jsonify({
            "success": True
        })
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "success": False,
        })

@app.route("/ESP8266/getState", methods=["GET"])
def espGetState():
    try:
        token = request.headers.get("Authorization")
        USERID = jwt.decode(token, SECRET_KEY, algorithms="HS256")["userid"]
        connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
        cursor = connection.cursor()
        query = """ 
            SELECT live FROM users
            WHERE userid = %s
            LIMIT 1;;
        """
        cursor.execute(query, (USERID,))
        ret = cursor.fetchone()
        cursor.close()

        return jsonify({
            "success": True,
            "state": ret[0]
        })
    
    except Exception as e:
        print(str(e))
        return jsonify({
            "success": False,
        })

# DONT WANT TO GET RID OF YET BC I WANT NOTIFICATIONS

# expo_tokens = []
# @app.route('/ESP8266/register-token', methods=['POST'])
# def register_token():
#     try:
#         TOKEN = request.headers.get("Authorization")
#         USERID = jwt.decode(TOKEN, SECRET_KEY, algorithms=["HS256"])["userid"]
#         connection = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, port=5432)
#         cursor = connection.cursor()
#         cursor.execute("SELECT live FROM users WHERE userid = %s", (USERID,))
#         data = cursor.fetchall()
#         if(len(data) != 1):
#             raise Exception("Invalid credentials")

#         data = request.get_json()
#         token = data["token"]
#         if token:
#             expo_tokens.append(token)
        
#         print(expo_tokens)
#         return jsonify({
#             'success': True
#         })
    
#     except Exception as e:
#         print(str(e))
#         return jsonify({
#             'success': False, 
#             'error': 'No token provided'
#         }), 400

if __name__ == "__main__":
    print(os.getenv("PORT"))
    port = os.getenv("PORT") or 3000
    print(f"running on port {port}")
    app.run(debug=True, port=port)
