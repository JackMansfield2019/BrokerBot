import React from 'react';
import { connect } from 'react-redux';
import Logo from '../images/BrokerBot.png';
import ReactApexChart from './Test';
import { AiOutlineGithub, AiFillSetting  } from "react-icons/ai"
import { VscSettings } from "react-icons/vsc";

import DataDisplay from "./DataDisplay";
import SummaryDisplay from "./SummaryDisplay";
import Popup from './Popup'
import DeleteHoldingPopup from './deleteHoldingPopup'
import SettingsPopup from './SettingsPopup'

    
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


    


    render(){
        return  <div className="page-wrapper">
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
                              <ReactApexChart />  
                            </div>
                        </div>
                          <div className="page-content-bottom-box-wrapper" >
                            <SummaryDisplay title={"Your Portfolio's Summary"} 
                                            categories={["Capital Gain", "Dividends", "Currency Gain", "Std. Dev", "Adj. Return", "Expected", "Total Return"]} 
                                            inputData={ [{title: "Monetary(USD) gains/losses", values: [ 500.00, 0.00, 0.00, 25.00, -4000, 15000.00, 500.00]}, 
                                                         {title: "Percentage(%) gains/losses", values: ["1.00%", "2.00%", "0.00%", "4.00%", "-5.00%", "6.00%", "6.62%"]}] }/>
                            <DataDisplay title={"Your Portfolio's Holdings"} categories={["Price", "Qty.", "Value", "Capital Gains", "Dividends", "Currency", "Return"]} inputData={ [{title: "$ERTC", values: [0, 1, 2, 0, 1, 2, 6]}, 
                                                                                                                               {title: "$NPKL", values: [1, 2, 3, 0, 1, 2, 6]},
                                                                                                                               {title: "$APED", values: [1, 2, 3, 0, 1, 2, 4]},
                                                                                                                               {title: "$OPEK", values: [1, 2, 3, 0, 1, 2, 0]}] }
                                                                                                                resultValues={[0, 0, 0, 0, 0, 0, 0] }
                                                                                                                delPopupTrigger={this.setDeleteHoldingPopup} />
                          </div>
                        </div>
                        <div className="page-footer-wrapper">
                              © 2021 BrokerBot v0.0.1  &nbsp; |  &nbsp; <AiOutlineGithub size={14} />  &nbsp; | &nbsp; An <div style={{color: '#fb4343'}}> &nbsp;RCOS&nbsp; </div> project
                        </div> 
                    </div>
                    <Popup trigger={this.state.deleteHoldingPopup} setTrigger={this.setDeleteHoldingPopup}>
                        <DeleteHoldingPopup setTrigger={this.setDeleteHoldingPopup} holdingName={this.state.deleteHoldingName}/>
                    </Popup>
                    <Popup trigger={this.state.settingsPopup} setTrigger={this.setSettingPopup}>
                        <SettingsPopup setTrigger={this.setSettingsPopup} />
                    </Popup>
                </div>
    }
}

/* 
 <div className="header-wrapper">
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

export default connect()(HomePage);