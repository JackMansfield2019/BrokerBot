import React from 'react';
import { BiHide } from "react-icons/bi";

class SettingsPopup extends React.Component  {

     constructor(props){
        super(props); 

        this.state = {
           hideKey: true,
           inputKey: '',
           inputSecret: '',
           secretValue: "LK421LI7Z",
           keyValue: "B5K21VH7",
        }
    }

    change = e => {
        this.setState({
            [e.target.name]: e.target.value
        });
    }

    onSubmit = (event) => {
        this.setState({
           secretValue: this.state.inputSecret,
           keyValue: this.state.inputKey,
        });
        
        event.preventDefault();
    }

    render(){
        return        <form><div className="settings-popup-inner">
          
                    <div className="settings-popup-title-wrapper" >
                        <div className="settings-popup-title" > Broker Bot Settings</div>
                        <div className="settings-popup-close-wrapper"><button onClick={() => this.props.setTrigger(false)}/>X</div>
                    </div>
                    <div className="settings-popup-content-wrapper">
                        <div className="settings-popup-subsection">
                            <div className="settings-popup-subsection-title">Your API & Secret Keys:</div>
                            <div className="settings-popup-key-subsection">
                                <div className="settings-popup-key-info" >
                                   API Key: &nbsp; <div className="settings-popup-key-info-value" >{this.state.keyValue}</div>
                                </div>

                                <input type="text" name="inputKey" placeholder="Change API Key" onChange={e => this.change(e) } />
                            </div>
                            <div className="settings-popup-key-subsection">
                                <div className="settings-popup-key-info" >
                                   <div className="settings-popup-key-info-title">Secret Key: 
                                    <div className="settings-popup-key-show" >
                                            <button type="button" onClick={() => this.setState({ hideKey: !this.state.hideKey})} />
                                            <BiHide color={ this.state.hideKey ? "#66ff66"  : "#f33e33"} size={16} />
                                        </div>
                                    </div>
                                   <div className="settings-popup-key-info-value" >{ this.state.hideKey ? "••••••••"  : this.state.secretValue}</div>
                                </div>
                                <input type="text" name="inputSecret" placeholder="Change Secret Key"  onChange={e => this.change(e) } />
                            </div>
                        </div>
                    </div>
                    <div className="settings-popup-submit-wrapper"><button type="submit" onClick={(event) => this.onSubmit(event)} />Submit Changes</div>
                </div> 
             </form>
                
    }
}
export default SettingsPopup;