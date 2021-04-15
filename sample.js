const { json } = require('body-parser');
const express = require('express');
const Signupdetails = require('../Model/Signupdetails');
const router = express.Router();
const signup = require('../Model/Signupdetails');

router.post('/' ,(req,res) => {
    email = req.body.email
    
    user = email.substring(0,email.lastIndexOf("@"))
    const signupdetails = new Signupdetails({
        email : req.body.email ,
        userName : user ,
        PersonalInformation : {
            firstName : req.body.PersonalInformation.firstName ,
            lastName : req.body.PersonalInformation.lastName ,
            phoneNumber : req.body.PersonalInformation.phoneNumber,
            DOB : req.body.PersonalInformation.DOB 
        } ,

        Address : {
            street : req.body.Address.street ,
            city : req.body.Address.city ,
            pincode : req.body.Address.pincode,
            state : req.body.Address.state,
            country : req.body.Address.country
        }
    });
    

    signupdetails.save() 
        .then (doc =>  {
            res.status(200).json(doc);
        })
        .catch (err => {
            res.json({ message : err });
        });
    console.log(user);
    console.log(signupdetails.password);
    console.log(signupdetails);
    
});


module.exports = router ;
