import React from 'react';
import { connect } from 'react-redux';
import Logo from '../images/BrokerBot.png';
import ReactApexChart from './Test';

    
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
        }
    }


    render(){
        return  <div className="page-wrapper">
                    <div className="flex-wrapper">
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
                        {/* make one flex div then split it */}
                        <div className="page-content-wrapper">
                        <div className="page-content-top-box-wrapper" >
                            https://apexcharts.com/react-chart-demos/area-charts/stacked/
                            <ReactApexChart />
                        </div>
                          <div className="page-content-bottom-box-wrapper" />
                        </div>
                        <div className="page-footer-wrapper"/> 
                    </div>
                </div>
    }
}

export default connect()(HomePage);