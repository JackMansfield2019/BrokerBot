import React from 'react';
import { connect } from 'react-redux';
import Logo from '../images/BrokerBot.png';
import ReactApexChart from './Test';
import ReactApexChart1 from './Test1';
import { AiOutlineGithub, AiFillSetting  } from "react-icons/ai"
import { VscSettings } from "react-icons/vsc";

import DataDisplay from "./DataDisplay";
import SummaryDisplay from "./SummaryDisplay";
import Popup from './Popup'
import DeleteHoldingPopup from './deleteHoldingPopup'
import SettingsPopup from './SettingsPopup'
import AddHoldingPopup from './AddHoldingPopup'

    
/* PUT THIS IN PAGE CONSTANTS LATER */
const HeaderNavButtons = [  {Name: 'Dashboard' }, 
                            {Name: 'Bots'}, 
                            {Name: 'Algorithms'}, 
                            {Name: 'Settings'}, 
                            {Name: 'Profile'} 
                         ]



class HomePage extends React.Component {
    constructor(props){
        super(props); 

        this.state = {
            /*Fill in the state variables later with Broker Data needed for graphs and bots */
            deleteHoldingPopup: false,
            deleteHoldingName: '',
            settingsPopup: false,
            addHoldingPopup: false,
            inputData: [{title: "$APPL", values: ["$303.19", "101","23362.18", "50.02%", "2.64", "0.0%", "55.01%"]}, 
                        {title: "$NEPL", values: ["$134.70", "53", "5,446.54", "20.32%", "3.64%", "0.0%", "25.26%"]},
                        {title: "$APED", values: ["$24.00", "10", "240.00", "12.50%", "0.0%", "0.0%", "12.50%"]},
                        {title: "$OPEK", values: ["$312.00", "12", "3744.00", "11.00%", "0.00%", "0.00%", "11.00%"]}],

        }
    }

    /**
     * This function changes the display value of the add calendar pop up menu.
     *
     * @param   {boolean} value A boolean true or false
     * @effect  Changes deleteHoldingPopup: value to be the input value and if the boolean is true it sets the delete Holding pop up to 
     *          be displayed on the screen, Otherwise if it is false it will not diplay the delete holding on the screen.
     */
    setDeleteHoldingPopup = (value, holding = '') => {
        this.setState({ deleteHoldingPopup: value, deleteHoldingName: holding  });

    }

    /**
     * This function changes the display value of the add calendar pop up menu.
     *
     * @param   {boolean} value A boolean true or false
     * @effect  Changes settingPopup: value to be the input value and if the boolean is true it sets the setting pop up to 
     *          be displayed on the screen, Otherwise if it is false it will not diplay the setting up on the screen.
     */
    setSettingsPopup = (value) => {
        this.setState({ settingsPopup: value });
    }


    /**
     * This function changes the display value of the add calendar pop up menu.
     *
     * @param   {boolean} value A boolean true or false
     * @effect  Changes settingPopup: value to be the input value and if the boolean is true it sets the setting pop up to 
     *          be displayed on the screen, Otherwise if it is false it will not diplay the setting up on the screen.
     */
    setHoldingPopup = (value) => {
        this.setState({  addHoldingPopup: value });

    }

    removeData = (searchVal) => {
        this.setState({  inputData: this.state.inputData.filter((value) => value.title !== searchVal) });
    }

    addData = (name, tot, qty) => {
        this.state.inputData.push({title: "$" + name, values: [tot, qty,"0.00", "0.00%", "0.00%", "0.00%", "0.00%"]});
    }

    


