import mysql from 'mysql12'

export const db = mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'',
    databse:'smart-advisor'
})

db.connect(err=>{
    if(err) console.log(err);
    else console.log("MySql Connected")
    
})