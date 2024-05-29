from fastapi import APIRouter,HTTPException,responses
from models import *
from mongo import *
import hashlib
import random
import smtplib
from email.message import EmailMessage
import uuid
from jwt_auth import *

router = APIRouter(prefix='/api/users')


@router.post("/register", tags=['user'])
async def user_register(data: register_params):
    try:
        redis_client = await redisConnection()
        temp_mail = redis_client.setex(f"{data.email}_email", 3000, data.email)
        temp_username = redis_client.setex(f"{data.email}_username", 3000, data.username)
        hash_temp_password = hashlib.md5(data.password.encode('utf-8')).hexdigest()
        temp_password = redis_client.setex(f"{data.email}_password", 3000, hash_temp_password)
        
        try:
            collection = await dbconnect('user_auth', 'users')
            res = collection.find_one({"email": data.email})
            if res:
                return {"msg": "User already exists"}
        except Exception as e:
            print(f"Database connection error: {str(e)}")
            return {"msg": "Failed to connect to database"}

        try:
            await send_otp(redis_client.get(f"{data.email}_email").decode())
        except Exception as e:
            print(f"Error sending OTP: {str(e)}")
            return {"msg": "Failed to send OTP"}

        return {"msg": "Details stored in Redis"}
    except Exception as e:
        print(f"Redis connection error: {str(e)}")
        return {"msg": "Failed to connect to Redis"}
    finally:
        if redis_client:
            redis_client.close()



@router.post("/send_otp", tags=["OTP"])
async def send_otp(request: otp_email):
    try:
        email = request
        print("send_mail_data", email)
        otp_generated = random.randint(10000, 99999)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        s.login("akhileswarreddymp@gmail.com", "xodgydwslhywjare")

        message = EmailMessage()
        message["From"] = "akhileswarreddymp@gmail.com"
        message["To"] = email
        message["Subject"] = "Verification code to change password"
        message.set_content(f"Your verification code is {otp_generated}")

        s.send_message(message)
        print("akhileswarreddymp@gmail.com", email, message)
        print("Mail sent successfully")
        s.quit()
        await redis_store(otp_generated, email)
        return {"msg": "Mail sent successfully"}
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {str(e)}")
        return {"msg": "Failed to send email"}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"msg": "An error occurred while sending OTP"}


async def redis_store(otp, email):
    redis_client = None
    try:
        redis_client = await redisConnection()
        key = f"{email}_otp"
        value = otp
        ttl = 3000
        redis_client.setex(key, ttl, value)
        saved_otp = redis_client.get(key)
        if saved_otp:
            print("OTP saved==>", saved_otp.decode())
        else:
            print("Failed to save OTP in Redis")
    except Exception as e:
        print(f"An error occurred while storing OTP in Redis: {str(e)}")
    finally:
        if redis_client:
            redis_client.close()



@router.post('/verify_otp', tags=['OTP'])
async def verifyOtp(request: only_otp):
    data = request
    print("otpdata===>", data.otp)
    try:
        redis_client = await redisConnection()
        stored_otp = redis_client.get(f"{data.email}_otp")
        if stored_otp is None:
            raise HTTPException(status_code=404, detail="OTP not found")
        stored_otp = stored_otp.decode()
        print("stored_otp=====>", stored_otp)

        email_id = redis_client.get(f"{data.email}_email")
        user_name = redis_client.get(f"{data.email}_username")
        user_password = redis_client.get(f"{data.email}_password")

        if None in (email_id, user_name, user_password):
            raise HTTPException(status_code=404, detail="User information is incomplete")

        email_id = email_id.decode()
        user_name = user_name.decode()
        user_password = user_password.decode()

        if data.otp == stored_otp:
            collection = await dbconnect('user_auth', 'users')
            user_data = {
                "email": email_id,
                "name": user_name,
                "password": user_password
            }
            add_user = collection.insert_one(user_data)
            print("add_user===>", add_user)
            print("user created successfully")
            return {"msg": "user created successfully"}
        else:
            raise HTTPException(status_code=401, detail="Invalid OTP")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        if redis_client:
            redis_client.close()

async def check_user(data):
    try:
        password = hashlib.md5(data.password.encode('utf-8')).hexdigest()
        collection = await dbconnect('user_auth', 'users')
        result = collection.find_one({"email": data.email})
        if result and result.get("email") == data.email and result.get("password") == password:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred while checking user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")




@router.post('/login', tags=['Authentication'])
async def Userlogin(data: login_params):
    cookie_name = "access_token"
    try:
        if await check_user(data):
            cookie_id = str(uuid.uuid4())
            access_token = signJWT(data.email)
            response = responses.JSONResponse({"status": "Logged in Successfully", "access_token": access_token}, status_code=200)
            response.set_cookie(cookie_name, cookie_id, path="/", expires=3600, samesite="Lax", secure=True)
            return response
        else:
            raise HTTPException(status_code=401, detail="Wrong Credentials received")
    except Exception as e:
        print(f"An error occurred during login: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")



@router.post('/forgot-password', tags=['Authentication'])
async def forgotPassword(data: forgotPassword_params):
    try:
        redis_client = await redisConnection()
        stored_otp = redis_client.get(f"{data.email}_otp")
        if stored_otp is None:
            raise HTTPException(status_code=404, detail="OTP not found or expired")
        
        if stored_otp.decode() == data.otp:
            if data.newpassword == data.confirm_Password:
                try:
                    collection = await dbconnect('user_auth', 'users')
                    result = collection.find_one({"email": data.email})
                    if result is None:
                        raise HTTPException(status_code=404, detail="User not found")
                    
                    filter = {"_id": result.get("_id")}
                    new_password = hashlib.md5(data.newpassword.encode('utf-8')).hexdigest()
                    update_field = collection.update_one(filter, {'$set': {"password": new_password}})
                    return {"msg": "Password Updated Successfully"}
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
            else:
                raise HTTPException(status_code=401, detail="New Password and re-entered password do not match")
        else:
            raise HTTPException(status_code=401, detail="Incorrect OTP")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    finally:
        if redis_client:
            redis_client.close()


@router.post('/reset-password', tags=['Authentication'])
async def resetPassword(data: resetPassword_params):
    try:
        collection = await dbconnect('user_auth', 'users')
        result = collection.find_one({"email": data.email})
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        oldPassword = result.get("password")
        user_entered_password = hashlib.md5(data.old_password.encode('utf-8')).hexdigest()
        
        if oldPassword != user_entered_password:
            raise HTTPException(status_code=401, detail="Received incorrect password")
        
        if data.new_password != data.confirm_password:
            raise HTTPException(status_code=401, detail="New Password and re-entered password do not match")
        
        new_pass = hashlib.md5(data.new_password.encode('utf-8')).hexdigest()
        filter = {"_id": result.get("_id")}
        update_field = collection.update_one(filter, {'$set': {"password": new_pass}})
        if update_field.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to update password")
        
        return {"msg": "Password Updated Successfully"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"An error occurred during password reset: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")
    

