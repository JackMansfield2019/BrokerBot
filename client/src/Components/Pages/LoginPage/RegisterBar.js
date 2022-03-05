import React from 'react';
import { HiOutlineMail } from "react-icons/hi";
import { HiOutlineLockClosed } from "react-icons/hi";
import { Link } from 'react-router-dom';

import FormTextInput from './FormTextInput'

var CURRENT_ID = 0;

export default function RegisterBar(props) {

    return  <div className="register-wrapper">
                <div className="login-header">
                    <div className="login-header-btn center">
                        <button className="center" onClick={() => console.log('im a button')}>Learn More</button>
                    </div>
                    <div className="login-header-btn center">
                        <button className="center" onClick={() => props.Functions.moveScreenTo(props.Variables.RightScreenPosition)}>Log In</button>
                    </div>
                </div>
                <div className="login-page-form-title-wrapper">
                    <div className="login-page-form-title center">
                        Welcome!
                    </div>
                    <div className="login-page-form-subtitle center">
                        Sign up for your new account today
                    </div>
                  </div>
                  {/* From here down not finished */}
                <form id="login-page-form1" onSubmit={e => props.Functions.registerSubmitClicked(e)}>
                    <div className="login-body">
                    <FormTextInput  Functions={ props.Functions } 
                                    Variables={{valueName: 'email', value: props.Variables.email, ID: 'Register',
                                                title: "Email Address", type: "text", backgroundColor: '#c57949'}}>
                        <HiOutlineMail fontSize="1.25rem" color="white"/>
                    </FormTextInput>
                    <FormTextInput  Functions={ props.Functions } 
                                    Variables={{valueName: 'password', value: props.Variables.password, ID: 'Register',
                                                title: "Password", type: "password", backgroundColor: '#c57949'}}>
                        <HiOutlineLockClosed fontSize="1.25rem" color="white"/>
                    </FormTextInput>
                     <FormTextInput  Functions={ props.Functions } 
                                    Variables={{valueName: 'confirmPassword', value: props.Variables.confirmPassword, ID: 'Register',
                                                title: "Confirm Password", type: "password", backgroundColor: '#c57949'}}>
                        <HiOutlineLockClosed fontSize="1.25rem" color="white"/>
                    </FormTextInput>
                    <div className="register-submit-btn-wrapper center">
                        <Link to="/Home">
                          <input type="submit" value="submit" onClick={e => props.Functions.registerSubmitClicked(e) } className="submit"></input>
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
            </div>
            
}
