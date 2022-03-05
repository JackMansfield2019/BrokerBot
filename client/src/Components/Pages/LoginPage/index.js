import React from 'react';
import MainImage from '../images/stocks.svg';
import Logo from '../images/BrokerBot.png';

/*------------------ React Redux --------------------*/
import { connect } from 'react-redux';
import { userLogin, userRegister } from '../../../redux/userSlice';
/*-------------- Page Constant Values -------------- */
import * as Constants from '../PageConstants'

/* ---------------- Icons for Links ---------------- */
import RCOS from '../images/RCOSlogo.png'
import GIT from '../images/github-logo.png'
import ALPACA from '../images/alpacaLogo.png'

/* -------------- Components for Page -------------- */
import LoginBar from "./LoginBar"
import LoginRegisterContent from "./LoginRegisterContent"
import RegisterBar from "./RegisterBar"

const LeftScreenPosition = Constants.LoginPageScreenPosition.Left;
const RightScreenPosition = Constants.LoginPageScreenPosition.Right;

class LoginPage extends React.Component {
  constructor(props) {
    super(props);
    
    this.state = {
      currentPosition: RightScreenPosition, 
      email: '',
      password: '',
      confirmPassword: '',
      LoginFunctions: { moveScreenTo: this.moveScreenTo,
                        LearnMorePressed: this.LearnMorePressed,
                        loginSubmitClicked: this.loginSubmitClicked,
                        updateText: this.updateText,
                        forgotPasswordPressed: this.forgotPasswordPressed,
                      },
      RegisterFunctions: {  moveScreenTo: this.moveScreenTo,
                            LearnMorePressed: this.LearnMorePressed,
                            registerSubmitClicked: this.registerSubmitClicked,
                            updateText: this.updateText },
    }
  }

  componentDidMount(){
    //console.log(this.props.userData);
  }

  componentDidUpdate(prevProps){
     //console.log(this.props.userData);
  }

  /**
   * Redirects the user to the forgot password page
   */
  forgotPasswordPressed = () => {
    alert('Forgot Password was Pressed but functionality is not finished');
  }

  /**
    * Redirects the user to the forgot password page
    */
  LearnMorePressed = () => {
    alert('Forgot Password was Pressed but functionality is not finished');
  }

  /**
   * Updates a text value to its new inputed value for input JSX tags
   * @param  {[event]} e the event holding the variable and new text value
   */
  updateText = e => {
    this.setState({
        [e.target.name]: e.target.value
    });
  }

  /**
   * Moves the login/register page screens view position resets the forms and forces an Update for the Component
   * @param  {[Number]} position a value between 0 and 35 where 0 is the farthest left and 35 is the farthest right
   */
  moveScreenTo = position => {
    this.setState({
      ...this.state,
      currentPosition: position, 
      email: '',
      password: '',
      confirmPassword: '',

    })
    this.forceUpdate();
  }

  /**
    * Sends a Request to the backend checking to see if the if the User and Password 
    * match a known user in the database. If the User exists re-route them to their 
    * account if they dont then keep them at he login screen
    * @param  {[event]} e the event holding the form that was submitted and its relevant data
    */
  loginSubmitClicked = event => {
    /*Check to see if Valid before prevent default*/
    //var AlertValue = `Email:  ${this.state.email}\nPassword: ${this.state.password}`;
    //alert(AlertValue);

    if(this.state.password === "TESTING"){
      this.props.dispatch(userLogin({
        ID: 1,
        email: this.state.email,
      }));
    }  else {

    event.preventDefault();
    }
  }

  /**
   * Sends a Request to the backend checking to see if the if the User email already exists in the database.
   * If the Request returns saying that the user has been made let them into their new account otherwise 
   * keep them on this page.
   * @param  {[event]} e the event holding the form that was submitted and its relevant data
   */
  registerSubmitClicked = event => {
    //var AlertValue = `Email:  ${this.state.email}\nPassword: ${this.state.password}\nConfirm Password: ${this.state.confirmPassword}`;
    ///alert(AlertValue);
    
    this.props.dispatch(userRegister({
        ID: 1,
        email: this.state.email,
    }));
    /*event.preventDefault();*/

  }

  render() {
    return (
         <div className="page-wrapper">
            <div className="login-page-wrapper" style={{left: `${-this.state.currentPosition}%`}}>
              <RegisterBar  Functions={ this.state.RegisterFunctions } 
                            Variables={{email:this.state.email, password: this.state.password, confirmPassword: this.state.confirmPassword,
                                        RightScreenPosition: RightScreenPosition, Icons: [{ img: RCOS,
                                                                                            url: 'https://rcos.io/' },
                                                                                          { img: GIT,
                                                                                            url: 'https://github.com/JackMansfield2019/BrokerBot' },
                                                                                          { img: ALPACA,
                                                                                            url: 'https://app.alpaca.markets/signup' }] }}/>
              <LoginRegisterContent Logo={ Logo } MainImage={ MainImage } />
              <LoginBar Functions={ this.state.LoginFunctions } 
                        Variables={{email:this.state.email, password: this.state.password, LeftScreenPosition: LeftScreenPosition, 
                                    Icons: [{ img: RCOS,
                                              url: 'https://rcos.io/' },
                                            { img: GIT,
                                              url: 'https://github.com/JackMansfield2019/BrokerBot' },
                                            { img: ALPACA,
                                              url: 'https://app.alpaca.markets/signup' }] }}/>
            </div>
        </div>
    );
  }
}

const MapStateToProps = (state) => ({
    userData: state.userData
});

export default connect(MapStateToProps)(LoginPage);