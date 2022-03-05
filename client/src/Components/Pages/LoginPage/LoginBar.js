import React from 'react';
import { HiOutlineMail } from "react-icons/hi";
import { HiOutlineLockClosed } from "react-icons/hi";
import FormTextInput from './FormTextInput'
import { Link } from 'react-router-dom';

var CURRENT_ID = 0;

export default function LoginBar(props) {

    return   <div className="login-wrapper">
                  <div className="login-header">
                    <div className="login-header-btn center">
                      <button className="center" onClick={() => props.Functions.moveScreenTo(props.Variables.LeftScreenPosition)}>Register</button>
                    </div>
                    <div className="login-header-btn center">
                      <button className="center" onClick={() => props.Functions.LearnMorePressed()}>Learn More</button>
                    </div>
                  </div>
                  <div className="login-page-form-title-wrapper">
                      <div className="login-page-form-title center">
                        Welcome Back!
                      </div>
                      <div className="login-page-form-subtitle center">
                        Sign into your account
                      </div>
                  </div>
                  <form id="login-page-form">
                    <div className="login-body">
                    <FormTextInput  Functions={ props.Functions } 
                                    Variables={{valueName: 'email', value: props.Variables.email, ID: 'Login',
                                                title: "Email Address", type: "text", backgroundColor: '#6290b0'}}>
                      <HiOutlineMail fontSize="1.25rem" color="white"/>
                    </FormTextInput>
                    <FormTextInput  Functions={ props.Functions } 
                                    Variables={{valueName: 'password', value: props.Variables.password, ID: 'Login',
                                                title: "Password", type: "password",  backgroundColor: '#6290b0', showForgotPassword: true}}>
                      <HiOutlineLockClosed fontSize="1.25rem" color="white"/>
                    </FormTextInput>
                      <div className="login-submit-btn-wrapper center">
                        <Link to="/Home">
                          <input type="submit" value="submit" onClick={e => props.Functions.loginSubmitClicked(e)} className="submit"></input>
                        </Link>
                      </div>
               
                    </div>
                    <div className="icons-wrapper center">
                      <div className="icons-container">
                        {props.Variables.Icons.map((item) => { 
                          return  <a key={++CURRENT_ID} href={item.url}>
                                    <img key={++CURRENT_ID} alt="" src={item.img} />
                                  </a>;
                        })}
                      </div>
                    </div>
                  </form>
                  <div className="login-footer"/>
                </div>
}