import React from 'react';

export default function FormTextInput(props) {
    return  <div className="login-page-input-wrapper">
                      <div className="login-page-text-input-title">{props.Variables.title}</div>
                      <div className="login-page-text-input-wrapper" >
                        <input  name={props.Variables.valueName}  type={props.Variables.type} id={props.Variables.ID + props.Variables.valueName} value={props.Variables.value} 
                                onChange={e => props.Functions.updateText(e)} autoComplete="off" spellCheck="false" style={{background: props.Variables.backgroundColor}} required ></input>
                        <label className="testing">{props.children}</label>
                      </div>
                    {props.Variables.showForgotPassword ? <div className="forgot-password">
                        <button type="button" onClick={() => props.Functions.forgotPasswordPressed()}>Forgot Password?</button>
                      </div> : <></>}
                    </div>
}