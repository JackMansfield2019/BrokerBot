import React from 'react';
import { BiHide } from "react-icons/bi";

class AddHoldingPopup extends React.Component  {

     constructor(props){
        super(props); 

        this.state = {
           totalCost: 0.00,
           inputQTY: 0,
           inputUSP: 0,
           inputName: "",
        }
    }

    


    change = e => {
        //console.lo
        if(e.target.name === "inputQTY"){
            this.setState({
                [e.target.name]: e.target.value,
                totalCost: e.target.value * this.state.inputUSP,
            });
        } else if(e.target.name === "inputUSP") {     
            this.setState({
                [e.target.name]: e.target.value,
                totalCost: this.state.inputQTY * e.target.value,
            });
        } else {
            this.setState({
                [e.target.name]: e.target.value,
            });
        }


        this.forceUpdate();

    }

    onSubmit = (event) => {
        this.setState({
           secretValue: this.state.inputSecret,
           keyValue: this.state.inputKey,
        });
        console.log("RANNNNN");
        event.preventDefault();
        this.props.setTrigger(false);
        this.props.addHold(this.state.inputName, "$" + this.state.totalCost.toString(), this.state.inputQTY);
    }

    render(){
        return  <form>
                    <div className="add-hold-popup-inner">
                        <div className="add-hold-title">
                            <div className="add-hold-popup-title" >Add New Holding</div>
                            <div className="add-hold-popup-close-wrapper"><button onClick={() => this.props.setTrigger(false)}/>X</div>
                        </div>
                        <div className="addhold-popup-content-wrapper">
                            <div className="add-hold-name-wrapper">
                                <div className="add-hold-name-title">Holding Name:</div>
                                <div className="add-hold-name-input-wrapper">
                                    <input type="text" name="inputName" placeholder="eg:  'Apple' , 'APPL'" onChange={e => this.change(e)} />
                                </div>
                            </div>
                            <div className="add-hold-content1-wrapper">
                                <div className="add-hold-content1-left-wrapper" >
                                <div className="add-hold-date-title">Trade Date:</div>
                                <div className="add-hold-date-input-wrapper">
                                    <input type="date"/>
                                </div>
                                </div>
                                <div className="add-hold-content1-right-wrapper" />
                            </div>
                            <div className="add-hold-qty-wrapper">
                                <div className="add-hold-qty-title">Quantity:</div>
                                <div className="add-hold-qty-input-wrapper">
                                    <input type="number" name="inputQTY" placeholder="eg: 90" onChange={e => this.change(e) } />
                                </div>
                            </div>
                            <div className="add-hold-usp-wrapper">
                                <div className="add-hold-usp-title">Unit/Share Price:</div>
                                <div className="add-hold-usp-input-wrapper">
                                    <input type="number" name="inputUSP" placeholder="eg: 1.23"  onChange={e => this.change(e)}  />
                                </div>
                            </div>
                            <div className="add-hold-er-wrapper">
                                <div className="add-hold-er-title">Exchange Rate:</div>
                                <div className="add-hold-er-input-wrapper">
                                    <input type="number" placeholder="eg: 1.23" />
                                </div>
                            </div>
                            <div className="add-hold-total-wrapper">
                                <div className="add-hold-total-title-wrapper">Total (USD):</div> 
                                <div className="add-hold-total-cost-wrapper">{"$" + this.state.totalCost }</div>
                            </div>
                        </div>
                        <div className="settings-popup-submit-wrapper"><button type="submit" onClick={(event) => this.onSubmit(event)} />Submit New Hold</div>
                    </div> 
                </form>
                
    }
}
export default AddHoldingPopup;