    render(){
        return !this.props.userRedux.isRegister ? <div className="page-wrapper">
                    <div className="flex-wrapper">   
                        {/* make one flex div then split it */}
                        <div className="page-content-wrapper">
                      <div className="header-wrapper">
                            <div className="header-img-wrapper center">
                                <img  alt='' src={Logo}/>
                            </div>
                            <div className="header-rest-wrapper">
                               <div className="settings-wrapper">
                                    <button onClick={() => this.setSettingsPopup(true)} />
                                    <VscSettings size={24} />
                               </div>
                            </div>
                        </div>
                        <div className="page-content-top-box-wrapper" >
                           {/* https://apexcharts.com/react-chart-demos/area-charts/stacked/ */}
                           <div className="graph-wrapper">
                              <ReactApexChart  />  
                            </div>
                        </div>
                          <div className="page-content-bottom-box-wrapper" >
                            <SummaryDisplay title={"Your Portfolio's Summary"} 
                                            categories={["Capital Gain", "Dividends", "Currency Gain", "Std. Dev", "Adj. Return", "Expected", "Total Return"]} 
                                            inputData={ [{title: "Monetary(USD) gains/losses", values: [ 500.00, 0.00, 0.00, 25.00, -4000, 15000.00, 500.00]}, 
                                                         {title: "Percentage(%) gains/losses", values: ["1.00%", "2.00%", "0.00%", "4.00%", "-5.00%", "6.00%", "6.62%"]}] }/>
                            <DataDisplay title={"Your Portfolio's Holdings"} categories={["Price", "Qty.", "Value", "Capital Gains", "Dividends", "Currency", "Return"]} inputData={ this.state.inputData }
                                                                                                                resultValues={["", "", "$242792.72", "93.84%", "6.28%", "0.00%", "103.67%"] }
                                                                                                                delPopupTrigger={this.setDeleteHoldingPopup} 
                                                                                                        
                                                                                                                addPopupTrigger={this.setHoldingPopup} />

                          </div>
                        </div>
                        <div className="page-footer-wrapper">
                              © 2021 BrokerBot v0.0.1  &nbsp; |  &nbsp; <AiOutlineGithub size={14} />  &nbsp; | &nbsp; An <div style={{color: '#fb4343'}}> &nbsp;RCOS&nbsp; </div> project
                        </div> 
                    </div>
                    <Popup trigger={this.state.deleteHoldingPopup} setTrigger={this.setDeleteHoldingPopup}>
                        <DeleteHoldingPopup setTrigger={this.setDeleteHoldingPopup}   delHold = {this.removeData} holdingName={this.state.deleteHoldingName}/>
                    </Popup>
                    <Popup trigger={this.state.settingsPopup} setTrigger={this.setSettingPopup}>
                        <SettingsPopup setTrigger={this.setSettingsPopup} />
                    </Popup>     
                    <Popup trigger={this.state.addHoldingPopup} setTrigger={this.setHoldingPopup}>
                        <AddHoldingPopup addHold={this.addData} setTrigger={this.setHoldingPopup} />
                    </Popup>
                </div> 
                : 
                <div className="page-wrapper">
                    <div className="flex-wrapper">   
                        {/* make one flex div then split it */}
                        <div className="page-content-wrapper">
                      <div className="header-wrapper">
                            <div className="header-img-wrapper center">
                                <img  alt='' src={Logo}/>
                            </div>
                            <div className="header-rest-wrapper">
                               <div className="settings-wrapper">
                                    <button onClick={() => this.setSettingsPopup(true)} />
                                    <VscSettings size={24} />
                               </div>
                            </div>
                        </div>
                        <div className="page-content-top-box-wrapper" >
                           {/* https://apexcharts.com/react-chart-demos/area-charts/stacked/ */}
                           <div className="graph-wrapper">
                              <ReactApexChart1  />  
                            </div>
                        </div>
                          <div className="page-content-bottom-box-wrapper" >
                            <SummaryDisplay title={"Your Portfolio's Summary"} 
                                            categories={["Capital Gain", "Dividends", "Currency Gain", "Std. Dev", "Adj. Return", "Expected", "Total Return"]} 
                                            inputData={ [{title: "Monetary(USD) gains/losses", values: [ 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]}, 
                                                         {title: "Percentage(%) gains/losses", values: ["0.00%", "0.00%", "0.00%", "0.00%", "0.00%", "0.00%", "0.00%"]}] }/>
                            <DataDisplay title={"Your Portfolio's Holdings"} categories={["Price", "Qty.", "Value", "Capital Gains", "Dividends", "Currency", "Return"]} inputData={ [] }
                                                                                                                resultValues={["", "", "$0.00", "0.00%", "0.00%", "0.00%", "0.00%"] }
                                                                                                                delPopupTrigger={this.setDeleteHoldingPopup} 
                                                                                                                addPopupTrigger={this.setHoldingPopup} />

                          </div>
                        </div>
                        <div className="page-footer-wrapper">
                              © 2021 BrokerBot v0.0.1  &nbsp; |  &nbsp; <AiOutlineGithub size={14} />  &nbsp; | &nbsp; An <div style={{color: '#fb4343'}}> &nbsp;RCOS&nbsp; </div> project
                        </div> 
                    </div>
                    <Popup trigger={this.state.deleteHoldingPopup} setTrigger={this.setDeleteHoldingPopup}>
                        <DeleteHoldingPopup setTrigger={this.setDeleteHoldingPopup}   delHold = {this.removeData} holdingName={this.state.deleteHoldingName}/>
                    </Popup>
                    <Popup trigger={this.state.settingsPopup} setTrigger={this.setSettingPopup}>
                        <SettingsPopup setTrigger={this.setSettingsPopup} />
                    </Popup>     
                    <Popup trigger={this.state.addHoldingPopup} setTrigger={this.setHoldingPopup}>
                        <AddHoldingPopup addHold={this.addData} setTrigger={this.setHoldingPopup} />
                    </Popup>
                </div> 
    }
}

/* <div className="header-wrapper">
                            <div className="header-img-wrapper center">
                                <img  alt='' src={Logo}/>
                            </div>
                            <div className="header-rest-wrapper">
                                {HeaderNavButtons.map((btn) => {
                                    return <div className="header-btn-wrapper center">{btn.Name}</div>
                                })}
                            </div>
                        </div>

*/
const MapStateToProps = (state) => ({
    userRedux: state.userData,
});

export default connect(MapStateToProps)(HomePage);