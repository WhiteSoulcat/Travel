from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import requests
import random
import math

OPENWEATHER_API_KEY = "8ac59134c80b6ba9b1ebbed5c8b312d8"
LAT_CHIANGMAI = 18.7883
LON_CHIANGMAI = 98.9853

HOTELS = [
    {"name": "โรงแรมเชียงใหม่ฮิลล์", "location": "18.7971,98.9636"},
    {"name": "โรงแรมฟูราม่า เชียงใหม่", "location": "18.7996,98.9629"},
    {"name": "โรงแรมยู นิมมาน เชียงใหม่", "location": "18.8005,98.9677"},
    {"name": "โรงแรมเชียงใหม่ออร์คิด", "location": "18.7952,98.9686"},
    {"name": "โรงแรมโลตัส ปางสวนแก้ว", "location": "18.7955,98.9685"},
]

PLACES = [
    # --------- ธรรมชาติ ---------
    {"name": "ห้วยตึงเฒ่า", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 20, "cost_thai_adult": 20, "cost_thai_child": 20, "cost_thai_senior": 20,
     "cost_foreigner": 20, "cost_foreigner_adult": 20, "cost_foreigner_child": 20, "cost_foreigner_senior": 20,
     "open": "07:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.86849483,98.94027689", "district": "แม่ริม", "rating": 4.4},

    {"name": "อ่างแก้ว มช.", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "05:00", "close": "22:00", "day_close": "-", "recommend_time": 60,
     "location": "18.80612291,98.95089494", "district": "เมือง", "rating": 4.7},

    {"name": "สวนพฤกษศาสตร์สมเด็จพระนางเจ้าสิริกิติ์", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 40, "cost_thai_adult": 40, "cost_thai_child": 20, "cost_thai_senior": 40,
     "cost_foreigner": 100, "cost_foreigner_adult": 100, "cost_foreigner_child": 50, "cost_foreigner_senior": 100,
     "open": "08:30", "close": "16:30", "day_close": "-", "recommend_time": 60,
     "location": "18.88823753,98.86185229", "district": "แม่ริม", "rating": 4.6},

    {"name": "ปางช้างแม่สา", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 100, "cost_thai_adult": 100, "cost_thai_child": 100, "cost_thai_senior": 100,
     "cost_foreigner": 300, "cost_foreigner_adult": 300, "cost_foreigner_child": 300, "cost_foreigner_senior": 300,
     "open": "08:30", "close": "16:00", "day_close": "-", "recommend_time": 60,
     "location": "18.89999556,98.87562347", "district": "แม่ริม", "rating": 4.2},

    {"name": "น้ำตกแม่สา", "category": "ธรรมชาติ", "type": "outdoor",
      "cost": 20, "cost_thai_adult": 20, "cost_thai_child": 10, "cost_thai_senior": 20,
      "cost_foreigner": 100, "cost_foreigner_adult": 100, "cost_foreigner_child": 50, "cost_foreigner_senior": 100,
      "open": "08:30", "close": "16:30", "day_close": "-", "recommend_time": 60,
      "location": "18.90645968,98.89719978", "district": "แม่ริม", "rating": 4.4},

    {"name": "สวนสัตว์เชียงใหม่", "category": "ธรรมชาติ", "type": "indoor",
     "cost": 130, "cost_thai_adult": 130, "cost_thai_child": 40, "cost_thai_senior": 130,
     "cost_foreigner": 350, "cost_foreigner_adult": 350, "cost_foreigner_child": 120, "cost_foreigner_senior": 350,
     "open": "08:00", "close": "17:00", "day_close": "-", "recommend_time": 60,
     "location": "18.81066322,98.94795790", "district": "เมือง", "rating": 3.9},

    {"name": "Tiger Kingdom", "category": "ธรรมชาติ", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "09:00", "close": "17:00", "day_close": "-", "recommend_time": 60,
     "location": "18.92481703,98.93202634", "district": "แม่ริม", "rating": 4.0,
     "price_note": "ราคาเป็นไปตามแพ็กเกจ"},

    {"name": "Elephant POOPOOPAPER Park Chiang Mai", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 150, "cost_thai_adult": 150, "cost_thai_child": 150, "cost_thai_senior": 150,
     "cost_foreigner": 150, "cost_foreigner_adult": 150, "cost_foreigner_child": 150, "cost_foreigner_senior": 150,
     "open": "08:30", "close": "17:15", "day_close": "-", "recommend_time": 60,
     "location": "18.92575681,98.93153906", "district": "แม่ริม", "rating": 4.5},

    {"name": "สวนสัตว์แมลงสยาม", "category": "ธรรมชาติ", "type": "indoor",
     "cost": 100, "cost_thai_adult": 100, "cost_thai_child": 60, "cost_thai_senior": 100,
     "cost_foreigner": 200, "cost_foreigner_adult": 200, "cost_foreigner_child": 150, "cost_foreigner_senior": 200,
     "open": "09:00", "close": "17:00", "day_close": "-", "recommend_time": 60,
     "location": "18.91822404,98.90850500", "district": "แม่ริม", "rating": 4.5},

    {"name": "Pongyang Jungle Coaster Zipline", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:30", "close": "17:00", "day_close": "-", "recommend_time": 60,
     "location": "18.91714823,98.82146999", "district": "แม่ริม", "rating": 4.4,
     "price_note": "ราคาเป็นไปตามแพ็กเกจ"},

    {"name": "น้ำตกมณฑาธาร", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 20, "cost_thai_adult": 20, "cost_thai_child": 10, "cost_thai_senior": 20,
     "cost_foreigner": 100, "cost_foreigner_adult": 100, "cost_foreigner_child": 50, "cost_foreigner_senior": 100,
     "open": "08:00", "close": "16:30", "day_close": "-", "recommend_time": 60,
     "location": "18.82271026,98.91733075", "district": "เมือง", "rating": 4.4},

    {"name": "อุทยานแห่งชาติสุเทพ-ปุย", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 20, "cost_thai_adult": 20, "cost_thai_child": 10, "cost_thai_senior": 20,
     "cost_foreigner": 100, "cost_foreigner_adult": 100, "cost_foreigner_child": 50, "cost_foreigner_senior": 100,
     "open": "08:30", "close": "16:30", "day_close": "-", "recommend_time": 60,
     "location": "18.80720832,98.91609596", "district": "เมือง", "rating": 4.5},

    {"name": "เส้นทางเดินป่าดอยสุเทพ (วัดผาลาด)", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 20, "cost_thai_adult": 20, "cost_thai_child": 10, "cost_thai_senior": 20,
     "cost_foreigner": 100, "cost_foreigner_adult": 100, "cost_foreigner_child": 50, "cost_foreigner_senior": 100,
     "open": "00:00", "close": "23:59", "day_close": "-", "recommend_time": 60,
     "location": "18.79958763,98.93214330", "district": "เมือง", "rating": 4.2},

    {"name": "สวนสาธารณะ อบจ.เชียงใหม่", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "00:00", "close": "23:59", "day_close": "-", "recommend_time": 60,
     "location": "18.83218611,98.96746293", "district": "เมือง", "rating": 4.7},

    {"name": "ช้างทองเฮอริเทจพาร์ค", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 150, "cost_thai_adult": 150, "cost_thai_child": 150, "cost_thai_senior": 150,
     "cost_foreigner": 250, "cost_foreigner_adult": 250, "cost_foreigner_child": 250, "cost_foreigner_senior": 250,
     "open": "09:00", "close": "19:00", "day_close": "-", "recommend_time": 60,
     "location": "18.86199204,98.99234915", "district": "เมือง", "rating": 4.5},

    {"name": "บ้านแกะแม่ขิ", "category": "ธรรมชาติ", "type": "outdoor",
     "cost": 100, "cost_thai_adult": 100, "cost_thai_child": 100, "cost_thai_senior": 100,
     "cost_foreigner": 100, "cost_foreigner_adult": 100, "cost_foreigner_child": 100, "cost_foreigner_senior": 100,
     "open": "07:30", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.95544637,98.80066768", "district": "แม่ริม", "rating": 4.6},

    {"name": "เชียงใหม่ไนท์ซาฟารี", "category": "ธรรมชาติ", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "11:00", "close": "22:00", "day_close": "-", "recommend_time": 60,
     "location": "18.74257382,98.91723290", "district": "เมือง", "rating": 4.2,
     "price_note": "ราคาเป็นไปตามแพ็กเกจ"},

    {"name": "อุทยานหลวงราชพฤกษ์", "category": "ธรรมชาติ", "type": "indoor",
     "cost": 100, "cost_thai_adult": 100, "cost_thai_child": 50, "cost_thai_senior": 100,
     "cost_foreigner": 200, "cost_foreigner_adult": 200, "cost_foreigner_child": 100, "cost_foreigner_senior": 200,
     "open": "08:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.74487301,98.92798398", "district": "เมือง", "rating": 4.5},
  {"name": "Merino Sheep Farm Chiang Mai", "category": "ธรรมชาติ", "type": "indoor",
     "cost": 100, "cost_thai_adult": 100, "cost_thai_child": 100, "cost_thai_senior": 100,
     "cost_foreigner": 100, "cost_foreigner_adult": 100, "cost_foreigner_child": 100, "cost_foreigner_senior": 100,
     "open": "08:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.89273441,98.8557597", "district": "แม่ริม", "rating": 4.4},
       # --------- วัฒนธรรม ---------
    {"name": "วัดป่าแดด", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:30", "close": "17:00", "day_close": "-", "recommend_time": 60,
     "location": "18.75192743,98.98600131", "district": "เมือง", "rating": 4.7},

    {"name": "วัดอุโมงค์", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "04:00", "close": "20:00", "day_close": "-", "recommend_time": 60,
     "location": "18.78325112,98.95208180", "district": "เมือง", "rating": 4.6},

    {"name": "วัดผาลาด (สกิทาคามี)", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "06:00", "close": "17:30", "day_close": "-", "recommend_time": 60,
     "location": "18.80004563,98.93416733", "district": "เมือง", "rating": 4.8},

    {"name": "วัดพระธาตุดอยคำ", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "06:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.75968231,98.91869801", "district": "เมือง", "rating": 4.7},

    {"name": "วัดป่าแดด", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:30", "close": "17:00", "day_close": "-", "recommend_time": 60,
     "location": "18.75181567,98.98603349", "district": "เมือง", "rating": 4.7},

    {"name": "วัดพระสิงห์ วรมหาวิหาร", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "05:30", "close": "19:30", "day_close": "-", "recommend_time": 60,
     "location": "18.78861575,98.98214929", "district": "เมือง", "rating": 4.7},

    {"name": "วัดเชียงมั่น", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "07:00", "close": "19:00", "day_close": "-", "recommend_time": 60,
     "location": "18.79393448,98.98927566", "district": "เมือง", "rating": 4.6},

    {"name": "พิพิธภัณฑ์พื้นถิ่นล้านนา", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 20, "cost_thai_adult": 20, "cost_thai_child": 10, "cost_thai_senior": 20,
     "cost_foreigner": 90, "cost_foreigner_adult": 90, "cost_foreigner_child": 40, "cost_foreigner_senior": 90,
     "open": "08:30", "close": "16:30", "day_close": "Monday,Tuesday", "recommend_time": 60,
     "location": "18.79038914,98.98842574", "district": "เมือง", "rating": 4.8},

    {"name": "พิพิธภัณฑสถานแห่งชาติ เชียงใหม่", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 20, "cost_thai_adult": 20, "cost_thai_child": 20, "cost_thai_senior": 20,
     "cost_foreigner": 200, "cost_foreigner_adult": 200, "cost_foreigner_child": 200, "cost_foreigner_senior": 200,
     "open": "09:00", "close": "16:00", "day_close": "Monday,Tuesday", "recommend_time": 60,
     "location": "18.81124305,98.97646252", "district": "เมือง", "rating": 4.2},

    {"name": "พิพิธภัณฑ์พระตำหนักดาราภิรมย์", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 20, "cost_thai_adult": 20, "cost_thai_child": 20, "cost_thai_senior": 20,
     "cost_foreigner": 20, "cost_foreigner_adult": 20, "cost_foreigner_child": 20, "cost_foreigner_senior": 20,
     "open": "09:00", "close": "17:00", "day_close": "Monday,Tuesday", "recommend_time": 60,
     "location": "18.91305768,98.94256433", "district": "แม่ริม", "rating": 4.7},

    {"name": "วัดป่าดาราภิรมย์", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "06:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.91087395,98.94136742", "district": "แม่ริม", "rating": 4.8},

    {"name": "ประตูท่าแพ", "category": "วัฒนธรรม", "type": "outdoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "00:00", "close": "23:59", "day_close": "-", "recommend_time": 60,
     "location": "18.78791397,98.99334218", "district": "เมือง", "rating": 4.3},

    {"name": "ถนนคนเดินวัวลาย", "category": "วัฒนธรรม", "type": "outdoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "18:00", "close": "23:00", "day_close": "Monday,Tuesday,Wednesday,Thursday,Friday,Sunday", "recommend_time": 60,
     "location": "18.78109836,98.98776256", "district": "เมือง", "rating": 4.5},

    {"name": "ถนนคนเดินท่าแพ", "category": "วัฒนธรรม", "type": "outdoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "17:00", "close": "22:30", "day_close": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday", "recommend_time": 60,
     "location": "18.78791397,98.99334218", "district": "เมือง", "rating": 4.5},

    {"name": "วัดโลกโมฬี", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "06:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.79615634,98.98273380", "district": "เมือง", "rating": 4.7},

    {"name": "วัดอินทราวาส(วัดต้นเกว๋น)", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "06:00", "close": "17:00", "day_close": "-", "recommend_time": 60,
     "location": "18.72286331,98.92599004", "district": "เมือง", "rating": 4.8},

    {"name": "หมู่บ้านม้งดอยปุย", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:00", "close": "17:00", "day_close": "-", "recommend_time": 60,
     "location": "18.81668639,98.88351018", "district": "เมือง", "rating": 4.2},

    {"name": "ตลาดวโรรส", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "06:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.79011348,99.00139873", "district": "เมือง", "rating": 4.4},

    {"name": "วัดเจดีย์หลวงวรวิหาร", "category": "วัฒนธรรม", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "05:00", "close": "22:30", "day_close": "-", "recommend_time": 60,
     "location": "18.78715213,98.98691836", "district": "เมือง", "rating": 4.7},
         # --------- สร้างสรรค์ ---------
    {"name": "The Baristro x Ping River", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.81601271,99.00025561", "district": "เมือง", "rating": 4.6},

    {"name": "บ้านข้างวัด", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "10:00", "close": "18:00", "day_close": "Monday", "recommend_time": 60,
     "location": "18.77656939,98.94885188", "district": "เมือง", "rating": 4.5},

    {"name": "ลานดิน", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:00", "close": "20:00", "day_close": "-", "recommend_time": 60,
     "location": "18.77463208,98.94671635", "district": "เมือง", "rating": 4.4},

    {"name": "วันนิมมาน", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "11:00", "close": "22:00", "day_close": "-", "recommend_time": 60,
     "location": "18.80010693,98.96748243", "district": "เมือง", "rating": 4.5},

    {"name": "Arte Café", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "09:00", "close": "17:00", "day_close": "Thursday", "recommend_time": 60,
     "location": "18.81080089,98.96705292", "district": "เมือง", "rating": 4.7},

    {"name": "Thong urai & Paw Made Painting", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:30", "close": "17:00", "day_close": "-", "recommend_time": 60,
     "location": "18.78522662,98.96968804", "district": "เมือง", "rating": 4.9},

    {"name": "fringe.th", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:30", "close": "00:00", "day_close": "-", "recommend_time": 60,
     "location": "18.79429360,99.00162522", "district": "เมือง", "rating": 4.6},

    {"name": "graph contemporary", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "09:00", "close": "17:00", "day_close": "-", "recommend_time": 60,
     "location": "18.78723317,99.00877618", "district": "เมือง", "rating": 4.5},

    {"name": "early owls", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "09:00", "close": "18:30", "day_close": "Wednesday", "recommend_time": 60,
     "location": "18.80598327,98.98925987", "district": "เมือง", "rating": 4.6},

    {"name": "enough for life", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:30", "close": "17:00", "day_close": "-", "recommend_time": 60,
     "location": "18.77297178,98.94898242", "district": "เมือง", "rating": 4.5},

    {"name": "Brewginning coffee", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "07:00", "close": "19:00", "day_close": "-", "recommend_time": 60,
     "location": "18.79047603,98.99477125", "district": "เมือง", "rating": 4.6},

    {"name": "จริงใจมาร์เก็ต เชียงใหม่", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:00", "close": "10:00", "day_close": "Monday,Tuesday,Wednesday,Thursday,Friday", "recommend_time": 60,
     "location": "18.80613674,98.99566006", "district": "เมือง", "rating": 4.5},

    {"name": "Chic Ruedoo", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:00", "close": "17:00", "day_close": "Wednesday", "recommend_time": 60,
     "location": "18.76504895,98.99906774", "district": "เมือง", "rating": 4.8},

    {"name": "99 Villa café", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "09:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.76757046,98.93838687", "district": "เมือง", "rating": 4.9},

    {"name": "The Baristro Asian Style", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.79025261,98.95170775", "district": "เมือง", "rating": 4.7},

    {"name": "Fernpresso at lake", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "07:45", "close": "17:15", "day_close": "-", "recommend_time": 60,
     "location": "18.76167876,98.93495016", "district": "เมือง", "rating": 4.6},

    {"name": "Forest Bake", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:30", "close": "17:00", "day_close": "Wednesday", "recommend_time": 60,
     "location": "18.79245894,99.00482539", "district": "เมือง", "rating": 4.2},

    {"name": "Think Park", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "09:00", "close": "00:00", "day_close": "-", "recommend_time": 60,
     "location": "18.80156176,98.96761281", "district": "เมือง", "rating": 4.3},

    {"name": "More Space", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "17:00", "close": "00:00", "day_close": "Monday,Friday,Saturday,Sunday", "recommend_time": 60,
     "location": "18.79473248,98.96408482", "district": "เมือง", "rating": 4.3},

    {"name": "Neighborhood Community", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "12:00", "close": "00:00", "day_close": "-", "recommend_time": 60,
     "location": "18.79033704,98.99418875", "district": "เมือง", "rating": 4.7},

    {"name": "Mori Natural farm", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "08:00", "close": "22:00", "day_close": "Tuesday,Wednesday", "recommend_time": 60,
     "location": "18.86722629,98.8313452", "district": "แม่ริม", "rating": 4.4},

    {"name": "WTF coffee Camp", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "09:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.87365129,98.81335585", "district": "แม่ริม", "rating": 4.5},

      {"name": "Fleur Café & Eatery", "category": "สร้างสรรค์", "type": "indoor",
     "cost": 0, "cost_thai_adult": 0, "cost_thai_child": 0, "cost_thai_senior": 0,
     "cost_foreigner": 0, "cost_foreigner_adult": 0, "cost_foreigner_child": 0, "cost_foreigner_senior": 0,
     "open": "09:00", "close": "18:00", "day_close": "-", "recommend_time": 60,
     "location": "18.90720065,98.90717316", "district": "แม่ริม", "rating": 4.7},
]

def get_place_cost(place, visitor_type, subtype=None):
    """คำนวณค่าใช้จ่ายของสถานที่ตามประเภทและกลุ่มของนักท่องเที่ยว"""
    if visitor_type == "ไทย":
        if subtype == "ผู้ใหญ่":
            return place.get("cost_thai_adult", place.get("cost", 0))
        elif subtype == "เด็ก":
            return place.get("cost_thai_child", place.get("cost", 0))
        elif subtype == "ผู้สูงวัย":
            return place.get("cost_thai_senior", place.get("cost", 0))
        else:
            return place.get("cost", 0)
    elif visitor_type == "ต่างประเทศ":
        if subtype == "ผู้ใหญ่":
            return place.get("cost_foreigner_adult", place.get("cost_foreigner", place.get("cost", 0)))
        elif subtype == "เด็ก":
            return place.get("cost_foreigner_child", place.get("cost_foreigner", place.get("cost", 0)))
        elif subtype == "ผู้สูงวัย":
            return place.get("cost_foreigner_senior", place.get("cost_foreigner", place.get("cost", 0)))
        else:
            return place.get("cost_foreigner", place.get("cost", 0))
    else:
        return place.get("cost", 0)

def calc_distance_km(loc1, loc2):
    """คำนวณระยะทางระหว่างสองจุดในหน่วยกิโลเมตร"""
    try:
        lat1, lon1 = map(float, loc1.split(","))
        lat2, lon2 = map(float, loc2.split(","))
        
        # Haversine formula
        R = 6371.0  # รัศมีโลกในกิโลเมตร
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    except:
        return 1.0  # ค่าเริ่มต้นหากคำนวณไม่ได้

def calc_gas_cost(dist_km, km_per_litre=12.0, gas_price=37.35):
    """คำนวณค่าน้ำมันจากระยะทาง"""
    return (dist_km / km_per_litre) * gas_price

def calc_total_gas(trip, km_per_litre=12.0, gas_price=37.35):
    """คำนวณค่าน้ำมันรวมของทริป"""
    total_gas = 0.0
    for i in range(len(trip)-1):
        a = trip[i]
        b = trip[i+1]
        dist = calc_distance_km(a["location"], b["location"])
        total_gas += calc_gas_cost(dist, km_per_litre, gas_price)
    return total_gas

def get_local_date_from_timestamp(ts, tz_offset_hours=7):
    """แปลง timestamp เป็นวันที่ท้องถิน"""
    utc_dt = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
    local_dt = utc_dt + datetime.timedelta(hours=tz_offset_hours)
    return local_dt.date()

def get_hourly_weather(lat, lon, date, hour):
    """ดึงข้อมูลพยากรณ์อากาศรายชั่วโมง"""
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "YOUR_API_KEY_HERE":
        # Mock weather data หากไม่มี API key
        weather_conditions = ["แจ่มใส", "มีเมฆบ้าง", "มีเมฆมาก", "ฝนเบา"]
        return random.randint(24, 35), random.random() * 0.3, random.choice(weather_conditions), "Clear"
    
    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={lat}&lon={lon}&exclude=current,minutely,alerts"
        f"&appid={OPENWEATHER_API_KEY}&units=metric&lang=th"
    )
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None, None, "ไม่สามารถดึงข้อมูลได้", None
            
        data = r.json()
        temp = None
        pop = None
        desc = None
        main = None
        
        if "hourly" in data:
            for h in data["hourly"]:
                dt = datetime.datetime.fromtimestamp(h["dt"], datetime.timezone.utc) + datetime.timedelta(hours=7)
                if dt.date() == date and dt.hour == hour:
                    temp = h.get("temp")
                    pop = h.get("pop", 0)
                    weather = h.get("weather", [{}])[0]
                    desc = weather.get("description", "")
                    main = weather.get("main", "")
                    return temp, pop, desc, main
        return temp, pop, desc, main
    except Exception as e:
        print(f"Error fetching hourly weather: {e}")
        return None, None, "ไม่สามารถดึงข้อมูลได้", None

def fetch_weather_summary(lat, lon, date):
    """ดึงข้อมูลสรุปอากาศประจำวัน"""
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "YOUR_API_KEY_HERE":
        # Mock weather data หากไม่มี API key
        weather_conditions = ["แจ่มใส", "มีเมฆบ้าง", "มีเมฆมาก", "ฝนเบา", "อากาศดี"]
        return random.choice(weather_conditions), "Clear sky", random.random() * 0.3, random.randint(28, 35), random.randint(24, 28), random.randint(32, 38)
    
    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts"
        f"&appid={OPENWEATHER_API_KEY}&units=metric&lang=th"
    )
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return "ไม่สามารถดึงข้อมูลได้", None, None, None, None, None
            
        data = r.json()
        if "daily" not in data:
            return "ไม่สามารถดึงข้อมูลได้", None, None, None, None, None
            
        for day in data["daily"]:
            dt = get_local_date_from_timestamp(day["dt"], tz_offset_hours=7)
            if dt == date:
                desc = day.get("weather", [{}])[0].get("description", "-")
                main = day.get("weather", [{}])[0].get("main", "")
                pop = day.get("pop", 0)
                rain_mm = day.get("rain", 0)
                temp_day = day.get("temp", {}).get("day")
                temp_min = day.get("temp", {}).get("min")
                temp_max = day.get("temp", {}).get("max")
                
                # คำนวณโอกาสฝนตก
                if pop > 0:
                    rain_prob = pop
                elif rain_mm > 0:
                    rain_prob = min(1.0, rain_mm / 10.0)
                else:
                    rain_prob = 0.0
                
                # กำหนดสถานการณ์อากาศ
                if rain_prob >= 0.7:
                    situation = "ฝนตกหนัก"
                elif rain_prob >= 0.4:
                    situation = "มีโอกาสฝนตก"
                elif rain_prob >= 0.2:
                    situation = "ฝนตก (เบาๆ)"
                elif "cloud" in desc.lower() or "เมฆ" in desc:
                    situation = "มีเมฆมาก"
                elif "rain" in desc.lower() or "ฝน" in desc:
                    situation = "ฝนตก"
                elif "clear" in desc.lower() or "แจ่มใส" in desc:
                    situation = "แดดจ้า"
                else:
                    situation = desc
                
                return situation, desc, rain_prob, temp_day, temp_min, temp_max
                
        return "ไม่สามารถดึงข้อมูลได้", None, None, None, None, None
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return "ไม่สามารถดึงข้อมูลได้", None, None, None, None, None

def simple_trip_planner(budget, time_limit, selected_categories, max_places, hotel_idx, used_place_idxs, visitor_type, subtype, type_filter=None):
    """วางแผนทริปแบบง่าย (ใช้แทน Gurobi)"""
    # กรองสถานที่ที่เหมาะสม
    available_places = []
    hotel_place = PLACES[hotel_idx]
    
    import datetime
    # trip_date must be passed in via caller's frame
    import inspect
    frame = inspect.currentframe()
    while frame:
        if "trip_date" in frame.f_locals:
            trip_date = frame.f_locals["trip_date"]
            break
        frame = frame.f_back
    else:
        trip_date = None

    for i, place in enumerate(PLACES):
        day_close = place.get("day_close", "-")
        is_closed = False
        reason = []
        if trip_date and day_close:
            weekday = trip_date.weekday()
            weekday_name = trip_date.strftime('%A')
            date_str = trip_date.strftime('%Y-%m-%d')
            if day_close == "-":
                pass
            elif isinstance(day_close, list):
                if weekday in day_close or weekday_name in day_close or date_str in day_close:
                    is_closed = True
                    reason.append(f"closed on {day_close}")
            elif isinstance(day_close, str):
                closed_days = [d.strip() for d in day_close.split(",") if d.strip()]
                if str(weekday) in closed_days or weekday_name in closed_days or date_str in closed_days:
                    is_closed = True
                    reason.append(f"closed on {day_close}")
        if i == hotel_idx:
            reason.append("is hotel")
        if place["category"] not in selected_categories:
            reason.append(f"category {place['category']} not in {selected_categories}")
        if i in used_place_idxs:
            reason.append("already used")
        if type_filter is not None and place["type"] != type_filter:
            reason.append(f"type {place['type']} != {type_filter}")
        if is_closed:
            reason.append("closed")
        if not (i != hotel_idx and 
            place["category"] in selected_categories and 
            i not in used_place_idxs and
            (type_filter is None or place["type"] == type_filter) and not is_closed):
            print(f"SKIP {place['name']}: {', '.join(reason)}")
        else:
            available_places.append((i, place))
    
    if len(available_places) == 0:
        return [], 0, 0.0, set(), 0
    
    # จำกัดจำนวนสถานที่ตาม input (ไม่รวมโรงแรม)
    # Always try to select exactly max_places (unless not enough available)
    max_places = min(max_places, len(available_places))

    # สร้างคะแนนรวมแต่ละสถานที่
    hotel_loc = tuple(map(float, hotel_place["location"].split(",")))
    def calc_score(idx, place):
        # ความพึงพอใจ (rating)
        sat_score = place["rating"] / 5.0 if place["rating"] else 0
        # ระยะทางจากโรงแรม
        place_loc = tuple(map(float, place["location"].split(",")))
        dist_score = 1.0 - (calc_distance_km(hotel_place["location"], place["location"]) / 30.0)  # 30 กม. ถือว่าไกลสุด
        dist_score = max(0, min(dist_score, 1))
        # งบประมาณ
        cost = get_place_cost(place, visitor_type, subtype)
        budget_score = 1.0 - (cost / budget) if budget > 0 else 0
        budget_score = max(0, min(budget_score, 1))
        # รวมคะแนน
        total_score = 0.5 * sat_score + 0.3 * dist_score + 0.2 * budget_score
        return total_score

    # เรียงตามคะแนนรวม
    available_places.sort(key=lambda x: calc_score(x[0], x[1]), reverse=True)
    selected_places = available_places[:max_places]
    # If budget is too low, only reduce if more than 1 place, but never below max_places unless not enough available
    while len(selected_places) > 1 and sum(get_place_cost(place, visitor_type, subtype) for _, place in selected_places) + calc_total_gas([hotel_place] + [p for _, p in selected_places] + [hotel_place]) > budget:
        selected_places.pop()

    # จัดเส้นทางแบบ TSP (Nearest Neighbor)
    remaining = selected_places.copy()
    trip = [hotel_place]
    selected_idxs = set()
    curr_loc = hotel_place["location"]
    while remaining:
        next_idx, next_place = min(remaining, key=lambda x: calc_distance_km(curr_loc, x[1]["location"]))
        trip.append(next_place)
        selected_idxs.add(next_idx)
        curr_loc = next_place["location"]
        remaining = [x for x in remaining if x[0] != next_idx]
    trip.append(hotel_place)
    # Ensure trip has hotel + max_places + hotel (if enough available)
    # If not enough available, trip will be shorter
    
    # คำนวณต้นทุน
    total_cost = 0
    total_distance = 0
    total_sat = 0
    
    # คำนวณค่าใช้จ่ายสถานที่
    for _, place in selected_places:
        cost = get_place_cost(place, visitor_type, subtype)
        total_cost += cost
        total_sat += place["rating"]
    
    # คำนวณค่าน้ำมัน
    gas_cost = calc_total_gas(trip)
    total_cost += gas_cost
    
    # คำนวณระยะทาง
    for i in range(len(trip)-1):
        distance = calc_distance_km(trip[i]["location"], trip[i+1]["location"])
        total_distance += distance
    
    # ตรวจสอบงบประมาณ
    if total_cost > budget:
        # ลดจำนวนสถานที่ลง
        while len(selected_places) > 1 and total_cost > budget:
            selected_places.pop()
            selected_idxs = set(idx for idx, _ in selected_places)
            
            # คำนวณใหม่
            trip = [hotel_place]
            for _, place in selected_places:
                trip.append(place)
            trip.append(hotel_place)
            
            total_cost = sum(get_place_cost(place, visitor_type, subtype) for _, place in selected_places)
            total_cost += calc_total_gas(trip)
            total_sat = sum(place["rating"] for _, place in selected_places)
            
            total_distance = 0
            for i in range(len(trip)-1):
                distance = calc_distance_km(trip[i]["location"], trip[i+1]["location"])
                total_distance += distance
    
    # ตรวจสอบเวลา
    total_time = sum(place["recommend_time"] for _, place in selected_places)
    total_time += (len(selected_places)) * 20  # เวลาเดินทาง
    
    if total_time > time_limit:
        # ลดเวลาแนะนำของแต่ละสถานที่
        pass  # ใช้เวลาเดิมไปก่อน
    
    return trip, total_cost, total_distance, selected_idxs, total_sat

app = Flask(__name__)
CORS(app)

@app.route("/plan", methods=["POST"])
def plan_trip():
    """API endpoint สำหรับวางแผนทริป"""
    try:
        data = request.get_json(force=True) or {}
        print(f"Received request data: {data}")  # Debug log
        
        # ดึงข้อมูลจาก request
        travelers = data.get("travelers", [])
        hotel_name = data.get("hotel", "")
        startDate = data.get("startDate", "")
        nDays = data.get("nDays", 1)
        startTimes = data.get("startTimes", [])
        maxPlaces_list = data.get("maxPlaces", [])
        budget = data.get("budget", 1000)
        categories = data.get("categories", [])
        returnTimes = data.get("returnTimes", [])

        # ตรวจสอบข้อมูลที่จำเป็น
        if not travelers:
            return jsonify({"error": "ไม่ได้ระบุข้อมูลนักท่องเที่ยว"}), 400
            
        if not hotel_name:
            return jsonify({"error": "ไม่ได้ระบุโรงแรม"}), 400
            
        if not startDate:
            return jsonify({"error": "ไม่ได้ระบุวันที่เริ่มเที่ยว"}), 400
            
        if not categories:
            return jsonify({"error": "ไม่ได้ระบุประเภทสถานที่"}), 400

        # แปลงข้อมูล
        try:
            nDays = int(nDays)
            budget = int(budget)
        except ValueError:
            return jsonify({"error": "จำนวนวันหรืองบประมาณไม่ถูกต้อง"}), 400

        # สร้าง returnTimes หากไม่มี
        if not returnTimes:
            returnTimes = ["ไม่ต้องการระบุ"] * nDays

        # หาโรงแรม
        hotel_idx = None
        for i, place in enumerate(PLACES):
            if hotel_name.strip() == place["name"]:
                hotel_idx = i
                break
                
        # หากไม่เจอในรายการ PLACES ให้เพิ่มเข้าไป
        if hotel_idx is None:
            for hotel in HOTELS:
                if hotel_name.strip() == hotel["name"]:
                    hotel_place = {
                        "name": hotel["name"],
                        "category": "ที่พัก",
                        "type": "hotel",
                        "cost": 0,
                        "cost_thai_adult": 0,
                        "cost_thai_child": 0,
                        "cost_thai_senior": 0,
                        "cost_foreigner": 0,
                        "cost_foreigner_adult": 0,
                        "cost_foreigner_child": 0,
                        "cost_foreigner_senior": 0,
                        "open": "00:00",
                        "close": "23:59",
                        "recommend_time": 0,
                        "location": hotel["location"],
                        "district": "สุเทพ",
                        "rating": 0
                    }
                    PLACES.append(hotel_place)
                    hotel_idx = len(PLACES) - 1
                    break
                    
        if hotel_idx is None:
            return jsonify({"error": f"ไม่พบโรงแรม: {hotel_name}"}), 400

        # เริ่มวางแผนทริป
        budget_per_day = budget // nDays
        used_place_idxs = set()
        trip_result = {"days": [], "summary": {}}
        
        # ตัวแปรสำหรับสรุปผล
        trip_sum_attractions = 0
        trip_sum_gas = 0
        trip_sum_budget = 0
        trip_sum_distance = 0
        trip_sum_sat = 0
        trip_sum_max_sat = 0

        today = datetime.date.today()

        for d in range(nDays):
            print(f"Planning day {d+1}")  # Debug log
            
            # คำนวณวันที่
            trip_date = datetime.datetime.strptime(startDate, "%Y-%m-%d").date() + datetime.timedelta(days=d)
            
            # กำหนดเวลา
            time_per_day = 8 * 60  # 8 ชั่วโมงในนาที
            
            # เวลาเริ่มต้น
            start_time_str = startTimes[d] if d < len(startTimes) else "08:00"
            try:
                h, m = map(int, start_time_str.split(':'))
            except:
                h, m = 8, 0

            # เวลากลับ
            return_time_str = returnTimes[d] if d < len(returnTimes) else "ไม่ต้องการระบุ"
            return_time_limit = None
            if return_time_str and return_time_str != "ไม่ต้องการระบุ":
                try:
                    rh, rm = map(int, return_time_str.split(':'))
                    return_time_limit = datetime.datetime.combine(trip_date, datetime.time(rh, rm))
                except:
                    return_time_limit = None

            # จำนวนสถานที่สูงสุด (input + 2)
            max_places = maxPlaces_list[d] if d < len(maxPlaces_list) else 3
            max_places = int(max_places) + 2

            # ดึงข้อมูลสภาพอากาศ
            weather_situation, weather_desc, rain_prob, temp_day, temp_min, temp_max = fetch_weather_summary(
                LAT_CHIANGMAI, LON_CHIANGMAI, trip_date)

            # กำหนดประเภทสถานที่ตามสภาพอากาศ
            use_indoor_only = False
            if rain_prob is not None and rain_prob >= 0.4:
                use_indoor_only = True

            plan_type = "indoor" if use_indoor_only else None

            # ดึงข้อมูลนักท่องเที่ยวหลัก (คนแรก)
            main_traveler = travelers[0]
            visitorType = main_traveler.get("type", "ไทย")
            subtype = main_traveler.get("subtype", "ผู้ใหญ่")

            # วางแผนทริปสำหรับวันนี้
            trip, used_budget, total_distance, selected_today_idxs, total_sat = simple_trip_planner(
                budget_per_day, time_per_day, categories, max_places, hotel_idx, 
                used_place_idxs, visitorType, subtype, plan_type
            )

            if not trip or len(trip) < 3:
                # ไม่มีสถานที่ให้เที่ยว
                trip_result["days"].append({
                    "date": str(trip_date),
                    "weather": weather_situation or "ไม่สามารถดึงข้อมูลได้",
                    "places": [],
                    "maps_url": "",
                })
                continue

            # อัปเดตสถานที่ที่ใช้แล้ว
            used_place_idxs.update(selected_today_idxs)

            # คำนวณค่าใช้จ่ายสำหรับนักท่องเที่ยวทุกคน
            total_attractions_budget = 0
            for traveler in travelers:
                for place in trip[1:-1]:  # ไม่นับโรงแรม
                    cost = get_place_cost(place, traveler.get("type", "ไทย"), traveler.get("subtype"))
                    total_attractions_budget += cost

            total_gas = calc_total_gas(trip)
            max_sat_day = 5.0 * max_places

            # อัปเดตผลรวม
            trip_sum_attractions += total_attractions_budget
            trip_sum_gas += total_gas
            trip_sum_budget += total_attractions_budget + total_gas
            trip_sum_distance += total_distance
            trip_sum_sat += total_sat
            trip_sum_max_sat += max_sat_day

            # สร้างรายการสถานที่สำหรับวันนี้
            current_time = datetime.datetime.combine(trip_date, datetime.time(h, m))
            day_places = []

            for i in range(1, len(trip)-1):  # ไม่นับโรงแรมตอนเริ่มและจบ
                curr = trip[i]
                
                # คำนวณเวลาเดินทาง (20 นาที + ระยะทาง)
                travel_min = 20
                if i < len(trip) - 2:  # ไม่ใช่สถานที่สุดท้าย
                    next_place = trip[i + 1]
                    distance_to_next = calc_distance_km(curr["location"], next_place["location"])
                    # เพิ่มเวลาตามระยะทาง (1 นาทีต่อ 1 กม.)
                    travel_min = 20 + int(distance_to_next)
                else:
                    # สถานที่สุดท้าย - เวลาเดินทางกลับโรงแรม
                    distance_to_hotel = calc_distance_km(curr["location"], trip[-1]["location"])
                    travel_min = 20 + int(distance_to_hotel)
                
                arrive_time = current_time + datetime.timedelta(minutes=travel_min)
                
                # ตรวจสอบเวลาเปิด
                try:
                    open_time = datetime.datetime.combine(trip_date, datetime.datetime.strptime(curr["open"], "%H:%M").time())
                    if arrive_time < open_time:
                        arrive_time = open_time
                except:
                    pass

                # ดึงข้อมูลสภาพอากาศเฉพาะจุด
                spot_lat, spot_lon = map(float, curr["location"].split(","))
                
                if abs((trip_date - today).days) <= 7:  # เฉพาะสัปดาหน์นี้
                    spot_temp, spot_pop, spot_desc, spot_main = get_hourly_weather(
                        spot_lat, spot_lon, trip_date, arrive_time.hour)
                else:
                    spot_temp = temp_day
                    spot_pop = rain_prob
                    spot_desc = weather_desc
                    spot_main = None

                # กำหนดสถานการณ์อากาศ
                spot_rain_prob = spot_pop if spot_pop is not None else 0.0
                if spot_rain_prob >= 0.7:
                    spot_situation = "ฝนตกหนัก"
                elif spot_rain_prob >= 0.4:
                    spot_situation = "มีโอกาสฝนตก"
                elif spot_rain_prob >= 0.2:
                    spot_situation = "ฝนตกเบา"
                elif spot_desc and ("cloud" in spot_desc.lower() or "เมฆ" in spot_desc):
                    spot_situation = "มีเมฆมาก"
                elif spot_desc and ("rain" in spot_desc.lower() or "ฝน" in spot_desc):
                    spot_situation = "ฝนตก"
                elif spot_desc and ("clear" in spot_desc.lower() or "แจ่มใส" in spot_desc):
                    spot_situation = "แดดจ้า"
                else:
                    spot_situation = spot_desc or "อากาศดี"

                # กำหนดเวลาออก
                depart_time = arrive_time + datetime.timedelta(minutes=curr["recommend_time"])
                
                # ตรวจสอบเวลากลับ
                if return_time_limit and depart_time > return_time_limit:
                    break

                current_time = depart_time

                # คำนวณค่าใช้จ่ายสำหรับนักท่องเที่ยวแต่ละคน
                cost_list = []
                for traveler in travelers:
                    cost = get_place_cost(curr, traveler.get("type", "ไทย"), traveler.get("subtype"))
                    cost_list.append(cost)

                day_places.append({
                    "name": curr["name"],
                    "time": arrive_time.strftime('%H:%M'),
                    "depart_time": depart_time.strftime('%H:%M'),
                    "recommend_time": curr["recommend_time"],
                    "travel_time": travel_min,
                    "open": curr["open"],
                    "close": curr["close"],
                    "costs": cost_list,
                    "rating": curr["rating"],
                    "location": curr["location"],
                    "weather": spot_situation,
                    "temp": spot_temp,
                    "rain_prob": spot_rain_prob
                })

            # สร้าง Google Maps URL
            locations = [place["location"] for place in trip]
            maps_url = f"https://www.google.com/maps/dir/" + "/".join(locations)

            trip_result["days"].append({
                "date": str(trip_date),
                "weather": weather_situation or "ไม่สามารถดึงข้อมูลได้",
                "places": day_places,
                "maps_url": maps_url,
            })

        # คำนวณคะแนนความพึงพอใจเฉลี่ย
        avg_sat_score = (trip_sum_sat / trip_sum_max_sat) * 5 if trip_sum_max_sat > 0 else 0

        trip_result["summary"] = {
            "total_cost": round(trip_sum_budget, 2),
            "total_attractions": round(trip_sum_attractions, 2),
            "total_gas": round(trip_sum_gas, 2),
            "total_distance": round(trip_sum_distance, 2),
            "avg_sat_score": round(avg_sat_score, 2)
        }

        print(f"Trip result: {trip_result}")  # Debug log
        return jsonify(trip_result)

    except Exception as e:
        print(f"Error in plan_trip: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"เกิดข้อผิดพลาดในระบบ: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def home():
    """หน้าแรกสำหรับทดสอบ"""
    return jsonify({
        "message": "Chiang Mai Trip Planner API",
        "status": "running",
        "endpoints": {
            "POST /plan": "วางแผนทริป"
        }
    })

@app.route("/places", methods=["GET"])
def get_places():
    """ดูรายการสถานที่ทั้งหมด"""
    return jsonify({
        "places": PLACES,
        "total": len(PLACES)
    })

@app.route("/hotels", methods=["GET"])
def get_hotels():
    """ดูรายการโรงแรมทั้งหมด"""
    return jsonify({
        "hotels": HOTELS,
        "total": len(HOTELS)
    })

if __name__ == "__main__":
    print("Starting Chiang Mai Trip Planner API...")
    print("Available endpoints:")
    print("- GET  / : หน้าแรก")
    print("- POST /plan : วางแผนทริป")
    print("- GET  /places : ดูรายการสถานที่")
    print("- GET  /hotels : ดูรายการโรงแรม")
    print("\nServer running on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)